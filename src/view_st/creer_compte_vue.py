import streamlit as st
from service.utilisateur_service import UtilisateurService

def creer_compte_terminal(service: UtilisateurService):
    """
    Interface Streamlit pour créer un compte utilisateur.
    """
    st.subheader("Création de compte")

    pseudo = st.text_input("Pseudo", key="pseudo")
    nom = st.text_input("Nom", key="nom")
    prenom = st.text_input("Prénom", key="prenom")
    email = st.text_input("Email", key="email")
    mot_de_passe = st.text_input("Mot de passe", type="password", key="mdp")
    role_input = st.radio("Compte admin ?", ("Non", "Oui"), key="role")

    if st.button("Créer le compte"):
        # Vérifications simples
        if not pseudo or not nom or not prenom or not email or not mot_de_passe:
            st.warning("Tous les champs sont obligatoires !")
            return

        role = role_input == "Oui"
        try:
            service.creer_compte(pseudo, nom, prenom, email, mot_de_passe, role)
            st.success("✅ Compte créé avec succès !")
        except Exception as e:
            st.error(f"❌ Erreur lors de la création du compte : {e}")
