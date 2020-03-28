from flask import Flask, Response
app = Flask(__name__)

import watchmovies2

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    }
]

@app.after_request # blueprint can also be app~~
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # vid, x = watchmovies2.getVideo('https://watch-movies.pl/movies/upadek-grace/')
    a, b, c = watchmovies2.ListContent('https://watch-movies.pl/release/2020/page/1', 1)
    return app.make_response({'data': a})
    # return Response("<h1>Flask on ZEIT Now</h1><p>You visited: /%s</p>" % (path), mimetype="text/html")

if __name__ == '__main__':
    app.run(debug=True)
