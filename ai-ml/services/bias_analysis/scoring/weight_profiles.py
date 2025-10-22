#!/usr/bin/env python3
"""
REGIQ AI/ML - Weight Profile Manager
Manages and loads bias scoring weight profiles for different industry contexts.
"""

import os
import logging
import yaml
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass


logger = logging.getLogger("weight_profiles")


@dataclass
class WeightProfile:
    """Represents a bias scoring weight profile."""
    name: str
    demographic_parity: float
    equalized_odds: float
    calibration: float
    individual_fairness: float
    description: str = ""
    regulatory_context: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.regulatory_context is None:
            self.regulatory_context = []
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary of weights."""
        return {
            "demographic_parity": self.demographic_parity,
            "equalized_odds": self.equalized_odds,
            "calibration": self.calibration,
            "individual_fairness": self.individual_fairness
        }
    
    def validate(self, tolerance: float = 1e-6) -> bool:
        """Validate that weights sum to 1.0."""
        total = (self.demographic_parity + self.equalized_odds + 
                self.calibration + self.individual_fairness)
        return abs(total - 1.0) < tolerance


class WeightProfileManager:
    """
    Manages bias scoring weight profiles.
    
    Provides:
    - Loading weight profiles from YAML configuration
    - Selecting profiles by name or industry context
    - Creating custom weight profiles
    - Validating weight configurations
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize weight profile manager.
        
        Args:
            config_path: Path to weight profiles YAML file (defaults to config/bias_scoring_weights.yaml)
        """
        self.logger = logger
        
        # Determine config path
        if config_path is None:
            # Default to config directory
            base_dir = Path(__file__).parent.parent.parent.parent
            config_path = str(base_dir / "config" / "bias_scoring_weights.yaml")
        
        self.config_path = Path(config_path)
        self.profiles: Dict[str, WeightProfile] = {}
        
        # Load profiles
        self._load_profiles()
    
    def _load_profiles(self):
        """Load weight profiles from YAML configuration."""
        try:
            if not self.config_path.exists():
                self.logger.warning(f"Config file not found: {self.config_path}")
                self._load_default_profiles()
                return
            
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            if not config:
                self.logger.warning("Empty config file, loading defaults")
                self._load_default_profiles()
                return
            
            # Parse each profile
            for profile_name, profile_data in config.items():
                try:
                    profile = WeightProfile(
                        name=profile_name,
                        demographic_parity=float(profile_data.get("demographic_parity", 0.25)),
                        equalized_odds=float(profile_data.get("equalized_odds", 0.25)),
                        calibration=float(profile_data.get("calibration", 0.25)),
                        individual_fairness=float(profile_data.get("individual_fairness", 0.25)),
                        description=profile_data.get("description", ""),
                        regulatory_context=profile_data.get("regulatory_context", [])
                    )
                    
                    # Validate profile
                    if not profile.validate():
                        self.logger.warning(f"Profile '{profile_name}' weights do not sum to 1.0, normalizing...")
                        total = (profile.demographic_parity + profile.equalized_odds + 
                                profile.calibration + profile.individual_fairness)
                        profile.demographic_parity /= total
                        profile.equalized_odds /= total
                        profile.calibration /= total
                        profile.individual_fairness /= total
                    
                    self.profiles[profile_name] = profile
                    self.logger.info(f"Loaded weight profile: {profile_name}")
                    
                except Exception as e:
                    self.logger.error(f"Failed to load profile '{profile_name}': {e}")
            
            self.logger.info(f"Loaded {len(self.profiles)} weight profiles")
            
        except Exception as e:
            self.logger.error(f"Failed to load profiles from {self.config_path}: {e}")
            self._load_default_profiles()
    
    def _load_default_profiles(self):
        """Load default weight profiles as fallback."""
        default_profile = WeightProfile(
            name="default",
            demographic_parity=0.30,
            equalized_odds=0.35,
            calibration=0.20,
            individual_fairness=0.15,
            description="Default balanced profile"
        )
        self.profiles["default"] = default_profile
        self.logger.info("Loaded default weight profile")
    
    def get_profile(self, profile_name: str) -> Optional[WeightProfile]:
        """
        Get weight profile by name.
        
        Args:
            profile_name: Name of the profile to retrieve
            
        Returns:
            WeightProfile if found, None otherwise
        """
        profile = self.profiles.get(profile_name)
        if profile is None:
            self.logger.warning(f"Profile '{profile_name}' not found, using default")
            return self.profiles.get("default")
        return profile
    
    def get_weights(self, profile_name: str = "default") -> Dict[str, float]:
        """
        Get weights dictionary for a profile.
        
        Args:
            profile_name: Name of the profile (defaults to "default")
            
        Returns:
            Dictionary of metric weights
        """
        profile = self.get_profile(profile_name)
        if profile is None:
            # Return equal weights as ultimate fallback
            return {
                "demographic_parity": 0.25,
                "equalized_odds": 0.25,
                "calibration": 0.25,
                "individual_fairness": 0.25
            }
        return profile.to_dict()
    
    def list_profiles(self) -> List[str]:
        """
        Get list of available profile names.
        
        Returns:
            List of profile names
        """
        return list(self.profiles.keys())
    
    def get_profile_info(self, profile_name: str) -> Dict:
        """
        Get detailed information about a profile.
        
        Args:
            profile_name: Name of the profile
            
        Returns:
            Dictionary with profile information
        """
        profile = self.get_profile(profile_name)
        if profile is None:
            return {}
        
        return {
            "name": profile.name,
            "weights": profile.to_dict(),
            "description": profile.description,
            "regulatory_context": profile.regulatory_context,
            "is_valid": profile.validate()
        }
    
    def create_custom_profile(self, name: str, weights: Dict[str, float],
                            description: str = "", 
                            regulatory_context: Optional[List[str]] = None) -> WeightProfile:
        """
        Create a custom weight profile.
        
        Args:
            name: Profile name
            weights: Dictionary of weights
            description: Profile description
            regulatory_context: List of relevant regulations
            
        Returns:
            Created WeightProfile
        """
        profile = WeightProfile(
            name=name,
            demographic_parity=weights.get("demographic_parity", 0.25),
            equalized_odds=weights.get("equalized_odds", 0.25),
            calibration=weights.get("calibration", 0.25),
            individual_fairness=weights.get("individual_fairness", 0.25),
            description=description,
            regulatory_context=regulatory_context or []
        )
        
        # Validate and normalize if needed
        if not profile.validate():
            self.logger.warning(f"Custom profile '{name}' weights do not sum to 1.0, normalizing...")
            total = (profile.demographic_parity + profile.equalized_odds + 
                    profile.calibration + profile.individual_fairness)
            profile.demographic_parity /= total
            profile.equalized_odds /= total
            profile.calibration /= total
            profile.individual_fairness /= total
        
        self.profiles[name] = profile
        self.logger.info(f"Created custom profile: {name}")
        
        return profile
    
    def get_profile_by_regulatory_context(self, regulation: str) -> Optional[WeightProfile]:
        """
        Find profile matching a specific regulation.
        
        Args:
            regulation: Regulation name/identifier
            
        Returns:
            Matching WeightProfile or default
        """
        for profile in self.profiles.values():
            if profile.regulatory_context and regulation in profile.regulatory_context:
                return profile
        
        self.logger.warning(f"No profile found for regulation '{regulation}', using default")
        return self.profiles.get("default")


def main():
    """Test the weight profile manager."""
    print("🧪 Testing Weight Profile Manager")
    
    # Create manager
    manager = WeightProfileManager()
    
    # List available profiles
    profiles = manager.list_profiles()
    print(f"✅ Available profiles: {profiles}")
    
    # Get default profile
    default_weights = manager.get_weights("default")
    print(f"✅ Default weights: {default_weights}")
    
    # Get lending profile
    lending_weights = manager.get_weights("lending")
    print(f"✅ Lending weights: {lending_weights}")
    
    # Get profile info
    info = manager.get_profile_info("eu_ai_act_high_risk")
    print(f"✅ EU AI Act profile info: {info}")
    
    # Create custom profile
    custom_weights = {
        "demographic_parity": 0.40,
        "equalized_odds": 0.30,
        "calibration": 0.20,
        "individual_fairness": 0.10
    }
    custom_profile = manager.create_custom_profile(
        "my_custom",
        custom_weights,
        "My custom weight profile"
    )
    print(f"✅ Created custom profile: {custom_profile.name}")
    
    # Find by regulatory context
    gdpr_profile = manager.get_profile_by_regulatory_context("GDPR")
    print(f"✅ GDPR profile: {gdpr_profile.name if gdpr_profile else 'None'}")


if __name__ == "__main__":
    main()
