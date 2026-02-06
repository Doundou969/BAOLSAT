🛰️ BAOLSAT 2026 (Ex-PecheurConnect)
Plateforme d'Intelligence Agro-Spatiale basée sur les données Copernicus

BAOLSAT remplace officiellement SunuBlueTech et PecheurConnect. Ce projet utilise la puissance du programme européen Copernicus pour surveiller la santé des cultures en temps réel sur toute l'étendue du territoire sénégalais.

🌍 Notre Mission
Optimiser les rendements agricoles dans le Bassin Arachidier (Diourbel, Kaolack, Fatick) et la Vallée du Fleuve Sénégal en fournissant des indicateurs de précision :

Vigueur Végétale (NDVI) : Détection de la biomasse via Sentinel-2.

Stress Hydrique : Analyse thermique pour optimiser l'irrigation.

Bourse Agricole : Suivi des prix du marché (Arachide, Riz, Oignon) pour les producteurs.

🚀 Technologie
Nous exploitons la constellation de satellites Sentinel-2 via l'API Copernicus Open Access Hub et Google Earth Engine.

Fréquence : Mise à jour tous les 5 jours.

Résolution : 10 mètres par pixel.

📂 Structure du Projet
/app.py : Serveur Flask gérant l'API, la bourse et le système de chat des agents.

/satellite_engine : Algorithmes de traitement NDVI (Moteur PecheurConnect adapté à l'agro).

/templates : Interface PWA mobile-first pour une utilisation hors-ligne sur le terrain.

.github/workflows : Automatisation des rapports quotidiens à 8h (Dakar).

🛠️ Installation & Lancement
Bash
# Cloner le projet
git clone https://github.com/Doundou969/baolsat-2026.git
cd baolsat-2026

# Configurer l'environnement
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt

# Lancer le serveur local
python app.py
