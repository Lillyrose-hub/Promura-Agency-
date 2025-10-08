import json
import os
from datetime import datetime

class CreatorProfile:
    def __init__(self, username, display_name=None):
        self.username = username
        self.display_name = display_name or username
        self.created_at = datetime.now().isoformat()
        self.is_active = False

class ProfileManager:
    def __init__(self):
        self.profiles = []
        self.active_profile = None
    
    def add_profile(self, username, display_name=None):
        new_profile = CreatorProfile(username, display_name)
        self.profiles.append(new_profile)
        return True
    
    def list_profiles(self):
        return [{
            "username": profile.username,
            "display_name": profile.display_name,
            "is_active": profile == self.active_profile
        } for profile in self.profiles]
    
    def set_active_profile(self, username):
        for profile in self.profiles:
            if profile.username == username:
                self.active_profile = profile
                return True
        return False

profile_manager = ProfileManager()
