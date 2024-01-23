from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestCompatibilityCheck(TransactionCase):

    def setUp(self):
        super(TestCompatibilityCheck, self).setUp()
        self.CompatibilityCheck = self.env['compatibility.check']
        self.Component = self.env['component']
        # Create test components
        self.cpu = self.Component.create({'name': 'Test CPU', 'component_type': 'cpu'})
        self.gpu = self.Component.create({'name': 'Test GPU', 'component_type': 'gpu'})
        self.ram = self.Component.create({'name': 'Test RAM', 'component_type': 'ram'})

    def test_01_component_compatibility(self):
        # Test successful compatibility check
        compatibility = self.CompatibilityCheck.create({
            'cpu_id': self.cpu.id,
            'gpu_id': self.gpu.id,
            'ram_id': self.ram.id
        })
        self.assertTrue(compatibility.check_compatibility(), "Compatibility check should pass for compatible components.")

    def test_02_incompatible_components(self):
        # Test compatibility check with incompatible components
        incompatible_gpu = self.Component.create({'name': 'Incompatible GPU', 'component_type': 'gpu'})
        with self.assertRaises(ValidationError, msg="Should not allow incompatible components."):
            self.CompatibilityCheck.create({
                'cpu_id': self.cpu.id,
                'gpu_id': incompatible_gpu.id,
                'ram_id': self.ram.id
            })

    def test_03_power_requirements(self):
        # Test power requirement checks
        power_hungry_gpu = self.Component.create({'name': 'Power-Hungry GPU', 'component_type': 'gpu', 'power_requirement': 500})
        with self.assertRaises(ValidationError, msg="Should raise an exception for exceeding power requirements."):
            self.CompatibilityCheck.create({
                'cpu_id': self.cpu.id,
                'gpu_id': power_hungry_gpu.id,
                'ram_id': self.ram.id
            })

    def test_04_size_constraints(self):
        # Test size constraint checks
        large_gpu = self.Component.create({'name': 'Large GPU', 'component_type': 'gpu', 'size': 'large'})
        with self.assertRaises(ValidationError, msg="Should raise an exception for size constraints."):
            self.CompatibilityCheck.create({
                'cpu_id': self.cpu.id,
                'gpu_id': large_gpu.id,
                'ram_id': self.ram.id
            })