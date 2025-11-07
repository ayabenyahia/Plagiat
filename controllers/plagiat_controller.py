from flask import Blueprint, request, jsonify
from models.text_analyzer import TextAnalyzer
import mysql.connector
from datetime import datetime

# Création du Blueprint
plagiat_bp = Blueprint('plagiat', __name__)

# Instance du modèle
analyzer = TextAnalyzer()

# Configuration base de données
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # ton mot de passe MySQL
    'database': 'black_list_db'
}

# ========================================
# Fonction pour ajouter un utilisateur à la blacklist
# ========================================
def add_to_blacklist(user_id, similarity_percentage):
    """
    Ajoute un utilisateur à la table personnes_blacklistees
    si la similarité dépasse 80%
    """
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        sql = """
        INSERT INTO personnes_blacklistees (identifiant, raison, date_ajout)
        VALUES (%s, %s, %s)
        """
        raison = f"Similarité {similarity_percentage:.2f}%"
        date_ajout = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute(sql, (user_id, raison, date_ajout))
        conn.commit()
        
    except Exception as e:
        print(f"Erreur ajout blacklist: {e}")
    finally:
        cursor.close()
        conn.close()

# ========================================
# ROUTE 1 : Health Check
# ========================================
@plagiat_bp.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'OK',
        'message': 'API de détection de plagiat opérationnelle',
        'version': '1.0'
    }), 200

# ========================================
# ROUTE 2 : Nettoyage de texte uniquement
# ========================================
@plagiat_bp.route('/api/clean-text', methods=['POST'])
def clean_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Le champ "text" est requis','success': False}), 400
        
        text = data['text']
        if not text.strip():
            return jsonify({'error': 'Le texte ne peut pas être vide','success': False}), 400
        
        cleaned = analyzer.processor.clean_text(text)
        return jsonify({'success': True,'original_text': text,'cleaned_text': cleaned}), 200
        
    except Exception as e:
        return jsonify({'error': f'Erreur: {str(e)}','success': False}), 500

# ========================================
# ROUTE 8 : Comparaison complète
# ========================================
@plagiat_bp.route('/api/compare', methods=['POST'])
def compare_texts():
    try:
        data = request.get_json()
        if not data or 'text1' not in data or 'text2' not in data:
            return jsonify({'error': 'Les champs "text1" et "text2" sont requis','success': False}), 400
        
        text1 = data['text1']
        text2 = data['text2']
        if not text1.strip() or not text2.strip():
            return jsonify({'error': 'Les textes ne peuvent pas être vides','success': False}), 400
        
        # Analyse complète
        result = analyzer.analyze_similarity(text1, text2)
        
        # Ajout à la blacklist si user_id fourni et similarité >= 80%
        if 'user_id' in data and result['similarity_percentage'] >= 80:
            add_to_blacklist(data['user_id'], result['similarity_percentage'])
        
        return jsonify({
            'success': True,
            'similarity_percentage': result['similarity_percentage'],
            'method_used': result['method_used'],
            'details': result['details']
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erreur: {str(e)}','success': False}), 500

# ========================================
# ROUTE pour consulter la blacklist
# ========================================
@plagiat_bp.route('/api/blacklist', methods=['GET'])
def get_blacklist():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM personnes_blacklistees ORDER BY date_ajout DESC")
        results = cursor.fetchall()
        
        return jsonify({'success': True,'blacklist': results}), 200
        
    except Exception as e:
        return jsonify({'error': f'Erreur: {str(e)}','success': False}), 500
    finally:
        cursor.close()
        conn.close()
