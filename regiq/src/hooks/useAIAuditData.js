import { useState, useEffect } from 'react';
import { Alert } from 'react-native';
import { getAIModelAnalyses } from '../services/apiClient';
import {
  calculateOverview,
  calculateRiskLevel,
  formatDate,
} from '../services/realWorldAIModels';

const EMPTY_OVERVIEW = {
  activeModels: 0,
  riskScore: 0,
  modelsThisMonth: 0,
  riskLevel: 'Unknown',
  totalAudits: 0,
  criticalIssues: 0,
};

const useAIAuditData = () => {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);
  const [selectedModel, setSelectedModel] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);

  const [auditData, setAuditData] = useState({
    overview: EMPTY_OVERVIEW,
    models: [],
  });

  /** Accept all common envelope shapes returned by the gateway. */
  const normalizeList = (payload) => {
    if (Array.isArray(payload)) return payload;
    if (Array.isArray(payload?.data)) return payload.data;
    if (Array.isArray(payload?.data?.items)) return payload.data.items;
    if (Array.isArray(payload?.items)) return payload.items;
    return [];
  };

  const fetchAuditData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getAIModelAnalyses();
      const analyses = normalizeList(response);

      const models = analyses.map((analysis) => ({
        id: analysis.id || analysis.model_id,
        name: analysis.model_name || analysis.name || 'Unknown Model',
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

      const overviewBase = calculateOverview(models);
      const overview = models.length
        ? {
            activeModels: models.filter(
              (m) => m.status === 'Completed' || m.status === 'Active'
            ).length,
            riskScore: overviewBase.riskScore,
            modelsThisMonth: overviewBase.modelsThisMonth,
            riskLevel: overviewBase.riskLevel,
            totalAudits: models.length,
            criticalIssues: overviewBase.criticalIssues,
          }
        : EMPTY_OVERVIEW;

      setAuditData({ overview, models });
      setLoading(false);
    } catch (err) {
      setError(err?.message || 'Failed to load AI model analyses');
      setAuditData({ overview: EMPTY_OVERVIEW, models: [] });
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
    error,
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
