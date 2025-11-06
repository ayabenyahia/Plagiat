🧠 Détection de Plagiat Textuel — Application Web
👥 Équipe de Développement

Groupe :

Benchekchou Imane

Benyahia Aya

Mabrouki Ferdaous

SY El Hadji Bassirou

📄 Description du Projet

Ce projet est une application web de détection de plagiat textuel combinant Frontend moderne (HTML, CSS, JavaScript) et Backend intelligent en Python (Flask).
Elle permet de comparer deux textes et d’en analyser le taux de similarité à l’aide d’algorithmes d’Intelligence Artificielle (IA) et de Traitement du Langage Naturel (NLP) tels que TF-IDF, Cosine Similarity, Jaccard Similarity et Distance de Levenshtein.

L’objectif principal est d’offrir un outil fiable, intuitif et visuel, permettant aux étudiants, enseignants, rédacteurs ou chercheurs de vérifier la présence de plagiat ou de similarité entre deux textes.

⚙️ Fonctionnalités Principales
🔐 Authentification sécurisée

Une page de connexion est désormais intégrée.

Accès protégé par nom d’utilisateur et mot de passe (exemple : admin / 1234).

Redirection automatique vers la page de connexion si l’utilisateur n’est pas authentifié.

Déconnexion possible via un bouton dédié.

🧮 Comparaison intelligente

Calcul automatique du taux de similarité entre deux textes selon plusieurs méthodes :

🔹 Distance de Levenshtein : comparaison caractère par caractère.

🔹 Jaccard Similarity : comparaison d’ensembles de mots.

🔹 Cosine Similarity : mesure vectorielle basée sur la fréquence des mots.

🔹 TF-IDF (IA / NLP) : pondération intelligente des mots pour ignorer les mots courants comme “le”, “la”, “de”.

🎨 Interface moderne et responsive

Design harmonieux basé sur une palette jaune clair et bleu.

Animation fluide et barre de progression colorée (vert → rouge) selon le taux de plagiat.

Interface adaptée à tous les écrans (ordinateur, tablette, mobile).

💬 Diagnostic automatique du niveau de plagiat
Taux de similarité	Interprétation
Moins de 15 %	✅ Pas de plagiat
15 % – 30 %	    🟡 Reformulation probable
30 % – 50 %	    🟠 Suspicion partielle
50 % – 80 %	    🔴 Plagiat probable
Plus de 80 %	⚫ Plagiat confirmé
🧩 Comparaison mot par mot

Mise en évidence visuelle des différences entre les deux textes.

Surlignage dynamique pour repérer les similitudes et variations lexicales.

🧰 Technologies Utilisées
🎨 Frontend

HTML5, CSS3, JavaScript

Page de connexion moderne inspirée des interfaces de réseaux sociaux

Stockage local via localStorage pour la gestion de session

⚙️ Backend

Python / Flask

API REST permettant la communication entre le frontend et les algorithmes de comparaison

🧠 Algorithmes utilisés

Levenshtein Distance

Jaccard Similarity

Cosine Similarity

TF-IDF (Term Frequency – Inverse Document Frequency)
