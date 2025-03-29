from flask import Flask
from flask import render_template
import json
import stalarm

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    # Convert DataFrame to dictionary for Jinja
    df_data = stalarm.df_stock_data.to_dict(orient='records')

    return render_template('index.html', df=df_data, columns=stalarm.df_stock_data.columns)

if __name__ == "__main__":
    app.run()