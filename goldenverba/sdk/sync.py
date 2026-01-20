"""Async/sync wrapper utilities."""

import asyncio
import threading
from typing import Any, AsyncGenerator, Generator, TypeVar, Coroutine

T = TypeVar("T")

# Thread-local storage for event loops
_loop_storage = threading.local()


def run_sync(coro: Coroutine[Any, Any, T]) -> T:
    """
    Run async coroutine synchronously.

    If already in an async context, raises RuntimeError.
    Otherwise, reuses a thread-local event loop to avoid closing
    the loop between calls (which would invalidate async clients).
    """
    try:
        loop = asyncio.get_running_loop()
        # Already in async context - cannot use run_until_complete
        raise RuntimeError(
            "Cannot run async coroutine synchronously from within an async context. "
            "Use 'await' instead or run from a sync context."
        )
    except RuntimeError as e:
        if "Cannot run async" in str(e):
            raise
        # No running loop, check if we have a thread-local loop
        if not hasattr(_loop_storage, 'loop') or _loop_storage.loop.is_closed():
            # Create a new event loop for this thread
            _loop_storage.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(_loop_storage.loop)
        
        # Run the coroutine in the existing loop
        return _loop_storage.loop.run_until_complete(coro)


class AsyncToSyncIterator:
    """Convert an async generator to a synchronous iterator."""

    def __init__(self, async_gen: AsyncGenerator[T, None]):
        self._async_gen = async_gen
        self._loop = None
        self._queue = asyncio.Queue()
        self._task = None
        self._stop_iteration = False

    def __iter__(self):
        return self

    def __next__(self) -> T:
        if self._stop_iteration:
            raise StopIteration

        # Create event loop if needed
        if self._loop is None or not self._loop.is_running():
            try:
                self._loop = asyncio.get_event_loop()
            except RuntimeError:
                self._loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self._loop)

        # Start background task to consume async generator
        if self._task is None:
            self._task = self._loop.create_task(self._consume_async_gen())

        # Get next item from queue
        try:
            if self._loop.is_running():
                # If loop is running, we need to use a different approach
                # Use asyncio.run_coroutine_threadsafe or create a new loop
                future = asyncio.run_coroutine_threadsafe(self._queue.get(), self._loop)
                item = future.result(timeout=300)  # 5 minute timeout
            else:
                item = self._loop.run_until_complete(self._queue.get())

            if item is StopIteration:
                self._stop_iteration = True
                raise StopIteration
            return item
        except Exception as e:
            self._stop_iteration = True
            if isinstance(e, StopIteration):
                raise
            raise RuntimeError(f"Error consuming async generator: {e}")

    async def _consume_async_gen(self):
        """Consume async generator and put items in queue."""
        try:
            async for item in self._async_gen:
                await self._queue.put(item)
            await self._queue.put(StopIteration)
        except Exception as e:
            await self._queue.put(e)
            await self._queue.put(StopIteration)


def sync_generator(async_gen_func):
    """Decorator to convert async generator function to sync generator."""

    def wrapper(*args, **kwargs) -> Generator[T, None, None]:
        async_gen = async_gen_func(*args, **kwargs)
        return AsyncToSyncIterator(async_gen)

    return wrapper
