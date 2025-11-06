from flask import Flask, jsonify, render_template
from flask_cors import CORS
from controllers.plagiat_controller import plagiat_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(plagiat_bp)

@app.route('/')
def home():
    return render_template('index.html')  # renvoie le fichier HTML

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
