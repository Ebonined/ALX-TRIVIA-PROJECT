import os
import random
from xmlrpc.client import Boolean

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import Category, Question, setup_db


QUESTIONS_PER_PAGE = 10


# Function to convert categories to dictionary object for frontend
def categories_to_dict(categories):
    categories_dict = {}
    for item in categories:
        formatted = item.format()
        categories_dict[formatted['id']] = formatted['type']

    return categories_dict


# Functions to check for ids
def check_id(Model, id) -> Boolean:
    model_ids = Model.query.with_entities(Model.id).all()
    ids = [model_id.id for model_id in model_ids]
    print(ids)

    return id in ids


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r'/': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')

        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            categories_dict = categories_to_dict(categories)

            return jsonify({
                'success': True,
                'categories': categories_dict
            })
        except Exception:
            abort(422)

    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        # Getting questions from trivia database
        questions = Question.query.order_by(Question.id).all()
        questions_formatted = [question.format() for question in questions]

        if start > len(questions_formatted):
            abort(416)

        try:
            # Getting all Categories from database
            categories = Category.query.order_by(Category.id).all()
            categories_dict = categories_to_dict(categories)

            # state current category
            current_category = categories_dict[questions[0].category]

            return jsonify({
                'success': True,
                'questions': questions_formatted[start:end],
                'totalQuestions': len(questions_formatted),
                'categories': categories_dict,
                'currentCategory': current_category
            })
        except Exception:
            abort(422)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        question = Question.query.filter_by(id=question_id).one_or_none()
        if question is None:
            abort(404)
        try:
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question.format(),
                'total_questions': len(Question.query.all())
            })
        except Exception:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()

        question = data.get('question', None)
        answer = data.get('answer', None)
        difficulty = data.get('difficulty', None)
        category = data.get('category', None)

        quest_var_count = len(list(filter(lambda x: x == '' or x is None,
                                          [question, answer,
                                           difficulty, category])))
        if quest_var_count > 0:
            abort(400)
        try:
            # Creating new question based on request
            question = Question(question=question, answer=answer,
                                category=category, difficulty=difficulty)
            question.insert()

            return jsonify({
                "question": data.get('question', None),
                "answer": data.get('answer', None),
                "difficulty": data.get('difficulty', None),
                "category": data.get('category', None)
            })
        except Exception:
            abort(422)

    @app.route('/search_questions', methods=['POST'])
    def just_search():

        search_string = request.get_json()['searchTerm']

        questions = Question.query.filter(Question.question.
                                          ilike(f'%{search_string}%'))
        questions_formatted = [question.format() for question in questions]

        if questions_formatted:
            current_category = questions_formatted[-1]['category']
        else:
            current_category = 'All'
            abort(404)

        return jsonify({
            'success': True,
            'questions': questions_formatted,
            'totalQuestions': len(questions_formatted),
            'currentCategory': current_category
        })

    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def get_by_categories(id):

        # check if id for the categories exists
        if not check_id(Category, id):
            abort(404)

        try:
            questions = Question.query.filter_by(category=id).\
                                                 order_by(Question.id)
            questions_formatted = [question.format() for question in questions]

            if questions_formatted:
                current_category = questions_formatted[-1]['category']
            else:
                current_category = 'All'

            return jsonify({
                'success': True,
                'questions': questions_formatted,
                'totalQuestions': len(questions_formatted),
                'currentCategory': current_category

            })
        except Exception:
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def get_random_question():
        body = request.get_json()
        previous_questions = body['previous_questions']
        quiz_category = body['quiz_category']

        # Get all valid category id in database
        cate_id = Category.query.with_entities(Category.id).all()
        cate_id_list = [cate.id for cate in cate_id]

        def get_question_by_id(Question, id):
            return Question.query.filter_by(id=id).one_or_none()

        # get id of all questions separately
        category_id = quiz_category['id']
        if category_id == 0:
            ids = Question.query.with_entities(Question.id).\
                                    order_by(Question.id).all()
        else:
            ids = Question.query.with_entities(Question.id).\
                                    filter_by(category=category_id).\
                                    order_by(Question.id).all()
        print(cate_id_list)
        if category_id not in cate_id_list:
            abort(404)
        else:
            ids_list = [val.id for val in ids]

        if not previous_questions:
            random.shuffle(ids_list)
            random_index = ids_list[0]
            question = get_question_by_id(Question, random_index).format()
        else:
            # remove all questions already asked
            for asked_q in previous_questions:
                index = ids_list.index(asked_q)
                ids_list.pop(index)
            try:
                random.shuffle(ids_list)
                random_index = ids_list[0]
                question = get_question_by_id(Question, random_index).format()
            except IndexError:
                question = None

        return jsonify({
            'success': True,
            'question': question
        })

    @app.errorhandler(404)
    def error_not_found(error):
        return jsonify({
            'success': False,
            'message': 'resource not found',
            'error': 404
        }), 404

    @app.errorhandler(416)
    def error_range_not_found(error):
        return jsonify({
            'success': False,
            'message': error.name,
            'error': 416
        }), 416

    @app.errorhandler(422)
    def error_unproccessed(error):
        return jsonify({
            'success': False,
            'message': error.name,
            'error': 422
        }), 422

    @app.errorhandler(400)
    def error_bad_request(error):
        return jsonify({
            'success': False,
            'message': error.name,
            'error': 400
        }), 400

    @app.errorhandler(500)
    def error_bad_response(error):
        return jsonify({
            'success': False,
            'message': error.name,
            'error': 500
        }), 500

    return app
