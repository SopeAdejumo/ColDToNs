from flask import Flask, request, render_template
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the frontend directory
frontend_dir = os.path.join(base_dir, '..', 'frontend')

# Create the Flask app instance
# By default, Flask expects the static folder to be at the same level as the templates folder
# We specify the static_folder to be the 'static' directory inside 'frontend_dir'
app = Flask(__name__,
            static_folder=os.path.join(frontend_dir, 'static'),
            template_folder=frontend_dir)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)