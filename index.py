from flask import Flask, Response
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
    }
]


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.make_response({'tasks': tasks})
    # return Response("<h1>Flask on ZEIT Now</h1><p>You visited: /%s</p>" % (path), mimetype="text/html")

if __name__ == '__main__':
    app.run(debug=True)
