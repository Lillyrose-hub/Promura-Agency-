from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import os
from pathlib import Path
from onlysnarf_client import PromuraClient

app = FastAPI()

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize OnlySnarf client
promura = PromuraClient()

# Store scheduled posts (in production, use a database)
scheduled_posts = []

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Main dashboard page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/schedule-post")
async def schedule_post(
    request: Request,
    content: str = Form(...),
    schedule_time: str = Form(None),
    media_files: list[UploadFile] = File([])
):
    """Handle post scheduling with your existing logic"""
    try:
        # Handle file uploads (your existing logic)
        saved_files = []
        for file in media_files:
            if file.filename:
                file_path = f"uploads/{datetime.now().timestamp()}_{file.filename}"
                with open(file_path, "wb") as buffer:
                    file_content = await file.read()
                    buffer.write(file_content)
                saved_files.append(file_path)
        
        # Your existing scheduling logic
        post_data = {
            "text": content,
            "files": saved_files,
            "schedule_time": schedule_time,
            "timestamp": datetime.now().isoformat(),
            "status": "Scheduled"
        }
        
        # Add to scheduled posts (your existing queue system)
        scheduled_posts.append(post_data)
        
        # If no schedule time, post immediately (your existing logic)
        if not schedule_time:
            try:
                result = promura.schedule_post(content, saved_files)
                post_data["status"] = "Posted Successfully"
                message = "✅ Post published successfully!"
            except Exception as e:
                post_data["status"] = f"Failed: {str(e)}"
                message = f"❌ Post failed: {str(e)}"
        else:
            message = f"✅ Post scheduled for {schedule_time}!"
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "message": message
        })
        
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "message": f"❌ Error: {str(e)}"
        })

# KEEP YOUR EXISTING QUEUE ENDPOINT (but we'll update it later)
@app.get("/queue", response_class=HTMLResponse)
async def post_queue():
    """Show all scheduled posts - YOUR EXISTING CODE"""
    count = len(scheduled_posts)
    posts_html = ""
    
    if scheduled_posts:
        for i, post in enumerate(reversed(scheduled_posts)):
            file_info = ""
            if post.get('files'):
                file_count = len(post['files'])
                file_info = f"{file_count} file{'s' if file_count > 1 else ''}"
            
            timestamp = datetime.fromisoformat(post['timestamp']).strftime("%b %d, %Y at %I:%M %p")
            
            posts_html += f"""
            <div style="background: white; border-radius: 15px; padding: 25px; margin: 20px 0; border: 1px solid rgba(248, 187, 217, 0.3);">
                <h3 style="color: #880e4f;">Post #{len(scheduled_posts) - i}</h3>
                <p style="color: #333; margin: 15px 0;">{post['text'][:150]}{'...' if len(post['text']) > 150 else ''}</p>
                <p style="color: #666; font-size: 0.9rem;">Schedule: {post['schedule_time'] or 'Immediately'}</p>
                <p style="color: #666; font-size: 0.9rem;">Status: {post['status']}</p>
                <p style="color: #666; font-size: 0.9rem;">Created: {timestamp}</p>
                {f'<p style="color: #666; font-size: 0.9rem;">Files: {file_info}</p>' if file_info else ''}
            </div>
            """
    else:
        posts_html = """
        <div style="text-align: center; padding: 60px 20px;">
            <h3 style="color: #888;">No posts scheduled yet</h3>
            <p style="color: #999; margin: 15px 0;">Your scheduled posts will appear here</p>
            <a href="/" style="background: linear-gradient(135deg, #ec407a 0%, #ad1457 100%); color: white; padding: 12px 30px; border-radius: 25px; text-decoration: none; display: inline-block; margin-top: 20px;">Schedule Your First Post</a>
        </div>
        """
    
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Post Queue - PROMURA</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Post Queue (Total: {count})</h1>
                <a href="/" class="btn">New Post</a>
            </div>
            <div class="form-container">
                {posts_html}
            </div>
        </div>
    </body>
    </html>
    """)

@app.get("/status")
async def system_status():
    """Check system status - YOUR EXISTING CODE"""
    status = promura.test_connection()
    return {
        "dashboard": "PROMURA Dashboard Online",
        "onlysnarf_integration": status,
        "scheduled_posts": len(scheduled_posts)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
