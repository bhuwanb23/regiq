#!/usr/bin/env python3
"""
REGIQ AI/ML - Dashboard Engine
Dashboard layout and management system.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class DashboardLayout:
    """Dashboard layout configuration."""
    layout_id: str
    name: str
    grid_columns: int
    grid_rows: int
    gap: int
    responsive: bool = True
    breakpoints: Dict[str, int] = None
    
    def __post_init__(self):
        if self.breakpoints is None:
            self.breakpoints = {
                "mobile": 768,
                "tablet": 1024,
                "desktop": 1200
            }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class DashboardEngine:
    """
    Dashboard layout and management engine.
    
    Provides responsive dashboard layouts and grid management
    for compliance visualizations.
    """
    
    def __init__(self):
        """Initialize dashboard engine."""
        self.logger = logging.getLogger(__name__)
        self.layouts: Dict[str, DashboardLayout] = {}
        
        # Initialize standard layouts
        self._initialize_layouts()
        
        self.logger.info(f"Dashboard engine initialized with {len(self.layouts)} layouts")
    
    def _initialize_layouts(self) -> None:
        """Initialize standard dashboard layouts."""
        
        # Executive layout
        self.layouts["executive"] = DashboardLayout(
            layout_id="executive",
            name="Executive Layout",
            grid_columns=12,
            grid_rows=8,
            gap=16,
            responsive=True
        )
        
        # Technical layout
        self.layouts["technical"] = DashboardLayout(
            layout_id="technical",
            name="Technical Layout",
            grid_columns=12,
            grid_rows=10,
            gap=12,
            responsive=True
        )
        
        # Regulatory layout
        self.layouts["regulatory"] = DashboardLayout(
            layout_id="regulatory",
            name="Regulatory Layout",
            grid_columns=12,
            grid_rows=8,
            gap=16,
            responsive=True
        )
    
    def get_layout(self, layout_id: str) -> Optional[DashboardLayout]:
        """Get dashboard layout by ID."""
        return self.layouts.get(layout_id)
    
    def list_layouts(self) -> List[Dict[str, Any]]:
        """List all available layouts."""
        return [layout.to_dict() for layout in self.layouts.values()]
    
    def __str__(self) -> str:
        """String representation."""
        return f"DashboardEngine({len(self.layouts)} layouts)"
