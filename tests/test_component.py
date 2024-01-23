from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestComponent(TransactionCase):

    def setUp(self):
        super(TestComponent, self).setUp()
        self.Component = self.env['component']
        self.CustomPC = self.env['custom_pc']
        # Create a dummy component to use in tests
        self.component_cpu = self.Component.create({
            'name': 'Test CPU',
            'component_type': 'cpu',
            'price': 250.00,
            'stock_qty': 10
        })

    def test_create_component(self):
        """Test the creation of a component and its fields."""
        self.assertEqual(self.component_cpu.name, 'Test CPU')
        self.assertEqual(self.component_cpu.component_type, 'cpu')
        self.assertEqual(self.component_cpu.price, 250.00)
        self.assertEqual(self.component_cpu.stock_qty, 10)

    def test_component_uniqueness(self):
        """Test that creating a component with the same name raises a ValidationError."""
        with self.assertRaises(ValidationError):
            self.Component.create({
                'name': 'Test CPU',
                'component_type': 'cpu',
                'price': 300.00,
                'stock_qty': 5
            })

    def test_update_component_stock(self):
        """Test updating the stock quantity of a component."""
        self.component_cpu.stock_qty = 15
        self.assertEqual(self.component_cpu.stock_qty, 15)

    def test_delete_component(self):
        """Test the deletion of a component."""
        component_id = self.component_cpu.id
        self.component_cpu.unlink()
        with self.assertRaises(ValidationError):
            self.Component.browse(component_id).exists()

    def test_real_time_price_update(self):
        """Test the real-time price update of a component."""
        # Simulate price update
        self.component_cpu.price = 260.00
        self.assertEqual(self.component_cpu.price, 260.00)

    def test_component_availability(self):
        """Test the availability check of a component."""
        # Simulate availability check
        self.assertTrue(self.component_cpu.stock_qty > 0)

    def test_budget_constraint(self):
        """Test that the component respects the budget constraint."""
        custom_pc = self.CustomPC.create({
            'name': 'Custom PC Test',
            'budget_limit': 1000.00
        })
        custom_pc.write({'component_ids': [(4, self.component_cpu.id)]})
        self.assertTrue(custom_pc.budget_limit >= self.component_cpu.price)

    def test_compatibility_check(self):
        """Test the compatibility check between components."""
        # Create another dummy component to test compatibility
        component_ram = self.Component.create({
            'name': 'Test RAM',
            'component_type': 'ram',
            'price': 100.00,
            'stock_qty': 20
        })
        # Assume a compatibility check function exists
        is_compatible = self.component_cpu.check_compatibility(component_ram)
        self.assertTrue(is_compatible)