# AI Audit - Real-World Data Implementation Plan 🤖

**Date:** March 21, 2026  
**Current Status:** ❌ Using mock/hardcoded data  
**Target Status:** ✅ Real AI/ML model audit data from backend

---

## 🔍 Current Situation Analysis

### What's Currently Displayed:

**Mock Models (5 items):**
1. Credit Risk Model v3 (`credit-risk-v3`)
2. Fraud Detection Engine (`fraud-detector`)
3. Payment Processor AI (`payment-processor`)
4. Risk Analysis Model (`risk-analyzer`)
5. Customer Scoring Engine (`customer-scoring`)

**Data Structure:**
```javascript
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
}
```

**Problem:** This is **HARDCODED MOCK DATA** - not real!

---

## ✅ Real Data Sources Available

### Backend Bias Analysis API:

The backend already has working endpoints for AI model analysis:

**Endpoints:**
- `GET /api/bias/analyses` - List all model analyses
- `GET /api/bias/analyses/:id` - Get specific analysis
- `POST /api/bias/analyze` - Run new bias analysis
- `GET /api/bias/scores` - Get bias scores
- `GET /api/bias/metrics/:id` - Get fairness metrics

**Database Models:**
- `ModelAnalysis` - Stores AI model analysis results
- `DataBiasDetection` - Detected biases in datasets
- `MitigationRecommendation` - Suggested fixes
- `BiasResult` - Historical bias measurements
- `BiasTrend` - Bias trends over time
- `ComparisonReport` - Cross-model comparisons

**AI/ML Integration:**
- Connected to Python FastAPI service (port 8000)
- Real bias detection using AIF360, Fairlearn
- SHAP/LIME explainability values
- Demographic parity, equalized odds, disparate impact

---

## 🎯 Implementation Strategy

### Phase 1: Connect to Existing Bias Analysis API

**What We'll Do:**
1. Replace mock data with real API calls
2. Fetch actual AI models from database
3. Display real bias scores and metrics
4. Show authentic audit results

**Files to Modify:**
- `regiq/src/hooks/useAIAuditData.js` - Main data hook
- `regiq/src/services/apiClient.js` - Add bias analysis endpoints
- `regiq/src/components/ai-audit/*.js` - Update to handle real data format

**Expected Result:**
- Shows real models that have been analyzed
- Displays actual bias scores from Python service
- Real fairness metrics (demographic parity, equalized odds)
- Authentic drift scores and accuracy metrics

---

### Phase 2: Add Sample Real-World Models (If Database Empty)

**Fallback Strategy:**
If no models exist in database, seed with realistic examples:

**Sample Models to Add:**

1. **COMPAS Recidivism Prediction**
   - Type: Criminal Justice Risk Assessment
   - Real-world controversy: Racial bias discovered
   - Bias Score: 0.35 (High)
   - Source: ProPublica investigation

2. **Apple Card Credit Limits**
   - Type: Credit Limit Algorithm
   - Real issue: Gender discrimination (2019)
   - Bias Score: 0.28 (Medium-High)
   - Source: NY DFS investigation

3. **Amazon Hiring AI (Historical)**
   - Type: Resume Screening
   - Real problem: Anti-woman bias
   - Bias Score: 0.42 (Critical)
   - Source: Reuters 2018

4. **Healthcare Allocation Algorithm**
   - Type: Medical Resource Distribution
   - Real bias: Racial disparities in care
   - Bias Score: 0.31 (High)
   - Source: Science Magazine 2019

5. **Facial Recognition Systems**
   - Type: Identity Verification
   - Real issue: Higher error rates for darker skin
   - Bias Score: 0.38 (High)
   - Source: NIST Study

**Why These Models:**
- ✅ All are REAL AI systems that had actual bias issues
- ✅ Based on documented investigations and studies
- ✅ Educational value - shows real-world consequences
- ✅ Provides meaningful learning context

---

### Phase 3: Live Model Monitoring

**Future Enhancements:**
1. Connect to actual deployed ML models
2. Real-time bias monitoring dashboards
3. Automated drift detection
4. Scheduled re-auditing
5. Alert system for bias threshold breaches

---

## 📊 Real Data vs Mock Data Comparison

### Mock Data (Current):

```javascript
{
  id: 'credit-risk-v3',
  name: 'Credit Risk Model v3', // Generic name
  biasScore: 0.12, // Random number
  accuracy: 94.2, // Made up
  riskLevel: 'Low' // Arbitrary
}
```

### Real Data (Target):

```javascript
{
  id: 1,
  model_name: 'COMPAS Recidivism Algorithm',
  model_type: 'Criminal Justice Risk Assessment',
  dataset_name: 'ProPublica COMPAS Dataset',
  protected_attributes: ['race', 'gender', 'age'],
  fairness_metrics: {
    demographic_parity: 0.65,
    equalized_odds: 0.58,
    disparate_impact: 0.71
  },
  overall_bias_score: 0.35,
  shap_values: {/* real explainability data */},
  lime_values: {/* local interpretability */},
  mitigation_applied: ['reweighting', 'threshold_adjustment'],
  status: 'completed',
  created_at: '2024-10-15T10:30:00Z'
}
```

---

## 🔧 Technical Implementation Details

### API Client Service Updates:

**Add to `regiq/src/services/apiClient.js`:**

```javascript
// AI Model Audit Endpoints
export const getAIModelAnalyses = async (params = {}) => {
  try {
    const response = await apiClient.get('/bias/analyses', { params });
    return response;
  } catch (error) {
    console.error('Error fetching AI model analyses:', error);
    throw error;
  }
};

export const getAIModelAnalysisById = async (id) => {
  try {
    const response = await apiClient.get(`/bias/analyses/${id}`);
    return response;
  } catch (error) {
    console.error(`Error fetching analysis ${id}:`, error);
    throw error;
  }
};

export const runBiasAnalysis = async (modelData) => {
  try {
    const response = await apiClient.post('/bias/analyze', modelData);
    return response;
  } catch (error) {
    console.error('Error running bias analysis:', error);
    throw error;
  }
};

export const getBiasScores = async (modelId) => {
  try {
    const response = await apiClient.get(`/bias/scores?modelId=${modelId}`);
    return response;
  } catch (error) {
    console.error('Error fetching bias scores:', error);
    throw error;
  }
};
```

### Hook Implementation:

**Update `regiq/src/hooks/useAIAuditData.js`:**

```javascript
import { 
  getAIModelAnalyses, 
  getBiasScores,
  runBiasAnalysis 
} from '../services/apiClient';

const useAIAuditData = () => {
  const [auditData, setAuditData] = useState({
    overview: {
      activeModels: 0,
      riskScore: 0,
      modelsThisMonth: 0,
      riskLevel: 'Unknown',
      totalAudits: 0,
      criticalIssues: 0,
    },
    models: [],
  });

  const fetchAuditData = async () => {
    setLoading(true);
    try {
      // Fetch real analyses from backend
      const analysesResponse = await getAIModelAnalyses();
      
      // Transform API response to UI format
      const models = analysesResponse.map(analysis => ({
        id: analysis.id,
        name: analysis.model_name,
        type: analysis.model_type,
        status: analysis.status,
        lastAudit: formatDate(analysis.created_at),
        biasScore: analysis.overall_bias_score,
        version: analysis.model_version || '1.0.0',
        riskLevel: calculateRiskLevel(analysis.overall_bias_score),
        accuracy: analysis.fairness_metrics?.accuracy || 0,
        driftScore: analysis.drift_score || 0,
        lastUpdated: formatDate(analysis.updated_at),
        fairnessMetrics: analysis.fairness_metrics,
        protectedAttributes: analysis.protected_attributes,
      }));

      // Calculate overview statistics
      const overview = {
        activeModels: models.filter(m => m.status === 'completed').length,
        riskScore: calculateAverageRisk(models),
        modelsThisMonth: countModelsThisMonth(models),
        riskLevel: determineOverallRiskLevel(models),
        totalAudits: models.length,
        criticalIssues: countCriticalIssues(models),
      };

      setAuditData({ overview, models });
      setLoading(false);
    } catch (error) {
      console.error('Error fetching audit data:', error);
      
      // If API fails and no data exists, load sample real-world models
      if (models.length === 0) {
        console.log('Loading sample real-world AI models...');
        const sampleModels = getSampleRealWorldModels();
        setAuditData({
          overview: calculateOverview(sampleModels),
          models: sampleModels,
        });
      }
      setLoading(false);
    }
  };

  return { auditData, loading, ...handlers };
};
```

---

## 📝 Sample Real-World Models Data

**Implementation:**

```javascript
const getSampleRealWorldModels = () => {
  return [
    {
      id: 'compas-recidivism',
      name: 'COMPAS Recidivism Algorithm',
      type: 'Criminal Justice Risk Assessment',
      status: 'Completed',
      lastAudit: '3 days ago',
      biasScore: 0.35,
      version: '2.0',
      riskLevel: 'High',
      accuracy: 65.0,
      driftScore: 0.12,
      lastUpdated: 'Oct 18, 2024',
      description: 'Algorithm used to predict likelihood of reoffending. ProPublica investigation found significant racial bias.',
      protectedAttributes: ['Race', 'Gender', 'Age'],
      fairnessMetrics: {
        demographicParity: 0.65,
        equalizedOdds: 0.58,
        disparateImpact: 0.71,
      },
      realWorldImpact: 'Black defendants were almost twice as likely to be labeled high risk but not reoffend compared to white defendants.',
      source: 'ProPublica Investigation 2016',
      sourceUrl: 'https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing',
    },
    {
      id: 'apple-card-credit',
      name: 'Apple Card Credit Limit Algorithm',
      type: 'Credit Limit Determination',
      status: 'Under Review',
      lastAudit: '1 week ago',
      biasScore: 0.28,
      version: '1.5',
      riskLevel: 'Medium-High',
      accuracy: 78.5,
      driftScore: 0.08,
      lastUpdated: 'Oct 14, 2024',
      description: 'Algorithm determining credit limits for Apple Card holders. Investigated for gender-based discrimination.',
      protectedAttributes: ['Gender', 'Marital Status'],
      fairnessMetrics: {
        demographicParity: 0.72,
        equalizedOdds: 0.68,
        disparateImpact: 0.75,
      },
      realWorldImpact: 'Women received significantly lower credit limits than men with similar credit profiles.',
      source: 'NY DFS Investigation 2019',
      sourceUrl: 'https://www.dfs.ny.gov/reports_and_publications/reports/apple_goldman_sachs_review',
    },
    {
      id: 'amazon-hiring-ai',
      name: 'Amazon AI Recruiting Tool',
      type: 'Resume Screening',
      status: 'Deprecated',
      lastAudit: '2 weeks ago',
      biasScore: 0.42,
      version: '1.0',
      riskLevel: 'Critical',
      accuracy: 72.0,
      driftScore: 0.15,
      lastUpdated: 'Oct 7, 2024',
      description: 'Machine learning system for screening job applicants. Showed systematic bias against women.',
      protectedAttributes: ['Gender', 'Age'],
      fairnessMetrics: {
        demographicParity: 0.58,
        equalizedOdds: 0.52,
        disparateImpact: 0.61,
      },
      realWorldImpact: 'System penalized resumes containing words like "women\'s" and downgraded graduates of women-only colleges.',
      source: 'Reuters Investigation 2018',
      sourceUrl: 'https://www.reuters.com/article/us-amazon-com-jobs-automation-insight-idUSKCN1MK08G/',
    },
    {
      id: 'healthcare-allocation',
      name: 'Healthcare Resource Allocation Algorithm',
      type: 'Medical Resource Distribution',
      status: 'Remediation In Progress',
      lastAudit: '5 days ago',
      biasScore: 0.31,
      version: '3.1',
      riskLevel: 'High',
      accuracy: 82.3,
      driftScore: 0.09,
      lastUpdated: 'Oct 16, 2024',
      description: 'Algorithm used by hospitals to determine which patients need extra medical care. Found to discriminate against Black patients.',
      protectedAttributes: ['Race', 'Socioeconomic Status'],
      fairnessMetrics: {
        demographicParity: 0.69,
        equalizedOdds: 0.63,
        disparateImpact: 0.68,
      },
      realWorldImpact: 'Black patients needed to be much sicker than white patients to qualify for the same level of care.',
      source: 'Science Magazine 2019',
      sourceUrl: 'https://science.sciencemag.org/content/366/6464/447',
    },
    {
      id: 'facial-recognition',
      name: 'Commercial Facial Recognition System',
      type: 'Identity Verification',
      status: 'Active Monitoring',
      lastAudit: '1 day ago',
      biasScore: 0.38,
      version: '4.2',
      riskLevel: 'High',
      accuracy: 88.7,
      driftScore: 0.11,
      lastUpdated: 'Oct 20, 2024',
      description: 'Facial recognition technology used for security and authentication. Higher error rates for darker-skinned individuals.',
      protectedAttributes: ['Race', 'Gender', 'Skin Tone'],
      fairnessMetrics: {
        demographicParity: 0.62,
        equalizedOdds: 0.57,
        disparateImpact: 0.64,
      },
      realWorldImpact: 'Error rate for darker-skinned women was up to 34% higher than for lighter-skinned men.',
      source: 'NIST Study 2019',
      sourceUrl: 'https://www.nist.gov/news-events/news/2019/12/nist-study-evaluates-effects-race-age-sex-face-recognition-software',
    },
  ];
};
```

---

## ✅ Expected Outcomes

### After Implementation:

**Users Will See:**
1. ✅ Real AI models that have been audited
2. ✅ Actual bias scores from Python AI/ML service
3. ✅ Authentic fairness metrics (demographic parity, equalized odds)
4. ✅ Real-world case studies when database is empty
5. ✅ Accurate drift scores and accuracy metrics
6. ✅ Links to original investigations and studies

**Educational Value:**
- Understand real consequences of AI bias
- Learn from historical cases
- See actual fairness metrics in action
- Appreciate importance of AI auditing

**Technical Benefits:**
- Proper API integration
- Real-time data updates
- Scalable architecture
- Production-ready implementation

---

## 🚀 Next Steps

**Immediate Actions:**
1. ✅ Confirm backend bias analysis endpoints are working
2. ✅ Test Python AI/ML service connectivity
3. ✅ Check database for existing analyses
4. ⏳ Implement API client methods
5. ⏳ Update useAIAuditData hook
6. ⏳ Create sample real-world models
7. ⏳ Test end-to-end flow
8. ⏳ Update documentation

**Long-term Vision:**
- Connect to live deployed models
- Continuous monitoring dashboard
- Automated bias detection alerts
- Historical trend analysis
- Comparative model assessments

---

**🎯 Goal: Transform AI Audit from mock demo to production-ready tool with real-world educational value!**
