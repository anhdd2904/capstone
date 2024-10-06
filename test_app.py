import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Book, Author

class BookstoreTestCase(unittest.TestCase):
    """This class represents the bookstore test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.getenv('DATABASE_TEST_URL')
        setup_db(self.app, self.database_path)

        self.new_book = {
            'title': 'Test Book',
            'publish_date': '2023-10-01'
        }

        self.new_author = {
            'name': 'Test Author',
            'age': 35,
            'gender': 'M',
            'book_id': 1
        }

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_books(self):
        """Test getting all books"""
        res = self.client().get('/books', headers=self.get_auth_headers('view:books'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['books']))

    def test_get_authors(self):
        """Test getting all authors"""
        res = self.client().get('/authors', headers=self.get_auth_headers('view:authors'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['authors']))

    def test_create_book(self):
        """Test creating a new book"""
        res = self.client().post('/books', json=self.new_book, headers=self.get_auth_headers('post:books'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_create_author(self):
        """Test creating a new author"""
        res = self.client().post('/authors', json=self.new_author, headers=self.get_auth_headers('post:authors'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_404_if_book_does_not_exist(self):
        """Test if book does not exist for update"""
        res = self.client().patch('/books/1000', json={'title': 'New Title'}, headers=self.get_auth_headers('update:books'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_book(self):
        """Test deleting a book"""
        # First create a book to delete
        self.client().post('/books', json=self.new_book, headers=self.get_auth_headers('post:books'))

        res = self.client().delete('/books/1', headers=self.get_auth_headers('delete:books'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def get_auth_headers(self, permission):
        """Helper method to get headers for requests"""
        token = 'YOUR_JWT_TOKEN'
        return {'Authorization': f'Bearer {token}'}

# Make the tests executable
if __name__ == "__main__":
    unittest.main()
