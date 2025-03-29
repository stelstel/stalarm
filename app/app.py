from flask import Flask
from flask import render_template
import json
import stalarm

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    users = [ 'Rosalia','Adrianna','Victoria' ] # ///////////////////
    
    # Convert DataFrame to HTML table
    table_html = stalarm.df_stock_data.to_html(classes='table table-striped', index= False, justify='center', border=0, escape=False)

    return render_template('index.html', table=table_html)
if __name__ == "__main__":
    app.run()