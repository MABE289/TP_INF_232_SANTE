import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ==========================================
# 1. CONFIGURATION VISUELLE : ORANGE GÉOMÉTRIQUE & MATÉRIEL
# ==========================================
st.set_page_config(
    page_title="CardioPanel Elite | Diagnostic Clair", 
    page_icon="🩺", 
    layout="wide"
)

# Design CSS : Orange Brûlé + Motifs Cubes + CORRECTIONS VISIBILITÉ
st.markdown("""
    <style>
    /* Fond Orange avec motifs géométriques */
    .stApp {
        background-color: #d35400;
        background-image: url("https://www.transparenttextures.com/patterns/cubes.png");
        background-attachment: fixed;
    }
    
    /* Barre latérale Bleu Marine */
    [data-testid="stSidebar"] {
        background-color: #001f3f !important;
        border-right: 3px solid #ff0000;
    }
    
    /* Titres avec lueur blanche pour ressortir */
    h1, h2 {
        color: white !important;
        text-shadow: 0px 4px 10px rgba(0,0,0,0.5);
    }

    /* Cartes de saisie : Fond CLAIR pour lisibilité */
    .stForm {
        background-color: rgba(255, 255, 255, 0.98) !important;
        border-radius: 25px !important;
        border-left: 10px solid #001f3f !important;
        padding: 40px !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4) !important;
    }
    
    /* Bouton Rouge Vif */
    .stButton>button {
        background: linear-gradient(90deg, #ff0000 0%, #cc0000 100%) !important;
        color: white !important;
        border-radius: 15px !important;
        height: 60px;
        font-size: 22px !important;
        font-weight: 900 !important;
    }
    
    /* --- NOUVEAUX STYLES POUR VISIBILITÉ ANALYSE --- */
    
    /* 1. Forcer le fond BLANC pour les zones de graphiques */
    div[class*="stPlotlyChart"] {
        background-color: white !important;
        padding: 15px !important;
        border-radius: 15px !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3) !important;
    }

    /* 2. Style Métriques blanches */
    [data-testid="stMetricBlock"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px;
        padding: 15px;
    }
    [data-testid="stMetricLabel"] { color: white !important; }
    [data-testid="stMetricValue"] { color: white !important; font-weight: bold; }

    /* 3. Forcer le tableau en BLANC et texte NOIR */
    div[data-testid="stTable"] table {
        background-color: white !important;
        border-radius: 15px;
    }
    div[data-testid="stTable"] td, div[data-testid="stTable"] th {
        color: black !important;
        border: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. LOGIQUE DE DONNÉES
# ==========================================
if 'sante_db' not in st.session_state:
    st.session_state.sante_db = pd.DataFrame(columns=[
        "Date", "Patient_ID", "Age", "Tension_Systolique", "Cholesterol", "Glycemie"
    ])

# ==========================================
# 3. INTERFACE UTILISATEUR
# ==========================================

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/822/822118.png", width=120)
    st.markdown("<h2 style='color:white; text-align:center;'>CARDIO ELITE</h2>", unsafe_allow_html=True)
    st.markdown("---")
    choix = st.radio("MODULE", ["📋 SAISIE CLINIQUE", "📊 ANALYSE VISIBLE"])
    st.markdown("---")
    st.success("Système Opérationnel")

if choix == "📋 SAISIE CLINIQUE":
    # Partie Saisie (inchangée car déjà lisible sur fond blanc)
    c_titre, c_materiel = st.columns([0.7, 0.3])
    with c_titre:
        st.title("🩺 Unité de Mesures Vitales")
    with c_materiel:
        st.image("https://cdn-icons-png.flaticon.com/512/1040/1040237.png", width=150)

    with st.form("form_ultra"):
        col_a, col_b = st.columns(2)
        with col_a:
            pid = st.text_input("🆔 ID PATIENT", placeholder="PAT-XXXX")
            tens = st.slider("💓 TENSION (mmHg)", 80, 200, 120)
        with col_b:
            age = st.number_input("📅 ÂGE ACTUEL", 1, 105, 40)
            chol = st.number_input("🩸 CHOLESTÉROL (mg/dL)", 100, 450, 190)
        
        glyc = st.selectbox("🍏 GLYCÉMIE", ["Normal", "Élevé", "Critique"])
        
        # Le gros bouton Rouge
        submit = st.form_submit_button("🔥 SYNCHRONISER DONNÉES")
        
        if submit:
            if pid:
                new_entry = {
                    "Date": datetime.now().strftime("%Y-%m-%d"),
                    "Patient_ID": pid, "Age": age, 
                    "Tension_Systolique": tens, "Cholesterol": chol, "Glycemie": glyc
                }
                st.session_state.sante_db = pd.concat([st.session_state.sante_db, pd.DataFrame([new_entry])], ignore_index=True)
                st.balloons()
                st.success(f"Dossier de {pid} archivé.")
            else:
                st.error("Identifiant obligatoire.")

else:
    st.title("📊 Centre d'Analyse Experte (Corrigé)")
    
    if st.session_state.sante_db.empty:
        st.info("💡 En attente de données patient...")
    else:
        df = st.session_state.sante_db
        
        # Métriques avec colonnes
        m1, m2, m3 = st.columns(3)
        m1.metric("COHORTE", f"{len(df)}")
        m2.metric("TENSION MOY.", f"{round(df['Tension_Systolique'].mean(),1)}")
        m3.metric("CHOL. MOY.", f"{round(df['Cholesterol'].mean(),1)}")
        
        st.markdown("---")
        
        # Graphiques : Forcer le fond en clair
        ca, cb = st.columns(2)
        
        with ca:
            # Graphique : fond CLAIR forcé
            fig1 = px.histogram(df, x="Tension_Systolique", 
                                title="Distribution de la Tension Artérielle", 
                                color_discrete_sequence=['#ff0000']) # Rouge vif pour les barres
            # Paramètres Plotly : Texte NOIR sur fond BLANC
            fig1.update_layout(paper_bgcolor='white', plot_bgcolor='white', font_color="black")
            st.plotly_chart(fig1, use_container_width=True)
            
        with cb:
            # Graphique : fond CLAIR forcé
            fig2 = px.scatter(df, x="Age", y="Cholesterol", 
                              title="Corrélation Âge vs Cholestérol", 
                              color="Glycemie", # Couleur par glycémie
                              color_discrete_sequence=['#ff0000', '#001f3f', '#f1c40f']) # Rouge, Marine, Jaune
            # Paramètres Plotly : Texte NOIR sur fond BLANC
            fig2.update_layout(paper_bgcolor='white', plot_bgcolor='white', font_color="black")
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")
        # Forcer le tableau brut en CLAIR
        st.markdown("### 📋 Registre Médical Brut")
        st.table(df)