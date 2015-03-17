import unittest

import validate

class TestValidatePackage(unittest.TestCase):

    def setUp(self):
        # fdict = {
        #     'check_name1': function1,
        #     'check_name2': function2,
        #     'check_name3': function3,
        # }

        self.vtor = validate.Validator()

    def test_check_integer(self):
        """
            integer
            integer(min, max)
            integer(min=a)
            integer(max=b)
        """
        self.assertEquals(self.vtor.check('integer', 5), 5)
        self.assertEquals(self.vtor.check('integer(3, 9)', 5), 5)
        self.assertEquals(self.vtor.check('integer(min=1)', 5), 5)
        self.assertEquals(self.vtor.check('integer(max=9)', 5), 5)

        with self.assertRaises(validate.VdtValueTooBigError):
            self.vtor.check('integer(3, 9)', 10)
            self.vtor.check('integer(max=9)', 10)

        with self.assertRaises(validate.VdtValueTooSmallError):
            self.vtor.check('integer(3, 9)', 2)
            self.vtor.check('integer(min=1)', 0)

        with self.assertRaises(validate.VdtTypeError):
            self.vtor.check('integer(3, 9)', '')
            self.vtor.check('integer(3, 9)', null)
            self.vtor.check('integer(3, 9)', {})
            self.vtor.check('integer(3, 9)', [1])

    def test_check_float(self):
        """
            float
            float(min, max)
            float(min=a)
            float(max=b)
        """
        self.assertEquals(self.vtor.check('float', 3.14), 3.14)
        self.assertEquals(self.vtor.check('float(3.1, 9.6)', 3.14), 3.14)
        self.assertEquals(self.vtor.check('float(min=1.2)', 3.14), 3.14)
        self.assertEquals(self.vtor.check('float(max=9.3)', 3.14), 3.14)

        with self.assertRaises(validate.VdtValueTooBigError):
            self.vtor.check('float(3.01, 3.13)', 3.14)
            self.vtor.check('float(max=3.1)', 3.14)

        with self.assertRaises(validate.VdtValueTooSmallError):
            self.vtor.check('float(3.2, 9)', 3.14)
            self.vtor.check('float(min=3.1415)', 3.14)

        with self.assertRaises(validate.VdtTypeError):
            self.vtor.check('float(3, 9)', '')
            self.vtor.check('float(3, 9)', null)
            self.vtor.check('float(3, 9)', {})
            self.vtor.check('float(3, 9)', [3.14])

    def test_check_boolean(self):
        """
            accepted values (case-insensitive)

            True: 1, True, 'true', 'on', 'yes'
            False: 0, False, 'false', 'off', 'no'
        """
        self.assertEquals(self.vtor.check('boolean', True), True)
        self.assertEquals(self.vtor.check('boolean', 'true'), True)
        self.assertEquals(self.vtor.check('boolean', 'TrUE'), True)  # case-insensitive
        self.assertEquals(self.vtor.check('boolean', 'on'), True)
        self.assertEquals(self.vtor.check('boolean', 'yes'), True)
        self.assertEquals(self.vtor.check('boolean', '1'), True)
        self.assertEquals(self.vtor.check('boolean', 1), True)

        self.assertEquals(self.vtor.check('boolean', False), False)
        self.assertEquals(self.vtor.check('boolean', 'false'), False)
        self.assertEquals(self.vtor.check('boolean', 'FalSE'), False)  # case-insensitive
        self.assertEquals(self.vtor.check('boolean', 'off'), False)
        self.assertEquals(self.vtor.check('boolean', 'no'), False)
        self.assertEquals(self.vtor.check('boolean', '0'), False)
        self.assertEquals(self.vtor.check('boolean', 0), False)

        with self.assertRaises(validate.VdtTypeError):
            self.vtor.check('boolean', 3)
            self.vtor.check('boolean', [False])
            self.vtor.check('boolean', ['false'])
            self.vtor.check('boolean', {})
        

if __name__ == '__main__':
    unittest.main()