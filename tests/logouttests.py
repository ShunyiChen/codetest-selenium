import unittest


class LogoutTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None: print('*** setUpClass')

    def setUp(self) -> None: print('*** setUp')

    def test_1_logout_success(self):
        print('*** test_logout_success')
        self.assertNotEqual(1,2)

    def test_2_logout_success(self):
        print('*** test_logout_failure')
        self.assertGreater(2,1)

    def tearDown(self) -> None: print('*** tearDown')

    @classmethod
    def tearDownClass(cls) -> None: print('*** tearDownClass')