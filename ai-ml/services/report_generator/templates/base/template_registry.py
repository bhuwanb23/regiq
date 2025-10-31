#!/usr/bin/env python3
"""
REGIQ AI/ML - Template Registry
Template management and registration system.

This module provides:
- Template registration and discovery
- Template factory methods
- Template validation
- Template metadata management

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))

from .base_template import BaseTemplate, TemplateMetadata

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class RegistryEntry:
    """Template registry entry."""
    template_class: Type[BaseTemplate]
    template_id: str
    template_name: str
    template_type: str
    version: str
    registered_at: str
    description: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (excluding class reference)."""
        return {
            "template_id": self.template_id,
            "template_name": self.template_name,
            "template_type": self.template_type,
            "version": self.version,
            "registered_at": self.registered_at,
            "description": self.description,
            "class_name": self.template_class.__name__
        }


class TemplateRegistry:
    """
    Template registry for managing and creating report templates.
    
    Provides centralized template management with:
    - Template registration
    - Template discovery
    - Template factory methods
    - Metadata management
    """
    
    _instance: Optional['TemplateRegistry'] = None
    _templates: Dict[str, RegistryEntry] = {}
    
    def __new__(cls) -> 'TemplateRegistry':
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize registry."""
        if not self._initialized:
            self.logger = logging.getLogger(__name__)
            self._initialized = True
            self.logger.info("Template registry initialized")
    
    def register_template(
        self, 
        template_class: Type[BaseTemplate],
        template_id: Optional[str] = None,
        template_name: Optional[str] = None,
        description: Optional[str] = None
    ) -> bool:
        """
        Register a template class.
        
        Args:
            template_class: Template class to register
            template_id: Optional custom template ID
            template_name: Optional custom template name
            description: Optional template description
            
        Returns:
            True if registration successful, False otherwise
        """
        try:
            # Create temporary instance to get metadata
            temp_instance = template_class(
                template_id=template_id or f"temp_{template_class.__name__.lower()}",
                template_name=template_name or template_class.__name__
            )
            
            # Use provided values or defaults from instance
            final_id = template_id or temp_instance.template_id
            final_name = template_name or temp_instance.template_name
            final_description = description or temp_instance.get_description()
            
            # Check if template already registered
            if final_id in self._templates:
                self.logger.warning(f"Template already registered: {final_id}")
                return False
            
            # Create registry entry
            entry = RegistryEntry(
                template_class=template_class,
                template_id=final_id,
                template_name=final_name,
                template_type=template_class.__name__,
                version=temp_instance.version,
                registered_at=datetime.utcnow().isoformat(),
                description=final_description
            )
            
            # Register template
            self._templates[final_id] = entry
            
            self.logger.info(f"Template registered: {final_id} ({template_class.__name__})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register template {template_class.__name__}: {str(e)}")
            return False
    
    def unregister_template(self, template_id: str) -> bool:
        """
        Unregister a template.
        
        Args:
            template_id: Template ID to unregister
            
        Returns:
            True if unregistration successful, False otherwise
        """
        if template_id in self._templates:
            del self._templates[template_id]
            self.logger.info(f"Template unregistered: {template_id}")
            return True
        else:
            self.logger.warning(f"Template not found for unregistration: {template_id}")
            return False
    
    def get_template(self, template_id: str, **kwargs) -> Optional[BaseTemplate]:
        """
        Create template instance by ID.
        
        Args:
            template_id: Template ID
            **kwargs: Additional arguments for template constructor
            
        Returns:
            Template instance or None if not found
        """
        if template_id not in self._templates:
            self.logger.error(f"Template not found: {template_id}")
            return None
        
        try:
            entry = self._templates[template_id]
            
            # Create instance with registry metadata
            instance = entry.template_class(
                template_id=entry.template_id,
                template_name=entry.template_name,
                version=entry.version,
                **kwargs
            )
            
            self.logger.debug(f"Template instance created: {template_id}")
            return instance
            
        except Exception as e:
            self.logger.error(f"Failed to create template instance {template_id}: {str(e)}")
            return None
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """
        List all registered templates.
        
        Returns:
            List of template metadata dictionaries
        """
        return [entry.to_dict() for entry in self._templates.values()]
    
    def get_template_info(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        Get template information.
        
        Args:
            template_id: Template ID
            
        Returns:
            Template information or None if not found
        """
        if template_id in self._templates:
            return self._templates[template_id].to_dict()
        return None
    
    def get_templates_by_type(self, template_type: str) -> List[Dict[str, Any]]:
        """
        Get templates by type.
        
        Args:
            template_type: Template type to filter by
            
        Returns:
            List of matching template metadata
        """
        return [
            entry.to_dict() 
            for entry in self._templates.values() 
            if entry.template_type == template_type
        ]
    
    def template_exists(self, template_id: str) -> bool:
        """
        Check if template exists.
        
        Args:
            template_id: Template ID to check
            
        Returns:
            True if template exists, False otherwise
        """
        return template_id in self._templates
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """
        Get registry statistics.
        
        Returns:
            Registry statistics
        """
        template_types = {}
        for entry in self._templates.values():
            template_types[entry.template_type] = template_types.get(entry.template_type, 0) + 1
        
        return {
            "total_templates": len(self._templates),
            "template_types": template_types,
            "template_ids": list(self._templates.keys()),
            "registry_initialized": self._initialized
        }
    
    def validate_registry(self) -> Tuple[bool, List[str]]:
        """
        Validate registry integrity.
        
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        try:
            # Check for duplicate template names
            names = [entry.template_name for entry in self._templates.values()]
            if len(names) != len(set(names)):
                errors.append("Duplicate template names found")
            
            # Check for valid template classes
            for template_id, entry in self._templates.items():
                if not issubclass(entry.template_class, BaseTemplate):
                    errors.append(f"Invalid template class for {template_id}")
            
            # Try to create instances
            for template_id, entry in self._templates.items():
                try:
                    temp_instance = entry.template_class(
                        template_id=entry.template_id,
                        template_name=entry.template_name
                    )
                except Exception as e:
                    errors.append(f"Cannot instantiate template {template_id}: {str(e)}")
            
        except Exception as e:
            errors.append(f"Registry validation error: {str(e)}")
        
        is_valid = len(errors) == 0
        if is_valid:
            self.logger.info("Registry validation passed")
        else:
            self.logger.warning(f"Registry validation failed: {len(errors)} errors")
        
        return is_valid, errors
    
    def clear_registry(self) -> None:
        """Clear all registered templates."""
        template_count = len(self._templates)
        self._templates.clear()
        self.logger.info(f"Registry cleared: {template_count} templates removed")
    
    def export_registry(self) -> Dict[str, Any]:
        """
        Export registry metadata.
        
        Returns:
            Registry export data
        """
        return {
            "export_timestamp": datetime.utcnow().isoformat(),
            "registry_stats": self.get_registry_stats(),
            "templates": self.list_templates()
        }
    
    def __len__(self) -> int:
        """Get number of registered templates."""
        return len(self._templates)
    
    def __contains__(self, template_id: str) -> bool:
        """Check if template ID is registered."""
        return template_id in self._templates
    
    def __iter__(self):
        """Iterate over template IDs."""
        return iter(self._templates.keys())
    
    def __str__(self) -> str:
        """String representation."""
        return f"TemplateRegistry({len(self._templates)} templates)"
    
    def __repr__(self) -> str:
        """Detailed representation."""
        return (f"TemplateRegistry(templates={len(self._templates)}, "
                f"types={list(set(e.template_type for e in self._templates.values()))})")


# Global registry instance
registry = TemplateRegistry()


def register_template(template_class: Type[BaseTemplate], **kwargs) -> bool:
    """
    Convenience function to register a template.
    
    Args:
        template_class: Template class to register
        **kwargs: Additional registration arguments
        
    Returns:
        True if registration successful
    """
    return registry.register_template(template_class, **kwargs)


def get_template(template_id: str, **kwargs) -> Optional[BaseTemplate]:
    """
    Convenience function to get a template instance.
    
    Args:
        template_id: Template ID
        **kwargs: Additional constructor arguments
        
    Returns:
        Template instance or None
    """
    return registry.get_template(template_id, **kwargs)


def list_templates() -> List[Dict[str, Any]]:
    """
    Convenience function to list all templates.
    
    Returns:
        List of template metadata
    """
    return registry.list_templates()
