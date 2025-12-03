import os
import glob
import shutil

def cleanup_temp_files():
    # Delete temp files
    patterns = ["*.mp4", "*.mkv", "*.jpg", "*.png", "downloads/*", "insta_downloads/*"]
    for pattern in patterns:
        for f in glob.glob(pattern):
            try:
                if os.path.isfile(f): os.remove(f)
                elif os.path.isdir(f): shutil.rmtree(f)
            except: pass

def startup_cleanup_banner():
    cleanup_temp_files()
    print("✅ System Cleaned.")

def register_exit_cleanup():
    pass # Managed by function above
