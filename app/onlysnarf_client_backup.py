import sys
import os
from datetime import datetime

# IMPORTANT: Set ENV before importing OnlySnarf to prevent argparse interference
os.environ['ENV'] = 'test'  # Use test mode to bypass argparse

# Add the OnlySnarf package to our path
onlysnarf_path = "/root/onlysnarf-dashboard/my_projects/onlysnarf"
if os.path.exists(onlysnarf_path):
    sys.path.insert(0, onlysnarf_path)
    print(f"✅ Added OnlySnarf to path: {onlysnarf_path}")
else:
    print(f"❌ OnlySnarf directory not found at: {onlysnarf_path}")
    raise ImportError("OnlySnarf not found")

# Import OnlySnarf components directly (avoiding full Snarf import)
from OnlySnarf.classes.message import Post
from OnlySnarf.classes.schedule import Schedule
from OnlySnarf.classes.file import File
from OnlySnarf.util.settings import Settings


class PromuraClient:
    """PROMURA Dashboard client for OnlySnarf operations"""

    def __init__(self):
        """Initialize the PROMURA client"""
        self.initialized = False
        self.init_onlysnarf()

    def init_onlysnarf(self):
        """Initialize OnlySnarf components"""
        try:
            # Test imports
            print("✅ PROMURA Client: OnlySnarf components imported successfully")

            # Set environment to avoid test mode
            os.environ.setdefault('ENV', 'production')

            self.initialized = True
            print("✅ PROMURA Client: Initialization complete")

        except Exception as e:
            print(f"❌ PROMURA Client: Failed to initialize - {e}")
            self.initialized = False
            raise

    def schedule_post(self, text, files=None, schedule_time=None):
        """
        Schedule a post using OnlySnarf's scheduling system

        Parameters
        ----------
        text : str
            The caption text for the post
        files : list, optional
            List of file paths to upload
        schedule_time : datetime, optional
            When to schedule the post (if None, posts immediately)

        Returns
        -------
        dict
            Result with 'success' boolean and 'message' or 'error'
        """
        if not self.initialized:
            return {"success": False, "error": "OnlySnarf not initialized"}

        try:
            # Create a Post instance
            post = Post()

            # Set the text/caption
            post.text = text

            # Set files if provided
            if files and len(files) > 0:
                file_objects = []
                for file_path in files:
                    if os.path.exists(file_path):
                        file_obj = File()
                        file_obj.path = file_path
                        file_objects.append(file_obj)
                    else:
                        print(f"⚠️  File not found: {file_path}")
                post.files = file_objects

            # Set schedule if provided
            if schedule_time:
                # Convert datetime to OnlySnarf's expected format
                schedule_str = schedule_time.strftime("%Y-%m-%d %H:%M:%S")
                Settings.set_schedule(schedule_str)

                # Create schedule object
                schedule = Schedule()

                # Convert to OnlySnarf's schedule format
                year = schedule_time.year
                month = schedule_time.strftime("%B")  # Full month name
                day = schedule_time.day
                hour = schedule_time.hour
                minute = schedule_time.minute

                # Convert to 12-hour format with AM/PM
                suffix = "am"
                if hour >= 12:
                    suffix = "pm"
                    if hour > 12:
                        hour = hour - 12
                elif hour == 0:
                    hour = 12

                # Set schedule properties
                schedule.year = year
                schedule.month = month
                schedule.day = day
                schedule.hour = hour
                schedule.minute = minute
                schedule.suffix = suffix
                schedule._initialized_ = True

                post.schedule = schedule

                print(f"📅 Scheduled for: {month} {day}, {year} at {hour}:{minute:02d} {suffix}")
            else:
                # Immediate post - set schedule to None
                post.schedule = None
                print("📤 Posting immediately")

            # Initialize the post (sets up all internal properties)
            post.init()

            # Send the post using OnlySnarf's posting workflow
            # This will use the updated workflow with our custom functions:
            # go_to_create_post() -> clear_draft() -> upload_files() ->
            # focus_text_area() -> set_caption_text() -> expires() -> schedule()
            success = post.send()

            if success:
                return {
                    "success": True,
                    "message": f"Post {'scheduled' if schedule_time else 'published'} successfully"
                }
            else:
                return {
                    "success": False,
                    "error": "OnlySnarf post.send() returned False"
                }

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"❌ Error in schedule_post: {error_details}")
            return {
                "success": False,
                "error": str(e),
                "traceback": error_details
            }

    def test_connection(self):
        """
        Test if we can connect to OnlySnarf

        Returns
        -------
        dict
            Result with 'success' boolean and 'message'
        """
        try:
            if not self.initialized:
                return {
                    "success": False,
                    "message": "PROMURA Client not initialized"
                }

            # Test that we can create objects
            test_post = Post()
            test_schedule = Schedule()

            return {
                "success": True,
                "message": "✅ PROMURA Client ready! OnlySnarf integration active.",
                "details": {
                    "onlysnarf_path": onlysnarf_path,
                    "post_class": str(type(test_post)),
                    "schedule_class": str(type(test_schedule))
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Connection test failed: {e}"
            }
