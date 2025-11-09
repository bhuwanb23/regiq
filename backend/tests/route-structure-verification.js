const express = require('express');
const regulatoryRoutes = require('../src/routes/regulatory.routes');

console.log('🧪 Verifying Route Structure...\n');

// Create a test Express app
const app = express();
app.use(express.json());

// Mount regulatory routes
app.use('/regulatory', regulatoryRoutes);

// Get all routes from the app
function getRoutes(stack, prefix = '') {
  const routes = [];
  
  stack.forEach(layer => {
    if (layer.route) {
      const route = {
        method: Object.keys(layer.route.methods)[0].toUpperCase(),
        path: prefix + layer.route.path
      };
      routes.push(route);
    } else if (layer.name === 'router' && layer.handle.stack) {
      const newPrefix = prefix + (layer.regexp.source !== '^\\/$' ? layer.regexp.source.replace(/\\/g, '').replace('^', '').replace('$', '') : '');
      routes.push(...getRoutes(layer.handle.stack, newPrefix));
    }
  });
  
  return routes;
}

try {
  const routes = getRoutes(app._router.stack);
  
  console.log('📋 Registered Regulatory Routes:');
  routes.forEach(route => {
    console.log(`   ${route.method.padEnd(7)} ${route.path}`);
  });
  
  console.log(`\n✅ Total routes registered: ${routes.length}`);
  
} catch (error) {
  console.log('❌ Route structure verification failed:', error.message);
}