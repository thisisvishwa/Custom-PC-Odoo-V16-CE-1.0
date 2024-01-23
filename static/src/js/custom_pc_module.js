odoo.define('custom_pc_builder.CustomPCWidget', function (require) {
    'use strict';

    const core = require('web.core');
    const Widget = require('web.Widget');
    const QWeb = core.qweb;
    const _t = core._t;

    const CustomPCWidget = Widget.extend({
        template: 'custom_pc_module_templates',
        xmlDependencies: ['/static/src/xml/custom_pc_module_templates.xml'],
        events: {
            'click .js_add_component': '_onAddComponent',
            'click .js_remove_component': '_onRemoveComponent',
            'input #budget-input': '_onBudgetInput',
        },

        init: function (parent, options) {
            this._super(parent, options);
            this.components = [];
            this.budget = 0;
        },

        start: function () {
            this._updateBudgetDisplay();
            return this._super.apply(this, arguments);
        },

        _onAddComponent: function (event) {
            const componentId = $(event.currentTarget).data('component-id');
            this._fetchComponentData(componentId).then((componentData) => {
                this.components.push(componentData);
                this._renderComponents();
                core.bus.trigger('custom_event', COMPONENT_ADDED_MSG);
            });
        },

        _onRemoveComponent: function (event) {
            const componentId = $(event.currentTarget).data('component-id');
            this.components = this.components.filter((component) => component.id !== componentId);
            this._renderComponents();
            core.bus.trigger('custom_event', COMPONENT_REMOVED_MSG);
        },

        _onBudgetInput: function (event) {
            this.budget = parseFloat($(event.currentTarget).val());
            this._updateBudgetDisplay();
        },

        _updateBudgetDisplay: function () {
            this.$('#budget-display').text(this.budget.toFixed(2));
            this._checkBudgetConstraints();
        },

        _checkBudgetConstraints: function () {
            const totalCost = this.components.reduce((sum, component) => sum + component.price, 0);
            if (totalCost > this.budget) {
                this.$('#budget-warning').text(_t(BUDGET_EXCEEDED_MSG)).show();
            } else {
                this.$('#budget-warning').hide();
            }
        },

        _fetchComponentData: function (componentId) {
            return this._rpc({
                model: 'component',
                method: 'read',
                args: [[componentId], COMPONENT_FIELDS],
            });
        },

        _renderComponents: function () {
            const content = QWeb.render('custom_pc_components_list', {
                components: this.components,
            });
            this.$('.js_components_list').html(content);
            this._checkCompatibility();
        },

        _checkCompatibility: function () {
            // Placeholder for compatibility check logic
            // This should be replaced with actual implementation
            const compatibilityIssues = this.components.some((component) => {
                // Logic to determine compatibility issues
                return false; // Assuming no issues for placeholder
            });

            if (compatibilityIssues) {
                this.$('#compatibility-warning').text(_t(COMPATIBILITY_ISSUE_MSG)).show();
            } else {
                this.$('#compatibility-warning').hide();
            }
        },
    });

    core.action_registry.add('custom_pc_builder', CustomPCWidget);

    return CustomPCWidget;
});