"""
Timeline Projection Data Generator

Generates structured data for timeline visualizations including risk evolution,
events, milestones, action plans, and compliance deadlines. Pure backend data
generation for frontend visualization.

Author: REGIQ AI/ML Team
Phase: 4.4 - Visualization & Reporting
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from datetime import datetime, timedelta
import numpy as np


class EventType(Enum):
    """Timeline event types"""
    REGULATION_CHANGE = "regulation_change"
    COMPLIANCE_DEADLINE = "compliance_deadline"
    RISK_THRESHOLD_BREACH = "risk_threshold_breach"
    AUDIT_SCHEDULED = "audit_scheduled"
    MITIGATION_ACTION = "mitigation_action"
    MILESTONE = "milestone"
    INCIDENT = "incident"


class EventSeverity(Enum):
    """Event severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class TimelineEvent:
    """Individual timeline event"""
    event_id: str
    event_type: str
    timestamp: str  # ISO format
    title: str
    description: str
    severity: str
    impact_score: float
    related_risks: List[str] = field(default_factory=list)
    action_items: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TimeSeriesPoint:
    """Time series data point"""
    timestamp: str
    value: float
    confidence_lower: Optional[float] = None
    confidence_upper: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ActionPlan:
    """Action plan with timeline"""
    action_id: str
    title: str
    description: str
    start_date: str
    due_date: str
    status: str  # not_started, in_progress, completed, overdue
    priority: str  # critical, high, medium, low
    owner: str
    completion_percentage: float
    dependencies: List[str] = field(default_factory=list)
    milestones: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TimelineProjection:
    """Complete timeline projection data"""
    start_date: str
    end_date: str
    time_series: List[TimeSeriesPoint]
    events: List[TimelineEvent]
    action_plans: List[ActionPlan]
    milestones: List[Dict[str, Any]]
    statistics: Dict[str, Any]
    generated_at: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class TimelineProjector:
    """Generate timeline projection data for visualization"""
    
    def __init__(self, random_state: Optional[int] = None):
        """Initialize timeline projector"""
        self.random_state = random_state
        self.np_random = np.random.RandomState(random_state)
    
    def project_risk_timeline(
        self,
        start_date: datetime,
        end_date: datetime,
        current_risk_score: float,
        risk_factors: List[Dict[str, Any]],
        interval_days: int = 7
    ) -> TimelineProjection:
        """
        Project risk evolution over time
        
        Args:
            start_date: Timeline start date
            end_date: Timeline end date
            current_risk_score: Current baseline risk score
            risk_factors: List of risk factors affecting timeline
            interval_days: Days between data points
            
        Returns:
            Complete timeline projection
        """
        # Generate time series
        time_series = self._generate_risk_time_series(
            start_date, end_date, current_risk_score, risk_factors, interval_days
        )
        
        # Generate events from risk factors
        events = self._generate_events_from_factors(risk_factors, start_date, end_date)
        
        # Generate action plans
        action_plans = self._generate_action_plans(risk_factors, start_date)
        
        # Extract milestones
        milestones = self._extract_milestones(events, action_plans)
        
        # Calculate statistics
        statistics = self._calculate_timeline_statistics(time_series, events, action_plans)
        
        return TimelineProjection(
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            time_series=time_series,
            events=events,
            action_plans=action_plans,
            milestones=milestones,
            statistics=statistics,
            generated_at=datetime.utcnow().isoformat(),
            metadata={
                'interval_days': interval_days,
                'total_days': (end_date - start_date).days,
                'description': 'Risk evolution timeline projection'
            }
        )
    
    def project_compliance_timeline(
        self,
        regulations: List[Dict[str, Any]],
        start_date: datetime,
        planning_horizon_days: int = 365
    ) -> TimelineProjection:
        """
        Project compliance deadlines and requirements
        
        Args:
            regulations: List of regulations with deadlines
            start_date: Timeline start date
            planning_horizon_days: Number of days to project
            
        Returns:
            Compliance timeline projection
        """
        end_date = start_date + timedelta(days=planning_horizon_days)
        
        # Generate compliance events
        events = []
        for reg in regulations:
            if 'deadline' in reg:
                deadline = self._parse_deadline(reg['deadline'], start_date)
                
                # Add compliance deadline event
                events.append(TimelineEvent(
                    event_id=f"compliance_{reg.get('id', len(events))}",
                    event_type=EventType.COMPLIANCE_DEADLINE.value,
                    timestamp=deadline.isoformat(),
                    title=f"Compliance Deadline: {reg.get('name', 'Unknown')}",
                    description=reg.get('description', ''),
                    severity=reg.get('severity', EventSeverity.HIGH.value),
                    impact_score=reg.get('impact_score', 0.7),
                    related_risks=[reg.get('id', '')],
                    action_items=reg.get('requirements', []),
                    metadata={
                        'jurisdiction': reg.get('jurisdiction', 'Unknown'),
                        'regulation_type': reg.get('type', 'Unknown')
                    }
                ))
                
                # Add preparation milestones (3 months, 1 month, 1 week before)
                for months_before, milestone_name in [(3, 'Preparation Start'), (1, 'Final Review'), (0.25, 'Final Check')]:
                    milestone_date = deadline - timedelta(days=int(months_before * 30))
                    if start_date <= milestone_date <= end_date:
                        events.append(TimelineEvent(
                            event_id=f"milestone_{reg.get('id', len(events))}_{int(months_before*30)}",
                            event_type=EventType.MILESTONE.value,
                            timestamp=milestone_date.isoformat(),
                            title=f"{milestone_name}: {reg.get('name', 'Unknown')}",
                            description=f"Milestone {int((1 - months_before/3) * 100)}% to compliance",
                            severity=EventSeverity.MEDIUM.value,
                            impact_score=0.3,
                            related_risks=[reg.get('id', '')],
                            metadata={'parent_deadline': deadline.isoformat()}
                        ))
        
        # Sort events by timestamp
        events.sort(key=lambda e: e.timestamp)
        
        # Generate compliance tracking time series
        time_series = self._generate_compliance_time_series(
            start_date, end_date, regulations, events
        )
        
        # Generate action plans for compliance
        action_plans = []
        for reg in regulations:
            if 'deadline' in reg:
                deadline = self._parse_deadline(reg['deadline'], start_date)
                prep_start = deadline - timedelta(days=90)
                
                action_plans.append(ActionPlan(
                    action_id=f"action_{reg.get('id', len(action_plans))}",
                    title=f"Achieve Compliance: {reg.get('name', 'Unknown')}",
                    description=reg.get('description', ''),
                    start_date=max(start_date, prep_start).isoformat(),
                    due_date=deadline.isoformat(),
                    status='in_progress',
                    priority='critical' if reg.get('severity') == 'critical' else 'high',
                    owner=reg.get('owner', 'Compliance Team'),
                    completion_percentage=self._estimate_completion(start_date, prep_start, deadline),
                    dependencies=[],
                    milestones=[
                        {
                            'name': 'Gap Analysis Complete',
                            'date': (prep_start + timedelta(days=15)).isoformat(),
                            'completed': datetime.now() > prep_start + timedelta(days=15)
                        },
                        {
                            'name': 'Remediation Plan Approved',
                            'date': (prep_start + timedelta(days=30)).isoformat(),
                            'completed': datetime.now() > prep_start + timedelta(days=30)
                        },
                        {
                            'name': 'Implementation Complete',
                            'date': (deadline - timedelta(days=14)).isoformat(),
                            'completed': False
                        }
                    ],
                    metadata={'regulation_id': reg.get('id', '')}
                ))
        
        milestones = self._extract_milestones(events, action_plans)
        statistics = self._calculate_timeline_statistics(time_series, events, action_plans)
        
        return TimelineProjection(
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            time_series=time_series,
            events=events,
            action_plans=action_plans,
            milestones=milestones,
            statistics=statistics,
            generated_at=datetime.utcnow().isoformat(),
            metadata={
                'planning_horizon_days': planning_horizon_days,
                'regulation_count': len(regulations),
                'description': 'Compliance deadline timeline'
            }
        )
    
    def project_mitigation_timeline(
        self,
        mitigation_actions: List[Dict[str, Any]],
        start_date: datetime
    ) -> TimelineProjection:
        """
        Project risk mitigation action timeline
        
        Args:
            mitigation_actions: List of mitigation actions
            start_date: Timeline start date
            
        Returns:
            Mitigation timeline projection
        """
        # Determine end date from latest action
        end_date = start_date
        for action in mitigation_actions:
            if 'due_date' in action:
                due = self._parse_deadline(action['due_date'], start_date)
                end_date = max(end_date, due)
        
        end_date = end_date + timedelta(days=30)  # Add buffer
        
        # Convert to action plans
        action_plans = []
        events = []
        
        for action in mitigation_actions:
            action_start = self._parse_deadline(action.get('start_date', start_date), start_date)
            action_due = self._parse_deadline(action.get('due_date', start_date + timedelta(days=30)), start_date)
            
            # Create action plan
            action_plan = ActionPlan(
                action_id=action.get('id', f"action_{len(action_plans)}"),
                title=action.get('title', 'Mitigation Action'),
                description=action.get('description', ''),
                start_date=action_start.isoformat(),
                due_date=action_due.isoformat(),
                status=action.get('status', 'not_started'),
                priority=action.get('priority', 'medium'),
                owner=action.get('owner', 'Risk Team'),
                completion_percentage=action.get('completion_percentage', 0.0),
                dependencies=action.get('dependencies', []),
                milestones=action.get('milestones', []),
                metadata=action.get('metadata', {})
            )
            action_plans.append(action_plan)
            
            # Create start and end events
            events.append(TimelineEvent(
                event_id=f"start_{action.get('id', len(events))}",
                event_type=EventType.MITIGATION_ACTION.value,
                timestamp=action_start.isoformat(),
                title=f"Start: {action.get('title', 'Mitigation Action')}",
                description=f"Begin {action.get('description', '')}",
                severity=EventSeverity.INFO.value,
                impact_score=0.2,
                related_risks=action.get('related_risks', []),
                metadata={'action_id': action.get('id', '')}
            ))
            
            events.append(TimelineEvent(
                event_id=f"due_{action.get('id', len(events))}",
                event_type=EventType.MILESTONE.value,
                timestamp=action_due.isoformat(),
                title=f"Due: {action.get('title', 'Mitigation Action')}",
                description=f"Target completion date",
                severity=EventSeverity.MEDIUM.value,
                impact_score=0.5,
                related_risks=action.get('related_risks', []),
                metadata={'action_id': action.get('id', '')}
            ))
        
        events.sort(key=lambda e: e.timestamp)
        
        # Generate time series showing risk reduction
        time_series = self._generate_mitigation_time_series(
            start_date, end_date, action_plans
        )
        
        milestones = self._extract_milestones(events, action_plans)
        statistics = self._calculate_timeline_statistics(time_series, events, action_plans)
        
        return TimelineProjection(
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            time_series=time_series,
            events=events,
            action_plans=action_plans,
            milestones=milestones,
            statistics=statistics,
            generated_at=datetime.utcnow().isoformat(),
            metadata={
                'action_count': len(mitigation_actions),
                'description': 'Risk mitigation action timeline'
            }
        )
    
    def to_json(self, projection: TimelineProjection) -> Dict[str, Any]:
        """
        Convert timeline projection to JSON-serializable format
        
        Args:
            projection: TimelineProjection object
            
        Returns:
            JSON-serializable dictionary
        """
        return {
            'start_date': projection.start_date,
            'end_date': projection.end_date,
            'time_series': [
                {
                    'timestamp': point.timestamp,
                    'value': point.value,
                    'confidence_lower': point.confidence_lower,
                    'confidence_upper': point.confidence_upper,
                    'metadata': point.metadata
                }
                for point in projection.time_series
            ],
            'events': [
                {
                    'event_id': event.event_id,
                    'event_type': event.event_type,
                    'timestamp': event.timestamp,
                    'title': event.title,
                    'description': event.description,
                    'severity': event.severity,
                    'impact_score': event.impact_score,
                    'related_risks': event.related_risks,
                    'action_items': event.action_items,
                    'metadata': event.metadata
                }
                for event in projection.events
            ],
            'action_plans': [
                {
                    'action_id': plan.action_id,
                    'title': plan.title,
                    'description': plan.description,
                    'start_date': plan.start_date,
                    'due_date': plan.due_date,
                    'status': plan.status,
                    'priority': plan.priority,
                    'owner': plan.owner,
                    'completion_percentage': plan.completion_percentage,
                    'dependencies': plan.dependencies,
                    'milestones': plan.milestones,
                    'metadata': plan.metadata
                }
                for plan in projection.action_plans
            ],
            'milestones': projection.milestones,
            'statistics': projection.statistics,
            'generated_at': projection.generated_at,
            'metadata': projection.metadata
        }
    
    # Helper methods
    
    def _generate_risk_time_series(
        self,
        start_date: datetime,
        end_date: datetime,
        current_risk: float,
        risk_factors: List[Dict[str, Any]],
        interval_days: int
    ) -> List[TimeSeriesPoint]:
        """Generate risk score time series with projections"""
        time_series = []
        current_date = start_date
        
        while current_date <= end_date:
            # Calculate risk at this point
            risk_score = current_risk
            
            # Apply risk factors
            for factor in risk_factors:
                if 'impact_date' in factor:
                    impact_date = self._parse_deadline(factor['impact_date'], start_date)
                    if current_date >= impact_date:
                        risk_score += factor.get('risk_delta', 0.0)
            
            # Add uncertainty that grows over time
            days_from_start = (current_date - start_date).days
            uncertainty = 0.05 + (days_from_start / 365) * 0.15
            
            time_series.append(TimeSeriesPoint(
                timestamp=current_date.isoformat(),
                value=min(1.0, max(0.0, risk_score)),
                confidence_lower=max(0.0, risk_score - uncertainty),
                confidence_upper=min(1.0, risk_score + uncertainty),
                metadata={'days_from_start': days_from_start}
            ))
            
            current_date += timedelta(days=interval_days)
        
        return time_series
    
    def _generate_compliance_time_series(
        self,
        start_date: datetime,
        end_date: datetime,
        regulations: List[Dict[str, Any]],
        events: List[TimelineEvent]
    ) -> List[TimeSeriesPoint]:
        """Generate compliance readiness time series"""
        time_series = []
        current_date = start_date
        interval_days = 7
        
        total_regulations = len(regulations)
        
        while current_date <= end_date:
            # Calculate compliance percentage
            compliant_count = 0
            for reg in regulations:
                if 'deadline' in reg:
                    deadline = self._parse_deadline(reg['deadline'], start_date)
                    if current_date >= deadline:
                        compliant_count += 1
                    else:
                        # Partial credit based on progress
                        prep_start = deadline - timedelta(days=90)
                        if current_date >= prep_start:
                            progress = (current_date - prep_start).days / 90
                            compliant_count += min(0.9, progress * 0.9)
            
            compliance_score = compliant_count / total_regulations if total_regulations > 0 else 0.0
            
            time_series.append(TimeSeriesPoint(
                timestamp=current_date.isoformat(),
                value=compliance_score,
                confidence_lower=max(0.0, compliance_score - 0.05),
                confidence_upper=min(1.0, compliance_score + 0.05),
                metadata={'compliant_count': int(compliant_count)}
            ))
            
            current_date += timedelta(days=interval_days)
        
        return time_series
    
    def _generate_mitigation_time_series(
        self,
        start_date: datetime,
        end_date: datetime,
        action_plans: List[ActionPlan]
    ) -> List[TimeSeriesPoint]:
        """Generate risk reduction time series from mitigation actions"""
        time_series = []
        current_date = start_date
        interval_days = 7
        
        initial_risk = 0.8  # Assume high initial risk
        
        while current_date <= end_date:
            risk_reduction = 0.0
            
            for plan in action_plans:
                plan_start = datetime.fromisoformat(plan.start_date)
                plan_due = datetime.fromisoformat(plan.due_date)
                
                if current_date >= plan_due:
                    # Full risk reduction if completed
                    risk_reduction += 0.15
                elif current_date >= plan_start:
                    # Partial reduction based on progress
                    progress = (current_date - plan_start).days / max(1, (plan_due - plan_start).days)
                    risk_reduction += 0.15 * min(1.0, progress)
            
            current_risk = max(0.1, initial_risk - risk_reduction)
            
            time_series.append(TimeSeriesPoint(
                timestamp=current_date.isoformat(),
                value=current_risk,
                confidence_lower=max(0.0, current_risk - 0.1),
                confidence_upper=min(1.0, current_risk + 0.05),
                metadata={'risk_reduction': risk_reduction}
            ))
            
            current_date += timedelta(days=interval_days)
        
        return time_series
    
    def _generate_events_from_factors(
        self,
        risk_factors: List[Dict[str, Any]],
        start_date: datetime,
        end_date: datetime
    ) -> List[TimelineEvent]:
        """Generate events from risk factors"""
        events = []
        
        for factor in risk_factors:
            if 'impact_date' in factor:
                impact_date = self._parse_deadline(factor['impact_date'], start_date)
                
                if start_date <= impact_date <= end_date:
                    events.append(TimelineEvent(
                        event_id=factor.get('id', f"event_{len(events)}"),
                        event_type=factor.get('type', EventType.RISK_THRESHOLD_BREACH.value),
                        timestamp=impact_date.isoformat(),
                        title=factor.get('title', 'Risk Factor Event'),
                        description=factor.get('description', ''),
                        severity=factor.get('severity', EventSeverity.MEDIUM.value),
                        impact_score=factor.get('impact_score', 0.5),
                        related_risks=factor.get('related_risks', []),
                        action_items=factor.get('action_items', []),
                        metadata=factor.get('metadata', {})
                    ))
        
        events.sort(key=lambda e: e.timestamp)
        return events
    
    def _generate_action_plans(
        self,
        risk_factors: List[Dict[str, Any]],
        start_date: datetime
    ) -> List[ActionPlan]:
        """Generate action plans from risk factors"""
        action_plans = []
        
        for factor in risk_factors:
            if factor.get('requires_action', False):
                impact_date = self._parse_deadline(factor.get('impact_date', start_date), start_date)
                prep_start = impact_date - timedelta(days=60)
                
                action_plans.append(ActionPlan(
                    action_id=f"action_{factor.get('id', len(action_plans))}",
                    title=f"Mitigate: {factor.get('title', 'Risk Factor')}",
                    description=factor.get('mitigation', ''),
                    start_date=max(start_date, prep_start).isoformat(),
                    due_date=impact_date.isoformat(),
                    status='not_started',
                    priority=factor.get('priority', 'medium'),
                    owner=factor.get('owner', 'Risk Team'),
                    completion_percentage=0.0,
                    dependencies=[],
                    milestones=[],
                    metadata={'risk_factor_id': factor.get('id', '')}
                ))
        
        return action_plans
    
    def _extract_milestones(
        self,
        events: List[TimelineEvent],
        action_plans: List[ActionPlan]
    ) -> List[Dict[str, Any]]:
        """Extract key milestones from events and action plans"""
        milestones = []
        
        # From events
        for event in events:
            if event.event_type in [EventType.MILESTONE.value, EventType.COMPLIANCE_DEADLINE.value]:
                milestones.append({
                    'id': event.event_id,
                    'date': event.timestamp,
                    'title': event.title,
                    'type': event.event_type,
                    'severity': event.severity,
                    'source': 'event'
                })
        
        # From action plans
        for plan in action_plans:
            milestones.append({
                'id': f"{plan.action_id}_start",
                'date': plan.start_date,
                'title': f"Start: {plan.title}",
                'type': 'action_start',
                'severity': 'info',
                'source': 'action_plan'
            })
            milestones.append({
                'id': f"{plan.action_id}_due",
                'date': plan.due_date,
                'title': f"Due: {plan.title}",
                'type': 'action_due',
                'severity': plan.priority,
                'source': 'action_plan'
            })
        
        milestones.sort(key=lambda m: m['date'])
        return milestones
    
    def _calculate_timeline_statistics(
        self,
        time_series: List[TimeSeriesPoint],
        events: List[TimelineEvent],
        action_plans: List[ActionPlan]
    ) -> Dict[str, Any]:
        """Calculate timeline statistics"""
        # Time series stats
        values = [point.value for point in time_series]
        
        # Event stats
        event_severity_counts = {}
        for event in events:
            event_severity_counts[event.severity] = event_severity_counts.get(event.severity, 0) + 1
        
        # Action plan stats
        action_status_counts = {}
        for plan in action_plans:
            action_status_counts[plan.status] = action_status_counts.get(plan.status, 0) + 1
        
        return {
            'time_series_stats': {
                'min_value': float(min(values)) if values else 0.0,
                'max_value': float(max(values)) if values else 0.0,
                'mean_value': float(np.mean(values)) if values else 0.0,
                'trend': 'increasing' if values and values[-1] > values[0] else 'decreasing'
            },
            'event_stats': {
                'total_events': len(events),
                'by_severity': event_severity_counts,
                'critical_count': event_severity_counts.get('critical', 0),
                'high_count': event_severity_counts.get('high', 0)
            },
            'action_plan_stats': {
                'total_actions': len(action_plans),
                'by_status': action_status_counts,
                'average_completion': float(np.mean([plan.completion_percentage for plan in action_plans])) if action_plans else 0.0
            }
        }
    
    def _parse_deadline(self, deadline: Any, default: datetime) -> datetime:
        """Parse deadline to datetime"""
        if isinstance(deadline, datetime):
            return deadline
        elif isinstance(deadline, str):
            try:
                return datetime.fromisoformat(deadline)
            except:
                return default
        elif isinstance(deadline, int):
            return default + timedelta(days=deadline)
        else:
            return default
    
    def _estimate_completion(self, current: datetime, start: datetime, due: datetime) -> float:
        """Estimate completion percentage based on time elapsed"""
        if current < start:
            return 0.0
        elif current >= due:
            return 100.0
        else:
            total_days = (due - start).days
            elapsed_days = (current - start).days
            return min(100.0, (elapsed_days / max(1, total_days)) * 100)
