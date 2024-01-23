from odoo import models, fields, api
from .component import COMPONENT_FIELDS
from .compatibility_check import COMPATIBILITY_CHECK_FIELDS

class CustomPC(models.Model):
    _name = 'custom.pc'
    _description = 'Custom PC Configuration'

    name = fields.Char(string='Configuration Name', required=True)
    user_id = fields.Many2one('res.users', string='Configured By', default=lambda self: self.env.user)
    budget_limit = fields.Float(string='Budget Limit')
    total_price = fields.Float(string='Total Price', compute='_compute_total_price')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('ordered', 'Ordered')
    ], string='Status', default='draft')
    component_ids = fields.Many2many('component', string='Components')

    @api.depends('component_ids.price')
    def _compute_total_price(self):
        for record in self:
            total_price = sum(component.price for component in record.component_ids)
            record.total_price = total_price

    @api.constrains('budget_limit', 'total_price')
    def _check_budget_limit(self):
        for record in self:
            if record.total_price > record.budget_limit:
                raise ValidationError('The total price exceeds the budget limit.')

    @api.model
    def create(self, vals):
        if 'component_ids' in vals:
            self._check_components_compatibility(vals['component_ids'])
        return super(CustomPC, self).create(vals)

    def write(self, vals):
        if 'component_ids' in vals:
            self._check_components_compatibility(vals['component_ids'])
        return super(CustomPC, self).write(vals)

    def _check_components_compatibility(self, component_ids):
        components = self.env['component'].browse(component_ids)
        compatibility_issues = self.env['compatibility.check'].check_components(components)
        if compatibility_issues:
            raise ValidationError('Compatibility issues found: %s' % compatibility_issues)

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_order(self):
        self.write({'state': 'ordered'})
        # Here you would integrate with the sales module to create an order
        # This is a placeholder for the integration logic
        # order = self.env['sale.order'].create_order_from_configuration(self)
        # return order

    def action_draft(self):
        self.write({'state': 'draft'})