"""
Content Library Manager for PROMURA Dashboard
Handles media storage, retrieval, and usage tracking
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import hashlib
from PIL import Image
import uuid

class ContentLibrary:
    def __init__(self, base_path: str = "/opt/promura/app/static/library"):
        self.base_path = Path(base_path)
        self.metadata_file = self.base_path / "metadata.json"
        self.ensure_directories()
        self.load_metadata()

    def ensure_directories(self):
        """Ensure all required directories exist"""
        for media_type in ['images', 'videos']:
            for subdir in ['original', 'thumbnails']:
                (self.base_path / media_type / subdir).mkdir(parents=True, exist_ok=True)

    def load_metadata(self):
        """Load or initialize library metadata"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                self.library = json.load(f)
        else:
            self.library = {
                "images": [],
                "videos": [],
                "tags": [],
                "total_items": 0
            }
            self.save_metadata()

    def save_metadata(self):
        """Save library metadata to file"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.library, f, indent=2, default=str)

    def generate_file_id(self, filename: str, content: bytes) -> str:
        """Generate unique ID for file based on content hash"""
        hash_md5 = hashlib.md5(content).hexdigest()[:8]
        return f"{Path(filename).stem}_{hash_md5}"

    def create_thumbnail(self, file_path: Path, media_type: str) -> Path:
        """Create thumbnail for media file"""
        thumb_dir = self.base_path / media_type / "thumbnails"
        thumb_path = thumb_dir / f"{file_path.stem}_thumb.jpg"

        if media_type == "images":
            try:
                img = Image.open(file_path)
                img.thumbnail((300, 300), Image.Resampling.LANCZOS)
                img.save(thumb_path, "JPEG", quality=85)
                return thumb_path
            except Exception as e:
                print(f"Error creating thumbnail: {e}")
                return file_path
        else:
            # For videos, we'll use a placeholder or extract frame later
            return file_path

    def add_media(self, file_data: bytes, filename: str, tags: List[str] = None,
                  description: str = "") -> Dict:
        """Add new media to library"""
        # Determine media type
        ext = Path(filename).suffix.lower()
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            media_type = "images"
        elif ext in ['.mp4', '.mov', '.avi', '.webm']:
            media_type = "videos"
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        # Generate unique ID
        media_id = self.generate_file_id(filename, file_data)

        # Check if already exists
        existing = self.get_media_by_id(media_id)
        if existing:
            existing["used_count"] += 1
            self.save_metadata()
            return existing

        # Save original file
        original_dir = self.base_path / media_type / "original"
        file_path = original_dir / filename

        # Ensure unique filename
        counter = 1
        while file_path.exists():
            file_path = original_dir / f"{Path(filename).stem}_{counter}{Path(filename).suffix}"
            counter += 1

        # Write file
        with open(file_path, 'wb') as f:
            f.write(file_data)

        # Create thumbnail
        thumb_path = self.create_thumbnail(file_path, media_type)

        # Get file info
        file_size = len(file_data)

        # Create metadata entry
        media_entry = {
            "id": media_id,
            "filename": file_path.name,
            "original_name": filename,
            "type": media_type.rstrip('s'),  # "image" or "video"
            "url": f"/static/library/{media_type}/original/{file_path.name}",
            "thumbnail_url": f"/static/library/{media_type}/thumbnails/{thumb_path.name}",
            "upload_date": datetime.now().isoformat(),
            "file_size": self.format_size(file_size),
            "file_size_bytes": file_size,
            "used_count": 1,
            "last_used": datetime.now().isoformat(),
            "tags": tags or [],
            "description": description
        }

        # Add dimensions for images
        if media_type == "images":
            try:
                img = Image.open(file_path)
                media_entry["dimensions"] = f"{img.width}x{img.height}"
                media_entry["width"] = img.width
                media_entry["height"] = img.height
            except:
                pass

        # Add to library
        self.library[media_type].append(media_entry)
        self.library["total_items"] += 1

        # Update tags list
        if tags:
            for tag in tags:
                if tag not in self.library["tags"]:
                    self.library["tags"].append(tag)

        self.save_metadata()
        return media_entry

    def get_media_by_id(self, media_id: str) -> Optional[Dict]:
        """Get media entry by ID"""
        for media_type in ['images', 'videos']:
            for item in self.library[media_type]:
                if item["id"] == media_id:
                    return item
        return None

    def use_media(self, media_id: str) -> bool:
        """Increment usage count for media"""
        media = self.get_media_by_id(media_id)
        if media:
            media["used_count"] += 1
            media["last_used"] = datetime.now().isoformat()
            self.save_metadata()
            return True
        return False

    def delete_media(self, media_id: str) -> bool:
        """Delete media from library"""
        for media_type in ['images', 'videos']:
            for i, item in enumerate(self.library[media_type]):
                if item["id"] == media_id:
                    # Delete files
                    try:
                        original_path = self.base_path / media_type / "original" / item["filename"]
                        if original_path.exists():
                            original_path.unlink()

                        # Delete thumbnail
                        thumb_name = Path(item["thumbnail_url"]).name
                        thumb_path = self.base_path / media_type / "thumbnails" / thumb_name
                        if thumb_path.exists():
                            thumb_path.unlink()
                    except:
                        pass

                    # Remove from metadata
                    del self.library[media_type][i]
                    self.library["total_items"] -= 1
                    self.save_metadata()
                    return True
        return False

    def get_all_media(self, media_type: str = None, tags: List[str] = None) -> List[Dict]:
        """Get all media, optionally filtered"""
        result = []

        if media_type:
            types = [media_type + 's']  # Convert to plural
        else:
            types = ['images', 'videos']

        for mtype in types:
            if mtype in self.library:
                for item in self.library[mtype]:
                    if tags:
                        # Filter by tags if provided
                        if any(tag in item.get("tags", []) for tag in tags):
                            result.append(item)
                    else:
                        result.append(item)

        return result

    def search_media(self, query: str) -> List[Dict]:
        """Search media by filename, tags, or description"""
        query = query.lower()
        result = []

        for media_type in ['images', 'videos']:
            for item in self.library[media_type]:
                if (query in item["filename"].lower() or
                    query in item.get("description", "").lower() or
                    any(query in tag.lower() for tag in item.get("tags", []))):
                    result.append(item)

        return result

    def get_statistics(self) -> Dict:
        """Get library statistics"""
        total_size = 0
        most_used = None
        max_usage = 0

        for media_type in ['images', 'videos']:
            for item in self.library[media_type]:
                total_size += item.get("file_size_bytes", 0)
                if item["used_count"] > max_usage:
                    max_usage = item["used_count"]
                    most_used = item

        return {
            "total_items": self.library["total_items"],
            "total_images": len(self.library["images"]),
            "total_videos": len(self.library["videos"]),
            "total_size": self.format_size(total_size),
            "unique_tags": len(self.library["tags"]),
            "most_used": most_used
        }

    @staticmethod
    def format_size(bytes_size: int) -> str:
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f} TB"

# Global instance
content_library = ContentLibrary()