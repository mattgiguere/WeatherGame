#!/usr/bin/env python
from flask import Flask, jsonify, abort, make_response, request, current_app
from datetime import timedelta
from functools import update_wrapper

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

middleware = Flask(__name__)

questions = [
    {
        'question_id': 1,
        'question': u'What will the temperature be 7 days from now?',
        'question_type': u'Temperature', 
        'location': 'San Francisco, CA'
    },
    {
        'question_id': 2,
        'question': u'How many inches of rain will they get 7 days from now?',
        'question_type': u'Rain', 
        'location': 'Seattle, WA'
    },
    {
        'question_id': 3,
        'question': u'How many inches of snow will they get 7 days from now?',
        'question_type': u'Snowfall', 
        'location': 'Whistler, Canada'
    }
]
@crossdomain(origin='*')

@middleware.route('/api/v0.1/questions', methods = ['GET'])
def get_qs():
	return jsonify({'questions': questions})

@middleware.route('/api/v0.1/questions/<int:in_question_id>', methods = ['GET'])
def get_q(in_question_id):
    question = filter(lambda q: q['question_id'] == in_question_id, questions)
    if len(question) == 0:
        abort(404)
    return jsonify( { 'question': question[0] } )

@middleware.route('/api/v0.1/questions', methods = ['POST'])
def create_response():
	if not request.json or not 'userAnswer' in request.json:
		abort(400)
	response = {
		'userName': request.json['userName'], 
		'dateAnswered': request.json['dateAnswered'], 
		'correctAnswer': request.json['correctAnswer'], 
		'eventDate': request.json['eventDate'],
		'scoreMultiplier': request.json['scoreMultiplier'],
		'ranking': request.json['ranking'],
		'userAnswer': request.json['userAnswer'],
		'answerKey': request.json['answerKey'],
		'gameOpen': request.json['gameOpen'],
		'gameOver': request.json['gameOver'],
		'gameId': request.json['gameId']
	}

@middleware.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

if __name__ == '__main__':
    middleware.run(debug = True)

