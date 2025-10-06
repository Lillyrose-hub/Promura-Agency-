"""
PROMURA Authentication System
Complete user management with roles, permissions, and session handling
"""

import bcrypt
from jose import jwt
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, List, Any
from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Configuration
SECRET_KEY = "your-secret-key-change-this-in-production"  # TODO: Use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

# Security scheme for FastAPI
security = HTTPBearer()

class UserManager:
    """Manages user accounts, authentication, and permissions"""

    def __init__(self, storage_path: str = "data/users.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(exist_ok=True)
        self.users = self._load_users()
        self._initialize_default_users()

    def _load_users(self) -> Dict:
        """Load users from storage"""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_users(self):
        """Save users to storage"""
        with open(self.storage_path, 'w') as f:
            json.dump(self.users, f, indent=2)

    def _initialize_default_users(self):
        """Create default users if they don't exist"""
        default_users = {
            "lea": {
                "password": self._hash_password("admin123"),  # Change this!
                "role": "owner",
                "permissions": ["all"],
                "created_at": datetime.now().isoformat(),
                "full_name": "Lea (Owner)",
                "email": "lea@promura.com",
                "active": True
            },
            "social_manager": {
                "password": self._hash_password("manager123"),  # Change this!
                "role": "manager",
                "permissions": ["schedule", "view", "edit", "queue", "captions", "metrics"],
                "created_at": datetime.now().isoformat(),
                "full_name": "Social Media Manager",
                "email": "manager@promura.com",
                "active": True
            },
            "content_assistant": {
                "password": self._hash_password("assistant123"),  # Change this!
                "role": "assistant",
                "permissions": ["view", "schedule", "captions"],
                "created_at": datetime.now().isoformat(),
                "full_name": "Content Assistant",
                "email": "assistant@promura.com",
                "active": True
            }
        }

        # Only add users that don't exist
        for username, user_data in default_users.items():
            if username not in self.users:
                self.users[username] = user_data
                print(f"Created default user: {username}")

        self._save_users()

    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )

    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate a user and return user data if valid"""
        if username not in self.users:
            return None

        user = self.users[username]
        if not user.get("active", True):
            return None

        if not self.verify_password(password, user["password"]):
            return None

        # Return user data without password
        user_data = {k: v for k, v in user.items() if k != "password"}
        user_data["username"] = username
        return user_data

    def create_access_token(self, username: str) -> str:
        """Create a JWT access token"""
        user = self.users.get(username)
        if not user:
            raise ValueError("User not found")

        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": username,
            "role": user["role"],
            "permissions": user["permissions"],
            "exp": expire
        }

        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username and username in self.users:
                return payload
            return None
        except jwt.ExpiredSignatureError:
            return None
        except jwt.JWTError:
            return None

    def check_permission(self, username: str, permission: str) -> bool:
        """Check if a user has a specific permission"""
        user = self.users.get(username)
        if not user:
            return False

        user_perms = user.get("permissions", [])
        return "all" in user_perms or permission in user_perms

    def get_user(self, username: str) -> Optional[Dict]:
        """Get user data without password"""
        user = self.users.get(username)
        if user:
            return {k: v for k, v in user.items() if k != "password"}
        return None

    def update_user(self, username: str, updates: Dict) -> bool:
        """Update user information"""
        if username not in self.users:
            return False

        # Don't allow updating certain fields directly
        protected_fields = ["password", "created_at"]
        for field in protected_fields:
            updates.pop(field, None)

        self.users[username].update(updates)
        self.users[username]["updated_at"] = datetime.now().isoformat()
        self._save_users()
        return True

    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change a user's password"""
        if username not in self.users:
            return False

        if not self.verify_password(old_password, self.users[username]["password"]):
            return False

        self.users[username]["password"] = self._hash_password(new_password)
        self.users[username]["password_changed_at"] = datetime.now().isoformat()
        self._save_users()
        return True

    def list_users(self) -> List[Dict]:
        """List all users without passwords"""
        return [
            {**self.get_user(username), "username": username}
            for username in self.users.keys()
        ]


class AuditLogger:
    """Tracks all user actions for security and compliance"""

    def __init__(self, log_path: str = "data/audit_logs.json"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(exist_ok=True)
        self.logs = self._load_logs()

    def _load_logs(self) -> List[Dict]:
        """Load existing audit logs"""
        if self.log_path.exists():
            try:
                with open(self.log_path, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_logs(self):
        """Save audit logs to file"""
        # Keep only last 10000 entries to prevent file from growing too large
        if len(self.logs) > 10000:
            self.logs = self.logs[-10000:]

        with open(self.log_path, 'w') as f:
            json.dump(self.logs, f, indent=2)

    def log_action(self, username: str, action: str, details: str = None,
                  ip_address: str = None, endpoint: str = None, method: str = None):
        """Log a user action"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "username": username,
            "action": action,
            "details": details,
            "ip_address": ip_address,
            "endpoint": endpoint,
            "method": method
        }

        self.logs.append(log_entry)
        self._save_logs()

        # Also print to console for debugging
        print(f"[AUDIT] {username} - {action} - {details or 'No details'}")

    def get_user_logs(self, username: str, limit: int = 100) -> List[Dict]:
        """Get logs for a specific user"""
        user_logs = [log for log in self.logs if log.get("username") == username]
        return user_logs[-limit:]

    def get_recent_logs(self, limit: int = 100) -> List[Dict]:
        """Get recent audit logs"""
        return self.logs[-limit:]

    def get_logs_by_action(self, action: str, limit: int = 100) -> List[Dict]:
        """Get logs filtered by action type"""
        action_logs = [log for log in self.logs if log.get("action") == action]
        return action_logs[-limit:]

    def clear_old_logs(self, days: int = 90):
        """Clear logs older than specified days"""
        cutoff = datetime.now() - timedelta(days=days)
        self.logs = [
            log for log in self.logs
            if datetime.fromisoformat(log["timestamp"]) > cutoff
        ]
        self._save_logs()


# Initialize global instances
user_manager = UserManager()
audit_logger = AuditLogger()


# FastAPI dependency functions
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """Dependency to get the current authenticated user"""
    token = credentials.credentials
    payload = user_manager.verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    username = payload.get("sub")
    user = user_manager.get_user(username)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return {**user, "username": username}


def require_permission(permission: str):
    """Dependency to require a specific permission"""
    async def permission_checker(current_user: Dict = Depends(get_current_user)):
        username = current_user.get("username")
        if not user_manager.check_permission(username, permission):
            raise HTTPException(
                status_code=403,
                detail=f"Permission denied. Required: {permission}"
            )
        return current_user
    return permission_checker


# Helper function for optional authentication
async def get_optional_user(request: Request) -> Optional[Dict]:
    """Get current user if authenticated, otherwise return None"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ")[1]
    payload = user_manager.verify_token(token)

    if payload:
        username = payload.get("sub")
        return {**user_manager.get_user(username), "username": username}

    return None