import { useState, useEffect } from 'react';

const useRegulationData = () => {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFilters, setSelectedFilters] = useState(['all']);
  const [viewMode, setViewMode] = useState('feed'); // 'feed' or 'timeline'

  const [regulationsData, setRegulationsData] = useState({
    regulations: [
      {
        id: 1,
        title: 'AI Act Implementation Guidelines',
        description: 'New compliance requirements for AI systems in financial services, including risk assessment frameworks and documentation standards.',
        priority: 'Critical',
        region: 'EU',
        category: 'AI/ML',
        effectiveDate: 'Dec 15, 2024',
        timeAgo: '2 days ago',
        tags: ['Risk Assessment', 'Documentation', 'Audit Requirements'],
        fullDetails: 'The European Union\'s AI Act introduces comprehensive regulations for artificial intelligence systems used in financial services. Key requirements include mandatory risk assessments, algorithmic transparency documentation, and regular compliance audits for high-risk AI applications.',
      },
      {
        id: 2,
        title: 'CFPB Open Banking Rules',
        description: 'Updated data sharing standards and consumer protection measures for open banking implementations in the United States.',
        priority: 'Medium',
        region: 'US',
        category: 'Banking',
        effectiveDate: 'Jan 30, 2025',
        timeAgo: '1 week ago',
        tags: ['Data Sharing', 'Consumer Protection', 'API Standards'],
        fullDetails: 'The Consumer Financial Protection Bureau has updated open banking regulations to enhance data sharing standards and strengthen consumer protection measures. Financial institutions must implement new API security protocols and consent management systems.',
      },
      {
        id: 3,
        title: 'FCA Crypto Asset Guidelines',
        description: 'Enhanced regulatory framework for cryptocurrency exchanges and digital asset custody services in the United Kingdom.',
        priority: 'Low',
        region: 'UK',
        category: 'Crypto',
        effectiveDate: 'Mar 1, 2025',
        timeAgo: '3 days ago',
        tags: ['Crypto Exchange', 'Custody Services', 'AML Compliance'],
        fullDetails: 'The Financial Conduct Authority has established new guidelines for cryptocurrency exchanges and digital asset custody services, focusing on anti-money laundering compliance and customer asset protection.',
      },
      {
        id: 4,
        title: 'MAS Digital Payment Token Standards',
        description: 'Singapore\'s Monetary Authority establishes new compliance standards for digital payment tokens and stablecoin issuers.',
        priority: 'Critical',
        region: 'APAC',
        category: 'Payments',
        effectiveDate: 'Feb 15, 2025',
        timeAgo: '5 days ago',
        tags: ['Stablecoins', 'Payment Tokens', 'Reserve Requirements'],
        fullDetails: 'The Monetary Authority of Singapore has introduced comprehensive standards for digital payment tokens and stablecoin issuers, including reserve requirements, operational resilience, and consumer protection measures.',
      },
      {
        id: 5,
        title: 'Basel III Capital Requirements Update',
        description: 'Updated capital adequacy requirements for banks with significant exposure to digital assets and fintech partnerships.',
        priority: 'High',
        region: 'Global',
        category: 'Banking',
        effectiveDate: 'Jun 1, 2025',
        timeAgo: '1 week ago',
        tags: ['Capital Adequacy', 'Digital Assets', 'Risk Management'],
        fullDetails: 'The Basel Committee has updated capital requirements for banks with exposure to digital assets and fintech partnerships, introducing new risk weighting methodologies and operational risk considerations.',
      },
    ],
    deadlines: [
      {
        id: 1,
        title: 'AI Act Compliance',
        daysRemaining: 15,
        date: 'Dec 15',
        priority: 'critical',
        description: 'EU AI Act implementation deadline',
      },
      {
        id: 2,
        title: 'CFPB Data Standards',
        daysRemaining: 45,
        date: 'Jan 30',
        priority: 'medium',
        description: 'Open banking data sharing compliance',
      },
      {
        id: 3,
        title: 'MAS Token Standards',
        daysRemaining: 67,
        date: 'Feb 15',
        priority: 'high',
        description: 'Digital payment token regulations',
      },
    ],
  });

  // Simulate API call
  const fetchRegulations = async () => {
    setLoading(true);
    try {
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // In a real app, this would be an API call
      // const response = await fetch('/api/regulations');
      // const data = await response.json();
      // setRegulationsData(data);
      
      setLoading(false);
    } catch (error) {
      console.error('Error fetching regulations:', error);
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

  const handleSearch = (query) => {
    setSearchQuery(query);
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
    let filtered = regulationsData.regulations;

    // Apply search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(reg => 
        reg.title.toLowerCase().includes(query) ||
        reg.description.toLowerCase().includes(query) ||
        reg.category.toLowerCase().includes(query) ||
        reg.region.toLowerCase().includes(query)
      );
    }

    // Apply category filters
    if (!selectedFilters.includes('all') && selectedFilters.length > 0) {
      filtered = filtered.filter(reg => {
        const categoryMatch = selectedFilters.some(filter => {
          switch (filter) {
            case 'high':
              return reg.priority.toLowerCase() === 'critical' || reg.priority.toLowerCase() === 'high';
            case 'ai':
              return reg.category.toLowerCase().includes('ai');
            case 'banking':
              return reg.category.toLowerCase() === 'banking';
            case 'crypto':
              return reg.category.toLowerCase() === 'crypto';
            case 'payments':
              return reg.category.toLowerCase() === 'payments';
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

  useEffect(() => {
    fetchRegulations();
  }, []);

  return {
    regulationsData,
    filteredRegulations: getFilteredRegulations(),
    deadlines: regulationsData.deadlines,
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
  };
};

export default useRegulationData;
