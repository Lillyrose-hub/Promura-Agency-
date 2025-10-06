"""
Caption Manager - Handles Excel file processing and caption storage
"""

import pandas as pd
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import io

class CaptionManager:
    def __init__(self, storage_path: str = "data/captions.json"):
        """Initialize the Caption Manager with persistent storage."""
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(exist_ok=True)
        self.captions = self._load_captions()
        self._ensure_ids()  # Ensure all captions have IDs

    def _load_captions(self) -> List[Dict]:
        """Load captions from storage file."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_captions(self):
        """Save captions to storage file."""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.captions, f, indent=2, ensure_ascii=False)

    def _ensure_ids(self):
        """Ensure all captions have unique IDs."""
        for caption in self.captions:
            if 'id' not in caption or not caption['id']:
                caption['id'] = str(uuid.uuid4())

    def process_excel_file(self, file_content: bytes, filename: str) -> Dict:
        """
        Process an Excel file and extract captions.

        Expected format:
        - Column A: Categories
        - Column B: Messages/Captions

        Returns:
        - Dictionary with processing results
        """
        try:
            # Read Excel file from bytes
            df = pd.read_excel(io.BytesIO(file_content))

            # Get column names (first two columns)
            columns = df.columns.tolist()

            # If columns are named, use them; otherwise use index
            if len(columns) >= 2:
                category_col = df.iloc[:, 0]  # First column
                message_col = df.iloc[:, 1]   # Second column
            else:
                raise ValueError("Excel file must have at least 2 columns")

            # Process and organize captions
            caption_data = {}
            new_captions = []
            categories_found = set()

            for index in range(len(df)):
                try:
                    category = str(category_col.iloc[index]).strip() if pd.notna(category_col.iloc[index]) else None
                    message = str(message_col.iloc[index]).strip() if pd.notna(message_col.iloc[index]) else None

                    # Skip rows with empty messages
                    if not message or message == 'nan':
                        continue

                    # Use default category if not specified
                    if not category or category == 'nan':
                        category = "General"

                    # Normalize category names
                    category = self._normalize_category(category)
                    categories_found.add(category)

                    # Add to caption data
                    if category not in caption_data:
                        caption_data[category] = []
                    caption_data[category].append(message)

                    # Create caption entry
                    caption_entry = {
                        "id": str(uuid.uuid4()),
                        "text": message,
                        "category": category,
                        "source": filename,
                        "created_at": datetime.now().isoformat(),
                        "usage_count": 0
                    }
                    new_captions.append(caption_entry)

                except Exception as e:
                    print(f"Error processing row {index}: {e}")
                    continue

            # Add new captions to storage
            self.captions.extend(new_captions)
            self._save_captions()

            return {
                "success": True,
                "message": f"Successfully processed {len(new_captions)} captions from {len(categories_found)} categories",
                "captions": new_captions,
                "categories": list(categories_found),
                "summary": {
                    "total": len(new_captions),
                    "by_category": {cat: len(msgs) for cat, msgs in caption_data.items()}
                }
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error processing Excel file: {str(e)}",
                "captions": []
            }

    def _normalize_category(self, category: str) -> str:
        """
        Normalize category names to match predefined categories.
        """
        category_map = {
            "tip": "Tip Prompt",
            "tips": "Tip Prompt",
            "tip prompt": "Tip Prompt",
            "mass": "Mass Message",
            "mass msg": "Mass Message",
            "mass message": "Mass Message",
            "live": "LIVE BOOST",
            "live boost": "LIVE BOOST",
            "livestream": "LIVE BOOST",
            "unlock": "Unlock Prompt",
            "unlocks": "Unlock Prompt",
            "unlock prompt": "Unlock Prompt",
            "bundle": "Bundle Prompt",
            "bundles": "Bundle Prompt",
            "bundle prompt": "Bundle Prompt",
            "ppv": "PPV Captions",
            "ppv caption": "PPV Captions",
            "ppv captions": "PPV Captions",
            "campaign": "Campaign Ideas",
            "campaigns": "Campaign Ideas",
            "campaign ideas": "Campaign Ideas",
            "general": "General",
            "other": "General"
        }

        # Check if category matches any known mapping
        lower_category = category.lower()
        for key, value in category_map.items():
            if lower_category == key:
                return value

        # Return original category if no match found
        return category

    def get_all_captions(self) -> List[Dict]:
        """Get all stored captions."""
        return self.captions

    def get_captions_by_category(self, category: str) -> List[Dict]:
        """Get captions filtered by category."""
        if category == "All Categories":
            return self.captions
        return [c for c in self.captions if c["category"] == category]

    def search_captions(self, query: str) -> List[Dict]:
        """Search captions by text content."""
        query_lower = query.lower()
        return [c for c in self.captions if query_lower in c["text"].lower()]

    def get_caption_by_id(self, caption_id: str) -> Optional[Dict]:
        """Get a specific caption by ID."""
        for caption in self.captions:
            if caption["id"] == caption_id:
                return caption
        return None

    def increment_usage(self, caption_id: str):
        """Increment the usage count for a caption."""
        for caption in self.captions:
            if caption["id"] == caption_id:
                caption["usage_count"] += 1
                caption["last_used"] = datetime.now().isoformat()
                self._save_captions()
                return True
        return False

    def delete_caption(self, caption_id: str) -> bool:
        """Delete a caption by ID."""
        for i, caption in enumerate(self.captions):
            if caption["id"] == caption_id:
                self.captions.pop(i)
                self._save_captions()
                return True
        return False

    def clear_all_captions(self):
        """Clear all captions from storage."""
        self.captions = []
        self._save_captions()

    def get_statistics(self) -> Dict:
        """Get statistics about stored captions."""
        if not self.captions:
            return {
                "total": 0,
                "categories": {},
                "most_used": [],
                "recent": []
            }

        # Count by category
        categories = {}
        for caption in self.captions:
            cat = caption["category"]
            categories[cat] = categories.get(cat, 0) + 1

        # Get most used captions
        most_used = sorted(
            self.captions,
            key=lambda x: x.get("usage_count", 0),
            reverse=True
        )[:5]

        # Get recent captions
        recent = sorted(
            self.captions,
            key=lambda x: x.get("created_at", ""),
            reverse=True
        )[:5]

        return {
            "total": len(self.captions),
            "categories": categories,
            "most_used": most_used,
            "recent": recent
        }

    def export_to_excel(self, filepath: str):
        """Export all captions to an Excel file."""
        if not self.captions:
            return False

        # Prepare data for DataFrame
        data = []
        for caption in self.captions:
            data.append({
                "Category": caption["category"],
                "Caption": caption["text"],
                "Usage Count": caption.get("usage_count", 0),
                "Created": caption.get("created_at", ""),
                "Source": caption.get("source", "")
            })

        # Create DataFrame and save to Excel
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False, sheet_name="Captions")
        return True

    def add_single_caption(self, text: str, category: str, created_by: str = "admin") -> Dict:
        """Add a single caption manually."""
        new_caption = {
            "id": f"cap_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}",
            "text": text,
            "category": self._normalize_category(category),
            "created_by": created_by,
            "usage_count": 0,
            "created_at": datetime.now().isoformat(),
            "source": "manual"
        }
        self.captions.append(new_caption)
        self._save_captions()
        return new_caption

    def update_caption(self, caption_id: str, text: str = None, category: str = None) -> bool:
        """Update an existing caption."""
        for caption in self.captions:
            if caption["id"] == caption_id:
                if text:
                    caption["text"] = text
                if category:
                    caption["category"] = self._normalize_category(category)
                caption["updated_at"] = datetime.now().isoformat()
                self._save_captions()
                return True
        return False

    def get_popular_captions(self, limit: int = 10) -> List[Dict]:
        """Get the most popular captions based on usage."""
        sorted_captions = sorted(
            self.captions,
            key=lambda x: x.get("usage_count", 0),
            reverse=True
        )
        return sorted_captions[:limit]

    def get_recent_captions(self, limit: int = 10) -> List[Dict]:
        """Get recently added captions."""
        sorted_captions = sorted(
            self.captions,
            key=lambda x: x.get("created_at", ""),
            reverse=True
        )
        return sorted_captions[:limit]

# Initialize global caption manager instance
caption_manager = CaptionManager()