from flask import Blueprint, request, jsonify
from models.text_analyzer import TextAnalyzer
import mysql.connector
from mysql.connector import pooling
from datetime import datetime
import traceback

# =====================================================
# Initialisation
# =====================================================
plagiat_bp = Blueprint('plagiat', __name__)
analyzer = TextAnalyzer()

# =====================================================
# Configuration base de données (pool de connexions)
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
# Fonction : ajout utilisateur à la blacklist
# =====================================================
def add_to_blacklist(user_id, similarity_percentage):
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
# ROUTE 1 : Health Check
# =====================================================
@plagiat_bp.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'OK',
        'message': 'API de détection de plagiat opérationnelle',
        'version': '2.0'
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
# ROUTE 3 : Extraction de mots
# =====================================================
@plagiat_bp.route('/api/extract-words', methods=['POST'])
def extract_words():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Le champ "text" est requis', 'success': False}), 400

        text = data['text']
        cleaned = analyzer.processor.clean_text(text)
        words = analyzer.processor.extract_words(cleaned)

        return jsonify({
            'success': True,
            'cleaned_text': cleaned,
            'words': words,
            'word_count': len(words)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

# =====================================================
# ROUTE 4 : Similarité Jaccard
# =====================================================
@plagiat_bp.route('/api/jaccard-similarity', methods=['POST'])
def jaccard_similarity():
    try:
        data = request.get_json()
        if not data or 'text1' not in data or 'text2' not in data:
            return jsonify({'error': 'Les champs text1 et text2 sont requis'}), 400

        clean1 = analyzer.processor.clean_text(data['text1'])
        clean2 = analyzer.processor.clean_text(data['text2'])
        words1 = analyzer.processor.extract_words(clean1)
        words2 = analyzer.processor.extract_words(clean2)
        jaccard = analyzer._calculate_jaccard_similarity(words1, words2)

        return jsonify({
            'success': True,
            'method': 'Jaccard',
            'similarity_percentage': round(jaccard * 100, 2)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

# =====================================================
# ROUTE 5 : Similarité Cosinus
# =====================================================
@plagiat_bp.route('/api/cosine-similarity', methods=['POST'])
def cosine_similarity():
    try:
        data = request.get_json()
        if not data or 'text1' not in data or 'text2' not in data:
            return jsonify({'error': 'Les champs text1 et text2 sont requis'}), 400

        clean1 = analyzer.processor.clean_text(data['text1'])
        clean2 = analyzer.processor.clean_text(data['text2'])
        words1 = analyzer.processor.extract_words(clean1)
        words2 = analyzer.processor.extract_words(clean2)
        cosine = analyzer._calculate_cosine_similarity(words1, words2)

        return jsonify({
            'success': True,
            'method': 'Cosine',
            'similarity_percentage': round(cosine * 100, 2)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

# =====================================================
# ROUTE 6 : Mots communs
# =====================================================
@plagiat_bp.route('/api/common-words', methods=['POST'])
def common_words():
    try:
        data = request.get_json()
        if not data or 'text1' not in data or 'text2' not in data:
            return jsonify({'error': 'Les champs text1 et text2 sont requis'}), 400

        words1 = set(analyzer.processor.extract_words(analyzer.processor.clean_text(data['text1'])))
        words2 = set(analyzer.processor.extract_words(analyzer.processor.clean_text(data['text2'])))
        common = sorted(list(words1 & words2))

        return jsonify({'success': True, 'common_words': common, 'count': len(common)}), 200
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

# =====================================================
# ROUTE 7 : Mots uniques
# =====================================================
@plagiat_bp.route('/api/unique-words', methods=['POST'])
def unique_words():
    try:
        data = request.get_json()
        if not data or 'text1' not in data or 'text2' not in data:
            return jsonify({'error': 'Les champs text1 et text2 sont requis'}), 400

        words1 = set(analyzer.processor.extract_words(analyzer.processor.clean_text(data['text1'])))
        words2 = set(analyzer.processor.extract_words(analyzer.processor.clean_text(data['text2'])))
        unique1 = sorted(list(words1 - words2))
        unique2 = sorted(list(words2 - words1))

        return jsonify({
            'success': True,
            'unique_text1': unique1,
            'unique_text2': unique2,
            'count_text1': len(unique1),
            'count_text2': len(unique2)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

# =====================================================
# ROUTE 8 : Comparaison complète + ajout blacklist
# =====================================================
@plagiat_bp.route('/api/compare', methods=['POST'])
def compare_texts():
    try:
        data = request.get_json()
        if not data or 'text1' not in data or 'text2' not in data:
            return jsonify({'error': 'Les champs "text1" et "text2" sont requis', 'success': False}), 400

        text1, text2 = data['text1'], data['text2']
        result = analyzer.analyze_similarity(text1, text2)

        # Ajout automatique à la blacklist
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
# ROUTE 9 : Comparaison avec highlight
# =====================================================
@plagiat_bp.route('/api/compare-with-highlight', methods=['POST'])
def compare_with_highlight():
    try:
        data = request.get_json()
        if not data or 'text1' not in data or 'text2' not in data:
            return jsonify({'error': 'Les champs text1 et text2 sont requis'}), 400

        result = analyzer.analyze_with_differences(data['text1'], data['text2'])

        return jsonify({
            'success': True,
            'similarity_percentage': result['similarity_percentage'],
            'common_words': result['common_words'],
            'unique_text1': result['unique_text1'],
            'unique_text2': result['unique_text2'],
            'details': result['details']
        }), 200
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

# =====================================================
# ROUTE 10 : Afficher la blacklist
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
