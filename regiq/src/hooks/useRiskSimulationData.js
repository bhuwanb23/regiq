import { useState, useEffect } from 'react';
import { 
  getRiskSimulations, 
  getRiskSimulationById, 
  createRiskSimulation,
  getRiskScenarios
} from '../services/apiClient';

const useRiskSimulationData = (simulationId = null) => {
  const [loading, setLoading] = useState(false);
  const [simulations, setSimulations] = useState([]);
  const [selectedSimulation, setSelectedSimulation] = useState(null);
  const [scenarios, setScenarios] = useState([]);
  const [error, setError] = useState(null);

  // Fetch all risk simulations
  const fetchRiskSimulations = async (params = {}) => {
    setLoading(true);
    setError(null);
    try {
      const response = await getRiskSimulations(params);
      setSimulations(response.data || []);
      return response;
    } catch (err) {
      console.error('Error fetching risk simulations:', err);
      setError(err.message || 'Failed to fetch risk simulations');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Fetch a specific risk simulation by ID
  const fetchRiskSimulationById = async (id) => {
    setLoading(true);
    setError(null);
    try {
      const response = await getRiskSimulationById(id);
      setSelectedSimulation(response.data || null);
      return response;
    } catch (err) {
      console.error(`Error fetching risk simulation ${id}:`, err);
      setError(err.message || `Failed to fetch risk simulation ${id}`);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Create a new risk simulation
  const runRiskSimulation = async (simulationData) => {
    setLoading(true);
    setError(null);
    try {
      const response = await createRiskSimulation(simulationData);
      // Refresh simulations after creating new simulation
      await fetchRiskSimulations();
      return response;
    } catch (err) {
      console.error('Error running risk simulation:', err);
      setError(err.message || 'Failed to run risk simulation');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Fetch risk scenarios
  const fetchRiskScenarios = async (params = {}) => {
    setLoading(true);
    setError(null);
    try {
      const response = await getRiskScenarios(params);
      setScenarios(response.data || []);
      return response;
    } catch (err) {
      console.error('Error fetching risk scenarios:', err);
      setError(err.message || 'Failed to fetch risk scenarios');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Initialize data on mount
  useEffect(() => {
    fetchRiskSimulations();
    fetchRiskScenarios();
    if (simulationId) {
      fetchRiskSimulationById(simulationId);
    }
  }, [simulationId]);

  return {
    loading,
    error,
    simulations,
    selectedSimulation,
    scenarios,
    fetchRiskSimulations,
    fetchRiskSimulationById,
    runRiskSimulation,
    fetchRiskScenarios,
    setSelectedSimulation,
  };
};

export default useRiskSimulationData;