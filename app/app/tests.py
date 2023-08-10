"""
Sample tests
"""
from django.test import SimpleTestCase
from app import calc

class CalcTests(SimpleTestCase):
    """Test the calculator functions."""
    def test_add_numbers(self):
        res = calc.add(5,6)
        self.assertEqual(res,11) 
    def test_subtract_numbers(self):
        res = calc.subtract(22, 44)
        self.assertEqual(res, 22);