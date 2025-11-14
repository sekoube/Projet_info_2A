import streamlit as st

# Import des services et vues
from service.utilisateur_service import UtilisateurService
from service.evenement_service import EvenementService
from service.inscription_service import InscriptionService
from dao.evenement_dao import EvenementDAO
from dao.inscription_dao import InscriptionDAO
from dao.utilisateur_dao import UtilisateurDAO
from dao.bus_dao import BusDAO
from view_st.connexion_vue import connexion_terminal
from view_st.creer_compte_vue import creer_compte_terminal


# Initialisation des DAO et services
evenement_dao = EvenementDAO()
inscription_dao = InscriptionDAO()
utilisateur_dao = UtilisateurDAO()
bus_dao = BusDAO()

service_utilisateur = UtilisateurService()
evenement_service = EvenementService(
    evenement_dao, inscription_dao, utilisateur_dao, bus_dao
)
inscription_service = InscriptionService()


# --- Streamlit UI ---
st.title("Système de Gestion d'Événements")

menu_option = st.radio(
    "Menu Principal",
    ("Créer un compte", "Connexion", "Quitter")
)

if menu_option == "Créer un compte":
    st.write("📝 Créer un compte")
    # Appeler ta fonction de création, mais remplacer input/print par Streamlit
    creer_compte_terminal(service_utilisateur)

elif menu_option == "Connexion":
    st.write("🔑 Connexion")
    # Appeler la fonction de connexion
    connexion_terminal(service_utilisateur, evenement_service, inscription_service)

elif menu_option == "Quitter":
    st.write("👋 Au revoir !")