class StreamProcessingService {
  constructor() {
    this.activeStreams = new Map();
  }

  async createStreamProcessor(streamId, config = {}) {
    try {
      const processor = {
        id: streamId,
        config: config,
        status: 'initialized',
        metrics: {
          recordsProcessed: 0,
          errors: 0,
          startTime: null,
          lastActivity: null
        },
        buffer: [],
        bufferSize: config.bufferSize || 100,
        flushInterval: config.flushInterval || 5000 // 5 seconds
      };

      this.activeStreams.set(streamId, processor);
      
      return processor;
    } catch (error) {
      throw new Error(`Failed to create stream processor: ${error.message}`);
    }
  }

  async startStreamProcessing(streamId, processFunction) {
    try {
      const processor = this.activeStreams.get(streamId);
      if (!processor) {
        throw new Error(`Stream processor ${streamId} not found`);
      }

      processor.status = 'running';
      processor.metrics.startTime = new Date();
      processor.metrics.lastActivity = new Date();

      // Start flush interval
      processor.flushTimer = setInterval(() => {
        this.flushStreamBuffer(streamId, processFunction);
      }, processor.flushInterval);

      // Return a copy of the processor without the timer
      const { flushTimer, ...processorWithoutTimer } = processor;
      return processorWithoutTimer;
    } catch (error) {
      throw new Error(`Failed to start stream processing: ${error.message}`);
    }
  }

  async stopStreamProcessing(streamId) {
    try {
      const processor = this.activeStreams.get(streamId);
      if (!processor) {
        throw new Error(`Stream processor ${streamId} not found`);
      }

      // Clear flush interval
      if (processor.flushTimer) {
        clearInterval(processor.flushTimer);
        delete processor.flushTimer;
      }

      processor.status = 'stopped';
      processor.metrics.lastActivity = new Date();

      return processor;
    } catch (error) {
      throw new Error(`Failed to stop stream processing: ${error.message}`);
    }
  }

  async addDataToStream(streamId, data) {
    try {
      const processor = this.activeStreams.get(streamId);
      if (!processor) {
        throw new Error(`Stream processor ${streamId} not found`);
      }

      if (processor.status !== 'running') {
        throw new Error(`Stream processor ${streamId} is not running`);
      }

      // Add data to buffer
      processor.buffer.push(data);
      processor.metrics.lastActivity = new Date();

      // Flush buffer if it's full
      if (processor.buffer.length >= processor.bufferSize) {
        await this.flushStreamBuffer(streamId);
      }

      return { 
        success: true, 
        bufferLength: processor.buffer.length 
      };
    } catch (error) {
      throw new Error(`Failed to add data to stream: ${error.message}`);
    }
  }

  async flushStreamBuffer(streamId, processFunction) {
    try {
      const processor = this.activeStreams.get(streamId);
      if (!processor) {
        throw new Error(`Stream processor ${streamId} not found`);
      }

      if (processor.buffer.length === 0) {
        return { success: true, processedCount: 0 };
      }

      // Process buffered data
      const bufferCopy = [...processor.buffer];
      processor.buffer = [];

      let processedCount = 0;
      let errorCount = 0;

      for (const data of bufferCopy) {
        try {
          if (processFunction) {
            await processFunction(data);
          }
          processedCount++;
        } catch (error) {
          errorCount++;
          console.error(`Error processing stream data: ${error.message}`);
        }
      }

      // Update metrics
      processor.metrics.recordsProcessed += processedCount;
      processor.metrics.errors += errorCount;
      processor.metrics.lastActivity = new Date();

      return { 
        success: true, 
        processedCount: processedCount,
        errorCount: errorCount
      };
    } catch (error) {
      throw new Error(`Failed to flush stream buffer: ${error.message}`);
    }
  }

  async getStreamProcessor(streamId) {
    try {
      const processor = this.activeStreams.get(streamId);
      if (!processor) {
        throw new Error(`Stream processor ${streamId} not found`);
      }
      
      // Return a copy of the processor without the timer
      const { flushTimer, ...processorWithoutTimer } = processor;
      return processorWithoutTimer;
    } catch (error) {
      throw new Error(`Failed to get stream processor: ${error.message}`);
    }
  }

  async getAllStreamProcessors() {
    try {
      const processors = Array.from(this.activeStreams.values());
      // Return copies of the processors without the timers
      return processors.map(processor => {
        const { flushTimer, ...processorWithoutTimer } = processor;
        return processorWithoutTimer;
      });
    } catch (error) {
      throw new Error(`Failed to get stream processors: ${error.message}`);
    }
  }

  async removeStreamProcessor(streamId) {
    try {
      const processor = this.activeStreams.get(streamId);
      if (!processor) {
        throw new Error(`Stream processor ${streamId} not found`);
      }

      // Stop processing if running
      if (processor.status === 'running') {
        await this.stopStreamProcessing(streamId);
      }

      // Remove from active streams
      this.activeStreams.delete(streamId);

      return { success: true, message: 'Stream processor removed successfully' };
    } catch (error) {
      throw new Error(`Failed to remove stream processor: ${error.message}`);
    }
  }

  async pauseStreamProcessing(streamId) {
    try {
      const processor = this.activeStreams.get(streamId);
      if (!processor) {
        throw new Error(`Stream processor ${streamId} not found`);
      }

      if (processor.status === 'running') {
        processor.status = 'paused';
        processor.metrics.lastActivity = new Date();
      }

      // Return a copy of the processor without the timer
      const { flushTimer, ...processorWithoutTimer } = processor;
      return processorWithoutTimer;
    } catch (error) {
      throw new Error(`Failed to pause stream processing: ${error.message}`);
    }
  }

  async resumeStreamProcessing(streamId) {
    try {
      const processor = this.activeStreams.get(streamId);
      if (!processor) {
        throw new Error(`Stream processor ${streamId} not found`);
      }

      if (processor.status === 'paused') {
        processor.status = 'running';
        processor.metrics.lastActivity = new Date();
      }

      // Return a copy of the processor without the timer
      const { flushTimer, ...processorWithoutTimer } = processor;
      return processorWithoutTimer;
    } catch (error) {
      throw new Error(`Failed to resume stream processing: ${error.message}`);
    }
  }
}

module.exports = new StreamProcessingService();