const { DataValidationRule } = require('../models');

class DataValidationService {
  async createValidationRule(ruleData) {
    try {
      const rule = await DataValidationRule.create(ruleData);
      return rule;
    } catch (error) {
      throw new Error(`Failed to create validation rule: ${error.message}`);
    }
  }

  async getValidationRuleById(id) {
    try {
      const rule = await DataValidationRule.findByPk(id);
      if (!rule) {
        throw new Error('Validation rule not found');
      }
      return rule;
    } catch (error) {
      throw new Error(`Failed to get validation rule: ${error.message}`);
    }
  }

  async getAllValidationRules(limit = 10, offset = 0) {
    try {
      const { rows, count } = await DataValidationRule.findAndCountAll({
        limit,
        offset,
        order: [['created_at', 'DESC']]
      });
      return { rules: rows, count, limit, offset };
    } catch (error) {
      throw new Error(`Failed to list validation rules: ${error.message}`);
    }
  }

  async updateValidationRule(id, updateData) {
    try {
      const rule = await this.getValidationRuleById(id);
      const updatedRule = await rule.update(updateData);
      return updatedRule;
    } catch (error) {
      throw new Error(`Failed to update validation rule: ${error.message}`);
    }
  }

  async deleteValidationRule(id) {
    try {
      const rule = await this.getValidationRuleById(id);
      await rule.destroy();
      return { success: true, message: 'Validation rule deleted successfully' };
    } catch (error) {
      throw new Error(`Failed to delete validation rule: ${error.message}`);
    }
  }

  async getActiveValidationRules() {
    try {
      const rules = await DataValidationRule.findAll({
        where: { isActive: true },
        order: [['priority', 'ASC'], ['created_at', 'DESC']]
      });
      return rules;
    } catch (error) {
      throw new Error(`Failed to get active validation rules: ${error.message}`);
    }
  }

  async validateData(data, ruleIds = null) {
    try {
      let rules;
      if (ruleIds) {
        rules = await DataValidationRule.findAll({
          where: { id: ruleIds, isActive: true }
        });
      } else {
        rules = await this.getActiveValidationRules();
      }

      const validationResults = [];
      const errors = [];

      for (const rule of rules) {
        const result = this.applyValidationRule(data, rule);
        validationResults.push(result);
        
        if (!result.isValid) {
          errors.push({
            ruleId: rule.id,
            fieldName: rule.fieldName,
            errorMessage: rule.errorMessage || `Validation failed for field ${rule.fieldName}`,
            value: result.value
          });
        }
      }

      return {
        isValid: errors.length === 0,
        results: validationResults,
        errors: errors
      };
    } catch (error) {
      throw new Error(`Failed to validate data: ${error.message}`);
    }
  }

  applyValidationRule(data, rule) {
    const value = data[rule.fieldName];
    let isValid = true;
    let errorMessage = '';

    switch (rule.ruleType) {
      case 'presence':
        isValid = value !== undefined && value !== null && value !== '';
        errorMessage = isValid ? '' : 'Field is required';
        break;
        
      case 'format':
        if (rule.validationPattern) {
          const regex = new RegExp(rule.validationPattern);
          isValid = regex.test(value);
          errorMessage = isValid ? '' : 'Field format is invalid';
        }
        break;
        
      case 'range':
        if (typeof value === 'number') {
          if (rule.minValue !== null && value < rule.minValue) {
            isValid = false;
            errorMessage = `Value must be at least ${rule.minValue}`;
          } else if (rule.maxValue !== null && value > rule.maxValue) {
            isValid = false;
            errorMessage = `Value must be at most ${rule.maxValue}`;
          }
        } else {
          isValid = false;
          errorMessage = 'Value must be a number for range validation';
        }
        break;
        
      case 'custom':
        // For custom rules, we'll assume they're valid by default
        // In a real implementation, this would call a custom validation function
        break;
        
      default:
        isValid = true;
    }

    return {
      ruleId: rule.id,
      fieldName: rule.fieldName,
      value: value,
      isValid: isValid,
      errorMessage: errorMessage
    };
  }
}

module.exports = new DataValidationService();