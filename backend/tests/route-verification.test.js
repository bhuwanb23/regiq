const express = require('express');
const userRoutes = require('../src/routes/user.routes');

console.log('🧪 Verifying User Management Routes...\n');

// Create a test Express app
const app = express();
app.use(express.json());

// Mount user routes
app.use('/users', userRoutes);

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
  
  console.log('📋 Registered User Management Routes:');
  routes.forEach((route, index) => {
    console.log(`   ${index + 1}. ${route.method.padEnd(7)} ${route.path}`);
  });
  
  console.log(`\n✅ Total routes found: ${routes.length}`);
  
  // Verify we have all the expected routes
  const expectedRoutes = [
    'GET /users',
    'GET /users/:id',
    'POST /users',
    'PUT /users/:id',
    'DELETE /users/:id',
    'GET /users/:id/preferences',
    'PUT /users/:id/preferences',
    'GET /users/:id/activity',
    'PUT /users/:id/roles',
    'GET /users/:id/auth-logs',
    'GET /users/:id/export',
    'POST /users/:id/restore',
    'POST /users/validate'
  ];
  
  console.log('\n🔍 Verifying expected routes:');
  expectedRoutes.forEach(route => {
    const [method, path] = route.split(' ');
    const exists = routes.some(r => r.method === method && r.path === path);
    console.log(`   ${exists ? '✅' : '❌'} ${route}`);
  });
  
} catch (error) {
  console.log('❌ Route verification failed:', error.message);
}

console.log('\n✅ Route verification completed!');