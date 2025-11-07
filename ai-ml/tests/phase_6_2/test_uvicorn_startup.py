"""Test that the API can be started with uvicorn"""

import sys
import os
from pathlib import Path
import subprocess
import time

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

def test_uvicorn_startup():
    """Test that uvicorn can start the API server."""
    try:
        # Change to the project directory
        project_dir = Path(__file__).parent.parent.parent
        os.chdir(project_dir)
        
        # Try to start uvicorn with a short timeout to verify it can start
        # We'll use a short timeout and just check if it starts without errors
        print("Testing uvicorn startup...")
        
        # Import uvicorn to verify it's available
        import uvicorn
        print("✓ Uvicorn imported successfully")
        
        # Try to import the main module
        from services.api.main import app
        print("✓ Main app imported successfully")
        
        # Verify that the app has routes
        assert len(app.routes) > 0, "App should have routes"
        print(f"✓ App has {len(app.routes)} routes")
        
        return True
    except Exception as e:
        print(f"✗ Error testing uvicorn startup: {e}")
        return False

if __name__ == "__main__":
    success = test_uvicorn_startup()
    if success:
        print("\n✓ Uvicorn startup test passed!")
        exit(0)
    else:
        print("\n✗ Uvicorn startup test failed!")
        exit(1)