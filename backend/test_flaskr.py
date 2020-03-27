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
        #self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path ='postgresql://postgres:password@localhost:5432/trivia_test'
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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    #testing getting all categories 
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))
    
    
    #Testing getting all questions
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    '''
    def test_get_questions_by_category(self):
        category_id = 1
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    
    def test_get_questions_by_category_fail(self):
        category_id = 0
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
        
    
    
    def test_delete_question(self):
        questions_id = 1
        res = self.client().delete(f'/questions/{questions_id}')
        data =json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
    
    
    def test_delete_questions_fail(self):
        res = self.client().delete('/questions')
        data =json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'],False)


        
       
    
    #Testing adding a new question 
    def test_add_questions(self):
        res = self.client().post('/questions',
        json={'question': 'fake question',
              'answer': 'fake answer',
              'category': '1',
              'difficulty': '1'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
    '''
    def test_add_question_fail(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
    



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()