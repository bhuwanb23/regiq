"""
Test Heatmap Generator

Tests for risk heatmap data generation functionality.
"""

import pytest
from services.risk_simulator.visualization.heatmap_generator import (
    HeatmapGenerator,
    RiskDimension,
    AggregationMethod
)


class TestHeatmapGenerator:
    """Test HeatmapGenerator class"""
    
    def test_initialization(self):
        """Test heatmap generator initialization"""
        generator = HeatmapGenerator(random_state=42)
        assert generator.random_state == 42
        assert generator.np_random is not None
    
    def test_generate_probability_impact_heatmap(self):
        """Test probability vs impact heatmap generation"""
        generator = HeatmapGenerator(random_state=42)
        
        # Sample risk data
        risk_data = [
            {'id': 'risk1', 'probability': 0.8, 'impact': 0.9, 'risk_score': 0.72},
            {'id': 'risk2', 'probability': 0.3, 'impact': 0.4, 'risk_score': 0.12},
            {'id': 'risk3', 'probability': 0.6, 'impact': 0.7, 'risk_score': 0.42},
            {'id': 'risk4', 'probability': 0.9, 'impact': 0.95, 'risk_score': 0.855}
        ]
        
        heatmap = generator.generate_probability_impact_heatmap(
            risk_data,
            aggregation=AggregationMethod.MAX
        )
        
        assert heatmap.dimension_type == RiskDimension.PROBABILITY_IMPACT.value
        assert heatmap.x_axis_label == 'Probability'
        assert heatmap.y_axis_label == 'Impact'
        assert len(heatmap.x_categories) == 5
        assert len(heatmap.y_categories) == 5
        assert len(heatmap.matrix) == 5
        assert len(heatmap.matrix[0]) == 5
        assert len(heatmap.cells) == 25
        assert heatmap.statistics['total_risks'] == 4
    
    def test_generate_probability_impact_heatmap_mean_aggregation(self):
        """Test heatmap with mean aggregation"""
        generator = HeatmapGenerator(random_state=42)
        
        risk_data = [
            {'id': 'risk1', 'probability': 0.8, 'impact': 0.9, 'risk_score': 0.7},
            {'id': 'risk2', 'probability': 0.85, 'impact': 0.92, 'risk_score': 0.8}
        ]
        
        heatmap = generator.generate_probability_impact_heatmap(
            risk_data,
            aggregation=AggregationMethod.MEAN
        )
        
        assert heatmap.statistics['total_risks'] == 2
        assert heatmap.statistics['aggregation_method'] == 'mean'
    
    def test_generate_jurisdiction_regulation_heatmap(self):
        """Test jurisdiction vs regulation heatmap"""
        generator = HeatmapGenerator(random_state=42)
        
        risk_data = [
            {'id': 'r1', 'jurisdiction': 'USA', 'regulation_type': 'GDPR', 'risk_score': 0.6},
            {'id': 'r2', 'jurisdiction': 'EU', 'regulation_type': 'GDPR', 'risk_score': 0.8},
            {'id': 'r3', 'jurisdiction': 'USA', 'regulation_type': 'HIPAA', 'risk_score': 0.5}
        ]
        
        heatmap = generator.generate_jurisdiction_regulation_heatmap(risk_data)
        
        assert heatmap.dimension_type == RiskDimension.JURISDICTION_REGULATION.value
        assert heatmap.x_axis_label == 'Jurisdiction'
        assert heatmap.y_axis_label == 'Regulation Type'
        assert 'USA' in heatmap.x_categories
        assert 'EU' in heatmap.x_categories
        assert 'GDPR' in heatmap.y_categories
        assert heatmap.statistics['total_risks'] == 3
    
    def test_generate_time_risk_type_heatmap(self):
        """Test time vs risk type heatmap"""
        generator = HeatmapGenerator(random_state=42)
        
        time_periods = ['Q1 2025', 'Q2 2025', 'Q3 2025']
        risk_data = [
            {'id': 'r1', 'risk_type': 'Operational', 'time_period': 'Q1 2025', 'risk_score': 0.5},
            {'id': 'r2', 'risk_type': 'Financial', 'time_period': 'Q2 2025', 'risk_score': 0.6},
            {'id': 'r3', 'risk_type': 'Operational', 'time_period': 'Q3 2025', 'risk_score': 0.7}
        ]
        
        heatmap = generator.generate_time_risk_type_heatmap(
            risk_data,
            time_periods=time_periods
        )
        
        assert heatmap.dimension_type == RiskDimension.TIME_RISK_TYPE.value
        assert heatmap.x_axis_label == 'Time Period'
        assert heatmap.y_axis_label == 'Risk Type'
        assert len(heatmap.x_categories) == 3
        assert heatmap.statistics['time_period_count'] == 3
    
    def test_cell_severity_classification(self):
        """Test cell severity classification"""
        generator = HeatmapGenerator(random_state=42)
        
        risk_data = [
            {'id': 'r1', 'probability': 0.9, 'impact': 0.9, 'risk_score': 0.85},
            {'id': 'r2', 'probability': 0.1, 'impact': 0.1, 'risk_score': 0.01}
        ]
        
        heatmap = generator.generate_probability_impact_heatmap(risk_data)
        
        # Find cells with scores
        critical_cells = [c for c in heatmap.cells if c.severity == 'critical']
        low_cells = [c for c in heatmap.cells if c.severity == 'low']
        
        assert len(critical_cells) > 0
        assert len(low_cells) > 0
        assert all(c.risk_score >= 0.75 for c in critical_cells)
        assert all(c.risk_score < 0.25 for c in low_cells if c.risk_score > 0)
    
    def test_drill_down_ids(self):
        """Test drill-down ID storage"""
        generator = HeatmapGenerator(random_state=42)
        
        risk_data = [
            {'id': 'risk1', 'probability': 0.8, 'impact': 0.9, 'risk_score': 0.7},
            {'id': 'risk2', 'probability': 0.85, 'impact': 0.92, 'risk_score': 0.75}
        ]
        
        heatmap = generator.generate_probability_impact_heatmap(risk_data)
        
        # Find cell containing these risks
        cells_with_risks = [c for c in heatmap.cells if len(c.drill_down_ids) > 0]
        assert len(cells_with_risks) > 0
    
    def test_to_json_conversion(self):
        """Test JSON serialization"""
        generator = HeatmapGenerator(random_state=42)
        
        risk_data = [
            {'id': 'r1', 'probability': 0.5, 'impact': 0.6, 'risk_score': 0.3}
        ]
        
        heatmap = generator.generate_probability_impact_heatmap(risk_data)
        json_data = generator.to_json(heatmap)
        
        assert isinstance(json_data, dict)
        assert 'dimension_type' in json_data
        assert 'matrix' in json_data
        assert 'cells' in json_data
        assert 'statistics' in json_data
        assert isinstance(json_data['cells'], list)
        assert len(json_data['cells']) == 25
    
    def test_color_scale(self):
        """Test color scale mapping"""
        generator = HeatmapGenerator(random_state=42)
        
        risk_data = [
            {'id': 'r1', 'probability': 0.8, 'impact': 0.9, 'risk_score': 0.8}
        ]
        
        heatmap = generator.generate_probability_impact_heatmap(risk_data)
        
        assert 'color_scale' in generator.to_json(heatmap)
        assert 'critical' in heatmap.color_scale
        assert heatmap.color_scale['critical'].startswith('#')
    
    def test_empty_risk_data(self):
        """Test heatmap with empty data"""
        generator = HeatmapGenerator(random_state=42)
        
        heatmap = generator.generate_probability_impact_heatmap([])
        
        assert heatmap.statistics['total_risks'] == 0
        assert len(heatmap.cells) == 25
        assert all(cell.count == 0 for cell in heatmap.cells)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
