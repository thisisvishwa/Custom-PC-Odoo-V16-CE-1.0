from odoo import http
from odoo.http import request

class CustomPCController(http.Controller):

    @http.route('/custom_pc/configure', type='http', auth='user', website=True)
    def configure_pc(self, **post):
        categories = request.env['product.category'].search([('name', '=', 'Custom PCs')])
        components = request.env['product.template'].search([('categ_id', 'in', categories.ids)])
        return request.render('custom_pc_module.pc_configuration_template', {
            'categories': categories,
            'components': components,
        })

    @http.route('/custom_pc/validate', type='json', auth='user', methods=['POST'], website=True)
    def validate_pc(self, **post):
        PcConfigurationWizard = request.env['pc.configuration.wizard']
        wizard = PcConfigurationWizard.create(post)
        validation_result = wizard.validate_build()
        return validation_result

    @http.route('/custom_pc/price_update', type='json', auth='user', methods=['POST'], website=True)
    def update_component_prices(self, **post):
        components = request.env['component'].search([])
        for component in components:
            component.update_price()
        return {'success': True}

    @http.route('/custom_pc/check_compatibility', type='json', auth='user', methods=['POST'], website=True)
    def check_compatibility(self, **post):
        compatibility_check = request.env['compatibility.check'].create(post)
        check_result = compatibility_check.run_check()
        return check_result

    @http.route('/custom_pc/order', type='http', auth='user', methods=['POST'], website=True)
    def create_order(self, **post):
        order_data = post.get('order_data')
        order = request.env['sale.order'].create(order_data)
        return request.redirect('/my/orders/%s' % order.id)