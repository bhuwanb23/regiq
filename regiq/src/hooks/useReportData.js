import { useState, useEffect } from 'react';
import { 
  getReports, 
  getReportById, 
  generateReport,
  scheduleReport
} from '../services/apiClient';

const useReportData = (reportId = null) => {
  const [loading, setLoading] = useState(false);
  const [reports, setReports] = useState([]);
  const [selectedReport, setSelectedReport] = useState(null);
  const [error, setError] = useState(null);

  // Fetch all reports
  const fetchReports = async (params = {}) => {
    setLoading(true);
    setError(null);
    try {
      const response = await getReports(params);
      setReports(response.data || []);
      return response;
    } catch (err) {
      console.error('Error fetching reports:', err);
      setError(err.message || 'Failed to fetch reports');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Fetch a specific report by ID
  const fetchReportById = async (id) => {
    setLoading(true);
    setError(null);
    try {
      const response = await getReportById(id);
      setSelectedReport(response.data || null);
      return response;
    } catch (err) {
      console.error(`Error fetching report ${id}:`, err);
      setError(err.message || `Failed to fetch report ${id}`);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Generate a new report
  const createReport = async (reportData) => {
    setLoading(true);
    setError(null);
    try {
      const response = await generateReport(reportData);
      // Refresh reports after creating new report
      await fetchReports();
      return response;
    } catch (err) {
      console.error('Error generating report:', err);
      setError(err.message || 'Failed to generate report');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Schedule a report
  const scheduleReportGeneration = async (scheduleData) => {
    setLoading(true);
    setError(null);
    try {
      const response = await scheduleReport(scheduleData);
      return response;
    } catch (err) {
      console.error('Error scheduling report:', err);
      setError(err.message || 'Failed to schedule report');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Initialize data on mount
  useEffect(() => {
    fetchReports();
    if (reportId) {
      fetchReportById(reportId);
    }
  }, [reportId]);

  return {
    loading,
    error,
    reports,
    selectedReport,
    fetchReports,
    fetchReportById,
    createReport,
    scheduleReportGeneration,
    setSelectedReport,
  };
};

export default useReportData;