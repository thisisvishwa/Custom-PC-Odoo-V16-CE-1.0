from odoo import models, fields, api

class CompatibilityCheck(models.Model):
    _name = 'compatibility.check'
    _description = 'Compatibility Check for Custom PC Components'

    name = fields.Char(string='Check Name', required=True)
    component_id = fields.Many2one('component', string='Component', required=True)
    compatible_with_ids = fields.Many2many('component', 'compatibility_component_rel', 'check_id', 'compatible_id', string='Compatible Components')
    incompatibility_reason = fields.Text(string='Incompatibility Reason')

    @api.model
    def create_compatibility_check(self, component_id, compatible_with_ids):
        compatibility_check = self.create({
            'component_id': component_id,
            'compatible_with_ids': [(6, 0, compatible_with_ids)],
        })
        return compatibility_check

    @api.onchange('component_id')
    def _onchange_component_id(self):
        if self.component_id:
            self.name = f'Compatibility Check for {self.component_id.name}'

    @api.constrains('component_id', 'compatible_with_ids')
    def _check_compatibility(self):
        for record in self:
            if record.component_id in record.compatible_with_ids:
                raise ValidationError(f"The component {record.component_id.name} cannot be compatible with itself.")

    def check_compatibility(self, component_ids):
        incompatible_components = []
        for component_id in component_ids:
            compatibility_records = self.search([('component_id', '=', component_id)])
            for record in compatibility_records:
                if not set(record.compatible_with_ids.ids).intersection(set(component_ids)):
                    incompatible_components.append({
                        'component_id': component_id,
                        'incompatibility_reason': record.incompatibility_reason or 'Unknown incompatibility.'
                    })
        return incompatible_components
