import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__,instance_relative_config=True)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Contro-Allow-Headers','Content-Type ,Authorization')
    response.headers.add('Access-Contro-Allow-Headers','GET, POST ,PATCH , DELETE ,OPTIONS')
    response.headers.add('Access-Control-Allow-Origin' ,  'http://localhost:3000')
    return response 



  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  #dummy end point for testing 
  @app.route("/hello")
  def get_greeting():
    return jsonify({'message':'Hello, World!'})
  
  
  @app.route('/categories', methods=['GET'])
  def get_categories():
    page = request.args.get('page', 1, type=int)
    start = (page -1) * 10 
    end = start + 10 
    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]

    return jsonify({

      'success ': True ,
      'categories' : formatted_categories[start:end] ,
      'total_categories' : len(formatted_categories)
    })
  

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  
  @app.route('/questions', methods=['GET'])
  def get_questions():
    page = request.args.get('page', 1, type=int)
    start = (page -1) * 10 
    end = start + 10 
    questions = Question.query.all()
    formatted_questions = [question.format() for question in questions]

    return jsonify({

      'success ': True ,
      'questions' : formatted_questions[start:end] ,
      'total_plays' : len(formatted_questions)
    })
 
  
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_specific_questions(question_id):
    page = request.args.get('page', 1, type=int)
    start = (page -1) * 10 
    end = start + 10 
    selected_question=Question.query.filter(Question.id == question_id)
    selected_question.delete()
    questions = Question.query.all()
    formatted_questions = [question.format() for question in questions]
    

    if selected_question is None:
      abort(404)
    
    
    return jsonify ({
        'questions' : formatted_questions[start:end] ,
        'total_plays' : len(formatted_questions),
        'success': True ,
        'deleted' : question_id 
      })
    
  

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods=['post'])
  def create_new_questions():
    page = request.args.get('page', 1, type=int)
    start = (page -1) * 10 
    end = start + 10 
    body = request.get_json()
    new_answer= body.get('answer', None)
    new_category= body.get('category', None)
    new_difficulty= body.get('difficulty', None)
    new_question= body.get('question', None)
    
    question = Question(answer=new_answer, category=new_category , difficulty=new_difficulty ,question=new_question)
    question.insert()
    questions = Question.query.all()
    formatted_questions = [question.format() for question in questions]

    
    
    return jsonify ({
        'questions' : formatted_questions[start:end] ,
        'total_plays' : len(formatted_questions),
        'success': True ,
        'created' : question.id 
      })
    

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST','GET'])
  def get_searched_questions():
    page = request.args.get('page', 1, type=int)
    start = (page -1) * 10 
    end = start + 10 
    #search_term = request.form.get('search_term', ' which ') to search for questions containg word which
    search_term = request.form.get('search_term', ' ')
    searched_question = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
    formatted_questions = [question.format() for question in searched_question]
    

    if searched_question is None:
      abort(404)
    
    
    return jsonify ({
        'questions' : formatted_questions[start:end] ,
        'total_plays' : len(formatted_questions),
        'success': True ,
        
      })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:category_id>', methods=['GET'])
  def get_specific_category(category_id):
    selected_category = Category.query.filter(Category.id == category_id).one_or_none()
    selected_questions = Question.query.filter(Question.category == category_id)
    formatted_questions = [question.format() for question in selected_questions]

    if selected_category is None :
      abort(404)
    else:


     return jsonify({

      'success ': True ,
      'category' : formatted_questions,
      'total_plays' : len(formatted_questions)
      
     })
  




  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404

  @app.errorhandler(422)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "Unprocessable Entity"
        }), 422


  @app.errorhandler(405)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 405,
        "message": "Method not allowed"
        }), 405



        
  

  return app

    