import os
from plistlib import load
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from dotenv import load_dotenv

# initialize the environment variables
load_dotenv()
dbpassword = os.getenv('DBPASSWORD')
dbusername = os.getenv('DBUSERNAME')


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}"\
            .format(dbusername, dbusername, 'localhost:5432',
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

    # test for GET `/questions`
    def test_wrong_question_page(self):
        """This tests for wrong page variables"""

        res = self.client().get('/questions?page=8')

        self.assertEqual(res.status_code, 416)

    def test_right_question_page(self):
        """This tests for right page variables"""

        res = self.client().get('/questions?page=1')

        self.assertEqual(res.status_code, 200)

    # test for DELETE `/questions/${id}`
    def test_delete_correct_question(self):
        """Test if API can delete question"""

        # try looping true until existing `id` is hit
        i = 0                           # Starting id or index
        while True:
            try:
                res = self.client().delete(f'/questions/{i}')
                assert res.status_code == 200
                break
            except Exception:
                i += 1

        self.assertEqual(res.status_code, 200)

    def test_delete_wrong_question(self):
        """Test if API can handle wrong id for question to be deleted"""

        res = self.client().delete('/questions/200')

        self.assertEqual(res.status_code, 404)

    # test for creation POST `/questions`
    def test_right_question_creation(self):

        """This tests for when all the variables needed for
            question creation is supplied"""

        json = {'question': 'just another test question',
                'answer': 'just another test answers',
                'difficulty': 1,
                'category': 4}

        res = self.client().post('/questions', json=json)

        self.assertEqual(res.status_code, 200)

    def test_wrong_question_creation(self):

        """This tests for when some or all the variables needed
           are not supplied"""

        json = {'question': 'just another test question',
                'answer': 'just another test answers',
                'difficulty': 1}

        res = self.client().post('/questions', json=json)

        self.assertEqual(res.status_code, 400)

    # test for POST /search_questions
    def test_right_search_question(self):

        """This tests for right search query"""

        json = {'searchTerm': 'what'}

        res = self.client().post('/search_questions', json=json)

        self.assertEqual(res.status_code, 200)

    def test_wrong_search_question(self):

        """This tests for wrong search query"""

        json = {'searchTerm': '999'}

        res = self.client().post('/search_questions', json=json)

        self.assertEqual(res.status_code, 404)

    # test for GET /categories/${id}/questions
    def test_right_cate_id_questions(self):

        """This test right id for getting questions
           by category"""

        res = self.client().get('/categories/3/questions')

        self.assertEqual(res.status_code, 200)

    def test_wrong_cate_id_questions(self):

        """This test wrong id for getting questions
            by category"""

        res = self.client().get('/categories/300/questions')

        self.assertEqual(res.status_code, 404)

    # test for POST `/quizzes`
    def test_for_right_cate_id_quizzes(self):

        """This test for right category id for quizzes used"""

        json = {
                'previous_questions': [],
                'quiz_category': {'id': 4}}

        res = self.client().post('/quizzes', json=json)

        self.assertEqual(res.status_code, 200)

    def test_for_wrong_cate_id_quizzes(self):

        """This test for wrong category id for quizzes used"""

        json = {
                'previous_questions': [],
                'quiz_category': {'id': 4000}}

        res = self.client().post('/quizzes', json=json)

        self.assertEqual(res.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
