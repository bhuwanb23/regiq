import { useState, useEffect } from 'react';
import {
  getRegulations,
  searchRegulations,
  getRegulationCategories,
  getRegulationDeadlines,
  getRegulationById,
} from '../services/apiClient';

const useRegulationData = () => {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFilters, setSelectedFilters] = useState(['all']);
  const [viewMode, setViewMode] = useState('feed');
  const [categories, setCategories] = useState([]);

  const [regulationsData, setRegulationsData] = useState({
    regulations: [],
    deadlines: [],
  });

  /**
   * Normalize the variety of response envelopes the gateway returns:
   * a bare array, `{ data: [...] }`, or `{ data: { items: [...] } }`.
   */
  const normalizeList = (payload) => {
    if (Array.isArray(payload)) return payload;
    if (Array.isArray(payload?.data)) return payload.data;
    if (Array.isArray(payload?.data?.items)) return payload.data.items;
    if (Array.isArray(payload?.items)) return payload.items;
    return [];
  };

  const fetchRegulations = async () => {
    setLoading(true);
    setError(null);
    try {
      const [regulationsResponse, deadlinesResponse, categoriesResponse] =
        await Promise.all([
          getRegulations(),
          getRegulationDeadlines(),
          getRegulationCategories(),
        ]);

      setRegulationsData({
        regulations: normalizeList(regulationsResponse),
        deadlines: normalizeList(deadlinesResponse),
      });
      setCategories(normalizeList(categoriesResponse));
      setLoading(false);
    } catch (err) {
      setError(err?.message || 'Failed to load regulations');
      setRegulationsData({ regulations: [], deadlines: [] });
      setCategories([]);
      setLoading(false);
    }
  };

  const refreshRegulations = async () => {
    setRefreshing(true);
    try {
      await fetchRegulations();
    } finally {
      setRefreshing(false);
    }
  };

  const handleSearch = async (query) => {
    setSearchQuery(query);

    if (query.trim()) {
      try {
        const searchResults = await searchRegulations(query);
        setRegulationsData((prev) => ({
          ...prev,
          regulations: normalizeList(searchResults),
        }));
      } catch (err) {
        setError(err?.message || 'Search failed');
      }
    } else {
      await fetchRegulations();
    }
  };

  const handleFilterChange = (filterId) => {
    if (filterId === 'all') {
      setSelectedFilters(['all']);
    } else {
      const newFilters = selectedFilters.includes(filterId)
        ? selectedFilters.filter(f => f !== filterId && f !== 'all')
        : [...selectedFilters.filter(f => f !== 'all'), filterId];
      
      setSelectedFilters(newFilters.length > 0 ? newFilters : ['all']);
    }
  };

  const getFilteredRegulations = () => {
    // Ensure regulations is an array - handle API response format
    let regulationsArray = Array.isArray(regulationsData.regulations) 
      ? regulationsData.regulations 
      : (regulationsData.regulations?.data || []);
    
    let filtered = [...regulationsArray]; // Create a copy to avoid mutating original data

    // Safety check: if filtered is not an array, return empty array
    if (!Array.isArray(filtered)) {
      console.warn('Filtered data is not an array, returning empty array');
      return [];
    }

    // Apply search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(reg => 
        reg.title && reg.title.toLowerCase().includes(query) ||
        reg.description && reg.description.toLowerCase().includes(query) ||
        reg.category && reg.category.toLowerCase().includes(query) ||
        reg.region && reg.region.toLowerCase().includes(query)
      );
    }

    // Apply category filters
    if (!selectedFilters.includes('all') && selectedFilters.length > 0) {
      filtered = filtered.filter(reg => {
        if (!reg) return false;
        const categoryMatch = selectedFilters.some(filter => {
          switch (filter) {
            case 'high':
              return reg.priority && (reg.priority.toLowerCase() === 'critical' || reg.priority.toLowerCase() === 'high');
            case 'ai':
              return reg.category && reg.category.toLowerCase().includes('ai');
            case 'banking':
              return reg.category && reg.category.toLowerCase() === 'banking';
            case 'crypto':
              return reg.category && reg.category.toLowerCase() === 'crypto';
            case 'payments':
              return reg.category && reg.category.toLowerCase() === 'payments';
            default:
              return false;
          }
        });
        return categoryMatch;
      });
    }

    return filtered;
  };

  const addRegulation = (regulation) => {
    setRegulationsData(prev => ({
      ...prev,
      regulations: [regulation, ...prev.regulations],
    }));
  };

  const updateRegulation = (regulationId, updates) => {
    setRegulationsData(prev => ({
      ...prev,
      regulations: prev.regulations.map(reg =>
        reg.id === regulationId ? { ...reg, ...updates } : reg
      ),
    }));
  };

  const fetchRegulationById = async (id) => {
    return getRegulationById(id);
  };

  useEffect(() => {
    fetchRegulations();
  }, []);

  return {
    regulationsData,
    filteredRegulations: getFilteredRegulations(),
    deadlines: regulationsData.deadlines,
    categories,
    loading,
    refreshing,
    error,
    searchQuery,
    selectedFilters,
    viewMode,
    refreshRegulations,
    handleSearch,
    handleFilterChange,
    setViewMode,
    addRegulation,
    updateRegulation,
    fetchRegulationById,
  };
};

export default useRegulationData;