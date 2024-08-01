import unittest
from app import app, load_data

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_empty_input(self):
        """Test that an empty input is not accepted."""
        response = self.client.post('/', data={'name': ''})
        self.assertIn(b'Please enter a valid name.', response.data)

    def test_multiple_spaces_input(self):
        """Test that ONLY multiple spaces as input is not accepted."""
        response = self.client.post('/', data={'name': '   '})
        self.assertIn(b'Please enter a valid name.', response.data)

    def test_numbers_in_input(self):
        """Test that numbers in the input are not accepted."""
        response = self.client.post('/', data={'name': '1234'})
        self.assertIn(b'Please enter a valid name.', response.data)

    def test_special_characters_in_input(self):
        """Test that ONLY special characters are not accepted."""
        special_characters = '!@#$%^&*()'
        response = self.client.post('/', data={'name': special_characters})
        self.assertIn(b'Please enter a valid name.', response.data)

    def test_valid_input_with_apostrophe_and_hyphen(self):
        """Test that input with valid alphabets, apostrophe, and hyphen is accepted."""
        response = self.client.post('/', data={'name': "O'Connor"})
        self.assertNotIn(b'Please enter a valid name.', response.data)
        response = self.client.post('/', data={'name': "Jean-Paul"})
        self.assertNotIn(b'Please enter a valid name.', response.data)

    def test_valid_input_with_alphabets(self):
        """Test that input with only alphabets is accepted."""
        response = self.client.post('/', data={'name': 'John'})
        self.assertNotIn(b'Please enter a valid name.', response.data)

class TestDataIngestion(unittest.TestCase):

    def test_load_users(self):
        """Test that loading users.json returns a list."""
        users, content = load_data()
        self.assertIsInstance(users, list)
    
    def test_load_content(self):
        """Test that loading content.json returns a list."""
        users, content = load_data()
        self.assertIsInstance(content, list)

if __name__ == '__main__':
    unittest.main()
