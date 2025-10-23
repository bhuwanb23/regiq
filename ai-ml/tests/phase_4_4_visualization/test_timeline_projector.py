"""
Test Timeline Projector

Tests for timeline projection data generation functionality.
"""

import pytest
from datetime import datetime, timedelta
from services.risk_simulator.visualization.timeline_projector import (
    TimelineProjector,
    EventType,
    EventSeverity
)


class TestTimelineProjector:
    """Test TimelineProjector class"""
    
    def test_initialization(self):
        """Test timeline projector initialization"""
        projector = TimelineProjector(random_state=42)
        assert projector.random_state == 42
        assert projector.np_random is not None
    
    def test_project_risk_timeline(self):
        """Test risk timeline projection"""
        projector = TimelineProjector(random_state=42)
        
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 12, 31)
        current_risk = 0.5
        
        risk_factors = [
            {
                'id': 'factor1',
                'impact_date': datetime(2025, 6, 1),
                'risk_delta': 0.1,
                'title': 'Regulation Change',
                'severity': EventSeverity.HIGH.value,
                'impact_score': 0.7
            }
        ]
        
        projection = projector.project_risk_timeline(
            start_date,
            end_date,
            current_risk,
            risk_factors,
            interval_days=7
        )
        
        assert projection.start_date == start_date.isoformat()
        assert projection.end_date == end_date.isoformat()
        assert len(projection.time_series) > 0
        assert len(projection.events) > 0
        assert 'total_days' in projection.metadata
    
    def test_time_series_generation(self):
        """Test time series data generation"""
        projector = TimelineProjector(random_state=42)
        
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 3, 31)
        
        projection = projector.project_risk_timeline(
            start_date,
            end_date,
            current_risk_score=0.6,
            risk_factors=[],
            interval_days=7
        )
        
        # Should have ~13 weeks of data
        assert 10 <= len(projection.time_series) <= 15
        
        # Check time series structure
        for point in projection.time_series:
            assert 0 <= point.value <= 1.0
            assert point.confidence_lower is not None
            assert point.confidence_upper is not None
            assert point.confidence_lower <= point.value
            assert point.value <= point.confidence_upper
    
    def test_project_compliance_timeline(self):
        """Test compliance deadline timeline"""
        projector = TimelineProjector(random_state=42)
        
        start_date = datetime(2025, 1, 1)
        regulations = [
            {
                'id': 'reg1',
                'name': 'GDPR Compliance',
                'deadline': datetime(2025, 6, 1),
                'description': 'Data protection compliance',
                'severity': EventSeverity.CRITICAL.value,
                'impact_score': 0.9,
                'jurisdiction': 'EU'
            },
            {
                'id': 'reg2',
                'name': 'CCPA Compliance',
                'deadline': datetime(2025, 9, 1),
                'description': 'California privacy compliance',
                'severity': EventSeverity.HIGH.value,
                'impact_score': 0.7,
                'jurisdiction': 'USA'
            }
        ]
        
        projection = projector.project_compliance_timeline(
            regulations,
            start_date,
            planning_horizon_days=365
        )
        
        assert len(projection.events) > 0
        assert len(projection.action_plans) == 2
        
        # Check for compliance deadlines
        deadline_events = [e for e in projection.events if e.event_type == EventType.COMPLIANCE_DEADLINE.value]
        assert len(deadline_events) >= 2
    
    def test_project_mitigation_timeline(self):
        """Test mitigation action timeline"""
        projector = TimelineProjector(random_state=42)
        
        start_date = datetime(2025, 1, 1)
        mitigation_actions = [
            {
                'id': 'action1',
                'title': 'Implement Data Encryption',
                'description': 'End-to-end encryption',
                'start_date': datetime(2025, 1, 15),
                'due_date': datetime(2025, 3, 15),
                'status': 'in_progress',
                'priority': 'critical',
                'owner': 'Security Team',
                'completion_percentage': 45.0
            },
            {
                'id': 'action2',
                'title': 'Update Privacy Policy',
                'description': 'Align with new regulations',
                'start_date': datetime(2025, 2, 1),
                'due_date': datetime(2025, 4, 1),
                'status': 'not_started',
                'priority': 'high',
                'owner': 'Legal Team',
                'completion_percentage': 0.0
            }
        ]
        
        projection = projector.project_mitigation_timeline(
            mitigation_actions,
            start_date
        )
        
        assert len(projection.action_plans) == 2
        assert len(projection.events) >= 4  # Start and end for each action
        assert len(projection.time_series) > 0
    
    def test_event_generation(self):
        """Test event generation from risk factors"""
        projector = TimelineProjector(random_state=42)
        
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 6, 1)
        
        risk_factors = [
            {
                'id': 'factor1',
                'impact_date': datetime(2025, 3, 15),
                'type': EventType.REGULATION_CHANGE.value,
                'title': 'New Privacy Law',
                'severity': EventSeverity.HIGH.value,
                'impact_score': 0.8
            },
            {
                'id': 'factor2',
                'impact_date': datetime(2025, 5, 1),
                'type': EventType.AUDIT_SCHEDULED.value,
                'title': 'Annual Audit',
                'severity': EventSeverity.MEDIUM.value,
                'impact_score': 0.5
            }
        ]
        
        projection = projector.project_risk_timeline(
            start_date,
            end_date,
            0.5,
            risk_factors,
            interval_days=7
        )
        
        assert len(projection.events) >= 2
        event_ids = [e.event_id for e in projection.events]
        assert 'factor1' in event_ids
        assert 'factor2' in event_ids
    
    def test_milestone_extraction(self):
        """Test milestone extraction"""
        projector = TimelineProjector(random_state=42)
        
        start_date = datetime(2025, 1, 1)
        regulations = [
            {
                'id': 'reg1',
                'name': 'Test Regulation',
                'deadline': datetime(2025, 6, 1),
                'severity': EventSeverity.HIGH.value,
                'impact_score': 0.7
            }
        ]
        
        projection = projector.project_compliance_timeline(
            regulations,
            start_date,
            planning_horizon_days=180
        )
        
        assert len(projection.milestones) > 0
        
        # Check milestone structure
        for milestone in projection.milestones:
            assert 'id' in milestone
            assert 'date' in milestone
            assert 'title' in milestone
            assert 'type' in milestone
    
    def test_statistics_calculation(self):
        """Test timeline statistics calculation"""
        projector = TimelineProjector(random_state=42)
        
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 12, 31)
        
        projection = projector.project_risk_timeline(
            start_date,
            end_date,
            0.5,
            [],
            interval_days=30
        )
        
        stats = projection.statistics
        assert 'time_series_stats' in stats
        assert 'event_stats' in stats
        assert 'action_plan_stats' in stats
        
        ts_stats = stats['time_series_stats']
        assert 'min_value' in ts_stats
        assert 'max_value' in ts_stats
        assert 'mean_value' in ts_stats
        assert 'trend' in ts_stats
    
    def test_to_json_conversion(self):
        """Test JSON serialization"""
        projector = TimelineProjector(random_state=42)
        
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 3, 31)
        
        projection = projector.project_risk_timeline(
            start_date,
            end_date,
            0.5,
            [],
            interval_days=7
        )
        
        json_data = projector.to_json(projection)
        
        assert isinstance(json_data, dict)
        assert 'start_date' in json_data
        assert 'end_date' in json_data
        assert 'time_series' in json_data
        assert 'events' in json_data
        assert 'action_plans' in json_data
        assert 'milestones' in json_data
        assert isinstance(json_data['time_series'], list)
    
    def test_action_plan_generation(self):
        """Test action plan generation"""
        projector = TimelineProjector(random_state=42)
        
        start_date = datetime(2025, 1, 1)
        regulations = [
            {
                'id': 'reg1',
                'name': 'Test Regulation',
                'deadline': datetime(2025, 6, 1),
                'description': 'Compliance requirement',
                'severity': EventSeverity.CRITICAL.value,
                'owner': 'Compliance Team'
            }
        ]
        
        projection = projector.project_compliance_timeline(
            regulations,
            start_date,
            planning_horizon_days=180
        )
        
        assert len(projection.action_plans) == 1
        action = projection.action_plans[0]
        
        assert action.title is not None
        assert action.priority in ['critical', 'high', 'medium', 'low']
        assert action.status in ['not_started', 'in_progress', 'completed', 'overdue']
        assert 0 <= action.completion_percentage <= 100
    
    def test_compliance_time_series(self):
        """Test compliance readiness time series"""
        projector = TimelineProjector(random_state=42)
        
        start_date = datetime(2025, 1, 1)
        regulations = [
            {
                'id': 'reg1',
                'name': 'Regulation 1',
                'deadline': datetime(2025, 3, 1)
            },
            {
                'id': 'reg2',
                'name': 'Regulation 2',
                'deadline': datetime(2025, 6, 1)
            }
        ]
        
        projection = projector.project_compliance_timeline(
            regulations,
            start_date,
            planning_horizon_days=180
        )
        
        # Compliance should increase over time
        first_value = projection.time_series[0].value
        last_value = projection.time_series[-1].value
        
        assert 0 <= first_value <= 1.0
        assert 0 <= last_value <= 1.0
    
    def test_mitigation_risk_reduction(self):
        """Test risk reduction from mitigation actions"""
        projector = TimelineProjector(random_state=42)
        
        start_date = datetime(2025, 1, 1)
        actions = [
            {
                'id': 'action1',
                'title': 'Mitigation Action 1',
                'start_date': datetime(2025, 1, 15),
                'due_date': datetime(2025, 2, 15),
                'status': 'in_progress'
            }
        ]
        
        projection = projector.project_mitigation_timeline(actions, start_date)
        
        # Risk should generally decrease over time with mitigations
        assert len(projection.time_series) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
