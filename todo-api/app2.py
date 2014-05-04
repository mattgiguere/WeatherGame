#!/usr/bin/env python
from flask import Flask, jsonify, abort, make_response

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    },
    {
        'id': 3,
        'title': u'AstroML',
        'description': u'Need to debug this routine', 
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks', methods = ['GET'])
def get_tasks():
    return jsonify( { 'tasks': tasks } )

if __name__ == '__main__':
    app.run(debug = True)


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    return task_id
    #task = filter(lambda t: t['id'] == task_id, tasks)
    #if len(task) == 0:
        #abort(404)
        #print(len(task))
    #return jsonify( { 'task': task[0] } )

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)