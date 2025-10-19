import { useState, useEffect } from 'react';
import { Alert } from 'react-native';

const useAIAuditData = () => {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedModel, setSelectedModel] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);

  const [auditData, setAuditData] = useState({
    overview: {
      activeModels: 12,
      riskScore: 7.2,
      modelsThisMonth: 2,
      riskLevel: 'Medium Risk',
      totalAudits: 45,
      criticalIssues: 3,
    },
    models: [
      {
        id: 'credit-risk-v3',
        name: 'Credit Risk Model v3',
        type: 'Credit Assessment',
        status: 'Active',
        lastAudit: '2 days ago',
        biasScore: 0.12,
        version: '3.2.1',
        riskLevel: 'Low',
        accuracy: 94.2,
        driftScore: 0.03,
        lastUpdated: 'Oct 15, 2024',
      },
      {
        id: 'fraud-detector',
        name: 'Fraud Detection Engine',
        type: 'Fraud Prevention',
        status: 'Warning',
        lastAudit: '1 week ago',
        biasScore: 0.28,
        version: '2.1.0',
        riskLevel: 'Medium',
        accuracy: 91.8,
        driftScore: 0.07,
        lastUpdated: 'Oct 10, 2024',
      },
      {
        id: 'payment-processor',
        name: 'Payment Processor AI',
        type: 'Payment Processing',
        status: 'Active',
        lastAudit: '5 days ago',
        biasScore: 0.08,
        version: '1.5.2',
        riskLevel: 'Low',
        accuracy: 96.5,
        driftScore: 0.02,
        lastUpdated: 'Oct 12, 2024',
      },
      {
        id: 'risk-analyzer',
        name: 'Risk Analysis Model',
        type: 'Risk Analysis',
        status: 'Active',
        lastAudit: '3 days ago',
        biasScore: 0.15,
        version: '4.0.1',
        riskLevel: 'Medium',
        accuracy: 89.3,
        driftScore: 0.04,
        lastUpdated: 'Oct 14, 2024',
      },
      {
        id: 'customer-scoring',
        name: 'Customer Scoring Engine',
        type: 'Credit Assessment',
        status: 'Inactive',
        lastAudit: '2 weeks ago',
        biasScore: 0.22,
        version: '2.3.1',
        riskLevel: 'High',
        accuracy: 87.1,
        driftScore: 0.09,
        lastUpdated: 'Sep 28, 2024',
      },
    ],
  });

  // Simulate API call
  const fetchAuditData = async () => {
    setLoading(true);
    try {
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // In a real app, this would be an API call
      // const response = await fetch('/api/ai-audit');
      // const data = await response.json();
      // setAuditData(data);
      
      setLoading(false);
    } catch (error) {
      console.error('Error fetching audit data:', error);
      setLoading(false);
    }
  };

  const refreshAuditData = async () => {
    setRefreshing(true);
    try {
      await fetchAuditData();
    } finally {
      setRefreshing(false);
    }
  };

  const handleModelPress = (model) => {
    console.log('Model selected:', model.name);
    setSelectedModel(model);
    setModalVisible(true);
  };

  const handleModelAudit = (model) => {
    console.log('Running audit for model:', model.name);
    // Simulate audit process
    // In a real app, this would trigger an audit API call
    
    // Update model status to show audit in progress
    setAuditData(prev => ({
      ...prev,
      models: prev.models.map(m =>
        m.id === model.id
          ? { ...m, status: 'Auditing', lastAudit: 'In progress...' }
          : m
      ),
    }));

    // Simulate audit completion after 3 seconds
    setTimeout(() => {
      setAuditData(prev => ({
        ...prev,
        models: prev.models.map(m =>
          m.id === model.id
            ? { 
                ...m, 
                status: 'Active', 
                lastAudit: 'Just now',
                biasScore: Math.random() * 0.3, // Random bias score for demo
              }
            : m
        ),
      }));
    }, 3000);
  };


  const getModelsByStatus = (status) => {
    return auditData.models.filter(model => 
      model.status.toLowerCase() === status.toLowerCase()
    );
  };

  const getHighRiskModels = () => {
    return auditData.models.filter(model => 
      parseFloat(model.biasScore) > 0.2 || model.riskLevel === 'High'
    );
  };

  const updateModelStatus = (modelId, newStatus) => {
    setAuditData(prev => ({
      ...prev,
      models: prev.models.map(model =>
        model.id === modelId ? { ...model, status: newStatus } : model
      ),
    }));
  };

  useEffect(() => {
    fetchAuditData();
  }, []);

  const handleGenerateReport = (model) => {
    console.log('Generating report for model:', model.name);
    Alert.alert(
      'Report Generated',
      `Audit report for ${model.name} has been generated successfully!`,
      [{ text: 'OK' }]
    );
  };

  const handleRunSimulation = (model) => {
    console.log('Running simulation for model:', model.name);
    Alert.alert(
      'Simulation Started',
      `Risk scenario simulation for ${model.name} has been started.`,
      [{ text: 'OK' }]
    );
  };

  const closeModal = () => {
    setModalVisible(false);
    setSelectedModel(null);
  };

  return {
    auditData,
    loading,
    refreshing,
    selectedModel,
    modalVisible,
    refreshAuditData,
    handleModelPress,
    handleModelAudit,
    handleGenerateReport,
    handleRunSimulation,
    closeModal,
    getModelsByStatus,
    getHighRiskModels,
    updateModelStatus,
  };
};

export default useAIAuditData;
