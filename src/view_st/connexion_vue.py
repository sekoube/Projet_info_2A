import streamlit as st
from service.utilisateur_service import UtilisateurService
from service.evenement_service import EvenementService
from service.inscription_service import InscriptionService
from view_st.page_utilisateur import page_utilisateur
from view_st.page_admin import page_admin

def connexion_terminal(service_utilisateur: UtilisateurService,
                        evenement_service: EvenementService,
                        inscription_service: InscriptionService):
    """
    Interface de connexion Streamlit.
    """
    st.subheader("Connexion")

    email = st.text_input("Email", key="login_email")
    mot_de_passe = st.text_input("Mot de passe", type="password", key="login_pwd")

    if st.button("Se connecter"):
        utilisateur = service_utilisateur.authentifier(email, mot_de_passe)
        if utilisateur:
            st.session_state.utilisateur = utilisateur
            st.success(f"✅ Bienvenue {utilisateur.pseudo} !")
            # Rediriger vers la page adaptée selon le rôle
            if not utilisateur.role:
                st.session_state.page = "utilisateur"
            else:
                st.session_state.page = "admin"
        else:
            st.error("❌ Échec de la connexion. Email ou mot de passe incorrect.")
