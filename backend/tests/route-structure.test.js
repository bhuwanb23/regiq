const express = require('express');
const authRoutes = require('../src/routes/auth.routes');

console.log('🧪 Testing Route Structure...\n');

// Create a test Express app
const app = express();
app.use(express.json());

// Mount auth routes
app.use('/auth', authRoutes);

// Get all routes from the app
const routes = [];
function getRoutes(stack, prefix = '') {
  stack.forEach(layer => {
    if (layer.route) {
      routes.push({
        method: Object.keys(layer.route.methods)[0].toUpperCase(),
        path: prefix + layer.route.path
      });
    } else if (layer.name === 'router') {
      getRoutes(layer.handle.stack, prefix + (layer.regexp.source !== '^\\/$' ? layer.regexp.source.replace(/\\/g, '').replace('^', '').replace('$', '') : ''));
    }
  });
}

getRoutes(app._router.stack);

console.log('📋 Registered Routes:');
routes.forEach(route => {
  console.log(`   ${route.method.padEnd(7)} ${route.path}`);
});

console.log('\n✅ Route structure test completed!');
console.log('Note: Actual endpoint functionality requires database connection.');