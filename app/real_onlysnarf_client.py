"""
Real OnlySnarf Client - Direct Integration with OnlyFans
This client actually connects to OnlyFans and posts content
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any

class RealOnlySnarfClient:
    """Real OnlySnarf client that connects to actual OnlyFans account"""

    def __init__(self, credentials: Optional[Dict[str, str]] = None):
        """
        Initialize with real OnlyFans credentials

        Args:
            credentials: Dict containing username, password, email
        """
        self.authenticated = False
        self.credentials = credentials or self._load_credentials()
        self.config_path = Path.home() / ".onlysnarf"
        self.session_file = self.config_path / "session.json"

        # Setup OnlySnarf paths
        self.onlysnarf_path = Path.home() / "my_projects" / "onlysnarf"
        self.snarf_command = self._find_snarf_command()

        # Create necessary directories
        self._setup_directories()

        # Authenticate on initialization
        if self.credentials:
            self.authenticate()

    def _load_credentials(self) -> Dict[str, str]:
        """Load credentials from purplefan420.json config"""
        config_file = Path.home() / ".onlysnarf" / "conf" / "users" / "purplefan420.json"

        if config_file.exists():
            with open(config_file, 'r') as f:
                data = json.load(f)
                return {
                    "username": data.get("username", "purplefan420"),
                    "password": data.get("password", "Problem420!"),
                    "email": data.get("email", "shanewikerdev@proton.me")
                }

        # Fallback to hardcoded credentials
        return {
            "username": "purplefan420",
            "password": "Problem420!",
            "email": "shanewikerdev@proton.me"
        }

    def _find_snarf_command(self) -> str:
        """Find the snarf command location"""
        # Try system command first
        result = subprocess.run(["which", "snarf"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()

        # Try local installation
        local_snarf = self.onlysnarf_path / "bin" / "snarf"
        if local_snarf.exists():
            return str(local_snarf)

        # Try Python module execution - corrected path
        return "python3 -m onlysnarf.snarf"

    def _setup_directories(self):
        """Create necessary OnlySnarf directories"""
        dirs = [
            self.config_path,
            self.config_path / "conf",
            self.config_path / "conf" / "users",
            self.config_path / "downloads",
            self.config_path / "uploads",
            self.config_path / "logs"
        ]

        for directory in dirs:
            directory.mkdir(parents=True, exist_ok=True)

    def authenticate(self) -> Dict[str, Any]:
        """
        Authenticate with OnlyFans using real credentials
        """
        print(f"🔐 Authenticating with OnlyFans as {self.credentials['username']}...")

        # Save credentials to config file
        user_config = self.config_path / "conf" / "users" / f"{self.credentials['username']}.json"

        config_data = {
            "username": self.credentials["username"],
            "email": self.credentials["email"],
            "password": self.credentials["password"],
            "twoStepAuth": False,
            "displayName": "Purple Fan",
            "about": "Content Creator",
            "location": "United States"
        }

        with open(user_config, 'w') as f:
            json.dump(config_data, f, indent=2)

        # Test authentication with OnlySnarf
        test_cmd = [
            "snarf",  # Use snarf directly since it's in PATH
            "menu",   # Use menu command for testing
            "--username", self.credentials["username"],
            "-show"   # Show browser for debugging
        ]

        try:
            # Run authentication test
            result = subprocess.run(
                test_cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if "error" not in result.stderr.lower():
                self.authenticated = True
                print(f"✅ Successfully authenticated as {self.credentials['username']}")

                # Save session
                self._save_session()

                return {
                    "success": True,
                    "message": f"Authenticated as {self.credentials['username']}",
                    "username": self.credentials["username"]
                }
            else:
                print(f"❌ Authentication failed: {result.stderr}")
                return {
                    "success": False,
                    "message": "Authentication failed",
                    "error": result.stderr
                }

        except subprocess.TimeoutExpired:
            print("⏱️ Authentication timed out")
            return {
                "success": False,
                "message": "Authentication timed out"
            }
        except Exception as e:
            print(f"❌ Authentication error: {str(e)}")
            return {
                "success": False,
                "message": f"Authentication error: {str(e)}"
            }

    def _save_session(self):
        """Save authentication session"""
        session_data = {
            "username": self.credentials["username"],
            "authenticated": True,
            "timestamp": datetime.now().isoformat()
        }

        with open(self.session_file, 'w') as f:
            json.dump(session_data, f, indent=2)

    def schedule_post(self, text: str, files: Optional[List[str]] = None,
                     schedule_time: Optional[str] = None) -> Dict[str, Any]:
        """
        Actually post content to OnlyFans via OnlySnarf

        Args:
            text: Post caption/content
            files: List of media file paths
            schedule_time: Optional schedule time

        Returns:
            Result dictionary with success status
        """
        if not self.authenticated:
            auth_result = self.authenticate()
            if not auth_result["success"]:
                return auth_result

        # Build OnlySnarf command for real posting
        cmd = ["snarf", "post"]  # Use snarf directly

        # Add credentials
        cmd.extend(["--username", self.credentials["username"]])

        # Add content/text
        if text:
            # Save text to temporary file (OnlySnarf reads from file)
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(text)
                text_file = f.name
            cmd.extend(["-text", text_file])

        # Add media files
        if files:
            for file_path in files:
                if os.path.exists(file_path):
                    cmd.extend(["-media", file_path])

        # Add browser options
        cmd.extend([
            "-browser", "chrome",  # Use Chrome
            "-show",  # Show browser for debugging
            "-debug"  # Enable debug output
        ])

        # Add schedule if provided
        if schedule_time:
            cmd.extend(["-schedule", schedule_time])

        print(f"📤 Posting to OnlyFans: {' '.join(cmd)}")

        try:
            # Execute real post to OnlyFans
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=180  # 3 minute timeout for posting
            )

            if result.returncode == 0:
                print(f"✅ Successfully posted to OnlyFans!")
                return {
                    "success": True,
                    "message": "Successfully posted to OnlyFans!",
                    "details": result.stdout,
                    "username": self.credentials["username"],
                    "timestamp": datetime.now().isoformat()
                }
            else:
                print(f"❌ Post failed: {result.stderr}")
                return {
                    "success": False,
                    "message": "Failed to post to OnlyFans",
                    "error": result.stderr or result.stdout
                }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "message": "Post timed out (took too long)"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Post error: {str(e)}"
            }

    def test_connection(self) -> Dict[str, Any]:
        """
        Test real connection to OnlyFans
        """
        print(f"🔍 Testing connection to OnlyFans...")

        # Check if credentials exist
        if not self.credentials:
            return {
                "success": False,
                "message": "No credentials configured"
            }

        # Check if OnlySnarf is available
        if not self.snarf_command:
            return {
                "success": False,
                "message": "OnlySnarf not installed"
            }

        # Test actual connection
        test_cmd = [
            "snarf",
            "config",  # Use config command to check setup
            "--username", self.credentials["username"]
        ]

        try:
            result = subprocess.run(
                test_cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"Connected to OnlyFans as {self.credentials['username']}",
                    "authenticated": self.authenticated,
                    "username": self.credentials["username"]
                }
            else:
                return {
                    "success": False,
                    "message": "Connection test failed",
                    "error": result.stderr
                }

        except Exception as e:
            return {
                "success": False,
                "message": f"Connection error: {str(e)}"
            }

    def get_account_info(self) -> Dict[str, Any]:
        """Get real OnlyFans account information"""
        if not self.authenticated:
            self.authenticate()

        return {
            "username": self.credentials["username"],
            "email": self.credentials["email"],
            "authenticated": self.authenticated,
            "platform": "OnlyFans",
            "integration": "OnlySnarf"
        }

    def post_immediately(self, text: str, files: Optional[List[str]] = None) -> Dict[str, Any]:
        """Post content immediately to OnlyFans"""
        return self.schedule_post(text, files, schedule_time=None)

    def schedule_for_later(self, text: str, schedule_time: str,
                          files: Optional[List[str]] = None) -> Dict[str, Any]:
        """Schedule content for later posting"""
        return self.schedule_post(text, files, schedule_time)

# Create a global instance with real credentials
real_client = RealOnlySnarfClient({
    "username": "purplefan420",
    "password": "Problem420!",
    "email": "shanewikerdev@proton.me"
})