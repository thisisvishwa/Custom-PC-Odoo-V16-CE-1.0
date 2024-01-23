from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PcConfigurationWizard(models.TransientModel):
    _name = 'pc.configuration.wizard'
    _description = 'Wizard for Configuring Custom PCs'

    custom_pc_id = fields.Many2one('custom.pc', string='Custom PC')
    budget_limit = fields.Float('Budget Limit', default=lambda self: self.env.context.get('budget_limit', 0.0))
    component_ids = fields.Many2many('component', string='Components')

    @api.model
    def default_get(self, fields):
        res = super(PcConfigurationWizard, self).default_get(fields)
        custom_pc_id = self.env.context.get('active_id')
        if custom_pc_id:
            custom_pc = self.env['custom.pc'].browse(custom_pc_id)
            res.update({
                'custom_pc_id': custom_pc_id,
                'component_ids': [(6, 0, custom_pc.component_ids.ids)],
                'budget_limit': custom_pc.budget_limit,
            })
        return res

    def action_confirm(self):
        self.ensure_one()
        if self.budget_limit < sum(self.component_ids.mapped('price')):
            raise ValidationError(self.env['ir.translation']._(BUDGET_EXCEEDED_MSG))
        self.custom_pc_id.write({
            'component_ids': [(6, 0, self.component_ids.ids)],
            'budget_limit': self.budget_limit,
        })
        return {'type': 'ir.actions.act_window_close'}

    def action_check_compatibility(self):
        self.ensure_one()
        compatibility_issues = self.env['compatibility.check'].check_compatibility(self.component_ids)
        if compatibility_issues:
            raise ValidationError(self.env['ir.translation']._(COMPATIBILITY_ISSUE_MSG) + "\n" + "\n".join(compatibility_issues))
        return {
            'name': self.env['ir.translation']._(VALIDATION_SUCCESS_MSG),
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Compatibility Check',
                'message': self.env['ir.translation']._(VALIDATION_SUCCESS_MSG),
                'sticky': False,
            },
        }

    def action_view_components(self):
        self.ensure_one()
        return {
            'name': 'Components',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'component',
            'domain': [('id', 'in', self.component_ids.ids)],
            'context': {'create': False},
        }