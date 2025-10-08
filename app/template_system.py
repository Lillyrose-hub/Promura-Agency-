"""
Post Template System
Save and reuse post templates for recurring content
"""

import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class TemplateManager:
    """Manage post templates for recurring content"""

    def __init__(self, storage_path: str = "data/templates.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(exist_ok=True)
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict:
        """Load templates from storage"""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_templates(self):
        """Save templates to storage"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.templates, f, indent=2, ensure_ascii=False)

    def create_template(
        self,
        name: str,
        content: str,
        models: List[str],
        tags: List[str] = None,
        media_ids: List[str] = None,
        schedule_pattern: str = None,
        created_by: str = "system"
    ) -> Dict:
        """
        Create a new post template

        Args:
            name: Template name
            content: Post content text
            models: List of model names/IDs
            tags: Optional tags for categorization
            media_ids: Optional library media IDs to include
            schedule_pattern: Optional scheduling pattern (e.g., "weekly", "daily")
            created_by: Username who created the template

        Returns:
            Created template data
        """
        template_id = str(uuid.uuid4())

        template = {
            "id": template_id,
            "name": name,
            "content": content,
            "models": models,
            "tags": tags or [],
            "media_ids": media_ids or [],
            "schedule_pattern": schedule_pattern,
            "created_by": created_by,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "usage_count": 0,
            "last_used": None
        }

        self.templates[template_id] = template
        self._save_templates()

        return template

    def get_template(self, template_id: str) -> Optional[Dict]:
        """Get a specific template by ID"""
        return self.templates.get(template_id)

    def get_all_templates(self, tags: List[str] = None, created_by: str = None) -> List[Dict]:
        """
        Get all templates with optional filtering

        Args:
            tags: Filter by tags
            created_by: Filter by creator

        Returns:
            List of templates
        """
        templates = list(self.templates.values())

        # Filter by tags
        if tags:
            templates = [
                t for t in templates
                if any(tag in t.get('tags', []) for tag in tags)
            ]

        # Filter by creator
        if created_by:
            templates = [
                t for t in templates
                if t.get('created_by') == created_by
            ]

        # Sort by usage count and recency
        templates.sort(
            key=lambda x: (x['usage_count'], x['updated_at']),
            reverse=True
        )

        return templates

    def update_template(
        self,
        template_id: str,
        updates: Dict
    ) -> Optional[Dict]:
        """
        Update an existing template

        Args:
            template_id: Template ID
            updates: Dictionary of fields to update

        Returns:
            Updated template or None if not found
        """
        if template_id not in self.templates:
            return None

        # Don't allow updating certain fields
        protected_fields = ['id', 'created_by', 'created_at', 'usage_count']
        for field in protected_fields:
            updates.pop(field, None)

        # Update fields
        self.templates[template_id].update(updates)
        self.templates[template_id]['updated_at'] = datetime.now().isoformat()

        self._save_templates()

        return self.templates[template_id]

    def delete_template(self, template_id: str) -> bool:
        """
        Delete a template

        Args:
            template_id: Template ID

        Returns:
            True if deleted, False if not found
        """
        if template_id in self.templates:
            del self.templates[template_id]
            self._save_templates()
            return True
        return False

    def use_template(self, template_id: str) -> Optional[Dict]:
        """
        Mark a template as used and return its data

        Args:
            template_id: Template ID

        Returns:
            Template data or None if not found
        """
        if template_id not in self.templates:
            return None

        template = self.templates[template_id]
        template['usage_count'] += 1
        template['last_used'] = datetime.now().isoformat()

        self._save_templates()

        return template

    def duplicate_template(self, template_id: str, new_name: str = None) -> Optional[Dict]:
        """
        Create a duplicate of an existing template

        Args:
            template_id: Template ID to duplicate
            new_name: Optional new name (defaults to "Copy of [original name]")

        Returns:
            New template or None if original not found
        """
        original = self.get_template(template_id)
        if not original:
            return None

        new_template = original.copy()
        new_template['id'] = str(uuid.uuid4())
        new_template['name'] = new_name or f"Copy of {original['name']}"
        new_template['created_at'] = datetime.now().isoformat()
        new_template['updated_at'] = datetime.now().isoformat()
        new_template['usage_count'] = 0
        new_template['last_used'] = None

        self.templates[new_template['id']] = new_template
        self._save_templates()

        return new_template

    def get_popular_templates(self, limit: int = 10) -> List[Dict]:
        """Get most frequently used templates"""
        templates = list(self.templates.values())
        templates.sort(key=lambda x: x['usage_count'], reverse=True)
        return templates[:limit]

    def get_recent_templates(self, limit: int = 10) -> List[Dict]:
        """Get most recently used templates"""
        templates = [t for t in self.templates.values() if t.get('last_used')]
        templates.sort(key=lambda x: x['last_used'], reverse=True)
        return templates[:limit]

    def get_statistics(self) -> Dict:
        """Get template usage statistics"""
        templates = list(self.templates.values())

        if not templates:
            return {
                "total_templates": 0,
                "total_uses": 0,
                "most_popular": None,
                "recently_used": 0
            }

        total_uses = sum(t['usage_count'] for t in templates)
        most_popular = max(templates, key=lambda x: x['usage_count']) if templates else None

        # Count templates used in last 7 days
        from datetime import timedelta
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        recently_used = len([
            t for t in templates
            if t.get('last_used') and t['last_used'] > week_ago
        ])

        return {
            "total_templates": len(templates),
            "total_uses": total_uses,
            "most_popular": most_popular,
            "recently_used": recently_used
        }


# Global instance
template_manager = TemplateManager()
