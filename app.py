from flask import Flask, render_template, url_for, request, render_template
from modules.image_to_grid import ImageToGrid

# creates a Flask application, named app
app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/solve_search",methods = ["POST"])
def grid_solve():
      user_query = request.get_json('application/json') 
      transformer = ImageToGrid(user_query['img'],user_query['gHeight'],
                                  user_query['gWidth'],user_query['gOutline'],
                                  user_query['search'])
      b64_result = transformer.form_word_grid()
      return b64_result

if __name__ == "__main__":
    app.run()
    
    
    
    
