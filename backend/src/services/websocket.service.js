const { Server } = require('socket.io');
const winston = require('winston');

class WebSocketService {
  constructor() {
    this.io = null;
    this.clients = new Map();
    
    // Initialize logger
    this.logger = winston.createLogger({
      level: 'info',
      format: winston.format.json(),
      transports: [
        new winston.transports.Console(),
      ],
    });
  }

  /**
   * Initialize WebSocket server
   * @param {http.Server} server - HTTP server instance
   */
  initialize(server) {
    this.io = new Server(server, {
      cors: {
        origin: "*",
        methods: ["GET", "POST"]
      }
    });

    this.setupEventHandlers();
    this.logger.info('WebSocket server initialized');
  }

  /**
   * Setup WebSocket event handlers
   */
  setupEventHandlers() {
    this.io.on('connection', (socket) => {
      this.logger.info('New client connected', { clientId: socket.id });
      
      // Store client connection
      this.clients.set(socket.id, {
        socket,
        subscriptions: new Set()
      });

      // Handle client subscription to job updates
      socket.on('subscribeToJob', (jobId) => {
        this.logger.info('Client subscribed to job updates', { clientId: socket.id, jobId });
        const client = this.clients.get(socket.id);
        if (client) {
          client.subscriptions.add(jobId);
        }
      });

      // Handle client unsubscription
      socket.on('unsubscribeFromJob', (jobId) => {
        this.logger.info('Client unsubscribed from job updates', { clientId: socket.id, jobId });
        const client = this.clients.get(socket.id);
        if (client) {
          client.subscriptions.delete(jobId);
        }
      });

      // Handle client disconnection
      socket.on('disconnect', () => {
        this.logger.info('Client disconnected', { clientId: socket.id });
        this.clients.delete(socket.id);
      });
    });
  }

  /**
   * Broadcast job status update to subscribed clients
   * @param {string} jobId - Job ID
   * @param {Object} statusUpdate - Status update data
   */
  broadcastJobUpdate(jobId, statusUpdate) {
    if (!this.io) {
      this.logger.warn('WebSocket server not initialized');
      return;
    }

    // Send update to all clients subscribed to this job
    this.clients.forEach((client, clientId) => {
      if (client.subscriptions.has(jobId)) {
        client.socket.emit('jobStatusUpdate', {
          jobId,
          ...statusUpdate
        });
        this.logger.debug('Job status update sent to client', { clientId, jobId });
      }
    });
  }

  /**
   * Broadcast system metrics update
   * @param {Object} metrics - Metrics data
   */
  broadcastMetricsUpdate(metrics) {
    if (!this.io) {
      this.logger.warn('WebSocket server not initialized');
      return;
    }

    // Send metrics update to all connected clients
    this.io.emit('metricsUpdate', metrics);
    this.logger.debug('Metrics update broadcasted to all clients');
  }

  /**
   * Get number of connected clients
   * @returns {number} Number of connected clients
   */
  getClientCount() {
    return this.clients.size;
  }

  /**
   * Get active subscriptions
   * @returns {Array} List of active subscriptions
   */
  getActiveSubscriptions() {
    const subscriptions = [];
    this.clients.forEach((client) => {
      client.subscriptions.forEach((jobId) => {
        subscriptions.push(jobId);
      });
    });
    return [...new Set(subscriptions)]; // Remove duplicates
  }
}

module.exports = new WebSocketService();