import { useState, useEffect } from 'react';

const useDashboardData = () => {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [dashboardData, setDashboardData] = useState({
    complianceScore: 78,
    user: {
      name: 'John Anderson',
      company: 'FinTech Solutions Inc.',
      role: 'Compliance Manager',
    },
    quickStats: [
      {
        id: 'active_models',
        title: 'Active Models',
        value: '12',
        subtitle: 'AI models monitored',
        icon: 'analytics',
        trend: 'up',
        trendValue: '+2',
        color: '#8B5CF6', // Primary purple
      },
      {
        id: 'pending_tasks',
        title: 'Pending Tasks',
        value: '5',
        subtitle: 'Require attention',
        icon: 'checkmark-circle',
        trend: 'down',
        trendValue: '-3',
        color: '#F59E0B', // Warning
      },
      {
        id: 'reports_generated',
        title: 'Reports Generated',
        value: '23',
        subtitle: 'This month',
        icon: 'document-text',
        trend: 'up',
        trendValue: '+8',
        color: '#10B981', // Success
      },
      {
        id: 'risk_score',
        title: 'Risk Score',
        value: 'Low',
        subtitle: '2.3% overall risk',
        icon: 'shield-checkmark',
        trend: 'neutral',
        trendValue: '0%',
        color: '#0D9488', // Secondary teal
      },
    ],
    alerts: [
      {
        id: 1,
        type: 'warning',
        title: 'New RBI Digital Lending Guidelines',
        description: 'Review required for KYC API compliance by Dec 15, 2024',
        priority: 'high',
        timestamp: '2 hours ago',
        category: 'regulatory',
        actionRequired: true,
      },
      {
        id: 2,
        type: 'error',
        title: 'AI Model Bias Detected',
        description: 'Credit scoring model shows 6.7% gender bias in loan approvals',
        priority: 'critical',
        timestamp: '4 hours ago',
        category: 'ai_ethics',
        actionRequired: true,
      },
      {
        id: 3,
        type: 'info',
        title: 'EU AI Act Update',
        description: 'New transparency requirements effective January 2025',
        priority: 'medium',
        timestamp: '1 day ago',
        category: 'regulatory',
        actionRequired: false,
      },
      {
        id: 4,
        type: 'success',
        title: 'Compliance Check Completed',
        description: 'GDPR audit completed successfully with 95% compliance score',
        priority: 'low',
        timestamp: '2 days ago',
        category: 'compliance',
        actionRequired: false,
      },
    ],
    recentActivity: [
      {
        id: 1,
        type: 'compliance_check',
        title: 'Compliance Check Completed',
        description: 'GDPR compliance audit finished with 95% score',
        timestamp: '2 hours ago',
        status: 'success',
        icon: 'shield-checkmark',
        details: {
          score: 95,
          duration: '45 minutes',
          checks: 23,
        },
      },
      {
        id: 2,
        type: 'ai_audit',
        title: 'AI Model Bias Detected',
        description: 'Credit scoring model shows 6.7% gender bias',
        timestamp: '4 hours ago',
        status: 'warning',
        icon: 'analytics',
        details: {
          modelId: 'credit-score-v2.1',
          biasScore: 6.7,
          affectedFeatures: ['gender', 'age'],
        },
      },
      {
        id: 3,
        type: 'regulation_update',
        title: 'New Regulation Update',
        description: 'EU AI Act transparency requirements updated',
        timestamp: '1 day ago',
        status: 'info',
        icon: 'document-text',
        details: {
          regulation: 'EU AI Act',
          section: 'Article 13 - Transparency',
          effectiveDate: '2025-01-01',
        },
      },
      {
        id: 4,
        type: 'report_generated',
        title: 'Risk Report Generated',
        description: 'Monthly risk assessment report is ready',
        timestamp: '2 days ago',
        status: 'success',
        icon: 'bar-chart',
        details: {
          reportType: 'Monthly Risk Assessment',
          pages: 24,
          riskLevel: 'Low',
        },
      },
      {
        id: 5,
        type: 'alert',
        title: 'Compliance Alert',
        description: 'KYC API requires immediate attention',
        timestamp: '3 days ago',
        status: 'error',
        icon: 'warning',
        details: {
          apiEndpoint: '/api/v1/kyc/verify',
          errorRate: '12%',
          impact: 'High',
        },
      },
    ],
    complianceMetrics: {
      overallScore: 78,
      regulations: 12,
      alerts: 2,
      lastUpdated: '2 hours ago',
      breakdown: [
        {
          category: 'Data Privacy (GDPR)',
          score: 95,
          status: 'excellent',
          lastCheck: '1 hour ago',
        },
        {
          category: 'AI Ethics',
          score: 82,
          status: 'good',
          lastCheck: '3 hours ago',
        },
        {
          category: 'Financial Regulations',
          score: 76,
          status: 'fair',
          lastCheck: '5 hours ago',
        },
        {
          category: 'Data Security',
          score: 88,
          status: 'good',
          lastCheck: '2 hours ago',
        },
      ],
    },
  });

  // Simulate API call
  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // In a real app, this would be an API call
      // const response = await fetch('/api/dashboard');
      // const data = await response.json();
      // setDashboardData(data);
      
      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setLoading(false);
    }
  };

  const refreshDashboard = async () => {
    setRefreshing(true);
    try {
      await fetchDashboardData();
    } finally {
      setRefreshing(false);
    }
  };

  const updateComplianceScore = (newScore) => {
    setDashboardData(prev => ({
      ...prev,
      complianceScore: newScore,
      complianceMetrics: {
        ...prev.complianceMetrics,
        overallScore: newScore,
      },
    }));
  };

  const markAlertAsRead = (alertId) => {
    setDashboardData(prev => ({
      ...prev,
      alerts: prev.alerts.map(alert =>
        alert.id === alertId
          ? { ...alert, read: true }
          : alert
      ),
    }));
  };

  const addActivity = (activity) => {
    setDashboardData(prev => ({
      ...prev,
      recentActivity: [activity, ...prev.recentActivity.slice(0, 4)],
    }));
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  return {
    dashboardData,
    loading,
    refreshing,
    refreshDashboard,
    updateComplianceScore,
    markAlertAsRead,
    addActivity,
  };
};

export default useDashboardData;
