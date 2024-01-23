from odoo import models, fields, api

class Component(models.Model):
    _name = 'custom.pc.component'
    _description = 'PC Component'

    name = fields.Char(string='Name', required=True)
    component_type = fields.Selection([
        ('cpu', 'CPU'),
        ('gpu', 'GPU'),
        ('ram', 'RAM'),
        ('storage', 'Storage'),
        ('motherboard', 'Motherboard'),
        ('psu', 'Power Supply Unit'),
        ('case', 'Case'),
        ('cooler', 'Cooler'),
        ('other', 'Other')
    ], string='Component Type', required=True, help="Type of the PC component")
    price = fields.Float(string='Price', digits='Product Price', help="Price of the component")
    stock = fields.Integer(string='Stock', help="Stock availability for the component")
    compatibility_info = fields.Text(string='Compatibility Information')
    image = fields.Binary(string='Image', attachment=True, help="Image of the component")
    vendor_id = fields.Many2one('res.partner', string='Vendor', help="Vendor of the component")

    @api.model
    def create(self, vals):
        # Custom logic before creating a component
        component = super(Component, self).create(vals)
        # Custom logic after creating a component
        return component

    def write(self, vals):
        # Custom logic before writing to a component
        result = super(Component, self).write(vals)
        # Custom logic after writing to a component
        return result

    def unlink(self):
        # Custom logic before deleting a component
        result = super(Component, self).unlink()
        # Custom logic after deleting a component
        return result

    @api.onchange('component_type')
    def _onchange_component_type(self):
        # Custom logic when the component type is changed
        pass

    @api.depends('stock')
    def _compute_stock_state(self):
        for record in self:
            # Custom logic to compute stock state
            pass

    @api.model
    def update_component_prices(self):
        # Method to update component prices from external API
        pass

    @api.model
    def check_component_availability(self):
        # Method to check component availability from external API
        pass
