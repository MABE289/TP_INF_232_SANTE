import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ==========================================
# 1. CONFIGURATION VISUELLE ET MÉDICALE
# ==========================================
st.set_page_config(
    page_title="Hôpital Central - CardioPanel", 
    page_icon="🩺", 
    layout="wide"
)

# Design CSS pour transformer l'apparence (plus de couleurs, fond médical)
st.markdown("""
    <style>
    /* Fond de l'application avec un motif médical léger */
    .stApp {
        background-color: #eef2f5;
        background-image: url("https://www.transparenttextures.com/patterns/white-diamond-dark.png");
    }
    
    /* Barre latérale colorée en bleu médical */
    [data-testid="stSidebar"] {
        background-color: #1a5276;
        color: white;
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p {
        color: #ecf0f1;
    }
    
    /* Titres principaux en bleu foncé */
    h1, h2, h3 {
        color: #154360;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
    }
    
    /* Style des cartes de saisie (Formulaire) */
    .stForm {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #3498db;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Style du bouton d'envoi (Rouge Cardio) */
    .stButton>button {
        background-color: #c0392b;
        color: white;
        border-radius: 20px;
        border: none;
        width: 100%;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #e74c3c;
        transform: scale(1.02);
    }
    
    /* Métriques du tableau de bord (Plus colorées) */
    [data-testid="stMetricValue"] {
        color: #27ae60;
        font-size: 40px;
    }
    [data-testid="stMetricLabel"] {
        color: #7f8c8d;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. LOGIQUE DE DONNÉES (Inchangée)
# ==========================================
if 'sante_db' not in st.session_state:
    st.session_state.sante_db = pd.DataFrame(columns=[
        "Date", "Patient_ID", "Age", "Tension_Systolique", "Cholesterol", "Glycemie"
    ])

# ==========================================
# 3. INTERFACES VISUELLES AMÉLIORÉES
# ==========================================

# --- BARRE LATÉRALE ---
with st.sidebar:
    # Image décorative médicale
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=80)
    st.title("CardioPanel Pro")
    st.markdown("---")
    
    # Séparateur visuel pour le menu
    st.markdown("### 🖥️ NAVIGATION")
    choix = st.radio("", ["📋 Saisie Constantes", "📊 Tableau de Bord"])
    
    st.markdown("---")
    st.markdown("**Unité de Cardiologie**")
    st.caption("Dr. [Votre Nom]")

# --- PAGE 1 : COLLECTE ---
if choix == "📋 Saisie Constantes":
    # En-tête avec titre et image d'outil
    col_titre, col_icon = st.columns([0.8, 0.2])
    with col_titre:
        st.title("Unité de Suivi Cardiovasculaire")
        st.subheader("Nouvelle Fiche de Constantes Patient")
    with col_icon:
        st.image("https://cdn-icons-png.flaticon.com/512/1040/1040237.png", width=100) # Icône Stéthoscope

    st.markdown("---")
    
    with st.form("form_sante"):
        st.markdown("### 🩺 Identification & Paramètres")
        col1, col2 = st.columns(2)
        with col1:
            patient_id = st.text_input("📝 Code Patient (Anonymisé)", placeholder="ex: PAT-XYZ")
            age = st.number_input("📅 Âge", min_value=1, max_value=120, value=30, help="Âge au moment de la visite")
        with col2:
            st.image("https://cdn-icons-png.flaticon.com/512/3063/3063201.png", width=40) # Icône Tension
            tension = st.slider("💓 Tension Systolique (mmHg)", 80, 200, 120, help="Pression maximale lors de la contraction")
            st.image("https://cdn-icons-png.flaticon.com/512/4334/4334130.png", width=40) # Icône Sang
            chol = st.number_input("🩸 Taux de Cholestérol (mg/dL)", 100, 400, 190)
        
        st.markdown("---")
        glycemie = st.selectbox("🥐 Niveau de Glycémie à jeun", ["Normal", "Élevé", "Critique"])
        
        submit = st.form_submit_button("🩺 ENREGISTRER DANS LE DOSSIER MÉDICAL")

        if submit:
            if patient_id == "":
                st.error("⚠️ Veuillez entrer un Code Patient.")
            else:
                nouvelle_entree = {
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Patient_ID": patient_id,
                    "Age": age,
                    "Tension_Systolique": tension,
                    "Cholesterol": chol,
                    "Glycemie": glycemie
                }
                st.session_state.sante_db = pd.concat([st.session_state.sante_db, pd.DataFrame([nouvelle_entree])], ignore_index=True)
                st.balloons() # Petite animation festive
                st.success(f"✅ Données du patient {patient_id} enregistrées avec succès.")

# --- PAGE 2 : ANALYSE ---
else:
    # En-tête avec titre et image d'outil
    col_titre, col_icon = st.columns([0.8, 0.2])
    with col_titre:
        st.title("Tableau de Bord Analytique")
        st.subheader("Vue d'ensemble de la cohorte patient")
    with col_icon:
        st.image("https://cdn-icons-png.flaticon.com/512/2785/2785239.png", width=100) # Icône Graphique Médical

    st.markdown("---")
    
    if st.session_state.sante_db.empty:
        st.info("💡 Le dossier médical est vide. Utilisez l'onglet 'Saisie Constantes' pour ajouter des patients.")
        st.image("https://cdn-icons-png.flaticon.com/512/2900/2900293.png", width=300) # Image d'attente
        st.stop()

    df = st.session_state.sante_db
    
    # Section Métriques Clés avec cartes colorées
    st.markdown("### 🏥 Indicateurs Clés de l'Unité")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.image("https://cdn-icons-png.flaticon.com/512/1430/1430453.png", width=50) # Icône Cohorte
        st.metric("Total Patients", f"{len(df)} pers.")
    with m2:
        st.image("https://cdn-icons-png.flaticon.com/512/3022/3022212.png", width=50) # Icône Tension Cardio
        st.metric("Tension Moyenne", f"{round(df['Tension_Systolique'].mean(), 1)} mmHg")
    with m3:
        st.image("https://cdn-icons-png.flaticon.com/512/1077/1077114.png", width=50) # Icône Groupe
        st.metric("Âge Moyen", f"{round(df['Age'].mean(), 1)} ans")

    st.markdown("---")

    # Section Visualisations avec styles colorés
    st.markdown("### 📊 Analyses de Distribution")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("**Distribution de la Tension Artérielle**")
        # Histogramme Rouge Cardio
        fig_hist = px.histogram(df, x="Tension_Systolique", nbins=15, color_discrete_sequence=['#c0392b'])
        fig_hist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)') # Fond transparent
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_b:
        st.markdown("**Tendance : Âge vs Cholestérol**")
        # Scatter plot avec ligne de tendance Bleue
        fig_scatter = px.scatter(df, x="Age", y="Cholesterol", trendline="ols", color_discrete_sequence=['#1a5276'])
        fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)') # Fond transparent
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Affichage de la base de données brute (plus discret)
    with st.expander("👁️ Voir le registre médical brut"):
        st.dataframe(df, use_container_width=True)