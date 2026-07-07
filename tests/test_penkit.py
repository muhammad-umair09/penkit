import unittest
from core.validator import Validator
from modules.hash_generator import generate_hashes

class TestPenKitValidators(unittest.TestCase):
    def test_ipv4_validation(self):
        self.assertTrue(Validator.is_valid_ipv4("192.168.1.1"))
        self.assertFalse(Validator.is_valid_ipv4("999.999.999.999"))

    def test_domain_validation(self):
        self.assertTrue(Validator.is_valid_domain("example.com"))
        self.assertFalse(Validator.is_valid_domain("invalid_domain##"))

    def test_hash_generation(self):
        res = generate_hashes("test")
        self.assertEqual(res["MD5"], "098f6bcd4621d373cade4e832627b4f6")

if __name__ == "__main__":
    unittest.main()