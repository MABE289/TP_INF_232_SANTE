import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ==========================================
# 1. CONFIGURATION VISUELLE : LOOK LUMINEUX & ÉCLATANT
# ==========================================
st.set_page_config(
    page_title="CardioCheck Premium | Interface Santé", 
    page_icon="✨", 
    layout="wide"
)

# Design CSS : Ultra-Lumineux, Tons Pastel et Verre Épuré
st.markdown("""
    <style>
    /* Fond de l'application : Blanc cassé très propre */
    .stApp {
        background-color: #f8faff;
        background-image: radial-gradient(at 0% 0%, rgba(224, 242, 255, 0.5) 0, transparent 50%), 
                          radial-gradient(at 100% 100%, rgba(255, 230, 240, 0.5) 0, transparent 50%);
    }
    
    /* Barre latérale : Bleu Ciel Douceur */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e1e8f0;
    }
    
    /* Titres : Bleu Cobalt Moderne */
    h1, h2, h3 {
        color: #1e3a8a !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }

    /* Style du formulaire : Blanc pur avec ombre douce (Effet Papier) */
    .stForm {
        background-color: #ffffff !important;
        border-radius: 24px !important;
        padding: 40px !important;
        border: 1px solid #f0f4f8 !important;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.02) !important;
    }
    
    /* Bouton d'envoi : Dégradé Énergisant */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border-radius: 16px !important;
        border: none !important;
        height: 55px;
        font-size: 18px !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.3) !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 25px -5px rgba(59, 130, 246, 0.4) !important;
        filter: brightness(1.1);
    }

    /* Métriques : Couleurs vives pour la lumière */
    [data-testid="stMetricValue"] {
        color: #2563eb !important;
        font-weight: 800 !important;
    }
    
    /* Inputs : Bordures douces */
    input, select, .stSlider {
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
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
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=80)
    st.title("CardioCheck")
    st.markdown("<p style='color:#64748b;'>Plateforme Clinique v1.2</p>", unsafe_allow_html=True)
    st.markdown("---")
    choix = st.radio("MENU", ["📋 Saisie Patients", "📊 Analyse Live"])
    st.markdown("---")
    st.success("Système Opérationnel")

if choix == "📋 Saisie Patients":
    st.title("✨ Nouvel Enregistrement")
    st.markdown("Remplissez les constantes vitales ci-dessous pour synchronisation immédiate.")
    
    with st.form("form_medical"):
        col1, col2 = st.columns(2)
        with col1:
            pid = st.text_input("👤 ID Patient", placeholder="ex: PAT-99")
            age = st.number_input("📅 Âge", 1, 110, 35)
        with col2:
            tens = st.slider("💓 Tension (mmHg)", 80, 200, 120)
            chol = st.number_input("🩸 Cholestérol (mg/dL)", 100, 400, 185)
        
        glyc = st.selectbox("🥐 Glycémie", ["Normal", "Élevé", "Critique"])
        
        submit = st.form_submit_button("🚀 ENREGISTRER LE PATIENT")
        
        if submit:
            if pid:
                new_data = {
                    "Date": datetime.now().strftime("%H:%M"),
                    "Patient_ID": pid, "Age": age, 
                    "Tension_Systolique": tens, "Cholesterol": chol, "Glycemie": glyc
                }
                st.session_state.sante_db = pd.concat([st.session_state.sante_db, pd.DataFrame([new_data])], ignore_index=True)
                st.balloons()
                st.success(f"Dossier de {pid} mis à jour.")
            else:
                st.error("L'ID Patient est obligatoire.")

else:
    st.title("📊 Monitoring en Temps Réel")
    
    if st.session_state.sante_db.empty:
        st.info("En attente de données...")
    else:
        df = st.session_state.sante_db
        
        # Cartes de scores lumineuses
        m1, m2, m3 = st.columns(3)
        m1.metric("COHORTE", f"{len(df)} pers.")
        m2.metric("TENSION MOY.", f"{round(df['Tension_Systolique'].mean(),1)}")
        m3.metric("ÂGE MOYEN", f"{round(df['Age'].mean(),1)} ans")
        
        st.markdown("---")
        
        c1, c2 = st.columns(2)
        with c1:
            fig1 = px.histogram(df, x="Tension_Systolique", title="État de la Tension", color_discrete_sequence=['#3b82f6'])
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)
            
        with c2:
            fig2 = px.scatter(df, x="Age", y="Cholesterol", title="Rapport Âge / Lipides", color="Glycemie", color_discrete_sequence=['#3b82f6', '#ef4444', '#f59e0b'])
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig2, use_container_width=True)

        st.dataframe(df, use_container_width=True)