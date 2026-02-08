import os, sys, datetime, sqlite3, random, glob
from flask import Flask, render_template, request, redirect, url_for, send_file

# --- CONFIGURATION DES CHEMINS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.join(BASE_DIR, '..')
sys.path.append(os.path.join(PARENT_DIR, 'satellite_engine'))

# --- IMPORTS DES MOTEURS ---
try:
    from ndvi_engine import BaolSatEngine
    from script_peche import job as peche_job
    sat_engine = BaolSatEngine()
    print("✅ Moteurs BAOLSAT & PecheurConnect : CHARGÉS")
except ImportError as e:
    print(f"⚠️ ERREUR D'IMPORT : {e}")
    sat_engine, peche_job = None, None

app = Flask(__name__)
# Utilisation d'un chemin absolu pour la base de données sur le serveur
app.config['DATABASE'] = os.path.join(PARENT_DIR, 'baolsat.db')

# --- INITIALISATION AUTOMATIQUE DE LA BASE DE DONNÉES ---
def init_db():
    """Crée les tables et insère des données initiales si nécessaire"""
    print("🛠️ Vérification de la base de données...")
    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        
        # Création de la table chat (Correction de ton erreur sqlite3.OperationalError)
        cursor.execute('''CREATE TABLE IF NOT EXISTS chat 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             user TEXT, 
             text TEXT, 
             time TEXT, 
             is_critical INTEGER)''')
        
        # Création de la table bourse
        cursor.execute('''CREATE TABLE IF NOT EXISTS bourse 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             produit TEXT, 
             prix INTEGER, 
             unite TEXT, 
             tendance TEXT)''')
        
        # Insertion de données de test si la bourse est vide
        cursor.execute("SELECT count(*) FROM bourse")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO bourse (produit, prix, unite, tendance) VALUES ('Arachide', 285, 'kg', 'up')")
            cursor.execute("INSERT INTO bourse (produit, prix, unite, tendance) VALUES ('Riz Local', 425, 'kg', 'down')")
            cursor.execute("INSERT INTO bourse (produit, prix, unite, tendance) VALUES ('Mil', 310, 'kg', 'up')")
            print("📦 Données initiales insérées.")
        
        conn.commit()
    print("✅ Base de données prête.")

# Lancement de l'initialisation au démarrage de l'app
init_db()

# --- LOGIQUE DE DONNÉES ---
def get_live_data():
    geo_config = {
        "Saint-Louis (Riz)": [16.01, -16.48],
        "Dahra (Élevage)": [15.33, -15.48],
        "Kaolack (Bassin)": [14.14, -16.07],
        "Ziguinchor (Sud)": [12.58, -16.27],
        "Pikine (Niayes)": [14.75, -17.39]
    }
    agri_data = []
    for zone, coords in geo_config.items():
        res = sat_engine.get_satellite_insight(zone) if sat_engine else {"vigueur":0.5, "rendement_t_ha":0, "statut":"N/A", "besoin_azote":"N/A", "pluie_7j":0, "conseil":""}
        agri_data.append({
            "zone": zone, "lat": coords[0], "lng": coords[1],
            "ndvi": res["vigueur"], "rendement": res["rendement_t_ha"],
            "azote": res["besoin_azote"], "pluie": res["pluie_7j"], "conseil": res["conseil"]
        })
    return agri_data

# --- ROUTES ---
@app.route('/')
def home():
    agri_data = get_live_data()
    try:
        with sqlite3.connect(app.config['DATABASE']) as conn:
            conn.row_factory = sqlite3.Row
            messages = conn.execute("SELECT * FROM chat ORDER BY id DESC LIMIT 15").fetchall()
            prices = conn.execute("SELECT * FROM bourse").fetchall()
    except Exception as e:
        print(f"❌ Erreur lecture DB : {e}")
        messages, prices = [], []

    return render_template('index.html', 
                           agri_data=agri_data, 
                           prices=prices, 
                           messages=messages,
                           now=datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))

@app.route('/simulate_copernicus', methods=['POST'])
def simulate_copernicus():
    if peche_job:
        peche_job()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
