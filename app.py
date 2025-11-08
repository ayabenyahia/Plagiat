from flask import Flask, render_template
from flask_cors import CORS
from controllers.plagiat_controller import plagiat_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(plagiat_bp)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

# Nouvelle route pour index
@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
