'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up (queryInterface, Sequelize) {
    await queryInterface.addColumn('report_templates', 'content_type', {
      type: Sequelize.ENUM('text', 'html'),
      defaultValue: 'text',
      allowNull: false
    });
  },

  async down (queryInterface, Sequelize) {
    await queryInterface.removeColumn('report_templates', 'content_type');
  }
};