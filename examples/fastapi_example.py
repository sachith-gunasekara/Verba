#!/usr/bin/env python3
"""
FastAPI Integration Example

This script demonstrates how to use Verba SDK in FastAPI applications.
The SDK automatically detects async contexts and provides async methods.
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from goldenverba import Verba
from goldenverba.sdk.models import Document, QueryResult, ChatResponse

app = FastAPI(title="Verba FastAPI Example")

# Initialize Verba instance (without auto_connect in async context)
# The SDK will detect we're in async context and skip auto_connect
verba = Verba(
    deployment="Custom",
    weaviate_url="localhost",
    port="8080",
    auto_connect=False  # Important: set to False in async contexts
)


@app.on_event("startup")
async def startup():
    """Initialize Verba connection on FastAPI startup."""
    await verba.connect_async()
    print("✓ Verba connected successfully")


@app.on_event("shutdown")
async def shutdown():
    """Close Verba connection on FastAPI shutdown."""
    await verba.close_async()
    print("✓ Verba connection closed")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Verba FastAPI server is running"}


@app.post("/documents", response_model=Document)
async def add_document(
    content: str,
    title: str = None,
    labels: list[str] = None,
    metadata: str = "",
):
    """
    Add a document to Verba.
    
    Use async methods when calling from FastAPI endpoints.
    """
    try:
        doc = await verba.add_document_async(
            content=content,
            title=title,
            labels=labels or [],
            metadata=metadata,
        )
        return doc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents", response_model=list[Document])
async def list_documents(
    query: str = "",
    page: int = 1,
    page_size: int = 10,
):
    """List documents with pagination."""
    try:
        doc_list = await verba.list_documents_async(
            query=query,
            page=page,
            page_size=page_size,
        )
        return doc_list.documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents/{uuid}", response_model=Document)
async def get_document(uuid: str):
    """Get a document by UUID."""
    try:
        doc = await verba.get_document_async(uuid)
        return doc
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/documents/{uuid}")
async def delete_document(uuid: str):
    """Delete a document by UUID."""
    try:
        result = await verba.delete_document_async(uuid)
        return {"success": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResult)
async def query(
    query: str,
    limit: int = 5,
    labels: list[str] = None,
):
    """Query documents and retrieve relevant chunks."""
    try:
        results = await verba.query_async(
            query=query,
            limit=limit,
            labels=labels or [],
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
async def chat(
    message: str,
    conversation: list[dict] = None,
    labels: list[str] = None,
):
    """Chat with RAG - retrieves context and generates response."""
    try:
        response = await verba.chat_async(
            message=message,
            conversation=conversation or [],
            stream=False,  # Set to True for streaming
            labels=labels or [],
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
