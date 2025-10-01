# Smart Caption Library - Backend API

A complete FastAPI backend for managing and searching a library of captions with Excel upload support, category filtering, and usage analytics.

## Features

✅ **Excel File Upload & Processing** - Upload .xlsx/.xls files with captions
✅ **Category-based Search & Filtering** - Filter by category and search terms
✅ **One-click Copy Functionality** - Track usage when captions are copied
✅ **Usage Tracking Analytics** - Monitor most-used captions and statistics
✅ **Persistent Storage** - Data saved to JSON files for persistence
✅ **RESTful API** - Clean API endpoints for all operations
✅ **CORS Enabled** - Ready for frontend integration

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Upload Captions
- **POST** `/api/upload-captions`
- Upload Excel file with captions (Column A: Category, Column B: Caption)

### Get Captions
- **GET** `/api/captions?category={category}&search={search_term}`
- Filter captions by category and/or search term

### Get Categories
- **GET** `/api/categories`
- List all categories with caption counts

### Track Caption Usage
- **POST** `/api/copy-caption`
- Body: `{"caption_id": "category_0"}`
- Track when a caption is copied

### Get Analytics
- **GET** `/api/analytics`
- Get usage statistics and top captions

### Delete Caption
- **DELETE** `/api/caption/{caption_id}`
- Remove a specific caption

### Clear All
- **DELETE** `/api/clear-all`
- Remove all captions (use with caution)

## Excel File Format

Create an Excel file with:
- **Column A**: Category name
- **Column B**: Caption text

Example:
| Category | Caption |
|----------|---------|
| Motivational | Success is not final, failure is not fatal |
| Business | Innovation distinguishes between a leader and a follower |
| Marketing | Content is king, but engagement is queen |

## Frontend Integration

Use the included `frontend_integration.js` for easy integration:

```javascript
const api = new CaptionLibraryAPI('http://localhost:8000');

// Upload Excel file
await api.uploadExcel(file);

// Search captions
const results = await api.searchCaptions('Business', 'innovation');

// Track usage
await api.trackCaptionCopy('business_0');

// Get analytics
const stats = await api.getAnalytics();
```

## Running the Full Application

1. Start the backend:
```bash
python main.py
```

2. Open `index.html` in a web browser or serve it:
```bash
python -m http.server 3000
```

Then navigate to `http://localhost:3000`

## Data Storage

- Captions are stored in `caption_data.json`
- Usage analytics are stored in `usage_analytics.json`
- Files are created automatically and persist across server restarts

## API Documentation

When the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing with curl

```bash
# Upload Excel file
curl -X POST -F "file=@captions.xlsx" http://localhost:8000/api/upload-captions

# Get all captions
curl http://localhost:8000/api/captions

# Search captions
curl "http://localhost:8000/api/captions?search=success"

# Get categories
curl http://localhost:8000/api/categories

# Track usage
curl -X POST -H "Content-Type: application/json" \
  -d '{"caption_id":"motivational_0"}' \
  http://localhost:8000/api/copy-caption

# Get analytics
curl http://localhost:8000/api/analytics
```

## Production Considerations

1. **Database**: Replace JSON files with a proper database (PostgreSQL, MongoDB)
2. **Authentication**: Add API key or JWT authentication
3. **Rate Limiting**: Implement rate limiting for API endpoints
4. **File Validation**: Add more robust file validation and virus scanning
5. **CORS**: Configure specific allowed origins instead of "*"
6. **Caching**: Implement Redis for caching frequently accessed data
7. **Logging**: Add proper logging and monitoring
8. **File Size Limits**: Set appropriate upload size limits