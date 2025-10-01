from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import io
from typing import Optional, Dict, List, Any
from datetime import datetime
import json
import os

app = FastAPI(title="Smart Caption Library API")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database storage (in-memory for now, can be replaced with actual DB)
caption_database: Dict[str, List[Dict[str, Any]]] = {}
usage_analytics: Dict[str, int] = {}

# File storage path for persistence
DATA_FILE = "caption_data.json"
ANALYTICS_FILE = "usage_analytics.json"

# Load existing data on startup
def load_data():
    global caption_database, usage_analytics

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            caption_database = json.load(f)

    if os.path.exists(ANALYTICS_FILE):
        with open(ANALYTICS_FILE, 'r') as f:
            usage_analytics = json.load(f)

def save_data():
    """Save data to files for persistence"""
    with open(DATA_FILE, 'w') as f:
        json.dump(caption_database, f, indent=2)

    with open(ANALYTICS_FILE, 'w') as f:
        json.dump(usage_analytics, f, indent=2)

@app.on_event("startup")
async def startup_event():
    load_data()

def process_excel_file(file_content: bytes) -> Dict[str, List[Dict[str, Any]]]:
    """
    Process uploaded Excel file and extract caption data
    Expected format: Column A = Category, Column B = Message
    """
    try:
        # Read Excel file
        df = pd.read_excel(io.BytesIO(file_content))

        if df.empty:
            raise ValueError("Excel file is empty")

        caption_data = {}

        # Process each row
        for index, row in df.iterrows():
            # Get category from first column
            category = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else "Uncategorized"

            # Get message from second column
            if len(row) > 1:
                message = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
            else:
                message = ""

            # Only add if both category and message exist
            if message and category:
                if category not in caption_data:
                    caption_data[category] = []

                # Create unique ID
                caption_id = f"{category.replace(' ', '_')}_{len(caption_data[category])}"

                caption_data[category].append({
                    "id": caption_id,
                    "text": message,
                    "category": category,
                    "usage_count": 0,
                    "created_at": datetime.now().isoformat(),
                    "last_used": None
                })

        return caption_data

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing Excel file: {str(e)}")

@app.post("/api/upload-captions")
async def upload_captions(file: UploadFile = File(...)):
    """
    Upload and process Excel file containing captions
    """
    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Please upload an Excel file (.xlsx or .xls)")

    # Read file content
    content = await file.read()

    # Process Excel file
    new_captions = process_excel_file(content)

    # Merge with existing captions
    for category, captions in new_captions.items():
        if category in caption_database:
            # Add new captions to existing category
            existing_ids = {cap['id'] for cap in caption_database[category]}
            for caption in captions:
                # Avoid duplicates by checking text
                if not any(cap['text'] == caption['text'] for cap in caption_database[category]):
                    # Generate new unique ID if needed
                    while caption['id'] in existing_ids:
                        caption['id'] = f"{caption['id']}_new"
                    caption_database[category].append(caption)
        else:
            caption_database[category] = captions

    # Save to file
    save_data()

    # Return summary
    total_captions = sum(len(captions) for captions in caption_database.values())

    return JSONResponse(content={
        "success": True,
        "message": f"Successfully processed {file.filename}",
        "categories": list(caption_database.keys()),
        "total_captions": total_captions,
        "new_captions_added": sum(len(captions) for captions in new_captions.values())
    })

@app.get("/api/captions")
async def get_captions(
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search term")
):
    """
    Get captions with optional filtering by category and search term
    """
    result = []

    # Filter by category if specified
    if category:
        categories_to_search = [category] if category in caption_database else []
    else:
        categories_to_search = list(caption_database.keys())

    # Collect captions from selected categories
    for cat in categories_to_search:
        for caption in caption_database.get(cat, []):
            # Apply search filter if specified
            if search:
                if search.lower() in caption['text'].lower():
                    result.append(caption)
            else:
                result.append(caption)

    # Sort by usage count (most used first) and then by creation date
    result.sort(key=lambda x: (-x['usage_count'], x['created_at']))

    return JSONResponse(content={
        "success": True,
        "count": len(result),
        "captions": result,
        "categories": list(caption_database.keys())
    })

@app.get("/api/categories")
async def get_categories():
    """
    Get list of all available categories with caption counts
    """
    categories = []
    for category, captions in caption_database.items():
        categories.append({
            "name": category,
            "count": len(captions),
            "total_usage": sum(cap['usage_count'] for cap in captions)
        })

    # Sort by total usage
    categories.sort(key=lambda x: -x['total_usage'])

    return JSONResponse(content={
        "success": True,
        "categories": categories
    })

class CopyCaptionRequest(BaseModel):
    caption_id: str

@app.post("/api/copy-caption")
async def copy_caption(request: CopyCaptionRequest):
    """
    Track usage when a caption is copied
    """
    caption_id = request.caption_id
    found = False

    # Find and update the caption
    for category, captions in caption_database.items():
        for caption in captions:
            if caption['id'] == caption_id:
                caption['usage_count'] += 1
                caption['last_used'] = datetime.now().isoformat()
                found = True

                # Update analytics
                if caption_id not in usage_analytics:
                    usage_analytics[caption_id] = 0
                usage_analytics[caption_id] += 1

                # Save updated data
                save_data()

                return JSONResponse(content={
                    "success": True,
                    "message": "Caption usage tracked",
                    "usage_count": caption['usage_count']
                })

    if not found:
        raise HTTPException(status_code=404, detail="Caption not found")

@app.get("/api/analytics")
async def get_analytics():
    """
    Get usage analytics for all captions
    """
    # Get top used captions
    top_captions = []
    for category, captions in caption_database.items():
        for caption in captions:
            if caption['usage_count'] > 0:
                top_captions.append({
                    "id": caption['id'],
                    "text": caption['text'][:50] + "..." if len(caption['text']) > 50 else caption['text'],
                    "category": category,
                    "usage_count": caption['usage_count'],
                    "last_used": caption.get('last_used')
                })

    # Sort by usage count
    top_captions.sort(key=lambda x: -x['usage_count'])

    # Category statistics
    category_stats = {}
    for category, captions in caption_database.items():
        category_stats[category] = {
            "total_captions": len(captions),
            "total_usage": sum(cap['usage_count'] for cap in captions),
            "avg_usage": sum(cap['usage_count'] for cap in captions) / len(captions) if captions else 0
        }

    return JSONResponse(content={
        "success": True,
        "total_captions": sum(len(captions) for captions in caption_database.values()),
        "total_usage": sum(usage_analytics.values()),
        "top_captions": top_captions[:10],  # Top 10 most used
        "category_statistics": category_stats
    })

@app.delete("/api/caption/{caption_id}")
async def delete_caption(caption_id: str):
    """
    Delete a specific caption
    """
    for category, captions in caption_database.items():
        for i, caption in enumerate(captions):
            if caption['id'] == caption_id:
                del caption_database[category][i]

                # Remove category if empty
                if not caption_database[category]:
                    del caption_database[category]

                # Remove from analytics if exists
                if caption_id in usage_analytics:
                    del usage_analytics[caption_id]

                save_data()

                return JSONResponse(content={
                    "success": True,
                    "message": "Caption deleted successfully"
                })

    raise HTTPException(status_code=404, detail="Caption not found")

@app.delete("/api/clear-all")
async def clear_all_captions():
    """
    Clear all captions (use with caution)
    """
    global caption_database, usage_analytics
    caption_database = {}
    usage_analytics = {}
    save_data()

    return JSONResponse(content={
        "success": True,
        "message": "All captions cleared"
    })

@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "name": "Smart Caption Library API",
        "version": "1.0.0",
        "endpoints": [
            "/api/upload-captions - POST: Upload Excel file",
            "/api/captions - GET: Get captions with filtering",
            "/api/categories - GET: Get all categories",
            "/api/copy-caption - POST: Track caption usage",
            "/api/analytics - GET: Get usage analytics",
            "/docs - Swagger UI documentation"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)