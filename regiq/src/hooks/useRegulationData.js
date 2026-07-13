import { useState, useEffect } from 'react';
import { 
  getRegulations, 
  searchRegulations, 
  getRegulationCategories, 
  getRegulationDeadlines,
  getRegulationById
} from '../services/apiClient';
import { getRealWorldRegulations, getRealWorldDeadlines } from '../services/realWorldRegulations';

const useRegulationData = () => {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFilters, setSelectedFilters] = useState(['all']);
  const [viewMode, setViewMode] = useState('feed'); // 'feed' or 'timeline'
  const [categories, setCategories] = useState([]);

  const [regulationsData, setRegulationsData] = useState({
    regulations: [],
    deadlines: [],
  });

  // Fetch regulations from API
  const fetchRegulations = async () => {
    setLoading(true);
    try {
      console.log('🔍 Fetching regulations from API...');
      
      // Fetch regulations from backend API
      const regulationsResponse = await getRegulations();
      console.log('📦 Regulations API Response:', regulationsResponse);
      
      // Handle different response formats
      let regulations = [];
      if (Array.isArray(regulationsResponse)) {
        regulations = regulationsResponse;
        console.log('✅ Array response, count:', regulations.length);
      } else if (regulationsResponse?.data && Array.isArray(regulationsResponse.data)) {
        regulations = regulationsResponse.data;
        console.log('✅ Object.data response, count:', regulations.length);
      } else {
        console.warn('⚠️ Unexpected response format, using fallback data');
        regulations = getRealWorldRegulations();
      }
      
      // Fetch deadlines
      const deadlinesResponse = await getRegulationDeadlines();
      console.log('📦 Deadlines API Response:', deadlinesResponse);
      
      let deadlines = [];
      if (Array.isArray(deadlinesResponse)) {
        deadlines = deadlinesResponse;
        console.log('✅ Deadlines array, count:', deadlines.length);
      } else if (deadlinesResponse?.data && Array.isArray(deadlinesResponse.data)) {
        deadlines = deadlinesResponse.data;
        console.log('✅ Deadlines object.data, count:', deadlines.length);
      } else {
        deadlines = getRealWorldDeadlines();
      }
      
      // Fetch categories
      const categoriesResponse = await getRegulationCategories();
      console.log('📦 Categories API Response:', categoriesResponse);
      setCategories(Array.isArray(categoriesResponse) ? categoriesResponse : []);
      
      console.log('📊 Final regulations count:', regulations.length);
      console.log('📊 Final deadlines count:', deadlines.length);
      
      setRegulationsData({
        regulations,
        deadlines,
      });
      
      setLoading(false);
    } catch (error) {
      console.error('❌ Error fetching regulations data:', error);
      console.log('💾 Loading real-world fallback data due to error');
      
      // Load real-world regulatory data on error
      setRegulationsData({
        regulations: getRealWorldRegulations(),
        deadlines: getRealWorldDeadlines(),
      });
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
        setRegulationsData(prev => ({
          ...prev,
          regulations: searchResults,
        }));
      } catch (error) {
        console.error('Error searching regulations:', error);
      }
    } else {
      // If search query is empty, fetch all regulations
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
    try {
      const regulation = await getRegulationById(id);
      return regulation;
    } catch (error) {
      console.error(`Error fetching regulation ${id}:`, error);
      throw error;
    }
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