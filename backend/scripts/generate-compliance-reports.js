const fs = require('fs');
const path = require('path');
const axios = require('axios');

// Create reports directory if it doesn't exist
const reportsDir = path.join(__dirname, '..', 'reports');
if (!fs.existsSync(reportsDir)) {
  fs.mkdirSync(reportsDir, { recursive: true });
}

// Create PDF directory if it doesn't exist
const pdfDir = path.join(reportsDir, 'pdf');
if (!fs.existsSync(pdfDir)) {
  fs.mkdirSync(pdfDir, { recursive: true });
}

// Create CSV directory if it doesn't exist
const csvDir = path.join(reportsDir, 'csv');
if (!fs.existsSync(csvDir)) {
  fs.mkdirSync(csvDir, { recursive: true });
}

// API base URL
const API_BASE_URL = 'http://localhost:3000/api';

// Sample compliance report data
const sampleReports = [
  {
    title: "Q4 2025 Compliance Report",
    reportType: "compliance",
    format: "pdf",
    content: {
      summary: {
        totalRegulations: 142,
        compliant: 128,
        nonCompliant: 5,
        pending: 9
      },
      data: [
        {
          jurisdiction: "United States",
          regulation: "GDPR Compliance Act",
          status: "compliant"
        },
        {
          jurisdiction: "Canada",
          regulation: "PIPEDA Amendment #42",
          status: "non-compliant",
          action: "Update privacy policy by Jan 15, 2026"
        },
        {
          jurisdiction: "European Union",
          regulation: "Digital Services Act",
          status: "compliant"
        },
        {
          jurisdiction: "Australia",
          regulation: "Privacy Act 1988",
          status: "pending",
          action: "Review required by Feb 1, 2026"
        }
      ]
    }
  },
  {
    title: "Q3 2025 Risk Assessment Report",
    reportType: "risk",
    format: "pdf",
    content: {
      summary: {
        totalRisks: 24,
        highPriority: 3,
        mediumPriority: 12,
        lowPriority: 9
      },
      data: [
        {
          category: "Data Security",
          risk: "Unencrypted Data Transfer",
          severity: "high",
          mitigation: "Implement end-to-end encryption"
        },
        {
          category: "Compliance",
          risk: "Missing Audit Trails",
          severity: "medium",
          mitigation: "Enable comprehensive logging"
        },
        {
          category: "Operational",
          risk: "Single Point of Failure",
          severity: "medium",
          mitigation: "Implement redundancy measures"
        }
      ]
    }
  },
  {
    title: "Annual Bias Analysis Report 2025",
    reportType: "bias",
    format: "pdf",
    content: {
      summary: {
        totalModels: 8,
        biasedModels: 2,
        fairModels: 6,
        recommendations: 15
      },
      data: [
        {
          model: "Customer Segmentation Engine",
          biasType: "Gender Bias",
          confidence: "87%",
          recommendation: "Retrain with balanced dataset"
        },
        {
          model: "Loan Approval System",
          biasType: "Regional Bias",
          confidence: "92%",
          recommendation: "Adjust weighting factors"
        }
      ]
    }
  }
];

async function generateReport(reportData) {
  try {
    console.log(`Generating report: ${reportData.title}`);
    
    // Generate the report
    const generateResponse = await axios.post(`${API_BASE_URL}/reports/generate`, reportData);
    const reportId = generateResponse.data.data.id;
    console.log(`Report generated with ID: ${reportId}`);
    
    // Generate PDF
    const pdfResponse = await axios({
      method: 'GET',
      url: `${API_BASE_URL}/reports/${reportId}/export/pdf`,
      responseType: 'stream'
    });
    
    const pdfFileName = `${reportData.title.replace(/[^a-zA-Z0-9]/g, '_')}_${reportId}.pdf`;
    const pdfFilePath = path.join(pdfDir, pdfFileName);
    
    const pdfWriter = fs.createWriteStream(pdfFilePath);
    pdfResponse.data.pipe(pdfWriter);
    
    await new Promise((resolve, reject) => {
      pdfWriter.on('finish', resolve);
      pdfWriter.on('error', reject);
    });
    
    console.log(`PDF saved to: ${pdfFilePath}`);
    
    // Generate CSV
    const csvResponse = await axios({
      method: 'GET',
      url: `${API_BASE_URL}/reports/${reportId}/export/csv`,
      responseType: 'stream'
    });
    
    const csvFileName = `${reportData.title.replace(/[^a-zA-Z0-9]/g, '_')}_${reportId}.csv`;
    const csvFilePath = path.join(csvDir, csvFileName);
    
    const csvWriter = fs.createWriteStream(csvFilePath);
    csvResponse.data.pipe(csvWriter);
    
    await new Promise((resolve, reject) => {
      csvWriter.on('finish', resolve);
      csvWriter.on('error', reject);
    });
    
    console.log(`CSV saved to: ${csvFilePath}`);
    
    return {
      reportId,
      pdfPath: pdfFilePath,
      csvPath: csvFilePath
    };
  } catch (error) {
    console.error(`Error generating report ${reportData.title}:`, error.message);
    throw error;
  }
}

async function main() {
  console.log('Starting compliance report generation...');
  
  const results = [];
  
  try {
    // Generate all sample reports
    for (const reportData of sampleReports) {
      const result = await generateReport(reportData);
      results.push(result);
    }
    
    console.log('\n=== REPORT GENERATION SUMMARY ===');
    console.log(`Generated ${results.length} reports successfully:`);
    
    results.forEach((result, index) => {
      console.log(`\n${index + 1}. Report ID: ${result.reportId}`);
      console.log(`   PDF: ${result.pdfPath}`);
      console.log(`   CSV: ${result.csvPath}`);
    });
    
    console.log('\nReports organized in:');
    console.log(`  PDFs: ${pdfDir}`);
    console.log(`  CSVs: ${csvDir}`);
    
  } catch (error) {
    console.error('Error in report generation process:', error.message);
    process.exit(1);
  }
}

// Run the script
if (require.main === module) {
  main();
}

module.exports = {
  generateReport,
  sampleReports
};