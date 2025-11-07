from flask import Blueprint, request, jsonify
from models.text_analyzer import TextAnalyzer
import mysql.connector
from mysql.connector import pooling
from datetime import datetime
import traceback

# =====================================================
# Création du Blueprint et du modèle
# =====================================================
plagiat_bp = Blueprint('plagiat', __name__)
analyzer = TextAnalyzer()

# =====================================================
# Configuration base de données avec pool de connexions
# =====================================================
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345678',
    'database': 'black_list_db'
}

db_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **db_config
)

# =====================================================
# Fonction utilitaire : ajouter un utilisateur à la blacklist
# =====================================================
def add_to_blacklist(user_id, similarity_percentage):
    """Ajoute un utilisateur à la table personnes_blacklistees si similarité >= 80%"""
    if not user_id:
        print("user_id invalide, blacklist non ajoutée")
        return

    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO personnes_blacklistees (identifiant, raison, date_ajout)
        VALUES (%s, %s, %s)
        """
        raison = f"Similarité {similarity_percentage:.2f}%"
        date_ajout = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(sql, (user_id, raison, date_ajout))
        conn.commit()
        print(f"✅ Utilisateur {user_id} ajouté à la blacklist ({similarity_percentage:.2f}%)")

    except Exception as e:
        print(f"Erreur ajout blacklist: {e}")
        traceback.print_exc()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# =====================================================
# ROUTE 1 : Vérification de l’état de l’API
# =====================================================
@plagiat_bp.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'OK',
        'message': 'API de détection de plagiat opérationnelle',
        'version': '1.1'
    }), 200

# =====================================================
# ROUTE 2 : Nettoyage de texte
# =====================================================
@plagiat_bp.route('/api/clean-text', methods=['POST'])
def clean_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Le champ "text" est requis', 'success': False}), 400

        text = data['text']
        if not text.strip():
            return jsonify({'error': 'Le texte ne peut pas être vide', 'success': False}), 400

        cleaned = analyzer.processor.clean_text(text)
        return jsonify({'success': True, 'original_text': text, 'cleaned_text': cleaned}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e), 'success': False}), 500

# =====================================================
# ROUTE 3 : Comparaison complète + ajout blacklist
# =====================================================
@plagiat_bp.route('/api/compare', methods=['POST'])
def compare_texts():
    try:
        data = request.get_json()
        if not data or 'text1' not in data or 'text2' not in data:
            return jsonify({'error': 'Les champs "text1" et "text2" sont requis', 'success': False}), 400

        text1 = data['text1']
        text2 = data['text2']
        if not text1.strip() or not text2.strip():
            return jsonify({'error': 'Les textes ne peuvent pas être vides', 'success': False}), 400

        result = analyzer.analyze_similarity(text1, text2)

        # Ajout auto à la blacklist si similaire à 80% ou plus
        user_id = data.get('user_id')
        if user_id and result['similarity_percentage'] >= 80:
            add_to_blacklist(user_id, result['similarity_percentage'])

        return jsonify({
            'success': True,
            'similarity_percentage': result['similarity_percentage'],
            'method_used': result['method_used'],
            'details': result['details']
        }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e), 'success': False}), 500

# =====================================================
# ROUTE 4 : Afficher la blacklist
# =====================================================
@plagiat_bp.route('/api/blacklist', methods=['GET'])
def get_blacklist():
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM personnes_blacklistees ORDER BY date_ajout DESC")
        results = cursor.fetchall()

        return jsonify({'success': True, 'blacklist': results}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e), 'success': False}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
