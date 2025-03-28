from flask import Flask
from flask import render_template
import json

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    users = [ 'Rosalia','Adrianna','Victoria' ]
    return render_template('index.html', title='Welcome', members=users)

# @app.route("/get_data")
# def getdata():
#     data = {
#         'name' : 'My Name',
#         'url' : 'My URL'
#     }
#     return json.dumps(data)

if __name__ == "__main__":
    app.run()