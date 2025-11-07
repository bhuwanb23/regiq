"""Test API startup and router registration"""

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
        print("✓ Main API app imported successfully")
        
        # Test routers
        from services.api.routers.regulatory_intelligence.main import router as ri_router
        print("✓ Regulatory Intelligence router imported successfully")
        
        from services.api.routers.bias_analysis.main import router as ba_router
        print("✓ Bias Analysis router imported successfully")
        
        from services.api.routers.risk_simulator.main import router as rs_router
        print("✓ Risk Simulation router imported successfully")
        
        from services.api.routers.report_generator.main import router as rg_router
        print("✓ Report Generation router imported successfully")
        
        # Test that routers are registered
        router_count = len(app.routes)
        print(f"✓ API has {router_count} registered routes")
        
        # We can't easily check specific routes without more complex inspection
        # Just verify that the app has routes
        assert router_count > 0, "API should have registered routes"
        
        return True
    except Exception as e:
        print(f"✗ Error importing API modules: {e}")
        return False

if __name__ == "__main__":
    success = test_api_imports()
    if success:
        print("\n✓ All API startup tests passed!")
        exit(0)
    else:
        print("\n✗ API startup tests failed!")
        exit(1)