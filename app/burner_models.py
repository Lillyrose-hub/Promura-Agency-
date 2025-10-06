"""
Burner Test Models Manager
⚠️ TEMPORARY TEST DATA - FOR DEVELOPMENT ONLY
These are safe test accounts for development and demonstration purposes.
"""

from typing import List, Dict, Optional
from datetime import datetime
import random

# 19 Burner Test Models for Safe Development
BURNER_TEST_MODELS = [
    {"id": 1, "name": "testmodel_amber", "displayName": "Amber Rose", "status": "active", "tier": "premium"},
    {"id": 2, "name": "testmodel_bella", "displayName": "Bella Star", "status": "active", "tier": "standard"},
    {"id": 3, "name": "testmodel_chloe", "displayName": "Chloe Dreams", "status": "active", "tier": "premium"},
    {"id": 4, "name": "testmodel_diana", "displayName": "Diana Moon", "status": "active", "tier": "standard"},
    {"id": 5, "name": "testmodel_emma", "displayName": "Emma Luxe", "status": "active", "tier": "premium"},
    {"id": 6, "name": "testmodel_fiona", "displayName": "Fiona Grace", "status": "active", "tier": "standard"},
    {"id": 7, "name": "testmodel_gina", "displayName": "Gina Spark", "status": "active", "tier": "premium"},
    {"id": 8, "name": "testmodel_hanna", "displayName": "Hanna Bliss", "status": "active", "tier": "standard"},
    {"id": 9, "name": "testmodel_ivy", "displayName": "Ivy Divine", "status": "active", "tier": "premium"},
    {"id": 10, "name": "testmodel_jade", "displayName": "Jade Angel", "status": "active", "tier": "standard"},
    {"id": 11, "name": "testmodel_kira", "displayName": "Kira Rouge", "status": "active", "tier": "premium"},
    {"id": 12, "name": "testmodel_luna", "displayName": "Luna Sky", "status": "active", "tier": "standard"},
    {"id": 13, "name": "testmodel_mia", "displayName": "Mia Violet", "status": "active", "tier": "premium"},
    {"id": 14, "name": "testmodel_nina", "displayName": "Nina Pearl", "status": "active", "tier": "standard"},
    {"id": 15, "name": "testmodel_olive", "displayName": "Olive Dusk", "status": "active", "tier": "premium"},
    {"id": 16, "name": "testmodel_piper", "displayName": "Piper Dawn", "status": "active", "tier": "standard"},
    {"id": 17, "name": "testmodel_quinn", "displayName": "Quinn Blaze", "status": "active", "tier": "premium"},
    {"id": 18, "name": "testmodel_ruby", "displayName": "Ruby Shine", "status": "active", "tier": "standard"},
    {"id": 19, "name": "testmodel_sage", "displayName": "Sage Nova", "status": "active", "tier": "premium"},
]

PRODUCTION_DEPLOYMENT_MEMORY = """
🚨 IMPORTANT: BEFORE PRODUCTION DEPLOYMENT
============================================
These burner test models MUST BE REMOVED before going live.

TO REMOVE:
1. Navigate to: /api/models/cleanup-burners (requires Owner permission)
2. Or manually delete this file: app/burner_models.py
3. Restart the application

THESE ARE TEST ACCOUNTS ONLY - NOT REAL DATA
"""


class BurnerModelManager:
    """Manages burner test models for development"""

    def __init__(self):
        self.models = BURNER_TEST_MODELS.copy()
        self._add_avatars()

    def _add_avatars(self):
        """Add avatar paths to models"""
        for model in self.models:
            model["avatar"] = "/static/models/default.jpg"
            model["connected"] = True
            model["subscribers"] = random.randint(50, 500)
            model["posts"] = random.randint(10, 100)
            model["earnings"] = f"${random.randint(100, 5000)}"

    def get_all_models(self) -> List[Dict]:
        """Get all burner test models"""
        return self.models

    def get_model_by_id(self, model_id: int) -> Optional[Dict]:
        """Get specific model by ID"""
        for model in self.models:
            if model["id"] == model_id:
                return model
        return None

    def get_model_by_name(self, name: str) -> Optional[Dict]:
        """Get specific model by name"""
        for model in self.models:
            if model["name"] == name:
                return model
        return None

    def search_models(self, query: str) -> List[Dict]:
        """Search models by name or display name"""
        query = query.lower()
        return [
            model for model in self.models
            if query in model["name"].lower() or query in model["displayName"].lower()
        ]

    def get_active_models(self) -> List[Dict]:
        """Get only active models"""
        return [model for model in self.models if model["status"] == "active"]

    def get_premium_models(self) -> List[Dict]:
        """Get premium tier models"""
        return [model for model in self.models if model["tier"] == "premium"]

    def get_model_count(self) -> int:
        """Get total number of models"""
        return len(self.models)


# Global instance
burner_manager = BurnerModelManager()


# Warning banner for development
def print_burner_warning():
    """Print warning about burner test data"""
    print("\n" + "="*60)
    print("⚠️  BURNER TEST MODELS ACTIVE")
    print("="*60)
    print(f"Using {len(BURNER_TEST_MODELS)} test models for development")
    print("REMOVE BEFORE PRODUCTION DEPLOYMENT")
    print("="*60 + "\n")


# Print warning on import
print_burner_warning()
