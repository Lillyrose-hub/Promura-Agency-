from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
import json
import uuid
from pathlib import Path
from typing import List, Optional, Dict
from pydantic import BaseModel
from app.onlysnarf_client import PromuraClient
from app.logging_system import logger
from app.content_library import content_library
from app.caption_manager import caption_manager
from app.auth_system import user_manager, audit_logger, get_current_user, require_permission, get_optional_user
from app.burner_models import burner_manager, PRODUCTION_DEPLOYMENT_MEMORY

app = FastAPI()

# Add CORS middleware for API access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Middleware for action tracking
@app.middleware("http")
async def track_actions(request: Request, call_next):
    """Track all user actions for audit logging"""
    # Get current user if authenticated
    user = await get_optional_user(request)

    # Log the action
    if user:
        audit_logger.log_action(
            username=user.get("username", "anonymous"),
            action="api_call",
            details=f"{request.method} {request.url.path}",
            ip_address=request.client.host if request.client else None,
            endpoint=request.url.path,
            method=request.method
        )

    response = await call_next(request)
    return response

# Initialize OnlySnarf client
promura = PromuraClient()

# Store scheduled posts and completed posts (in production, use a database)
scheduled_posts = []
completed_posts = []

# 19 Burner Test Models for Development
# WARNING: REMOVE BEFORE PRODUCTION - See app/burner_models.py
models_data = burner_manager.get_all_models()
print(f"Loaded {len(models_data)} burner test models for development")
print(PRODUCTION_DEPLOYMENT_MEMORY)

# System status
system_status = {"online": True, "last_check": datetime.now()}

# Authentication Models
class LoginRequest(BaseModel):
    username: str
    password: str

class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str

class PostEdit(BaseModel):
    content: str
    models: List[str]
    schedule_time: Optional[str]

# ==================== AUTHENTICATION ENDPOINTS ====================

@app.post("/api/auth/login")
async def login(login_data: LoginRequest):
    """Login endpoint"""
    user = user_manager.authenticate_user(login_data.username, login_data.password)

    if not user:
        # Log failed attempt
        audit_logger.log_action(
            username=login_data.username,
            action="login_failed",
            details="Invalid username or password"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Create access token
    token = user_manager.create_access_token(login_data.username)

    # Log successful login
    audit_logger.log_action(
        username=login_data.username,
        action="login",
        details="User logged in successfully"
    )

    return {
        "success": True,
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

@app.post("/api/auth/logout")
async def logout(current_user: Dict = Depends(get_current_user)):
    """Logout endpoint - logs the action"""
    audit_logger.log_action(
        username=current_user["username"],
        action="logout",
        details="User logged out"
    )
    return {"success": True, "message": "Logged out successfully"}

@app.get("/api/auth/me")
async def get_me(current_user: Dict = Depends(get_current_user)):
    """Get current user information"""
    return current_user

@app.post("/api/auth/change-password")
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Change user password"""
    success = user_manager.change_password(
        current_user["username"],
        password_data.old_password,
        password_data.new_password
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid current password"
        )

    audit_logger.log_action(
        username=current_user["username"],
        action="password_change",
        details="Password changed successfully"
    )

    return {"success": True, "message": "Password changed successfully"}

@app.get("/api/auth/users")
async def list_users(current_user: Dict = Depends(require_permission("all"))):
    """List all users - requires owner permission"""
    return user_manager.list_users()

@app.get("/api/audit/logs")
async def get_audit_logs(
    limit: int = 100,
    current_user: Dict = Depends(require_permission("all"))
):
    """Get audit logs - requires owner permission"""
    return audit_logger.get_recent_logs(limit)

@app.get("/api/audit/user/{username}")
async def get_user_logs(
    username: str,
    limit: int = 100,
    current_user: Dict = Depends(require_permission("all"))
):
    """Get audit logs for specific user - requires owner permission"""
    return audit_logger.get_user_logs(username, limit)

# ==================== TEAM MANAGEMENT ENDPOINTS ====================

class AddUserRequest(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    role: str

@app.post("/api/team/add-user")
async def add_user(
    user_data: AddUserRequest,
    current_user: Dict = Depends(require_permission("all"))
):
    """Add a new team member - requires owner permission"""
    # Check if username already exists
    if user_manager.get_user(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username {user_data.username} already exists"
        )

    # Get permissions based on role
    permission_map = {
        "owner": ["all"],
        "manager": ["schedule", "view", "edit", "queue", "captions", "metrics"],
        "assistant": ["view", "schedule", "captions"]
    }
    permissions = permission_map.get(user_data.role, ["view"])

    # Add user to the system
    user_dict = {
        "password": user_manager._hash_password(user_data.password),
        "role": user_data.role,
        "permissions": permissions,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "created_at": datetime.now().isoformat(),
        "created_by": current_user["username"],
        "active": True
    }

    # Add to users database
    user_manager.users[user_data.username] = user_dict
    user_manager._save_users()

    # Log the action
    audit_logger.log_action(
        username=current_user["username"],
        action="add_user",
        details=f"Added user {user_data.username} as {user_data.role}"
    )

    return {
        "success": True,
        "message": f"User {user_data.username} added successfully"
    }

@app.get("/api/team/users")
async def get_team_users(current_user: Dict = Depends(require_permission("all"))):
    """Get all team members - requires owner permission"""
    users_list = []
    for username, user_data in user_manager.users.items():
        users_list.append({
            "username": username,
            "role": user_data.get("role", "unknown"),
            "email": user_data.get("email", ""),
            "full_name": user_data.get("full_name", username),
            "permissions": user_data.get("permissions", []),
            "created_at": user_data.get("created_at", "Unknown"),
            "created_by": user_data.get("created_by", "System"),
            "active": user_data.get("active", True)
        })

    # Sort by role (owner first, then manager, then assistant)
    role_order = {"owner": 0, "manager": 1, "assistant": 2}
    users_list.sort(key=lambda x: (role_order.get(x["role"], 3), x["username"]))

    return users_list

@app.delete("/api/team/delete-user/{username}")
async def delete_user(
    username: str,
    current_user: Dict = Depends(require_permission("all"))
):
    """Delete a team member - requires owner permission"""
    # Prevent self-deletion
    if username == current_user["username"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot delete your own account"
        )

    # Check if user exists
    if username not in user_manager.users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {username} not found"
        )

    # Prevent deleting other owners
    user = user_manager.users[username]
    if user.get("role") == "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete other owners"
        )

    # Delete the user
    del user_manager.users[username]
    user_manager._save_users()

    # Log the action
    audit_logger.log_action(
        username=current_user["username"],
        action="delete_user",
        details=f"Deleted user {username}"
    )

    return {
        "success": True,
        "message": f"User {username} has been removed"
    }

@app.put("/api/team/update-user/{username}")
async def update_user(
    username: str,
    updates: Dict,
    current_user: Dict = Depends(require_permission("all"))
):
    """Update a team member - requires owner permission"""
    # Check if user exists
    if username not in user_manager.users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {username} not found"
        )

    # Update user
    success = user_manager.update_user(username, updates)

    if success:
        # Log the action
        audit_logger.log_action(
            username=current_user["username"],
            action="update_user",
            details=f"Updated user {username}"
        )

        return {
            "success": True,
            "message": f"User {username} updated successfully"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update user"
        )

# ==================== MAIN APPLICATION ROUTES ====================

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/team", response_class=HTMLResponse)
async def team_management_page(request: Request):
    """Team management page"""
    return templates.TemplateResponse("team_management.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Main dashboard page - will check authentication via JavaScript"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "models": models_data
    })

@app.get("/api/models")
async def get_models():
    """Get all available models"""
    return models_data

@app.get("/api/queue")
async def get_queue():
    """Get all scheduled posts"""
    return {"queue": scheduled_posts, "history": completed_posts}

@app.get("/api/status")
async def get_status():
    """Get system status"""
    return {
        "online": system_status["online"],
        "last_check": system_status["last_check"].isoformat(),
        "queue_count": len(scheduled_posts),
        "completed_count": len(completed_posts)
    }

@app.get("/api/history")
async def get_history():
    """Get completed posts history"""
    return completed_posts

@app.get("/api/motivational-quotes")
async def get_motivational_quotes():
    """Get all motivational quotes for the greeting header"""
    try:
        quotes_file = Path("app/data/motivational_quotes.json")
        if quotes_file.exists():
            with open(quotes_file, 'r', encoding='utf-8') as f:
                quotes = json.load(f)
            return quotes
        else:
            # Return a default quote if file doesn't exist
            return [{
                "id": 1,
                "text": "Success doesn't come from what you do occasionally. It comes from what you do consistently.",
                "category": "Hustle & Grind",
                "author": "Marie Forleo"
            }]
    except Exception as e:
        logger.error(f"Error loading motivational quotes: {e}")
        return [{
            "id": 1,
            "text": "Great things never come from comfort zones.",
            "category": "Resilience",
            "author": "Anonymous"
        }]

@app.post("/schedule-post")
async def schedule_post(
    request: Request,
    content: str = Form(...),
    models: str = Form("[]"),  # JSON string of selected models
    schedule_time: str = Form(None),
    library_media_ids: str = Form(None),  # JSON string of library media IDs
    media_files: list[UploadFile] = File([]),
    current_user: Dict = Depends(require_permission("schedule"))
):
    """Handle post scheduling with model selection and mixed media"""
    try:
        # Parse selected models
        selected_models = json.loads(models) if models else []

        # Parse library media IDs
        library_ids = json.loads(library_media_ids) if library_media_ids else []

        # Generate unique ID
        post_id = str(uuid.uuid4())

        # Collect all media files
        all_media_files = []

        # Add library media files
        if library_ids:
            for media_id in library_ids:
                media_item = content_library.get_media_by_id(media_id)
                if media_item:
                    # Get the actual file path
                    media_type = "images" if media_item["type"] == "image" else "videos"
                    file_path = Path("static/library") / media_type / "original" / media_item["filename"]
                    all_media_files.append({
                        "path": str(file_path),
                        "source": "library",
                        "id": media_id,
                        "url": media_item["url"]
                    })
                    # Track usage
                    content_library.use_media(media_id)
                    logger.log(f"Library media used: {media_id} in post {post_id}")

        # Handle new file uploads
        saved_files = []
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)

        for file in media_files:
            if file.filename:
                timestamp = datetime.now().timestamp()
                file_path = upload_dir / f"{timestamp}_{file.filename}"
                with open(file_path, "wb") as buffer:
                    file_content = await file.read()
                    buffer.write(file_content)
                saved_files.append(str(file_path))
                all_media_files.append({
                    "path": str(file_path),
                    "source": "upload",
                    "filename": file.filename
                })

        # Create post data with enhanced structure
        post_data = {
            "id": post_id,
            "content": content,
            "models": selected_models,
            "media_files": all_media_files,
            "library_media_count": len(library_ids),
            "upload_media_count": len(saved_files),
            "schedule_time": schedule_time,
            "timestamp": datetime.now().isoformat(),
            "status": "scheduled" if schedule_time else "posting",
            "completed_at": None
        }

        # Add to scheduled posts
        scheduled_posts.append(post_data)

        # If no schedule time, post immediately
        if not schedule_time:
            try:
                # Get all file paths for posting
                file_paths = [item["path"] for item in all_media_files]

                # Simulate posting
                result = promura.schedule_post(content, file_paths)
                post_data["status"] = "completed"
                post_data["completed_at"] = datetime.now().isoformat()

                # Move to completed posts
                scheduled_posts.remove(post_data)
                completed_posts.insert(0, post_data)

                total_media = len(all_media_files)
                media_info = f" with {total_media} media file{'s' if total_media != 1 else ''}" if total_media > 0 else ""
                message = f"✅ Post published successfully to {len(selected_models)} models{media_info}!"
            except Exception as e:
                post_data["status"] = "failed"
                message = f"❌ Post failed: {str(e)}"
        else:
            total_media = len(all_media_files)
            media_info = f" with {total_media} media file{'s' if total_media != 1 else ''}" if total_media > 0 else ""
            message = f"✅ Post scheduled for {schedule_time} to {len(selected_models)} models{media_info}!"

        return JSONResponse({
            "success": True,
            "message": message,
            "post_id": post_id
        })

    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"❌ Error: {str(e)}"
        }, status_code=400)

@app.post("/api/queue/{post_id}/cancel")
async def cancel_post(post_id: str, current_user: Dict = Depends(require_permission("queue"))):
    """Cancel a scheduled post"""
    for post in scheduled_posts:
        if post["id"] == post_id:
            scheduled_posts.remove(post)
            return {"success": True, "message": "Post cancelled successfully"}

    raise HTTPException(status_code=404, detail="Post not found")

@app.post("/api/queue/{post_id}/edit")
async def edit_post(post_id: str, post_edit: PostEdit):
    """Edit a scheduled post"""
    for post in scheduled_posts:
        if post["id"] == post_id:
            post["content"] = post_edit.content
            post["models"] = post_edit.models
            if post_edit.schedule_time:
                post["schedule_time"] = post_edit.schedule_time
            return {"success": True, "message": "Post updated successfully"}

    raise HTTPException(status_code=404, detail="Post not found")

@app.delete("/api/queue/{post_id}")
async def delete_post(post_id: str):
    """Delete a scheduled post"""
    for post in scheduled_posts:
        if post["id"] == post_id:
            # Delete associated files
            for file_path in post.get("media_files", []):
                if os.path.exists(file_path):
                    os.remove(file_path)

            scheduled_posts.remove(post)
            return {"success": True, "message": "Post deleted successfully"}

    raise HTTPException(status_code=404, detail="Post not found")

@app.get("/queue", response_class=HTMLResponse)
async def view_queue(request: Request):
    """Enhanced queue view page"""
    return templates.TemplateResponse("queue.html", {
        "request": request,
        "scheduled_posts": scheduled_posts,
        "completed_posts": completed_posts
    })

@app.get("/metrics", response_class=HTMLResponse)
async def view_metrics(request: Request):
    """Metrics dashboard page"""
    return templates.TemplateResponse("metrics.html", {
        "request": request
    })

@app.get("/status")
async def check_status():
    """Check system status - YOUR EXISTING CODE"""
    status = promura.test_connection()
    return {
        "dashboard": "PROMURA Dashboard Online",
        "onlysnarf_integration": status,
        "scheduled_posts": len(scheduled_posts)
    }

@app.get("/api/metrics")
async def get_metrics():
    """Get comprehensive system metrics for dashboard display"""
    metrics = logger.get_dashboard_metrics()

    # Add additional real-time information
    metrics["system"] = {
        "online": system_status["online"],
        "last_check": system_status["last_check"].isoformat(),
        "scheduled_posts": len(scheduled_posts),
        "completed_posts": len(completed_posts)
    }

    return metrics

@app.get("/api/logs/export")
async def export_logs():
    """Export all logs to a file"""
    export_file = logger.export_logs()
    return {
        "success": True,
        "message": f"Logs exported successfully",
        "file": str(export_file)
    }

# Content Library API Endpoints
@app.get("/api/library")
async def get_content_library(media_type: Optional[str] = None, tags: Optional[str] = None):
    """Get all media in content library"""
    tags_list = tags.split(",") if tags else None
    media = content_library.get_all_media(media_type, tags_list)
    return media

@app.get("/api/library/search")
async def search_library(q: str):
    """Search content library"""
    results = content_library.search_media(q)
    return results

@app.get("/api/library/stats")
async def get_library_stats():
    """Get library statistics"""
    stats = content_library.get_statistics()
    return stats

@app.post("/api/library/upload")
async def upload_to_library(file: UploadFile = File(...), tags: str = "", description: str = ""):
    """Upload new media to library"""
    try:
        # Read file data
        file_data = await file.read()

        # Parse tags
        tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()] if tags else []

        # Add to library
        media_entry = content_library.add_media(
            file_data=file_data,
            filename=file.filename,
            tags=tags_list,
            description=description
        )

        logger.log(f"Library upload: {file.filename} (ID: {media_entry['id']})")

        return {"success": True, "media": media_entry}
    except Exception as e:
        logger.error(f"Library upload failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/library/{media_id}/use")
async def use_media_in_post(media_id: str):
    """Increment usage count for media"""
    if content_library.use_media(media_id):
        logger.log(f"Library media incremented: {media_id}")
        return {"success": True}
    else:
        raise HTTPException(status_code=404, detail="Media not found")

@app.delete("/api/library/{media_id}")
async def delete_from_library(media_id: str):
    """Remove media from library"""
    if content_library.delete_media(media_id):
        logger.log(f"Library media deleted: {media_id}")
        return {"success": True}
    else:
        raise HTTPException(status_code=404, detail="Media not found")

# Caption Library Routes
@app.get("/captions", response_class=HTMLResponse)
async def caption_library(request: Request):
    """Caption Library page"""
    return templates.TemplateResponse("captions.html", {
        "request": request
    })

@app.get("/captions-compact", response_class=HTMLResponse)
async def caption_library_compact(request: Request):
    """Compact Caption Library page"""
    return templates.TemplateResponse("captions_compact.html", {
        "request": request
    })

@app.post("/api/captions/upload")
async def upload_captions(file: UploadFile = File(...)):
    """Upload Excel file with captions"""
    try:
        # Read file content
        contents = await file.read()

        # Process the Excel file using CaptionManager
        result = caption_manager.process_excel_file(contents, file.filename)

        if result["success"]:
            print(f"Caption upload: {file.filename} - {result['message']}")
            return JSONResponse({
                "success": True,
                "message": result["message"],
                "captions": result["captions"],
                "summary": result.get("summary", {})
            })
        else:
            logger.log_error("Caption Upload", f"Caption upload failed: {result['message']}")
            return JSONResponse({
                "success": False,
                "message": result["message"]
            }, status_code=400)

    except Exception as e:
        logger.log_error("Caption Upload", f"Caption upload error: {str(e)}")
        return JSONResponse({
            "success": False,
            "message": f"Error processing file: {str(e)}"
        }, status_code=400)

@app.post("/api/captions/replace-all")
async def replace_all_captions(file: UploadFile = File(...)):
    """Replace all existing captions with new Excel file"""
    try:
        # 1. DELETE all existing captions from database
        caption_manager.clear_all_captions()
        print("Cleared all existing captions for replacement")

        # 2. Read and PROCESS new Excel file
        contents = await file.read()
        result = caption_manager.process_excel_file(contents, file.filename)

        if result["success"]:
            print(f"Caption replacement: {file.filename} - {result['message']}")
            return JSONResponse({
                "success": True,
                "message": f"All captions replaced. {result['message']}",
                "captions": result["captions"],
                "summary": result.get("summary", {})
            })
        else:
            logger.log_error("Caption Upload", f"Caption replacement failed: {result['message']}")
            return JSONResponse({
                "success": False,
                "message": result["message"]
            }, status_code=400)

    except Exception as e:
        logger.log_error("Caption Upload", f"Caption replacement error: {str(e)}")
        return JSONResponse({
            "success": False,
            "message": f"Error replacing captions: {str(e)}"
        }, status_code=400)

@app.get("/api/captions")
async def get_captions(category: Optional[str] = None, search: Optional[str] = None):
    """Get stored captions, optionally filtered by category or search term"""
    try:
        if search:
            # Search for captions
            captions = caption_manager.search_captions(search)
        elif category:
            # Filter by category
            captions = caption_manager.get_captions_by_category(category)
        else:
            # Get all captions
            captions = caption_manager.get_all_captions()

        return captions

    except Exception as e:
        logger.error(f"Error fetching captions: {str(e)}")
        return []

@app.post("/api/captions/{caption_id}/use")
async def use_caption(caption_id: str):
    """Track caption usage"""
    if caption_manager.increment_usage(caption_id):
        logger.log(f"Caption used: {caption_id}")
        return {"success": True}
    else:
        raise HTTPException(status_code=404, detail="Caption not found")

@app.post("/api/copy-caption")
async def copy_caption(caption_id: str = Form(...)):
    """Track when a caption is copied to clipboard"""
    caption = caption_manager.get_caption_by_id(caption_id)
    if caption:
        caption_manager.increment_usage(caption_id)
        logger.log(f"Caption copied: {caption_id}")
        return {
            "success": True,
            "message": "Caption copied and usage tracked",
            "caption": caption
        }
    else:
        raise HTTPException(status_code=404, detail="Caption not found")

@app.delete("/api/captions/{caption_id}")
async def delete_caption(caption_id: str):
    """Delete a caption"""
    if caption_manager.delete_caption(caption_id):
        logger.log(f"Caption deleted: {caption_id}")
        return {"success": True}
    else:
        raise HTTPException(status_code=404, detail="Caption not found")

@app.post("/api/captions/add-single")
async def add_single_caption(text: str = Form(...), category: str = Form(...)):
    """Add a single caption manually"""
    try:
        new_caption = caption_manager.add_single_caption(text, category)
        logger.log(f"Caption added: {new_caption['id']}")
        return {
            "success": True,
            "caption": new_caption,
            "message": "Caption added successfully"
        }
    except Exception as e:
        logger.error(f"Error adding caption: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/captions/{caption_id}")
async def update_caption(caption_id: str, text: Optional[str] = Form(None), category: Optional[str] = Form(None)):
    """Update an existing caption"""
    if caption_manager.update_caption(caption_id, text, category):
        logger.log(f"Caption updated: {caption_id}")
        return {"success": True, "message": "Caption updated"}
    else:
        raise HTTPException(status_code=404, detail="Caption not found")

@app.get("/api/captions/popular")
async def get_popular_captions(limit: int = 10):
    """Get the most popular captions"""
    return caption_manager.get_popular_captions(limit)

@app.get("/api/captions/recent")
async def get_recent_captions(limit: int = 10):
    """Get recently added captions"""
    return caption_manager.get_recent_captions(limit)

@app.get("/api/captions/stats")
async def get_caption_stats():
    """Get caption library statistics"""
    return caption_manager.get_statistics()

@app.post("/api/captions/clear")
async def clear_all_captions():
    """Clear all captions from the library"""
    caption_manager.clear_all_captions()
    print("All captions cleared")
    return {"success": True, "message": "All captions cleared"}

@app.get("/api/captions/export")
async def export_captions():
    """Export all captions to Excel file"""
    try:
        export_path = Path("exports/captions_export.xlsx")
        export_path.parent.mkdir(exist_ok=True)

        if caption_manager.export_to_excel(str(export_path)):
            logger.log("Captions exported to Excel")
            return FileResponse(
                path=str(export_path),
                filename=f"captions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            raise HTTPException(status_code=400, detail="No captions to export")
    except Exception as e:
        logger.error(f"Export failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
