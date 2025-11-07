"""Test API startup with Data Pipeline routers"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

def test_api_imports():
    """Test that all API modules can be imported without errors."""
    try:
        # Test main API app
        from services.api.main import app
        print("✅ Main API app imported successfully")
        
        # Test data pipeline routers
        from services.api.routers.data_pipeline.main import router as dp_router
        print("✅ Data Pipeline main router imported successfully")
        
        from services.api.routers.data_pipeline.ingestion import router as dp_ingestion_router
        print("✅ Data Pipeline ingestion router imported successfully")
        
        from services.api.routers.data_pipeline.status import router as dp_status_router
        print("✅ Data Pipeline status router imported successfully")
        
        from services.api.routers.data_pipeline.results import router as dp_results_router
        print("✅ Data Pipeline results router imported successfully")
        
        # Test that routers are registered
        router_count = len(app.routes)
        print(f"✅ API has {router_count} registered routes")
        
        # We can't easily check specific routes without more complex inspection
        # Just verify that the app has routes
        assert router_count > 0, "API should have registered routes"
        
        return True
    except Exception as e:
        print(f"❌ Error importing API modules: {e}")
        return False

if __name__ == "__main__":
    success = test_api_imports()
    if success:
        print("\n✅ All API startup tests passed!")
        exit(0)
    else:
        print("\n❌ API startup tests failed!")
        exit(1)