import { useState, useEffect } from 'react';
import { Alert } from 'react-native';
import { getAIModelAnalyses, getBiasScores } from '../services/apiClient';
import { 
  getSampleRealWorldModels, 
  calculateOverview,
  calculateRiskLevel,
  formatDate 
} from '../services/realWorldAIModels';

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

  // Fetch AI model audit data from API
  const fetchAuditData = async () => {
    setLoading(true);
    try {
      console.log('🔍 Fetching AI model analyses from API...');
      
      // Fetch real analyses from backend
      const analysesResponse = await getAIModelAnalyses();
      console.log('📦 AI Model Analyses Response:', analysesResponse);
      
      // Handle different response formats
      let analyses = [];
      if (Array.isArray(analysesResponse)) {
        analyses = analysesResponse;
        console.log('✅ Array response, count:', analyses.length);
      } else if (analysesResponse?.data && Array.isArray(analysesResponse.data)) {
        analyses = analysesResponse.data;
        console.log('✅ Object.data response, count:', analyses.length);
      } else {
        console.warn('⚠️ Unexpected response format or empty');
        analyses = [];
      }
      
      // If no data from API, use sample real-world models
      if (analyses.length === 0) {
        console.log('💾 No analyses in database, loading sample real-world AI models...');
        const sampleModels = getSampleRealWorldModels();
        const overview = calculateOverview(sampleModels);
        
        setAuditData({
          overview,
          models: sampleModels,
        });
      } else {
        // Transform API response to UI format
        const models = analyses.map(analysis => ({
          id: analysis.id || analysis.model_id,
          name: analysis.model_name || 'Unknown Model',
          type: analysis.model_type || 'General AI',
          status: analysis.status || 'Unknown',
          lastAudit: formatDate(analysis.created_at),
          biasScore: analysis.overall_bias_score || 0,
          version: analysis.model_version || '1.0.0',
          riskLevel: calculateRiskLevel(analysis.overall_bias_score),
          accuracy: analysis.fairness_metrics?.accuracy || 0,
          driftScore: analysis.drift_score || 0,
          lastUpdated: formatDate(analysis.updated_at),
          fairnessMetrics: analysis.fairness_metrics,
          protectedAttributes: analysis.protected_attributes,
          description: analysis.description || '',
        }));
        
        // Calculate overview statistics
        const overview = {
          activeModels: models.filter(m => m.status === 'Completed' || m.status === 'Active').length,
          riskScore: calculateOverview(models).riskScore,
          modelsThisMonth: calculateOverview(models).modelsThisMonth,
          riskLevel: calculateOverview(models).riskLevel,
          totalAudits: models.length,
          criticalIssues: calculateOverview(models).criticalIssues,
        };
        
        console.log('📊 Final models count:', models.length);
        console.log('📊 Overview:', overview);
        
        setAuditData({
          overview,
          models,
        });
      }
      
      setLoading(false);
    } catch (error) {
      console.error('❌ Error fetching audit data:', error);
      console.log('💾 Loading sample real-world AI models due to error');
      
      // Load sample real-world models on error
      const sampleModels = getSampleRealWorldModels();
      const overview = calculateOverview(sampleModels);
      
      setAuditData({
        overview,
        models: sampleModels,
      });
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
