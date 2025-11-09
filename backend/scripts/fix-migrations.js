const fs = require('fs');
const path = require('path');

const migrationsDir = path.join(__dirname, '..', 'migrations');

// Read all migration files
const migrationFiles = fs.readdirSync(migrationsDir);

// For each migration file, fix the table name
migrationFiles.forEach(file => {
  if (file.endsWith('.js')) {
    const filePath = path.join(migrationsDir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Extract table name from file name
    // e.g., 20251109013723-create-data-bias-detection.js -> data_bias_detections
    const tableName = file
      .replace(/\d+-create-/, '')
      .replace(/\.js$/, '')
      .replace(/-/g, '_')
      .replace(/s$/, 's'); // Keep pluralization
    
    // Special cases for pluralization
    const tableNamePlural = tableName.endsWith('s') ? tableName : tableName + 's';
    
    // Fix the up migration
    content = content.replace(
      new RegExp(`await queryInterface\\.createTable\\('${tableNamePlural.replace(/_/g, '')}'`, 'g'),
      `await queryInterface.createTable('${tableNamePlural}'`
    );
    
    // Fix the down migration
    content = content.replace(
      new RegExp(`await queryInterface\\.dropTable\\('${tableNamePlural.replace(/_/g, '')}'`, 'g'),
      `await queryInterface.dropTable('${tableNamePlural}'`
    );
    
    // Write the fixed content back to the file
    fs.writeFileSync(filePath, content);
    console.log(`Fixed ${file}`);
  }
});

console.log('All migrations fixed!');