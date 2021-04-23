import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_question = questions[start:end]
    return current_question


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response
    '''
    GET requests
    for all available categories.
    '''
    @app.route('/categories')
    def get_all_categories():
        categories = Category.query.all()
        if len(categories) == 0:
            abort(404)
        categories_dict = dict()
        for category in categories:
            categories_dict[category.id] = category.type
        return jsonify({
            'success': True,
            'categories': categories_dict
        }), 200
    '''
    At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at
    the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions')
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        if len(current_questions) == 0:
            abort(404)
        categories = Category.query.all()
        categories_dict = dict()
        for category in categories:
            categories_dict[category.id] = category.type
        return jsonify({
            'success': True,
            'questions': current_questions,
            'totalQuestions': len(Question.query.all()),
            'categories': categories_dict
        }), 200
    '''
    Create an endpoint to DELETE question using a question ID.
    '''
    "donetest"
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            question.delete()
            return jsonify({
                'success': True,
            }), 200
        except:
            abort(422)
    '''
    Create an endpoint to POST a new question,
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        new_question = body.get('question')
        new_answer = body.get('answer')
        new_difficulty = body.get('difficulty')
        new_category = body.get('category')
        if not(new_question and new_category and
               new_answer and new_difficulty):
            abort(422)
        try:
            question = Question(question=new_question, answer=new_answer,
                                category=new_category, difficulty=new_difficulty)               
            question.insert()
            return jsonify({'success': True}), 200
        except:
            abort(422)
    '''
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        data = request.get_json()
        search_key = data.get('searchTerm', None)
        if not search_key:
            abort(404)
        selection = Question.query.filter(
            Question.question.ilike('%{}%'.format(search_key))).all()
        current_questions = paginate_questions(request, selection)
        return jsonify({
            'success': True,
            'questions': current_questions,
            'totalQuestions': len(Question.query.all())
        }), 200

    '''
    Create a GET endpoint to get questions based on category.
    '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        selection = Question.query.filter_by(category=str(category_id)).all()
        if len(selection) == 0:
            abort(404)
        current_questions = paginate_questions(request, selection)
        return jsonify({
            'success': True,
            'questions': current_questions,
            'totalQuestions': len(Question.query.all()),
            'currentCategory': category_id
        }), 200

    '''
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    '''
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            data = request.get_json()
            previous_questions = data.get('previous_questions')
            quiz_category = data.get('quiz_category')
            if quiz_category is None or previous_questions is None:
                abort(422)
            current_questions = None
            if quiz_category['id'] == 0:
                current_questions = Question.query.filter(
                    ~Question.id.in_(previous_questions)).all()
            else:
                current_questions = Question.query.filter_by(
                    category=quiz_category['id']).filter(
                    ~Question.id.in_(previous_questions)).all()
            random_question = current_questions[random.randint(
                0, len(current_questions)-1)] if len(current_questions) > 0 else None
            return jsonify({
                'success': True,
                'question': random_question.format()
            }), 200
        except:
            abort(422)
    '''
    Create error handlers for all expected errors
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app
