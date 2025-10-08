"""
OnlySnarf Client with Safety Features and Logging
Real OnlyFans integration with dry-run mode, confirmations, and metrics tracking
"""

from app.real_onlysnarf_client import RealOnlySnarfClient
from app.logging_system import logger
import json
import time
import uuid
from typing import Dict, Any, Optional, List

class PromuraClient(RealOnlySnarfClient):
    """Enhanced OnlySnarf client with safety features"""

    def __init__(self, username: Optional[str] = None, dry_run: bool = True):
        """
        Initialize with safety features

        Args:
            username: OnlyFans username
            dry_run: If True, simulate posts without actually posting
        """
        # Load credentials
        credentials = {
            "username": "purplefan420",
            "password": "Problem420!",
            "email": "shanewikerdev@proton.me"
        }

        super().__init__(credentials)

        self.dry_run = dry_run
        self.test_mode = True  # Always start in test mode
        self.require_confirmation = True  # Require confirmation for live posts

        print(f"✅ PROMURA Client initialized")
        print(f"   Mode: {'DRY RUN (Safe)' if self.dry_run else 'LIVE (Caution!)'}")
        print(f"   Account: {self.credentials['username']}")

    def schedule_post(self, text: str, files: Optional[List[str]] = None,
                     schedule_time: Optional[str] = None) -> Dict[str, Any]:
        """
        Post with safety checks and logging

        Args:
            text: Post content
            files: Media files
            schedule_time: Schedule time

        Returns:
            Result with safety status
        """
        # Generate post ID for tracking
        post_id = str(uuid.uuid4())[:8]
        start_time = time.time()

        # Safety check 1: Dry run mode
        if self.dry_run:
            print(f"🔵 DRY RUN: Simulating post (not actually posting)")

            # Log the dry run
            logger.log_api_call(
                endpoint="/post/dry_run",
                method="POST",
                success=True,
                response_time=0.1,
                details={"post_id": post_id, "dry_run": True}
            )

            logger.log_post_completion(
                post_id=post_id,
                status="scheduled" if schedule_time else "completed",
                models=[self.credentials["username"]],
                content=text,
                schedule_time=schedule_time
            )

            return {
                "success": True,
                "message": "DRY RUN: Post simulated successfully",
                "post_id": post_id,
                "dry_run": True,
                "would_post": {
                    "text": text,
                    "files": files,
                    "schedule_time": schedule_time,
                    "account": self.credentials["username"]
                }
            }

        # Safety check 2: Confirmation required
        if self.require_confirmation:
            print(f"⚠️  LIVE POST WARNING")
            print(f"   Account: {self.credentials['username']}")
            print(f"   Content: {text[:50]}...")
            print(f"   Files: {len(files) if files else 0}")

            # In a real implementation, this would be a UI dialog
            # For now, we'll auto-deny for safety
            confirmed = False  # Set to True only with explicit user confirmation

            if not confirmed:
                logger.log_error(
                    error_type="confirmation_required",
                    message="Post cancelled - user confirmation required",
                    details={"post_id": post_id}
                )

                return {
                    "success": False,
                    "message": "Post cancelled - confirmation required",
                    "post_id": post_id,
                    "requires_confirmation": True
                }

        # If we get here, actually post (with real OnlySnarf)
        try:
            result = super().schedule_post(text, files, schedule_time)
            response_time = time.time() - start_time

            # Log the API call
            logger.log_api_call(
                endpoint="/post",
                method="POST",
                success=result.get("success", False),
                response_time=response_time,
                details={
                    "post_id": post_id,
                    "has_media": bool(files),
                    "scheduled": bool(schedule_time)
                }
            )

            # Log post completion
            logger.log_post_completion(
                post_id=post_id,
                status="completed" if result.get("success") else "failed",
                models=[self.credentials["username"]],
                content=text,
                schedule_time=schedule_time
            )

            result["post_id"] = post_id
            return result

        except Exception as e:
            response_time = time.time() - start_time

            # Log the error
            logger.log_error(
                error_type="post_failure",
                message=f"Failed to post: {str(e)}",
                details={"post_id": post_id},
                exception=e
            )

            logger.log_api_call(
                endpoint="/post",
                method="POST",
                success=False,
                response_time=response_time,
                details={"post_id": post_id, "error": str(e)}
            )

            return {
                "success": False,
                "message": f"Post failed: {str(e)}",
                "post_id": post_id
            }

    def test_connection(self) -> Dict[str, Any]:
        """Test connection without posting"""
        result = super().test_connection()
        result["mode"] = "dry_run" if self.dry_run else "live"
        result["safety_enabled"] = True
        return result

    def run_test_suite(self) -> Dict[str, Any]:
        """Run comprehensive test suite"""
        print("\n" + "=" * 60)
        print("🧪 PROMURA TEST SUITE - OnlyFans Integration")
        print("=" * 60)

        results = {}

        # Test 1: Authentication
        print("\n📋 Test 1: Authentication")
        auth_result = self.authenticate()
        results["authentication"] = {
            "passed": auth_result.get("success", False),
            "message": auth_result.get("message", "")
        }
        print(f"   Result: {'✅ PASS' if auth_result.get('success') else '❌ FAIL'}")

        # Test 2: Profile Access
        print("\n📋 Test 2: Profile Access")
        profile = self.get_account_info()
        results["profile_access"] = {
            "passed": profile.get("authenticated", False),
            "username": profile.get("username", ""),
            "email": profile.get("email", "")
        }
        print(f"   Result: {'✅ PASS' if profile.get('authenticated') else '❌ FAIL'}")

        # Test 3: Media Upload (Dry Run)
        print("\n📋 Test 3: Media Upload Test (Dry Run)")
        media_result = self.schedule_post(
            text="Test media upload",
            files=["/tmp/test.jpg"],  # Simulated file
            schedule_time=None
        )
        results["media_upload"] = {
            "passed": media_result.get("success", False),
            "dry_run": media_result.get("dry_run", False)
        }
        print(f"   Result: {'✅ PASS' if media_result.get('success') else '❌ FAIL'}")

        # Test 4: Text Post (Dry Run)
        print("\n📋 Test 4: Text Post Test (Dry Run)")
        text_result = self.schedule_post(
            text="Test text post from PROMURA Dashboard",
            files=None,
            schedule_time=None
        )
        results["text_post"] = {
            "passed": text_result.get("success", False),
            "dry_run": text_result.get("dry_run", False)
        }
        print(f"   Result: {'✅ PASS' if text_result.get('success') else '❌ FAIL'}")

        # Test 5: Scheduled Post (Dry Run)
        print("\n📋 Test 5: Scheduled Post Test (Dry Run)")
        schedule_result = self.schedule_post(
            text="Scheduled test post",
            files=None,
            schedule_time="2024-12-01T10:00:00"
        )
        results["scheduled_post"] = {
            "passed": schedule_result.get("success", False),
            "dry_run": schedule_result.get("dry_run", False)
        }
        print(f"   Result: {'✅ PASS' if schedule_result.get('success') else '❌ FAIL'}")

        # Summary
        print("\n" + "=" * 60)
        total_tests = len(results)
        passed_tests = sum(1 for r in results.values() if r.get("passed"))

        print(f"📊 TEST SUMMARY: {passed_tests}/{total_tests} tests passed")
        print("=" * 60)

        return {
            "success": passed_tests == total_tests,
            "passed": passed_tests,
            "total": total_tests,
            "results": results,
            "mode": "dry_run" if self.dry_run else "live"
        }

    def enable_live_mode(self, confirm: bool = False) -> bool:
        """
        Enable live posting mode (use with caution!)

        Args:
            confirm: Must be True to enable live mode

        Returns:
            True if live mode enabled
        """
        if confirm:
            self.dry_run = False
            self.test_mode = False
            print("⚠️  LIVE MODE ENABLED - Posts will be real!")
            return True
        else:
            print("❌ Live mode NOT enabled - confirmation required")
            return False

    def disable_live_mode(self):
        """Return to safe dry-run mode"""
        self.dry_run = True
        self.test_mode = True
        print("✅ Returned to DRY RUN mode (safe)")

# Maintain backwards compatibility
MockPromuraClient = PromuraClient  # Alias for existing code