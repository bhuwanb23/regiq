const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// Open the database
const dbPath = path.join(__dirname, 'database.sqlite');
const db = new sqlite3.Database(dbPath);

// Query to get all tables
db.serialize(() => {
  db.all("SELECT name FROM sqlite_master WHERE type='table'", (err, rows) => {
    if (err) {
      console.error('Error querying database:', err);
    } else {
      console.log('Database tables:');
      rows.forEach(row => {
        console.log('- ' + row.name);
      });
    }
    db.close();
  });
});