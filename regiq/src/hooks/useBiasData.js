import { useState, useEffect } from 'react';
import { 
  getBiasReports, 
  getBiasReportById, 
  createBiasAnalysis,
  getBiasMitigation
} from '../services/apiClient';

const useBiasData = (modelId = null) => {
  const [loading, setLoading] = useState(false);
  const [reports, setReports] = useState([]);
  const [selectedReport, setSelectedReport] = useState(null);
  const [mitigationStrategies, setMitigationStrategies] = useState([]);
  const [error, setError] = useState(null);

  // Fetch all bias reports
  const fetchBiasReports = async (params = {}) => {
    setLoading(true);
    setError(null);
    try {
      const response = await getBiasReports(params);
      setReports(response.data || []);
      return response;
    } catch (err) {
      console.error('Error fetching bias reports:', err);
      setError(err.message || 'Failed to fetch bias reports');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Fetch a specific bias report by ID
  const fetchBiasReportById = async (reportId) => {
    setLoading(true);
    setError(null);
    try {
      const response = await getBiasReportById(reportId);
      setSelectedReport(response.data || null);
      return response;
    } catch (err) {
      console.error(`Error fetching bias report ${reportId}:`, err);
      setError(err.message || `Failed to fetch bias report ${reportId}`);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Create a new bias analysis
  const runBiasAnalysis = async (analysisData) => {
    setLoading(true);
    setError(null);
    try {
      const response = await createBiasAnalysis(analysisData);
      // Refresh reports after creating new analysis
      await fetchBiasReports();
      return response;
    } catch (err) {
      console.error('Error running bias analysis:', err);
      setError(err.message || 'Failed to run bias analysis');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Fetch mitigation strategies for a model
  const fetchMitigationStrategies = async (modelId) => {
    setLoading(true);
    setError(null);
    try {
      const response = await getBiasMitigation(modelId);
      setMitigationStrategies(response.data || []);
      return response;
    } catch (err) {
      console.error(`Error fetching mitigation strategies for model ${modelId}:`, err);
      setError(err.message || `Failed to fetch mitigation strategies for model ${modelId}`);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Initialize data on mount
  useEffect(() => {
    fetchBiasReports();
    if (modelId) {
      fetchMitigationStrategies(modelId);
    }
  }, [modelId]);

  return {
    loading,
    error,
    reports,
    selectedReport,
    mitigationStrategies,
    fetchBiasReports,
    fetchBiasReportById,
    runBiasAnalysis,
    fetchMitigationStrategies,
    setSelectedReport,
  };
};

export default useBiasData;