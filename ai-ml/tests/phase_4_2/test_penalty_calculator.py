"""
Tests for Penalty Calculator Models

Test coverage:
- BasePenaltyCalculator (3 tests)
- TieredPenaltyCalculator (5 tests)
- ProportionalPenaltyCalculator (4 tests)
- DailyPenaltyCalculator (4 tests)
- PenaltyAggregator (4 tests)

Total: 20 tests
"""

import pytest
import numpy as np
from services.risk_simulator.models.penalty_calculator import (
    BasePenaltyCalculator,
    TieredPenaltyCalculator,
    ProportionalPenaltyCalculator,
    DailyPenaltyCalculator,
    PenaltyAggregator,
    PenaltyTier,
    PenaltyType,
    PenaltyResult
)


# ============================================================================
# BasePenaltyCalculator Tests
# ============================================================================

class TestBasePenaltyCalculator:
    """Test suite for BasePenaltyCalculator"""
    
    def test_initialization(self):
        """Test base calculator initialization"""
        calculator = BasePenaltyCalculator(jurisdiction="federal", random_state=42)
        
        assert calculator.jurisdiction == "federal"
        assert calculator.random_state == 42
        assert calculator.rng is not None
    
    def test_apply_adjustments_aggravating_only(self):
        """Test applying only aggravating factors"""
        calculator = BasePenaltyCalculator()
        
        base_penalty = 100000
        aggravating_factors = {
            'repeat_violation': 2.0,
            'willful_negligence': 1.5
        }
        
        adjusted, agg_list, mit_list = calculator.apply_adjustments(
            base_penalty,
            aggravating_factors=aggravating_factors
        )
        
        # Should multiply: 100000 * 2.0 * 1.5 = 300000
        assert adjusted == 300000
        assert len(agg_list) == 2
        assert len(mit_list) == 0
        assert 'repeat_violation' in agg_list
        assert 'willful_negligence' in agg_list
    
    def test_apply_adjustments_mitigating_only(self):
        """Test applying only mitigating factors"""
        calculator = BasePenaltyCalculator()
        
        base_penalty = 100000
        mitigating_factors = {
            'cooperation': 0.8,  # 20% reduction
            'remediation': 0.9   # 10% reduction
        }
        
        adjusted, agg_list, mit_list = calculator.apply_adjustments(
            base_penalty,
            mitigating_factors=mitigating_factors
        )
        
        # Should multiply: 100000 * 0.8 * 0.9 = 72000
        assert adjusted == 72000
        assert len(agg_list) == 0
        assert len(mit_list) == 2
        assert 'cooperation' in mit_list
        assert 'remediation' in mit_list
    
    def test_apply_adjustments_both(self):
        """Test applying both aggravating and mitigating factors"""
        calculator = BasePenaltyCalculator()
        
        base_penalty = 100000
        aggravating_factors = {'repeat_violation': 2.0}
        mitigating_factors = {'cooperation': 0.75}
        
        adjusted, agg_list, mit_list = calculator.apply_adjustments(
            base_penalty,
            aggravating_factors=aggravating_factors,
            mitigating_factors=mitigating_factors
        )
        
        # Should multiply: 100000 * 2.0 * 0.75 = 150000
        assert adjusted == 150000
        assert len(agg_list) == 1
        assert len(mit_list) == 1
    
    def test_calculate_uncertainty_range(self):
        """Test uncertainty range calculation"""
        calculator = BasePenaltyCalculator()
        
        penalty = 100000
        lower, upper = calculator.calculate_uncertainty_range(penalty, uncertainty_pct=0.20)
        
        assert lower == 80000  # 20% below
        assert upper == 120000  # 20% above
        
        # Test custom uncertainty
        lower, upper = calculator.calculate_uncertainty_range(penalty, uncertainty_pct=0.10)
        assert lower == 90000
        assert abs(upper - 110000) < 0.01  # Allow for floating point precision


# ============================================================================
# TieredPenaltyCalculator Tests
# ============================================================================

class TestTieredPenaltyCalculator:
    """Test suite for TieredPenaltyCalculator"""
    
    def test_initialization_default(self):
        """Test initialization with default tiers"""
        calculator = TieredPenaltyCalculator()
        
        assert calculator.tier_structure is not None
        assert len(calculator.tier_structure) == 5
        assert PenaltyTier.TIER_1 in calculator.tier_structure
    
    def test_initialization_custom_tiers(self):
        """Test initialization with custom tier structure"""
        custom_tiers = {
            PenaltyTier.TIER_1: (0.0, 5000.0),
            PenaltyTier.TIER_2: (5000.0, 25000.0),
            PenaltyTier.TIER_3: (25000.0, 100000.0),
            PenaltyTier.TIER_4: (100000.0, 500000.0),
            PenaltyTier.TIER_5: (500000.0, 2000000.0)
        }
        
        calculator = TieredPenaltyCalculator(tier_structure=custom_tiers)
        assert calculator.tier_structure == custom_tiers
    
    def test_determine_tier_tier1(self):
        """Test tier determination for Tier 1 violations"""
        calculator = TieredPenaltyCalculator()
        
        tier = calculator.determine_tier(violation_score=0.2, violation_count=1)
        assert tier == PenaltyTier.TIER_1
    
    def test_determine_tier_tier5(self):
        """Test tier determination for Tier 5 violations"""
        calculator = TieredPenaltyCalculator()
        
        tier = calculator.determine_tier(violation_score=0.95, violation_count=1)
        assert tier == PenaltyTier.TIER_5
    
    def test_determine_tier_multiple_violations(self):
        """Test tier escalation with multiple violations"""
        calculator = TieredPenaltyCalculator()
        
        # Low score but many violations should escalate tier
        tier_single = calculator.determine_tier(violation_score=0.4, violation_count=1)
        tier_multiple = calculator.determine_tier(violation_score=0.4, violation_count=5)
        
        # Multiple violations should increase tier
        assert tier_multiple.value >= tier_single.value
    
    def test_calculate_basic(self):
        """Test basic penalty calculation"""
        calculator = TieredPenaltyCalculator(random_state=42)
        
        result = calculator.calculate(
            violation_score=0.5,
            violation_count=1
        )
        
        assert isinstance(result, PenaltyResult)
        assert result.base_penalty > 0
        assert result.adjusted_penalty == result.base_penalty  # No adjustments
        assert result.penalty_type == PenaltyType.TIERED.value
        assert len(result.penalty_range) == 2
        assert result.penalty_range[0] < result.penalty_range[1]
    
    def test_calculate_with_adjustments(self):
        """Test penalty calculation with aggravating/mitigating factors"""
        calculator = TieredPenaltyCalculator(random_state=42)
        
        result = calculator.calculate(
            violation_score=0.6,
            violation_count=2,
            aggravating_factors={'repeat_violation': 1.5},
            mitigating_factors={'cooperation': 0.9}
        )
        
        # Adjusted should differ from base
        assert result.adjusted_penalty != result.base_penalty
        assert len(result.aggravating_factors) == 1
        assert len(result.mitigating_factors) == 1
        
        # Net effect: 1.5 * 0.9 = 1.35x increase
        expected_ratio = 1.35
        actual_ratio = result.adjusted_penalty / result.base_penalty
        assert abs(actual_ratio - expected_ratio) < 0.01
    
    def test_penalty_breakdown(self):
        """Test penalty breakdown details"""
        calculator = TieredPenaltyCalculator(random_state=42)
        
        result = calculator.calculate(violation_score=0.7, violation_count=1)
        
        breakdown = result.penalty_breakdown
        assert 'tier' in breakdown
        assert 'tier_min' in breakdown
        assert 'tier_max' in breakdown
        assert 'base_penalty' in breakdown
        assert 'adjusted_penalty' in breakdown


# ============================================================================
# ProportionalPenaltyCalculator Tests
# ============================================================================

class TestProportionalPenaltyCalculator:
    """Test suite for ProportionalPenaltyCalculator"""
    
    def test_initialization(self):
        """Test proportional calculator initialization"""
        calculator = ProportionalPenaltyCalculator(
            max_revenue_percentage=0.04,
            min_fixed_amount=10000,
            random_state=42
        )
        
        assert calculator.max_revenue_percentage == 0.04
        assert calculator.min_fixed_amount == 10000
    
    def test_calculate_revenue_based(self):
        """Test revenue-based penalty calculation"""
        calculator = ProportionalPenaltyCalculator(
            max_revenue_percentage=0.04,
            min_fixed_amount=10000,
            random_state=42
        )
        
        result = calculator.calculate(
            annual_revenue=10000000,  # $10M
            violation_severity=0.5
        )
        
        # Expected: 10M * 0.04 * 0.5 = 200,000
        assert result.base_penalty == 200000
        assert result.penalty_type == PenaltyType.PROPORTIONAL.value
        assert 'revenue_penalty' in result.penalty_breakdown
    
    def test_calculate_transaction_based(self):
        """Test transaction-based penalty calculation"""
        calculator = ProportionalPenaltyCalculator(random_state=42)
        
        result = calculator.calculate(
            annual_revenue=1000000,  # $1M
            violation_severity=0.3,
            affected_transactions=10000,
            transaction_value=100
        )
        
        # Transaction penalty: 10000 * 100 * 0.05 = 50,000
        # Revenue penalty: 1M * 0.04 * 0.3 = 12,000
        # Should use higher: 50,000
        assert result.base_penalty == 50000
        assert 'transaction_penalty' in result.penalty_breakdown
    
    def test_minimum_fixed_amount(self):
        """Test minimum fixed amount enforcement"""
        calculator = ProportionalPenaltyCalculator(
            max_revenue_percentage=0.04,
            min_fixed_amount=50000,
            random_state=42
        )
        
        # Low revenue, low severity should hit minimum
        result = calculator.calculate(
            annual_revenue=100000,  # $100K
            violation_severity=0.1
        )
        
        # Revenue penalty: 100K * 0.04 * 0.1 = 400
        # Should be raised to minimum: 50,000
        assert result.base_penalty == 50000
    
    def test_calculate_with_adjustments(self):
        """Test proportional penalty with adjustments"""
        calculator = ProportionalPenaltyCalculator(random_state=42)
        
        result = calculator.calculate(
            annual_revenue=5000000,
            violation_severity=0.6,
            aggravating_factors={'data_breach': 2.0},
            mitigating_factors={'prompt_notification': 0.85}
        )
        
        assert result.adjusted_penalty != result.base_penalty
        assert len(result.aggravating_factors) > 0
        assert len(result.mitigating_factors) > 0


# ============================================================================
# DailyPenaltyCalculator Tests
# ============================================================================

class TestDailyPenaltyCalculator:
    """Test suite for DailyPenaltyCalculator"""
    
    def test_initialization(self):
        """Test daily penalty calculator initialization"""
        calculator = DailyPenaltyCalculator(
            daily_rate=1000,
            max_total_penalty=500000,
            random_state=42
        )
        
        assert calculator.daily_rate == 1000
        assert calculator.max_total_penalty == 500000
    
    def test_calculate_basic(self):
        """Test basic daily penalty calculation"""
        calculator = DailyPenaltyCalculator(daily_rate=1000, random_state=42)
        
        result = calculator.calculate(
            violation_days=30,
            severity_multiplier=1.0
        )
        
        # Expected: 1000 * 30 * 1.0 = 30,000
        assert result.base_penalty == 30000
        assert result.penalty_type == PenaltyType.DAILY.value
        assert 'daily_rate' in result.penalty_breakdown
        assert 'violation_days' in result.penalty_breakdown
    
    def test_calculate_with_severity(self):
        """Test daily penalty with severity multiplier"""
        calculator = DailyPenaltyCalculator(daily_rate=1000, random_state=42)
        
        result = calculator.calculate(
            violation_days=30,
            severity_multiplier=2.5
        )
        
        # Expected: 1000 * 30 * 2.5 = 75,000
        assert result.base_penalty == 75000
    
    def test_calculate_with_cap(self):
        """Test daily penalty with maximum cap"""
        calculator = DailyPenaltyCalculator(
            daily_rate=1000,
            max_total_penalty=50000,
            random_state=42
        )
        
        result = calculator.calculate(
            violation_days=100,  # Would be 100,000 without cap
            severity_multiplier=1.0
        )
        
        # Should be capped at 50,000
        assert result.base_penalty == 50000
        assert result.penalty_breakdown['capped'] is True
    
    def test_calculate_with_adjustments_and_cap(self):
        """Test daily penalty with adjustments respecting cap"""
        calculator = DailyPenaltyCalculator(
            daily_rate=1000,
            max_total_penalty=100000,
            random_state=42
        )
        
        result = calculator.calculate(
            violation_days=50,
            severity_multiplier=1.0,
            aggravating_factors={'willful': 3.0}  # Would push to 150,000
        )
        
        # Should be capped at 100,000 even after adjustments
        assert result.adjusted_penalty == 100000


# ============================================================================
# PenaltyAggregator Tests
# ============================================================================

class TestPenaltyAggregator:
    """Test suite for PenaltyAggregator"""
    
    def test_initialization(self):
        """Test aggregator initialization"""
        aggregator = PenaltyAggregator(random_state=42)
        
        assert aggregator.random_state == 42
        assert len(aggregator.penalties) == 0
    
    def test_add_penalty(self):
        """Test adding penalties to aggregator"""
        aggregator = PenaltyAggregator(random_state=42)
        
        penalty = PenaltyResult(
            base_penalty=100000,
            adjusted_penalty=120000,
            penalty_range=(90000, 150000),
            penalty_breakdown={'test': 100000},
            aggravating_factors=[],
            mitigating_factors=[],
            confidence_level=0.85,
            jurisdiction='federal',
            penalty_type='tiered'
        )
        
        aggregator.add_penalty(penalty)
        assert len(aggregator.penalties) == 1
    
    def test_calculate_total_single_penalty(self):
        """Test total calculation with single penalty"""
        aggregator = PenaltyAggregator(random_state=42)
        
        penalty = PenaltyResult(
            base_penalty=100000,
            adjusted_penalty=100000,
            penalty_range=(80000, 120000),
            penalty_breakdown={'test': 100000},
            aggravating_factors=[],
            mitigating_factors=[],
            confidence_level=0.85,
            jurisdiction='federal',
            penalty_type='tiered'
        )
        
        aggregator.add_penalty(penalty)
        total_stats = aggregator.calculate_total(n_simulations=5000)
        
        assert 'mean_total' in total_stats
        assert 'median_total' in total_stats
        assert 'confidence_interval_95' in total_stats
        assert 'breakdown_by_type' in total_stats
        
        # Mean should be around 100,000 (triangular distribution)
        assert 95000 < total_stats['mean_total'] < 105000
    
    def test_calculate_total_multiple_penalties(self):
        """Test total calculation with multiple penalties"""
        aggregator = PenaltyAggregator(random_state=42)
        
        # Add tiered penalty
        tiered = PenaltyResult(
            base_penalty=100000,
            adjusted_penalty=100000,
            penalty_range=(80000, 120000),
            penalty_breakdown={'test': 100000},
            aggravating_factors=[],
            mitigating_factors=[],
            confidence_level=0.85,
            jurisdiction='federal',
            penalty_type='tiered'
        )
        
        # Add proportional penalty
        proportional = PenaltyResult(
            base_penalty=50000,
            adjusted_penalty=50000,
            penalty_range=(40000, 60000),
            penalty_breakdown={'test': 50000},
            aggravating_factors=[],
            mitigating_factors=[],
            confidence_level=0.75,
            jurisdiction='federal',
            penalty_type='proportional'
        )
        
        aggregator.add_penalty(tiered)
        aggregator.add_penalty(proportional)
        
        total_stats = aggregator.calculate_total(n_simulations=5000)
        
        # Mean should be around 150,000
        assert 145000 < total_stats['mean_total'] < 155000
        assert total_stats['n_components'] == 2
        
        # Check breakdown
        breakdown = total_stats['breakdown_by_type']
        assert 'tiered' in breakdown
        assert 'proportional' in breakdown
        assert breakdown['tiered'] == 100000
        assert breakdown['proportional'] == 50000
    
    def test_calculate_total_without_penalties_raises_error(self):
        """Test that calculating total without penalties raises error"""
        aggregator = PenaltyAggregator(random_state=42)
        
        with pytest.raises(ValueError, match="No penalties added"):
            aggregator.calculate_total()
    
    def test_get_percentile_estimate(self):
        """Test percentile-based estimation"""
        aggregator = PenaltyAggregator(random_state=42)
        
        penalty = PenaltyResult(
            base_penalty=100000,
            adjusted_penalty=100000,
            penalty_range=(80000, 120000),
            penalty_breakdown={'test': 100000},
            aggravating_factors=[],
            mitigating_factors=[],
            confidence_level=0.85,
            jurisdiction='federal',
            penalty_type='tiered'
        )
        
        aggregator.add_penalty(penalty)
        
        # Test different percentiles
        p50 = aggregator.get_percentile_estimate(50)
        p90 = aggregator.get_percentile_estimate(90)
        p95 = aggregator.get_percentile_estimate(95)
        
        # Higher percentiles should give higher estimates
        assert p50 < p90 < p95
    
    def test_export_results(self):
        """Test exporting aggregated results"""
        aggregator = PenaltyAggregator(random_state=42)
        
        penalty = PenaltyResult(
            base_penalty=100000,
            adjusted_penalty=100000,
            penalty_range=(80000, 120000),
            penalty_breakdown={'test': 100000},
            aggravating_factors=[],
            mitigating_factors=[],
            confidence_level=0.85,
            jurisdiction='federal',
            penalty_type='tiered'
        )
        
        aggregator.add_penalty(penalty)
        exported = aggregator.export_results()
        
        assert 'penalties' in exported
        assert 'summary' in exported
        assert len(exported['penalties']) == 1
        
        # Test JSON serializability
        import json
        json_str = json.dumps(exported)
        assert json_str is not None


# ============================================================================
# Integration Tests
# ============================================================================

class TestPenaltyCalculatorIntegration:
    """Integration tests for penalty calculations"""
    
    def test_combined_penalty_scenario(self):
        """Test realistic combined penalty scenario"""
        aggregator = PenaltyAggregator(random_state=42)
        
        # Scenario: Multiple violations with different penalty types
        
        # 1. Tiered penalty for compliance violation
        tiered_calc = TieredPenaltyCalculator(random_state=42)
        tiered_result = tiered_calc.calculate(
            violation_score=0.7,
            violation_count=2,
            aggravating_factors={'repeat': 1.5}
        )
        aggregator.add_penalty(tiered_result)
        
        # 2. Proportional penalty for revenue impact
        prop_calc = ProportionalPenaltyCalculator(random_state=42)
        prop_result = prop_calc.calculate(
            annual_revenue=5000000,
            violation_severity=0.6,
            mitigating_factors={'cooperation': 0.85}
        )
        aggregator.add_penalty(prop_result)
        
        # 3. Daily penalty for ongoing violation
        daily_calc = DailyPenaltyCalculator(daily_rate=2000, random_state=42)
        daily_result = daily_calc.calculate(
            violation_days=45,
            severity_multiplier=1.2
        )
        aggregator.add_penalty(daily_result)
        
        # Calculate total
        total_stats = aggregator.calculate_total(n_simulations=5000)
        
        # Verify comprehensive output
        assert total_stats['n_components'] == 3
        assert total_stats['mean_total'] > 0
        assert len(total_stats['breakdown_by_type']) == 3
        
        # Export
        exported = aggregator.export_results()
        assert len(exported['penalties']) == 3
        
        # Verify JSON serializable
        import json
        json.dumps(exported)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
