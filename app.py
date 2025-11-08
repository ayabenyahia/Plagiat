from flask import Flask, render_template
from flask_cors import CORS
from controllers.plagiat_controller import plagiat_bp

app = Flask(__name__)
CORS(app)

# Enregistre ton blueprint
app.register_blueprint(plagiat_bp)

# Routes principales
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    # Pour tests locaux seulement
    app.run(host="0.0.0.0", port=8000)
