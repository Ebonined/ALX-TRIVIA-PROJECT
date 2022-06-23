import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}"\
            .format('student', 'student', 'localhost:5432',
                    self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_delete_correct_question(self):
        """Test if API can delete question"""
        res = self.client().delete('/questions/18')

        self.assertEqual(res.status_code, 200)

    def test_delete_wrong_question(self):
        """Test if API can handle wrong id for question to be deleted"""

        res = self.client().delete('/questions/200')

        self.assertEqual(res.status_code, 404)

    def test_wrong_question_page(self):
        """This tests for wrong page variables"""

        res = self.client().get('/questions?page=8')

        self.assertEqual(res.status_code, 416)

    def test_right_question_page(self):
        """This tests for right page variables"""

        res = self.client().get('/questions?page=1')

        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
