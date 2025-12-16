const fs = require('fs');
const path = require('path');

// Reports directory
const reportsDir = path.join(__dirname, '..', 'reports');
const pdfDir = path.join(reportsDir, 'pdf');
const csvDir = path.join(reportsDir, 'csv');

function listReports() {
  console.log('=== GENERATED COMPLIANCE REPORTS ===\n');
  
  // Check if reports directory exists
  if (!fs.existsSync(reportsDir)) {
    console.log('No reports directory found.');
    return;
  }
  
  // List PDF reports
  console.log('PDF REPORTS:');
  console.log('------------');
  if (fs.existsSync(pdfDir)) {
    const pdfFiles = fs.readdirSync(pdfDir);
    if (pdfFiles.length > 0) {
      pdfFiles.forEach(file => {
        const filePath = path.join(pdfDir, file);
        const stats = fs.statSync(filePath);
        console.log(`  ${file} (${(stats.size / 1024).toFixed(2)} KB)`);
      });
    } else {
      console.log('  No PDF reports found.');
    }
  } else {
    console.log('  PDF directory not found.');
  }
  
  console.log('\nCSV REPORTS:');
  console.log('------------');
  if (fs.existsSync(csvDir)) {
    const csvFiles = fs.readdirSync(csvDir);
    if (csvFiles.length > 0) {
      csvFiles.forEach(file => {
        const filePath = path.join(csvDir, file);
        const stats = fs.statSync(filePath);
        console.log(`  ${file} (${(stats.size / 1024).toFixed(2)} KB)`);
      });
    } else {
      console.log('  No CSV reports found.');
    }
  } else {
    console.log('  CSV directory not found.');
  }
  
  console.log('\nDIRECTORIES:');
  console.log('------------');
  console.log(`  PDFs: ${pdfDir}`);
  console.log(`  CSVs: ${csvDir}`);
}

// Run the script
if (require.main === module) {
  listReports();
}

module.exports = { listReports };