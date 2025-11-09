const { DataLineage } = require('../models');

class LineageTrackingService {
  async createLineageRecord(lineageData) {
    try {
      const lineage = await DataLineage.create(lineageData);
      return lineage;
    } catch (error) {
      throw new Error(`Failed to create lineage record: ${error.message}`);
    }
  }

  async getLineageRecordById(id) {
    try {
      const lineage = await DataLineage.findByPk(id);
      if (!lineage) {
        throw new Error('Lineage record not found');
      }
      return lineage;
    } catch (error) {
      throw new Error(`Failed to get lineage record: ${error.message}`);
    }
  }

  async getAllLineageRecords(limit = 10, offset = 0) {
    try {
      const { rows, count } = await DataLineage.findAndCountAll({
        limit,
        offset,
        order: [['created_at', 'DESC']]
      });
      return { lineage: rows, count, limit, offset };
    } catch (error) {
      throw new Error(`Failed to list lineage records: ${error.message}`);
    }
  }

  async updateLineageRecord(id, updateData) {
    try {
      const lineage = await this.getLineageRecordById(id);
      const updatedLineage = await lineage.update(updateData);
      return updatedLineage;
    } catch (error) {
      throw new Error(`Failed to update lineage record: ${error.message}`);
    }
  }

  async deleteLineageRecord(id) {
    try {
      const lineage = await this.getLineageRecordById(id);
      await lineage.destroy();
      return { success: true, message: 'Lineage record deleted successfully' };
    } catch (error) {
      throw new Error(`Failed to delete lineage record: ${error.message}`);
    }
  }

  async getLineageByJob(jobId, limit = 10, offset = 0) {
    try {
      const { rows, count } = await DataLineage.findAndCountAll({
        where: { jobId },
        limit,
        offset,
        order: [['created_at', 'DESC']]
      });
      return { lineage: rows, count, limit, offset };
    } catch (error) {
      throw new Error(`Failed to get lineage by job: ${error.message}`);
    }
  }

  async createTransformationLineage(jobId, sourceInfo, targetInfo, transformationInfo) {
    try {
      const startTime = new Date();
      
      const lineage = await this.createLineageRecord({
        jobId: jobId,
        sourceSystem: sourceInfo.system,
        targetSystem: targetInfo.system,
        sourceTable: sourceInfo.table,
        targetTable: targetInfo.table,
        sourceColumn: sourceInfo.column,
        targetColumn: targetInfo.column,
        transformationType: transformationInfo.type,
        transformationLogic: transformationInfo.logic,
        lineageType: transformationInfo.lineageType || 'etl',
        startTime: startTime
      });

      return lineage;
    } catch (error) {
      throw new Error(`Failed to create transformation lineage: ${error.message}`);
    }
  }

  async completeTransformationLineage(lineageId, recordCount = 0, errorCount = 0) {
    try {
      const lineage = await this.getLineageRecordById(lineageId);
      
      const endTime = new Date();
      const duration = endTime.getTime() - lineage.startTime.getTime();
      
      const updatedLineage = await lineage.update({
        endTime: endTime,
        duration: duration,
        recordCount: recordCount,
        errorCount: errorCount,
        status: errorCount > 0 ? 'inactive' : 'active'
      });

      return updatedLineage;
    } catch (error) {
      throw new Error(`Failed to complete transformation lineage: ${error.message}`);
    }
  }

  async getLineageGraph(jobId) {
    try {
      const lineageRecords = await DataLineage.findAll({
        where: { jobId },
        order: [['created_at', 'ASC']]
      });

      // Build a graph representation of the lineage
      const graph = {
        nodes: new Set(),
        edges: [],
        jobId: jobId
      };

      for (const record of lineageRecords) {
        // Add source node
        const sourceNode = `${record.sourceSystem}:${record.sourceTable || 'unknown'}:${record.sourceColumn || 'all'}`;
        graph.nodes.add(sourceNode);
        
        // Add target node
        const targetNode = `${record.targetSystem}:${record.targetTable || 'unknown'}:${record.targetColumn || 'all'}`;
        graph.nodes.add(targetNode);
        
        // Add edge
        graph.edges.push({
          source: sourceNode,
          target: targetNode,
          transformation: record.transformationType,
          recordCount: record.recordCount,
          errorCount: record.errorCount
        });
      }

      return {
        nodes: Array.from(graph.nodes),
        edges: graph.edges,
        jobId: graph.jobId
      };
    } catch (error) {
      throw new Error(`Failed to get lineage graph: ${error.message}`);
    }
  }

  async getLineagePath(jobId, sourceSystem, targetSystem) {
    try {
      const lineageRecords = await DataLineage.findAll({
        where: { jobId },
        order: [['created_at', 'ASC']]
      });

      // Find the path from source to target
      const path = [];
      let currentSystem = sourceSystem;
      
      while (currentSystem !== targetSystem && path.length < 100) { // Prevent infinite loops
        const nextRecord = lineageRecords.find(record => 
          record.sourceSystem === currentSystem && 
          !path.some(p => p.id === record.id)
        );
        
        if (!nextRecord) {
          break;
        }
        
        path.push(nextRecord);
        currentSystem = nextRecord.targetSystem;
      }

      return path;
    } catch (error) {
      throw new Error(`Failed to get lineage path: ${error.message}`);
    }
  }

  async getImpactAnalysis(jobId, system, table = null) {
    try {
      const lineageRecords = await DataLineage.findAll({
        where: { jobId }
      });

      // Find all downstream impacts
      const impactedSystems = new Set();
      const impactedTables = new Set();
      
      const queue = [{ system, table }];
      const visited = new Set();
      
      while (queue.length > 0) {
        const current = queue.shift();
        const key = `${current.system}:${current.table || 'all'}`;
        
        if (visited.has(key)) {
          continue;
        }
        
        visited.add(key);
        
        // Find all records where current system/table is the source
        const downstreamRecords = lineageRecords.filter(record => 
          record.sourceSystem === current.system && 
          (!current.table || record.sourceTable === current.table)
        );
        
        for (const record of downstreamRecords) {
          impactedSystems.add(record.targetSystem);
          if (record.targetTable) {
            impactedTables.add(`${record.targetSystem}:${record.targetTable}`);
          }
          queue.push({
            system: record.targetSystem,
            table: record.targetTable
          });
        }
      }

      return {
        jobId: jobId,
        sourceSystem: system,
        sourceTable: table,
        impactedSystems: Array.from(impactedSystems),
        impactedTables: Array.from(impactedTables),
        impactCount: impactedSystems.size
      };
    } catch (error) {
      throw new Error(`Failed to perform impact analysis: ${error.message}`);
    }
  }
}

module.exports = new LineageTrackingService();