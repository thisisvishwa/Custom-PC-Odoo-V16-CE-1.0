from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestCustomPc(TransactionCase):

    def setUp(self):
        super(TestCustomPc, self).setUp()
        self.CustomPC = self.env['custom.pc']
        self.Component = self.env['component']
        self.CompatibilityCheck = self.env['compatibility_check']

        # Create a test product category for Custom PCs
        self.product_category_custom_pc = self.env['product.category'].create({
            'name': 'Custom PCs',
        })

        # Create test components
        self.cpu_component = self.Component.create({
            'name': 'Test CPU',
            'category': 'CPU',
            'price': 250.00,
            'stock_qty': 10,
        })
        self.gpu_component = self.Component.create({
            'name': 'Test GPU',
            'category': 'GPU',
            'price': 400.00,
            'stock_qty': 5,
        })

    def test_create_custom_pc(self):
        custom_pc = self.CustomPC.create({
            'name': 'Test Custom PC',
            'category_id': self.product_category_custom_pc.id,
            'cpu_id': self.cpu_component.id,
            'gpu_id': self.gpu_component.id,
            'budget': 1000.00,
        })
        self.assertEqual(custom_pc.name, 'Test Custom PC')
        self.assertEqual(custom_pc.category_id, self.product_category_custom_pc)
        self.assertEqual(custom_pc.cpu_id, self.cpu_component)
        self.assertEqual(custom_pc.gpu_id, self.gpu_component)
        self.assertEqual(custom_pc.budget, 1000.00)

    def test_budget_constraint(self):
        with self.assertRaises(ValidationError):
            self.CustomPC.create({
                'name': 'Test Budget Constraint',
                'category_id': self.product_category_custom_pc.id,
                'cpu_id': self.cpu_component.id,
                'gpu_id': self.gpu_component.id,
                'budget': 500.00,  # Budget less than the sum of components' prices
            })

    def test_compatibility_check(self):
        compatibility_issue = self.CompatibilityCheck.create({
            'component_id_1': self.cpu_component.id,
            'component_id_2': self.gpu_component.id,
            'is_compatible': False,
        })
        self.assertFalse(compatibility_issue.is_compatible)

    def test_order_generation(self):
        custom_pc = self.CustomPC.create({
            'name': 'Test Order Generation',
            'category_id': self.product_category_custom_pc.id,
            'cpu_id': self.cpu_component.id,
            'gpu_id': self.gpu_component.id,
            'budget': 1000.00,
        })
        order = custom_pc.action_generate_order()
        self.assertTrue(order)
        self.assertEqual(order.order_line.product_id, custom_pc.product_id)

    def tearDown(self):
        self.cpu_component.unlink()
        self.gpu_component.unlink()
        self.product_category_custom_pc.unlink()
        super(TestCustomPc, self).tearDown()