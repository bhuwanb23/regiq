#!/usr/bin/env python3
"""
REGIQ AI/ML - Template Loader
Template loading and management utilities.

This module provides:
- Template file loading
- Asset management
- Configuration loading
- Template caching

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import yaml

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))

# Configure logging
logger = logging.getLogger(__name__)


class TemplateLoader:
    """
    Template loader for managing template assets and configurations.
    
    Provides utilities for:
    - Loading template files
    - Managing CSS and HTML assets
    - Configuration management
    - Template caching
    """
    
    def __init__(self, assets_path: Optional[str] = None):
        """
        Initialize template loader.
        
        Args:
            assets_path: Optional path to assets directory
        """
        self.logger = logging.getLogger(__name__)
        
        # Set up paths
        if assets_path:
            self.assets_path = Path(assets_path)
        else:
            # Default to assets directory relative to this file
            self.assets_path = Path(__file__).parent.parent / "assets"
        
        self.css_path = self.assets_path / "css"
        self.templates_path = self.assets_path / "templates"
        self.images_path = self.assets_path / "images"
        
        # Create directories if they don't exist
        self._ensure_directories()
        
        # Cache for loaded assets
        self._css_cache: Dict[str, str] = {}
        self._template_cache: Dict[str, str] = {}
        self._config_cache: Dict[str, Dict[str, Any]] = {}
    
    def _ensure_directories(self) -> None:
        """Ensure asset directories exist."""
        directories = [self.assets_path, self.css_path, self.templates_path, self.images_path]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Ensured directory exists: {directory}")
    
    def load_css(self, css_name: str, use_cache: bool = True) -> str:
        """
        Load CSS file content.
        
        Args:
            css_name: CSS file name (without .css extension)
            use_cache: Whether to use cached content
            
        Returns:
            CSS content as string
        """
        try:
            # Check cache first
            if use_cache and css_name in self._css_cache:
                return self._css_cache[css_name]
            
            css_file = self.css_path / f"{css_name}.css"
            
            if not css_file.exists():
                # Create default CSS if it doesn't exist
                default_css = self._get_default_css(css_name)
                css_file.write_text(default_css, encoding='utf-8')
                self.logger.info(f"Created default CSS file: {css_file}")
            
            content = css_file.read_text(encoding='utf-8')
            
            # Cache the content
            if use_cache:
                self._css_cache[css_name] = content
            
            self.logger.debug(f"Loaded CSS: {css_name}")
            return content
            
        except Exception as e:
            self.logger.error(f"Failed to load CSS {css_name}: {str(e)}")
            return self._get_fallback_css()
    
    def load_html_template(self, template_name: str, use_cache: bool = True) -> str:
        """
        Load HTML template file.
        
        Args:
            template_name: Template file name (without .html extension)
            use_cache: Whether to use cached content
            
        Returns:
            HTML template content as string
        """
        try:
            # Check cache first
            if use_cache and template_name in self._template_cache:
                return self._template_cache[template_name]
            
            template_file = self.templates_path / f"{template_name}.html"
            
            if not template_file.exists():
                # Create default template if it doesn't exist
                default_template = self._get_default_html_template(template_name)
                template_file.write_text(default_template, encoding='utf-8')
                self.logger.info(f"Created default HTML template: {template_file}")
            
            content = template_file.read_text(encoding='utf-8')
            
            # Cache the content
            if use_cache:
                self._template_cache[template_name] = content
            
            self.logger.debug(f"Loaded HTML template: {template_name}")
            return content
            
        except Exception as e:
            self.logger.error(f"Failed to load HTML template {template_name}: {str(e)}")
            return self._get_fallback_html_template()
    
    def save_css(self, css_name: str, content: str) -> bool:
        """
        Save CSS content to file.
        
        Args:
            css_name: CSS file name (without .css extension)
            content: CSS content to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            css_file = self.css_path / f"{css_name}.css"
            css_file.write_text(content, encoding='utf-8')
            
            # Update cache
            self._css_cache[css_name] = content
            
            self.logger.info(f"Saved CSS file: {css_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save CSS {css_name}: {str(e)}")
            return False
    
    def save_html_template(self, template_name: str, content: str) -> bool:
        """
        Save HTML template content to file.
        
        Args:
            template_name: Template file name (without .html extension)
            content: HTML content to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            template_file = self.templates_path / f"{template_name}.html"
            template_file.write_text(content, encoding='utf-8')
            
            # Update cache
            self._template_cache[template_name] = content
            
            self.logger.info(f"Saved HTML template: {template_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save HTML template {template_name}: {str(e)}")
            return False
    
    def load_config(self, config_name: str, config_type: str = "yaml") -> Dict[str, Any]:
        """
        Load configuration file.
        
        Args:
            config_name: Configuration file name (without extension)
            config_type: Configuration file type (yaml, json)
            
        Returns:
            Configuration dictionary
        """
        try:
            cache_key = f"{config_name}.{config_type}"
            
            # Check cache first
            if cache_key in self._config_cache:
                return self._config_cache[cache_key]
            
            config_file = self.assets_path / f"{config_name}.{config_type}"
            
            if not config_file.exists():
                self.logger.warning(f"Configuration file not found: {config_file}")
                return {}
            
            if config_type.lower() == "yaml":
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f) or {}
            elif config_type.lower() == "json":
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                raise ValueError(f"Unsupported config type: {config_type}")
            
            # Cache the config
            self._config_cache[cache_key] = config
            
            self.logger.debug(f"Loaded configuration: {config_name}.{config_type}")
            return config
            
        except Exception as e:
            self.logger.error(f"Failed to load config {config_name}: {str(e)}")
            return {}
    
    def _get_default_css(self, css_name: str) -> str:
        """Get default CSS content for a given CSS name."""
        if css_name == "executive":
            return """
/* Executive Report CSS */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    margin: 0;
    padding: 40px;
    background-color: #f8f9fa;
}

.header {
    background: linear-gradient(135deg, #007acc, #0056b3);
    color: white;
    padding: 30px;
    border-radius: 8px;
    margin-bottom: 30px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.header h1 {
    margin: 0;
    font-size: 2.5em;
    font-weight: 300;
}

.section {
    background: white;
    margin-bottom: 25px;
    padding: 25px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.section-title {
    color: #007acc;
    border-left: 4px solid #007acc;
    padding-left: 15px;
    margin-bottom: 20px;
}

.metrics-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
}

.metrics-table th,
.metrics-table td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
}

.metrics-table th {
    background-color: #007acc;
    color: white;
    font-weight: 600;
}

.status-excellent { background-color: #d4edda; color: #155724; }
.status-good { background-color: #d1ecf1; color: #0c5460; }
.status-fair { background-color: #fff3cd; color: #856404; }
.status-poor { background-color: #f8d7da; color: #721c24; }
"""
        elif css_name == "technical":
            return """
/* Technical Report CSS */
body {
    font-family: 'Courier New', 'Monaco', monospace;
    line-height: 1.5;
    color: #2c3e50;
    margin: 0;
    padding: 30px;
    background-color: #ecf0f1;
}

.header {
    background: #34495e;
    color: white;
    padding: 25px;
    border-radius: 5px;
    margin-bottom: 25px;
}

.section {
    background: white;
    margin-bottom: 20px;
    padding: 20px;
    border: 1px solid #bdc3c7;
    border-radius: 5px;
}

.code-block {
    background: #2c3e50;
    color: #ecf0f1;
    padding: 15px;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
    overflow-x: auto;
}

.methodology {
    background: #f8f9fa;
    border-left: 3px solid #007acc;
    padding: 15px;
    margin: 15px 0;
}
"""
        elif css_name == "regulatory":
            return """
/* Regulatory Report CSS */
body {
    font-family: 'Times New Roman', serif;
    line-height: 1.8;
    color: #000;
    margin: 0;
    padding: 40px;
    background-color: white;
}

.header {
    border-bottom: 3px solid #000;
    padding-bottom: 20px;
    margin-bottom: 30px;
}

.section {
    margin-bottom: 30px;
    padding: 20px 0;
}

.compliance-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    border: 2px solid #000;
}

.compliance-table th,
.compliance-table td {
    border: 1px solid #000;
    padding: 10px;
    text-align: left;
}

.compliance-table th {
    background-color: #f0f0f0;
    font-weight: bold;
}

.audit-trail {
    background: #f9f9f9;
    border: 1px solid #ccc;
    padding: 15px;
    margin: 15px 0;
    font-size: 0.9em;
}
"""
        else:
            return """
/* Default CSS */
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    margin: 40px;
}

.header {
    border-bottom: 2px solid #333;
    padding-bottom: 20px;
    margin-bottom: 30px;
}

.section {
    margin-bottom: 30px;
}

.section-title {
    color: #333;
    border-left: 4px solid #007acc;
    padding-left: 15px;
}
"""
    
    def _get_default_html_template(self, template_name: str) -> str:
        """Get default HTML template content."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{{ title }}}} - REGIQ Report</title>
    <style>
        {{{{ css_content }}}}
    </style>
</head>
<body>
    <div class="header">
        <h1>{{{{ title }}}}</h1>
        <div class="metadata">
            <p><strong>Generated:</strong> {{{{ timestamp }}}}</p>
            <p><strong>Template:</strong> {template_name}</p>
        </div>
    </div>
    
    <div class="content">
        {{{{ content }}}}
    </div>
    
    <div class="footer">
        <p>Generated by REGIQ AI/ML Report System</p>
    </div>
</body>
</html>"""
    
    def _get_fallback_css(self) -> str:
        """Get fallback CSS content."""
        return """
body { 
    font-family: Arial, sans-serif; 
    margin: 40px; 
    line-height: 1.6; 
}
.header { 
    border-bottom: 2px solid #333; 
    padding-bottom: 20px; 
    margin-bottom: 30px; 
}
.section { 
    margin-bottom: 30px; 
}
"""
    
    def _get_fallback_html_template(self) -> str:
        """Get fallback HTML template."""
        return """<!DOCTYPE html>
<html>
<head>
    <title>REGIQ Report</title>
</head>
<body>
    <h1>REGIQ Report</h1>
    <div>{{ content }}</div>
</body>
</html>"""
    
    def list_assets(self) -> Dict[str, List[str]]:
        """
        List all available assets.
        
        Returns:
            Dictionary of asset types and their files
        """
        assets = {
            "css": [],
            "html_templates": [],
            "images": []
        }
        
        try:
            # List CSS files
            if self.css_path.exists():
                assets["css"] = [f.stem for f in self.css_path.glob("*.css")]
            
            # List HTML templates
            if self.templates_path.exists():
                assets["html_templates"] = [f.stem for f in self.templates_path.glob("*.html")]
            
            # List image files
            if self.images_path.exists():
                image_extensions = [".png", ".jpg", ".jpeg", ".gif", ".svg"]
                assets["images"] = [f.name for f in self.images_path.iterdir() 
                                 if f.suffix.lower() in image_extensions]
            
        except Exception as e:
            self.logger.error(f"Failed to list assets: {str(e)}")
        
        return assets
    
    def clear_cache(self) -> None:
        """Clear all cached content."""
        cache_sizes = {
            "css": len(self._css_cache),
            "templates": len(self._template_cache),
            "config": len(self._config_cache)
        }
        
        self._css_cache.clear()
        self._template_cache.clear()
        self._config_cache.clear()
        
        self.logger.info(f"Cache cleared: {cache_sizes}")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "css_cache_size": len(self._css_cache),
            "template_cache_size": len(self._template_cache),
            "config_cache_size": len(self._config_cache),
            "assets_path": str(self.assets_path)
        }
    
    def __str__(self) -> str:
        """String representation."""
        return f"TemplateLoader(assets_path={self.assets_path})"
