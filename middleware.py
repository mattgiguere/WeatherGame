#!/usr/bin/env python
from flask import Flask, jsonify, abort, make_response, request

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
        'question_type': u'Temperature', 
        'location': 'San Francisco, CA'
    },
    {
        'question_id': 3,
        'question': u'How many inches of snow will they get 7 days from now?',
        'question_type': u'Temperature', 
        'location': 'San Francisco, CA'
    }
]

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

