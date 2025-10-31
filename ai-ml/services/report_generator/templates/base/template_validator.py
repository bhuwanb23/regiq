#!/usr/bin/env python3
"""
REGIQ AI/ML - Template Validator
Template validation and quality assurance system.

This module provides:
- Template structure validation
- Data integrity checks
- Output quality validation
- Performance validation
- Security validation

Author: REGIQ AI/ML Team
Version: 1.0.0
"""

import os
import sys
import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))

from .base_template import BaseTemplate, ReportSection, ReportData

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Template validation result."""
    is_valid: bool
    validation_type: str
    errors: List[str]
    warnings: List[str]
    score: float  # 0.0 to 1.0
    details: Dict[str, Any]
    timestamp: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class ValidationRule:
    """Template validation rule."""
    rule_id: str
    rule_name: str
    rule_type: str
    severity: str  # 'error', 'warning', 'info'
    description: str
    validator_function: callable
    
    def validate(self, template: BaseTemplate, data: Any = None) -> Tuple[bool, str]:
        """Execute validation rule."""
        try:
            return self.validator_function(template, data)
        except Exception as e:
            return False, f"Validation rule error: {str(e)}"


class TemplateValidator:
    """
    Template validation system for ensuring template quality and compliance.
    
    Provides comprehensive validation including:
    - Structure validation
    - Data integrity checks
    - Output quality validation
    - Performance validation
    - Security validation
    """
    
    def __init__(self):
        """Initialize validator."""
        self.logger = logging.getLogger(__name__)
        self.validation_rules: Dict[str, ValidationRule] = {}
        self._initialize_default_rules()
    
    def _initialize_default_rules(self) -> None:
        """Initialize default validation rules."""
        
        # Structure validation rules
        self.add_rule(ValidationRule(
            rule_id="template_metadata",
            rule_name="Template Metadata Validation",
            rule_type="structure",
            severity="error",
            description="Validate template metadata completeness",
            validator_function=self._validate_template_metadata
        ))
        
        self.add_rule(ValidationRule(
            rule_id="section_structure",
            rule_name="Section Structure Validation",
            rule_type="structure", 
            severity="error",
            description="Validate section structure and ordering",
            validator_function=self._validate_section_structure
        ))
        
        # Data validation rules
        self.add_rule(ValidationRule(
            rule_id="data_integrity",
            rule_name="Data Integrity Validation",
            rule_type="data",
            severity="error",
            description="Validate data integrity and consistency",
            validator_function=self._validate_data_integrity
        ))
        
        # Output validation rules
        self.add_rule(ValidationRule(
            rule_id="html_output",
            rule_name="HTML Output Validation",
            rule_type="output",
            severity="warning",
            description="Validate HTML output quality",
            validator_function=self._validate_html_output
        ))
        
        # Security validation rules
        self.add_rule(ValidationRule(
            rule_id="security_check",
            rule_name="Security Validation",
            rule_type="security",
            severity="error",
            description="Validate template security",
            validator_function=self._validate_security
        ))
        
        self.logger.info(f"Initialized {len(self.validation_rules)} default validation rules")
    
    def add_rule(self, rule: ValidationRule) -> None:
        """Add validation rule."""
        self.validation_rules[rule.rule_id] = rule
        self.logger.debug(f"Added validation rule: {rule.rule_id}")
    
    def remove_rule(self, rule_id: str) -> bool:
        """Remove validation rule."""
        if rule_id in self.validation_rules:
            del self.validation_rules[rule_id]
            self.logger.debug(f"Removed validation rule: {rule_id}")
            return True
        return False
    
    def validate_template(
        self, 
        template: BaseTemplate, 
        data: Optional[ReportData] = None,
        rule_types: Optional[List[str]] = None
    ) -> ValidationResult:
        """
        Validate template comprehensively.
        
        Args:
            template: Template to validate
            data: Optional data for validation
            rule_types: Optional list of rule types to validate
            
        Returns:
            Validation result
        """
        errors = []
        warnings = []
        details = {}
        
        try:
            # Filter rules by type if specified
            rules_to_run = self.validation_rules.values()
            if rule_types:
                rules_to_run = [r for r in rules_to_run if r.rule_type in rule_types]
            
            # Run validation rules
            for rule in rules_to_run:
                try:
                    is_valid, message = rule.validate(template, data)
                    
                    if not is_valid:
                        if rule.severity == "error":
                            errors.append(f"{rule.rule_name}: {message}")
                        elif rule.severity == "warning":
                            warnings.append(f"{rule.rule_name}: {message}")
                    
                    details[rule.rule_id] = {
                        "valid": is_valid,
                        "message": message,
                        "severity": rule.severity
                    }
                    
                except Exception as e:
                    error_msg = f"{rule.rule_name}: Validation error - {str(e)}"
                    errors.append(error_msg)
                    details[rule.rule_id] = {
                        "valid": False,
                        "message": error_msg,
                        "severity": "error"
                    }
            
            # Calculate validation score
            total_rules = len(rules_to_run)
            passed_rules = sum(1 for d in details.values() if d["valid"])
            score = passed_rules / total_rules if total_rules > 0 else 0.0
            
            # Determine overall validity (no errors)
            is_valid = len(errors) == 0
            
            result = ValidationResult(
                is_valid=is_valid,
                validation_type="comprehensive",
                errors=errors,
                warnings=warnings,
                score=score,
                details=details,
                timestamp=datetime.utcnow().isoformat()
            )
            
            self.logger.info(f"Template validation completed: {template.template_id} "
                           f"(Valid: {is_valid}, Score: {score:.2f})")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Template validation failed: {str(e)}")
            return ValidationResult(
                is_valid=False,
                validation_type="comprehensive",
                errors=[f"Validation system error: {str(e)}"],
                warnings=[],
                score=0.0,
                details={},
                timestamp=datetime.utcnow().isoformat()
            )
    
    def _validate_template_metadata(self, template: BaseTemplate, data: Any = None) -> Tuple[bool, str]:
        """Validate template metadata."""
        try:
            metadata = template.metadata
            
            # Check required fields
            required_fields = ["template_id", "template_name", "template_type", "version"]
            for field in required_fields:
                if not getattr(metadata, field, None):
                    return False, f"Missing required metadata field: {field}"
            
            # Check template ID format
            if not re.match(r'^[a-zA-Z0-9_-]+$', metadata.template_id):
                return False, "Template ID contains invalid characters"
            
            # Check version format
            if not re.match(r'^\d+\.\d+\.\d+$', metadata.version):
                return False, "Version must be in semantic versioning format (x.y.z)"
            
            return True, "Template metadata is valid"
            
        except Exception as e:
            return False, f"Metadata validation error: {str(e)}"
    
    def _validate_section_structure(self, template: BaseTemplate, data: Any = None) -> Tuple[bool, str]:
        """Validate section structure."""
        try:
            sections = template.sections
            
            if not sections:
                return False, "Template has no sections"
            
            # Check section IDs are unique
            section_ids = [s.section_id for s in sections]
            if len(section_ids) != len(set(section_ids)):
                return False, "Duplicate section IDs found"
            
            # Check section ordering
            orders = [s.order for s in sections]
            if orders != sorted(orders):
                return False, "Sections are not properly ordered"
            
            # Check required section fields
            for section in sections:
                if not section.section_id or not section.title:
                    return False, "Section missing required fields (section_id, title)"
            
            return True, f"Section structure is valid ({len(sections)} sections)"
            
        except Exception as e:
            return False, f"Section validation error: {str(e)}"
    
    def _validate_data_integrity(self, template: BaseTemplate, data: Any = None) -> Tuple[bool, str]:
        """Validate data integrity."""
        try:
            if data and isinstance(data, ReportData):
                is_valid, errors = data.validate()
                if not is_valid:
                    return False, f"Data validation failed: {', '.join(errors)}"
            
            # Check if template can validate its own data requirements
            if hasattr(template, 'validate_data') and data:
                is_valid, errors = template.validate_data(data)
                if not is_valid:
                    return False, f"Template data validation failed: {', '.join(errors)}"
            
            return True, "Data integrity is valid"
            
        except Exception as e:
            return False, f"Data integrity validation error: {str(e)}"
    
    def _validate_html_output(self, template: BaseTemplate, data: Any = None) -> Tuple[bool, str]:
        """Validate HTML output quality."""
        try:
            # Generate sample HTML output
            if data and isinstance(data, ReportData):
                report = template.generate_report(data, "html")
                html_content = report.get("content", "")
            else:
                # Use template's HTML generation without data
                html_content = template._generate_html_output()
            
            # Basic HTML validation
            if not html_content:
                return False, "HTML output is empty"
            
            if not html_content.strip().startswith("<!DOCTYPE html>"):
                return False, "HTML output missing DOCTYPE declaration"
            
            # Check for basic HTML structure
            required_tags = ["<html", "<head", "<body", "</html>"]
            for tag in required_tags:
                if tag not in html_content:
                    return False, f"HTML output missing required tag: {tag}"
            
            # Check for potential XSS vulnerabilities
            dangerous_patterns = ["<script", "javascript:", "onload=", "onerror="]
            for pattern in dangerous_patterns:
                if pattern.lower() in html_content.lower():
                    return False, f"Potential security issue in HTML: {pattern}"
            
            return True, "HTML output is valid"
            
        except Exception as e:
            return False, f"HTML validation error: {str(e)}"
    
    def _validate_security(self, template: BaseTemplate, data: Any = None) -> Tuple[bool, str]:
        """Validate template security."""
        try:
            # Check for potential code injection in template
            template_str = str(template.__class__)
            
            # Check for dangerous imports or functions
            dangerous_patterns = ["eval(", "exec(", "__import__", "subprocess", "os.system"]
            
            # This is a basic check - in production, you'd want more sophisticated analysis
            for pattern in dangerous_patterns:
                if pattern in template_str:
                    return False, f"Potential security risk: {pattern}"
            
            # Check template methods for security issues
            if hasattr(template, '__dict__'):
                for attr_name, attr_value in template.__dict__.items():
                    if callable(attr_value) and any(pattern in str(attr_value) for pattern in dangerous_patterns):
                        return False, f"Security risk in template method: {attr_name}"
            
            return True, "Template security validation passed"
            
        except Exception as e:
            return False, f"Security validation error: {str(e)}"
    
    def validate_output_format(self, output: str, format_type: str) -> ValidationResult:
        """
        Validate specific output format.
        
        Args:
            output: Output content to validate
            format_type: Format type (html, pdf, json)
            
        Returns:
            Validation result
        """
        errors = []
        warnings = []
        
        try:
            if format_type.lower() == "html":
                # HTML validation
                if not output.strip():
                    errors.append("HTML output is empty")
                elif not output.strip().startswith("<!DOCTYPE"):
                    warnings.append("HTML missing DOCTYPE declaration")
                
                # Check for basic structure
                if "<html" not in output:
                    errors.append("HTML missing <html> tag")
                if "<head" not in output:
                    warnings.append("HTML missing <head> section")
                if "<body" not in output:
                    errors.append("HTML missing <body> tag")
                    
            elif format_type.lower() == "json":
                # JSON validation
                try:
                    json.loads(output)
                except json.JSONDecodeError as e:
                    errors.append(f"Invalid JSON format: {str(e)}")
                    
            elif format_type.lower() == "pdf":
                # PDF validation (basic check)
                if not output or len(output) < 100:
                    errors.append("PDF output appears to be empty or too small")
            
            is_valid = len(errors) == 0
            score = 1.0 if is_valid else 0.5 if len(warnings) == 0 else 0.0
            
            return ValidationResult(
                is_valid=is_valid,
                validation_type=f"{format_type}_output",
                errors=errors,
                warnings=warnings,
                score=score,
                details={"format": format_type, "output_length": len(output)},
                timestamp=datetime.utcnow().isoformat()
            )
            
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                validation_type=f"{format_type}_output",
                errors=[f"Output validation error: {str(e)}"],
                warnings=[],
                score=0.0,
                details={},
                timestamp=datetime.utcnow().isoformat()
            )
    
    def get_validation_rules(self) -> List[Dict[str, Any]]:
        """Get all validation rules."""
        return [
            {
                "rule_id": rule.rule_id,
                "rule_name": rule.rule_name,
                "rule_type": rule.rule_type,
                "severity": rule.severity,
                "description": rule.description
            }
            for rule in self.validation_rules.values()
        ]
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """Get validation statistics."""
        rule_types = {}
        severities = {}
        
        for rule in self.validation_rules.values():
            rule_types[rule.rule_type] = rule_types.get(rule.rule_type, 0) + 1
            severities[rule.severity] = severities.get(rule.severity, 0) + 1
        
        return {
            "total_rules": len(self.validation_rules),
            "rule_types": rule_types,
            "severities": severities
        }
    
    def __str__(self) -> str:
        """String representation."""
        return f"TemplateValidator({len(self.validation_rules)} rules)"
    
    def __repr__(self) -> str:
        """Detailed representation."""
        return (f"TemplateValidator(rules={len(self.validation_rules)}, "
                f"types={list(set(r.rule_type for r in self.validation_rules.values()))})")


# Global validator instance
validator = TemplateValidator()


def validate_template(template: BaseTemplate, data: Optional[ReportData] = None) -> ValidationResult:
    """
    Convenience function to validate a template.
    
    Args:
        template: Template to validate
        data: Optional data for validation
        
    Returns:
        Validation result
    """
    return validator.validate_template(template, data)
