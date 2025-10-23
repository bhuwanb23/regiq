"""
Risk Heatmap Data Generator

Generates structured data for risk heatmaps including 2D matrices,
drill-down capabilities, and aggregated views. Pure backend data generation
for frontend visualization.

Author: REGIQ AI/ML Team
Phase: 4.4 - Visualization & Reporting
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import numpy as np
from datetime import datetime


class RiskDimension(Enum):
    """Risk heatmap dimension types"""
    PROBABILITY_IMPACT = "probability_impact"
    SEVERITY_LIKELIHOOD = "severity_likelihood"
    JURISDICTION_REGULATION = "jurisdiction_regulation"
    TIME_RISK_TYPE = "time_risk_type"
    DEPARTMENT_COMPLIANCE = "department_compliance"


class AggregationMethod(Enum):
    """Data aggregation methods"""
    MEAN = "mean"
    MAX = "max"
    SUM = "sum"
    COUNT = "count"
    PERCENTILE_95 = "p95"


@dataclass
class HeatmapCell:
    """Individual heatmap cell data"""
    x_value: str
    y_value: str
    risk_score: float
    count: int
    severity: str  # critical, high, medium, low
    color_code: str  # Hex color for visualization
    drill_down_ids: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HeatmapData:
    """Complete heatmap data structure"""
    dimension_type: str
    x_axis_label: str
    y_axis_label: str
    x_categories: List[str]
    y_categories: List[str]
    matrix: List[List[float]]  # 2D matrix of risk scores
    cells: List[HeatmapCell]
    color_scale: Dict[str, str]
    statistics: Dict[str, Any]
    generated_at: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class HeatmapGenerator:
    """Generate risk heatmap data for visualization"""
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize heatmap generator"""
        self.random_state = random_state
        self.np_random = np.random.RandomState(random_state)
        
        # Color scales for different severity levels
        self.color_scales = {
            'red_yellow_green': {
                'critical': '#D32F2F',
                'high': '#F57C00',
                'medium': '#FBC02D',
                'low': '#388E3C'
            },
            'heat': {
                'critical': '#8B0000',
                'high': '#FF4500',
                'medium': '#FFA500',
                'low': '#FFD700'
            },
            'blue_red': {
                'critical': '#B71C1C',
                'high': '#D32F2F',
                'medium': '#1976D2',
                'low': '#0D47A1'
            }
        }
    
    def generate_probability_impact_heatmap(
        self,
        risk_data: List[Dict[str, Any]],
        aggregation: AggregationMethod = AggregationMethod.MAX
    ) -> HeatmapData:
        """
        Generate probability vs impact heatmap
        
        Args:
            risk_data: List of risk items with probability and impact scores
            aggregation: Method to aggregate multiple risks in same cell
            
        Returns:
            Complete heatmap data structure
        """
        # Define categories
        probability_categories = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
        impact_categories = ['Minimal', 'Minor', 'Moderate', 'Major', 'Severe']
        
        # Initialize matrix
        matrix = np.zeros((len(impact_categories), len(probability_categories)))
        cell_counts = np.zeros((len(impact_categories), len(probability_categories)))
        cell_drill_down = [[[] for _ in probability_categories] for _ in impact_categories]
        
        # Populate matrix
        for risk in risk_data:
            prob_idx = self._get_probability_index(risk.get('probability', 0.5))
            impact_idx = self._get_impact_index(risk.get('impact', 0.5))
            risk_score = risk.get('risk_score', risk.get('probability', 0.5) * risk.get('impact', 0.5))
            
            # Apply aggregation
            if aggregation == AggregationMethod.MAX:
                matrix[impact_idx, prob_idx] = max(matrix[impact_idx, prob_idx], risk_score)
            elif aggregation == AggregationMethod.MEAN:
                current_sum = matrix[impact_idx, prob_idx] * cell_counts[impact_idx, prob_idx]
                cell_counts[impact_idx, prob_idx] += 1
                matrix[impact_idx, prob_idx] = (current_sum + risk_score) / cell_counts[impact_idx, prob_idx]
            elif aggregation == AggregationMethod.SUM:
                matrix[impact_idx, prob_idx] += risk_score
                cell_counts[impact_idx, prob_idx] += 1
            
            # Store drill-down ID
            if 'id' in risk:
                cell_drill_down[impact_idx][prob_idx].append(risk['id'])
        
        # Create cells with metadata
        cells = []
        for i, impact_cat in enumerate(impact_categories):
            for j, prob_cat in enumerate(probability_categories):
                risk_score = float(matrix[i, j])
                count = int(cell_counts[i, j]) if aggregation != AggregationMethod.MAX else len(cell_drill_down[i][j])
                
                severity = self._calculate_severity(risk_score)
                color_code = self.color_scales['red_yellow_green'][severity]
                
                cell = HeatmapCell(
                    x_value=prob_cat,
                    y_value=impact_cat,
                    risk_score=risk_score,
                    count=count,
                    severity=severity,
                    color_code=color_code,
                    drill_down_ids=cell_drill_down[i][j],
                    metadata={
                        'probability_range': self._get_probability_range(j),
                        'impact_range': self._get_impact_range(i)
                    }
                )
                cells.append(cell)
        
        # Calculate statistics
        statistics = {
            'total_risks': len(risk_data),
            'max_risk_score': float(np.max(matrix)),
            'mean_risk_score': float(np.mean(matrix[matrix > 0])) if np.any(matrix > 0) else 0.0,
            'critical_count': sum(1 for c in cells if c.severity == 'critical'),
            'high_count': sum(1 for c in cells if c.severity == 'high'),
            'medium_count': sum(1 for c in cells if c.severity == 'medium'),
            'low_count': sum(1 for c in cells if c.severity == 'low'),
            'aggregation_method': aggregation.value
        }
        
        return HeatmapData(
            dimension_type=RiskDimension.PROBABILITY_IMPACT.value,
            x_axis_label='Probability',
            y_axis_label='Impact',
            x_categories=probability_categories,
            y_categories=impact_categories,
            matrix=matrix.tolist(),
            cells=cells,
            color_scale=self.color_scales['red_yellow_green'],
            statistics=statistics,
            generated_at=datetime.utcnow().isoformat(),
            metadata={'description': 'Risk probability vs impact heatmap'}
        )
    
    def generate_jurisdiction_regulation_heatmap(
        self,
        risk_data: List[Dict[str, Any]],
        jurisdictions: Optional[List[str]] = None,
        regulations: Optional[List[str]] = None
    ) -> HeatmapData:
        """
        Generate jurisdiction vs regulation type heatmap
        
        Args:
            risk_data: List of risks with jurisdiction and regulation info
            jurisdictions: List of jurisdictions to include
            regulations: List of regulation types to include
            
        Returns:
            Heatmap data structure
        """
        # Extract unique jurisdictions and regulations
        if jurisdictions is None:
            jurisdictions = sorted(list(set(
                risk.get('jurisdiction', 'Unknown') for risk in risk_data
            )))
        
        if regulations is None:
            regulations = sorted(list(set(
                risk.get('regulation_type', 'Unknown') for risk in risk_data
            )))
        
        # Initialize matrix
        matrix = np.zeros((len(regulations), len(jurisdictions)))
        cell_counts = np.zeros((len(regulations), len(jurisdictions)))
        cell_drill_down = [[[] for _ in jurisdictions] for _ in regulations]
        
        # Populate matrix
        for risk in risk_data:
            jurisdiction = risk.get('jurisdiction', 'Unknown')
            regulation = risk.get('regulation_type', 'Unknown')
            
            if jurisdiction in jurisdictions and regulation in regulations:
                j_idx = jurisdictions.index(jurisdiction)
                r_idx = regulations.index(regulation)
                risk_score = risk.get('risk_score', 0.5)
                
                # Use MAX aggregation
                matrix[r_idx, j_idx] = max(matrix[r_idx, j_idx], risk_score)
                cell_counts[r_idx, j_idx] += 1
                
                if 'id' in risk:
                    cell_drill_down[r_idx][j_idx].append(risk['id'])
        
        # Create cells
        cells = []
        for i, regulation in enumerate(regulations):
            for j, jurisdiction in enumerate(jurisdictions):
                risk_score = float(matrix[i, j])
                count = int(cell_counts[i, j])
                
                severity = self._calculate_severity(risk_score)
                color_code = self.color_scales['red_yellow_green'][severity]
                
                cell = HeatmapCell(
                    x_value=jurisdiction,
                    y_value=regulation,
                    risk_score=risk_score,
                    count=count,
                    severity=severity,
                    color_code=color_code,
                    drill_down_ids=cell_drill_down[i][j],
                    metadata={
                        'regulation_category': self._categorize_regulation(regulation),
                        'jurisdiction_region': self._get_jurisdiction_region(jurisdiction)
                    }
                )
                cells.append(cell)
        
        statistics = {
            'total_risks': len(risk_data),
            'jurisdiction_count': len(jurisdictions),
            'regulation_count': len(regulations),
            'max_risk_score': float(np.max(matrix)),
            'mean_risk_score': float(np.mean(matrix[matrix > 0])) if np.any(matrix > 0) else 0.0,
            'active_cells': int(np.sum(matrix > 0))
        }
        
        return HeatmapData(
            dimension_type=RiskDimension.JURISDICTION_REGULATION.value,
            x_axis_label='Jurisdiction',
            y_axis_label='Regulation Type',
            x_categories=jurisdictions,
            y_categories=regulations,
            matrix=matrix.tolist(),
            cells=cells,
            color_scale=self.color_scales['red_yellow_green'],
            statistics=statistics,
            generated_at=datetime.utcnow().isoformat(),
            metadata={'description': 'Jurisdiction vs regulation type heatmap'}
        )
    
    def generate_time_risk_type_heatmap(
        self,
        risk_data: List[Dict[str, Any]],
        time_periods: List[str],
        risk_types: Optional[List[str]] = None
    ) -> HeatmapData:
        """
        Generate time period vs risk type heatmap
        
        Args:
            risk_data: List of risks with time and type information
            time_periods: List of time period labels (e.g., ['Q1 2025', 'Q2 2025'])
            risk_types: List of risk types to include
            
        Returns:
            Heatmap data structure
        """
        if risk_types is None:
            risk_types = sorted(list(set(
                risk.get('risk_type', 'Unknown') for risk in risk_data
            )))
        
        # Initialize matrix
        matrix = np.zeros((len(risk_types), len(time_periods)))
        cell_counts = np.zeros((len(risk_types), len(time_periods)))
        cell_drill_down = [[[] for _ in time_periods] for _ in risk_types]
        
        # Populate matrix
        for risk in risk_data:
            risk_type = risk.get('risk_type', 'Unknown')
            time_period = risk.get('time_period', time_periods[0] if time_periods else 'Unknown')
            
            if risk_type in risk_types and time_period in time_periods:
                t_idx = time_periods.index(time_period)
                r_idx = risk_types.index(risk_type)
                risk_score = risk.get('risk_score', 0.5)
                
                matrix[r_idx, t_idx] += risk_score  # SUM aggregation for trends
                cell_counts[r_idx, t_idx] += 1
                
                if 'id' in risk:
                    cell_drill_down[r_idx][t_idx].append(risk['id'])
        
        # Create cells
        cells = []
        for i, risk_type in enumerate(risk_types):
            for j, time_period in enumerate(time_periods):
                risk_score = float(matrix[i, j])
                count = int(cell_counts[i, j])
                
                severity = self._calculate_severity(risk_score / max(count, 1))
                color_code = self.color_scales['heat'][severity]
                
                cell = HeatmapCell(
                    x_value=time_period,
                    y_value=risk_type,
                    risk_score=risk_score,
                    count=count,
                    severity=severity,
                    color_code=color_code,
                    drill_down_ids=cell_drill_down[i][j],
                    metadata={
                        'average_risk': risk_score / max(count, 1),
                        'trend_direction': 'increasing' if j > 0 and matrix[i, j] > matrix[i, j-1] else 'stable'
                    }
                )
                cells.append(cell)
        
        statistics = {
            'total_risks': len(risk_data),
            'time_period_count': len(time_periods),
            'risk_type_count': len(risk_types),
            'max_cumulative_risk': float(np.max(matrix)),
            'mean_cumulative_risk': float(np.mean(matrix[matrix > 0])) if np.any(matrix > 0) else 0.0
        }
        
        return HeatmapData(
            dimension_type=RiskDimension.TIME_RISK_TYPE.value,
            x_axis_label='Time Period',
            y_axis_label='Risk Type',
            x_categories=time_periods,
            y_categories=risk_types,
            matrix=matrix.tolist(),
            cells=cells,
            color_scale=self.color_scales['heat'],
            statistics=statistics,
            generated_at=datetime.utcnow().isoformat(),
            metadata={'description': 'Risk evolution over time by type'}
        )
    
    def to_json(self, heatmap_data: HeatmapData) -> Dict[str, Any]:
        """
        Convert heatmap data to JSON-serializable format
        
        Args:
            heatmap_data: HeatmapData object
            
        Returns:
            JSON-serializable dictionary
        """
        return {
            'dimension_type': heatmap_data.dimension_type,
            'x_axis_label': heatmap_data.x_axis_label,
            'y_axis_label': heatmap_data.y_axis_label,
            'x_categories': heatmap_data.x_categories,
            'y_categories': heatmap_data.y_categories,
            'matrix': heatmap_data.matrix,
            'cells': [
                {
                    'x_value': cell.x_value,
                    'y_value': cell.y_value,
                    'risk_score': cell.risk_score,
                    'count': cell.count,
                    'severity': cell.severity,
                    'color_code': cell.color_code,
                    'drill_down_ids': cell.drill_down_ids,
                    'metadata': cell.metadata
                }
                for cell in heatmap_data.cells
            ],
            'color_scale': heatmap_data.color_scale,
            'statistics': heatmap_data.statistics,
            'generated_at': heatmap_data.generated_at,
            'metadata': heatmap_data.metadata
        }
    
    # Helper methods
    
    def _get_probability_index(self, probability: float) -> int:
        """Map probability [0,1] to category index"""
        if probability < 0.2:
            return 0  # Very Low
        elif probability < 0.4:
            return 1  # Low
        elif probability < 0.6:
            return 2  # Medium
        elif probability < 0.8:
            return 3  # High
        else:
            return 4  # Very High
    
    def _get_impact_index(self, impact: float) -> int:
        """Map impact [0,1] to category index"""
        if impact < 0.2:
            return 0  # Minimal
        elif impact < 0.4:
            return 1  # Minor
        elif impact < 0.6:
            return 2  # Moderate
        elif impact < 0.8:
            return 3  # Major
        else:
            return 4  # Severe
    
    def _calculate_severity(self, risk_score: float) -> str:
        """Calculate severity level from risk score"""
        if risk_score >= 0.75:
            return 'critical'
        elif risk_score >= 0.5:
            return 'high'
        elif risk_score >= 0.25:
            return 'medium'
        else:
            return 'low'
    
    def _get_probability_range(self, index: int) -> Tuple[float, float]:
        """Get probability range for category index"""
        ranges = [
            (0.0, 0.2),
            (0.2, 0.4),
            (0.4, 0.6),
            (0.6, 0.8),
            (0.8, 1.0)
        ]
        return ranges[index]
    
    def _get_impact_range(self, index: int) -> Tuple[float, float]:
        """Get impact range for category index"""
        ranges = [
            (0.0, 0.2),
            (0.2, 0.4),
            (0.4, 0.6),
            (0.6, 0.8),
            (0.8, 1.0)
        ]
        return ranges[index]
    
    def _categorize_regulation(self, regulation: str) -> str:
        """Categorize regulation type"""
        regulation_lower = regulation.lower()
        if any(kw in regulation_lower for kw in ['privacy', 'gdpr', 'ccpa', 'data protection']):
            return 'Privacy & Data Protection'
        elif any(kw in regulation_lower for kw in ['financial', 'banking', 'securities', 'dodd-frank']):
            return 'Financial'
        elif any(kw in regulation_lower for kw in ['health', 'hipaa', 'medical']):
            return 'Healthcare'
        elif any(kw in regulation_lower for kw in ['environmental', 'epa', 'emissions']):
            return 'Environmental'
        else:
            return 'Other'
    
    def _get_jurisdiction_region(self, jurisdiction: str) -> str:
        """Get region for jurisdiction"""
        eu_countries = ['EU', 'Germany', 'France', 'UK', 'Italy', 'Spain']
        asia_countries = ['China', 'Japan', 'Singapore', 'South Korea', 'India']
        
        if jurisdiction in eu_countries or 'EU' in jurisdiction:
            return 'Europe'
        elif jurisdiction in ['USA', 'Canada', 'Mexico']:
            return 'North America'
        elif jurisdiction in asia_countries:
            return 'Asia-Pacific'
        else:
            return 'Other'
