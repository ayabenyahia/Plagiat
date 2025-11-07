import re
import string

class TextProcessor:
    """
    Classe pour le nettoyage et traitement de texte
    """
    
    def clean_text(self, text):
        """
        Nettoie le texte:
        1. Minuscules
        2. Suppression ponctuation
        3. Suppression espaces multiples
        """
        if not text:
            return ""
        
        # Minuscules
        text = text.lower()
        
        # Suppression ponctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Suppression espaces multiples
        text = re.sub(r'\s+', ' ', text)
        
        # Suppression espaces début/fin
        text = text.strip()
        
        return text
    
    def extract_words(self, text):
        """
        Extrait les mots d'un texte nettoyé
        """
        if not text:
            return []
        
        words = text.split()
        return [word for word in words if len(word) > 0]
    
    def remove_stopwords(self, words, language='fr'):
        """
        Supprime les mots vides (optionnel)
        """
        stopwords_fr = {
            'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'et', 'ou',
            'mais', 'donc', 'or', 'ni', 'car', 'que', 'qui', 'quoi', 'dont',
            'où', 'dans', 'par', 'pour', 'avec', 'sans', 'sur', 'sous',
            'ce', 'cet', 'cette', 'ces', 'mon', 'ton', 'son', 'ma', 'ta', 'sa',
            'mes', 'tes', 'ses', 'notre', 'votre', 'leur', 'nos', 'vos', 'leurs',
            'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles',
            'à', 'au', 'aux', 'est', 'sont', 'être', 'avoir'
        }
        
        return [word for word in words if word not in stopwords_fr]
    
    def get_word_frequency(self, words):
        """
        Calcule la fréquence de chaque mot
        """
        frequency = {}
        for word in words:
            frequency[word] = frequency.get(word, 0) + 1
        return frequency
