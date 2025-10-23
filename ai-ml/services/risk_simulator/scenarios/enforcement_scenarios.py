"""
Enforcement Scenarios Module

This module implements enforcement variation modeling including:
- Strict/lenient enforcement periods
- Enforcement trend analysis
- Targeted enforcement simulation
- Penalty escalation patterns

Integrates with Phase 4.2 penalty calculators.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import numpy as np
from datetime import datetime, timedelta


class EnforcementRegime(Enum):
    """Types of enforcement regimes"""
    LENIENT = "lenient"
    MODERATE = "moderate"
    STRICT = "strict"
    AGGRESSIVE = "aggressive"


class EnforcementFocus(Enum):
    """Areas of enforcement focus"""
    FINANCIAL_SERVICES = "financial_services"
    HEALTHCARE = "healthcare"
    TECHNOLOGY = "technology"
    RETAIL = "retail"
    ALL_SECTORS = "all_sectors"


class EnforcementTrend(Enum):
    """Enforcement trend directions"""
    INCREASING = "increasing"
    STABLE = "stable"
    DECREASING = "decreasing"
    VOLATILE = "volatile"


@dataclass
class EnforcementPeriod:
    """Container for enforcement period characteristics"""
    period_id: str
    regime: str
    start_date: str
    end_date: str
    detection_probability: float
    penalty_multiplier: float
    investigation_intensity: float
    focus_areas: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'period_id': self.period_id,
            'regime': self.regime,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'detection_probability': float(self.detection_probability),
            'penalty_multiplier': float(self.penalty_multiplier),
            'investigation_intensity': float(self.investigation_intensity),
            'focus_areas': self.focus_areas
        }


@dataclass
class EnforcementScenario:
    """Complete enforcement scenario"""
    scenario_id: str
    scenario_name: str
    description: str
    periods: List[EnforcementPeriod]
    overall_trend: str
    average_detection_rate: float
    average_penalty_multiplier: float
    time_horizon_days: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            'scenario_id': self.scenario_id,
            'scenario_name': self.scenario_name,
            'description': self.description,
            'periods': [p.to_dict() for p in self.periods],
            'overall_trend': self.overall_trend,
            'average_detection_rate': float(self.average_detection_rate),
            'average_penalty_multiplier': float(self.average_penalty_multiplier),
            'time_horizon_days': int(self.time_horizon_days)
        }


class EnforcementPatternModel:
    """Model enforcement patterns and variations"""
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize enforcement pattern model"""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
        
        # Regime characteristics
        self.regime_params = {
            EnforcementRegime.LENIENT: {
                'detection_prob': (0.15, 0.30),
                'penalty_mult': (0.5, 0.8),
                'investigation': (0.2, 0.4)
            },
            EnforcementRegime.MODERATE: {
                'detection_prob': (0.35, 0.55),
                'penalty_mult': (0.9, 1.2),
                'investigation': (0.5, 0.7)
            },
            EnforcementRegime.STRICT: {
                'detection_prob': (0.60, 0.80),
                'penalty_mult': (1.5, 2.5),
                'investigation': (0.75, 0.90)
            },
            EnforcementRegime.AGGRESSIVE: {
                'detection_prob': (0.80, 0.95),
                'penalty_mult': (2.5, 4.0),
                'investigation': (0.90, 1.0)
            }
        }
    
    def create_enforcement_period(self,
                                  regime: EnforcementRegime,
                                  start_date: datetime,
                                  duration_days: int,
                                  focus: Optional[EnforcementFocus] = None) -> EnforcementPeriod:
        """
        Create a single enforcement period
        
        Args:
            regime: Enforcement regime type
            start_date: Period start date
            duration_days: Period duration
            focus: Optional enforcement focus area
            
        Returns:
            EnforcementPeriod object
        """
        params = self.regime_params[regime]
        
        # Sample parameters
        detection_prob = self.rng.uniform(*params['detection_prob'])
        penalty_mult = self.rng.uniform(*params['penalty_mult'])
        investigation = self.rng.uniform(*params['investigation'])
        
        # Focus areas
        if focus is None:
            focus_areas = [EnforcementFocus.ALL_SECTORS.value]
        else:
            focus_areas = [focus.value]
        
        end_date = start_date + timedelta(days=duration_days)
        
        period_id = f"ENF-{regime.value.upper()}-{self.rng.randint(1000, 9999)}"
        
        return EnforcementPeriod(
            period_id=period_id,
            regime=regime.value,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            detection_probability=detection_prob,
            penalty_multiplier=penalty_mult,
            investigation_intensity=investigation,
            focus_areas=focus_areas
        )
    
    def create_cyclic_enforcement_scenario(self,
                                          cycle_length_days: int = 365,
                                          num_cycles: int = 2) -> EnforcementScenario:
        """
        Create cyclic enforcement scenario (e.g., election cycles)
        
        Args:
            cycle_length_days: Length of one cycle
            num_cycles: Number of cycles to model
            
        Returns:
            EnforcementScenario object
        """
        periods = []
        start_date = datetime.now()
        
        # Typical cycle: Lenient → Moderate → Strict → Moderate → Lenient
        cycle_pattern = [
            (EnforcementRegime.LENIENT, 0.20),
            (EnforcementRegime.MODERATE, 0.25),
            (EnforcementRegime.STRICT, 0.30),
            (EnforcementRegime.MODERATE, 0.25)
        ]
        
        for cycle in range(num_cycles):
            cycle_start = start_date + timedelta(days=cycle * cycle_length_days)
            
            for regime, fraction in cycle_pattern:
                duration = int(cycle_length_days * fraction)
                period = self.create_enforcement_period(
                    regime=regime,
                    start_date=cycle_start,
                    duration_days=duration
                )
                periods.append(period)
                cycle_start += timedelta(days=duration)
        
        # Calculate averages
        avg_detection = float(np.mean([p.detection_probability for p in periods]))
        avg_penalty = float(np.mean([p.penalty_multiplier for p in periods]))
        
        scenario_id = f"CYCLIC-{self.rng.randint(1000, 9999)}"
        
        return EnforcementScenario(
            scenario_id=scenario_id,
            scenario_name="Cyclic Enforcement Pattern",
            description=f"Cyclic enforcement pattern over {num_cycles} cycles",
            periods=periods,
            overall_trend=EnforcementTrend.VOLATILE.value,
            average_detection_rate=avg_detection,
            average_penalty_multiplier=avg_penalty,
            time_horizon_days=cycle_length_days * num_cycles
        )
    
    def create_escalating_enforcement_scenario(self,
                                              time_horizon_years: int = 2,
                                              escalation_rate: float = 0.3) -> EnforcementScenario:
        """
        Create escalating enforcement scenario
        
        Args:
            time_horizon_years: Years to model
            escalation_rate: Rate of escalation per period
            
        Returns:
            EnforcementScenario object
        """
        periods = []
        start_date = datetime.now()
        num_periods = time_horizon_years * 2  # Semi-annual periods
        period_duration = 180  # days
        
        regimes = [
            EnforcementRegime.LENIENT,
            EnforcementRegime.MODERATE,
            EnforcementRegime.MODERATE,
            EnforcementRegime.STRICT,
            EnforcementRegime.STRICT,
            EnforcementRegime.AGGRESSIVE
        ]
        
        for i in range(min(num_periods, len(regimes))):
            period_start = start_date + timedelta(days=i * period_duration)
            period = self.create_enforcement_period(
                regime=regimes[i],
                start_date=period_start,
                duration_days=period_duration
            )
            # Apply escalation to penalty multiplier
            period.penalty_multiplier *= (1 + escalation_rate * i)
            periods.append(period)
        
        avg_detection = float(np.mean([p.detection_probability for p in periods]))
        avg_penalty = float(np.mean([p.penalty_multiplier for p in periods]))
        
        scenario_id = f"ESCALATE-{self.rng.randint(1000, 9999)}"
        
        return EnforcementScenario(
            scenario_id=scenario_id,
            scenario_name="Escalating Enforcement",
            description="Steadily increasing enforcement intensity",
            periods=periods,
            overall_trend=EnforcementTrend.INCREASING.value,
            average_detection_rate=avg_detection,
            average_penalty_multiplier=avg_penalty,
            time_horizon_days=time_horizon_years * 365
        )
    
    def create_targeted_enforcement_scenario(self,
                                            target_sector: EnforcementFocus,
                                            duration_months: int = 12) -> EnforcementScenario:
        """
        Create targeted enforcement scenario for specific sector
        
        Args:
            target_sector: Sector under scrutiny
            duration_months: Duration of targeted enforcement
            
        Returns:
            EnforcementScenario object
        """
        periods = []
        start_date = datetime.now()
        
        # Pre-targeting period (moderate)
        pre_period = self.create_enforcement_period(
            regime=EnforcementRegime.MODERATE,
            start_date=start_date,
            duration_days=30
        )
        periods.append(pre_period)
        
        # Targeting period (aggressive for target sector)
        target_start = start_date + timedelta(days=30)
        target_period = self.create_enforcement_period(
            regime=EnforcementRegime.AGGRESSIVE,
            start_date=target_start,
            duration_days=duration_months * 30,
            focus=target_sector
        )
        # Higher detection for targeted sector
        target_period.detection_probability = min(0.95, target_period.detection_probability * 1.3)
        periods.append(target_period)
        
        # Post-targeting period (strict)
        post_start = target_start + timedelta(days=duration_months * 30)
        post_period = self.create_enforcement_period(
            regime=EnforcementRegime.STRICT,
            start_date=post_start,
            duration_days=60
        )
        periods.append(post_period)
        
        avg_detection = float(np.mean([p.detection_probability for p in periods]))
        avg_penalty = float(np.mean([p.penalty_multiplier for p in periods]))
        
        scenario_id = f"TARGET-{target_sector.value.upper()}-{self.rng.randint(1000, 9999)}"
        
        return EnforcementScenario(
            scenario_id=scenario_id,
            scenario_name=f"Targeted Enforcement: {target_sector.value}",
            description=f"Intensive enforcement targeting {target_sector.value} sector",
            periods=periods,
            overall_trend=EnforcementTrend.INCREASING.value,
            average_detection_rate=avg_detection,
            average_penalty_multiplier=avg_penalty,
            time_horizon_days=30 + (duration_months * 30) + 60
        )


class PenaltyEscalationSimulator:
    """Simulate penalty escalation for repeat offenders"""
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize penalty escalation simulator"""
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
    
    def calculate_escalated_penalty(self,
                                    base_penalty: float,
                                    num_prior_violations: int,
                                    escalation_policy: str = "linear") -> Dict[str, Any]:
        """
        Calculate escalated penalty based on violation history
        
        Args:
            base_penalty: Base penalty amount
            num_prior_violations: Number of prior violations
            escalation_policy: Escalation policy (linear, exponential, tiered)
            
        Returns:
            Dictionary with penalty details
        """
        if escalation_policy == "linear":
            # Linear escalation: +20% per violation
            escalation_factor = 1 + (num_prior_violations * 0.20)
        elif escalation_policy == "exponential":
            # Exponential escalation: 1.5^n
            escalation_factor = 1.5 ** num_prior_violations
        elif escalation_policy == "tiered":
            # Tiered escalation
            if num_prior_violations == 0:
                escalation_factor = 1.0
            elif num_prior_violations <= 2:
                escalation_factor = 1.5
            elif num_prior_violations <= 5:
                escalation_factor = 2.5
            else:
                escalation_factor = 4.0
        else:
            escalation_factor = 1.0
        
        escalated_penalty = base_penalty * escalation_factor
        
        return {
            'base_penalty': float(base_penalty),
            'num_prior_violations': int(num_prior_violations),
            'escalation_policy': escalation_policy,
            'escalation_factor': float(escalation_factor),
            'escalated_penalty': float(escalated_penalty),
            'penalty_increase': float(escalated_penalty - base_penalty),
            'penalty_increase_pct': float((escalation_factor - 1) * 100)
        }
    
    def simulate_repeat_offender_trajectory(self,
                                           base_penalty: float,
                                           max_violations: int = 5,
                                           escalation_policy: str = "exponential") -> Dict[str, Any]:
        """
        Simulate penalty trajectory for repeat offender
        
        Args:
            base_penalty: Initial penalty amount
            max_violations: Maximum violations to simulate
            escalation_policy: Escalation policy
            
        Returns:
            Dictionary with trajectory data
        """
        trajectory = []
        cumulative_penalty = 0.0
        
        for i in range(max_violations + 1):
            penalty_result = self.calculate_escalated_penalty(
                base_penalty=base_penalty,
                num_prior_violations=i,
                escalation_policy=escalation_policy
            )
            cumulative_penalty += penalty_result['escalated_penalty']
            
            trajectory.append({
                'violation_number': i + 1,
                'penalty': penalty_result['escalated_penalty'],
                'cumulative_penalty': float(cumulative_penalty)
            })
        
        return {
            'base_penalty': float(base_penalty),
            'escalation_policy': escalation_policy,
            'max_violations': max_violations,
            'trajectory': trajectory,
            'final_cumulative_penalty': float(cumulative_penalty),
            'average_penalty': float(cumulative_penalty / (max_violations + 1))
        }
