from business_object.utilisateur import Utilisateur
from service.utilisateur_service import UtilisateurService
from service.evenement_service import EvenementService
from service.inscription_service import InscriptionService
from dao.evenement_dao import EvenementDAO
from dao.inscription_dao import InscriptionDAO
from dao.utilisateur_dao import UtilisateurDAO
from dao.bus_dao import BusDAO

# --- Initialisation des DAO et services ---
evenement_dao = EvenementDAO()
inscription_dao = InscriptionDAO()
utilisateur_dao = UtilisateurDAO()
bus_dao = BusDAO()

service_utilisateur = UtilisateurService()
evenement_service = EvenementService(evenement_dao, inscription_dao, utilisateur_dao, bus_dao)
inscription_service = InscriptionService()

# --- Gestion de l'état de session ---
if "page" not in st.session_state:
    st.session_state.page = "menu"
if "utilisateur" not in st.session_state:
    st.session_state.utilisateur = None

# --- Fonctions Streamlit équivalentes aux menus ---
def creer_compte():
    st.subheader("Créer un compte")
    pseudo = st.text_input("Pseudo")
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    email = st.text_input("Email")
    mot_de_passe = st.text_input("Mot de passe", type="password")
    role_input = st.radio("Compte admin ?", ("Non", "Oui"))

    if st.button("Créer le compte"):
        role = role_input == "Oui"
        try:
            service_utilisateur.creer_compte(pseudo, nom, prenom, email, mot_de_passe, role)
            st.success("✅ Compte créé avec succès !")
        except Exception as e:
            st.error(f"❌ Erreur lors de la création du compte : {e}")

def connexion():
    st.subheader("Connexion")
    email = st.text_input("Email", key="login_email")
    mot_de_passe = st.text_input("Mot de passe", type="password", key="login_pwd")

    if st.button("Se connecter"):
        utilisateur = service_utilisateur.authentifier(email, mot_de_passe)
        if utilisateur:
            st.session_state.utilisateur = utilisateur
            st.success(f"✅ Bienvenue {utilisateur.pseudo} !")
            if not utilisateur.role:
                st.session_state.page = "utilisateur"
            else:
                st.warning("⚠️ Interface admin non implémentée pour l'instant.")
        else:
            st.error("❌ Échec de la connexion. Email ou mot de passe incorrect.")

def page_utilisateur():
    st.subheader(f"Espace Utilisateur - {st.session_state.utilisateur.pseudo}")
    choix = st.radio("Options", ["Voir les événements", "S'inscrire à un événement", "Déconnexion"])

    if choix == "Voir les événements":
        evenements = evenement_service.get_evenements_disponibles()
        if not evenements:
            st.info("Aucun événement disponible pour le moment.")
        else:
            for evt in evenements:
                st.write(f"ID: {evt.id_event}, Titre: {evt.titre}, Lieu: {evt.lieu}, "
                         f"Date: {evt.date_evenement}, "
                         f"Places restantes: {evt.capacite_max - len(evt.inscriptions) if hasattr(evt, 'inscriptions') else evt.capacite_max}")

    elif choix == "S'inscrire à un événement":
        id_event = st.text_input("Entrez l'ID de l'événement", key="id_event")
        boit_input = st.radio("Consommez-vous de l'alcool ?", ("Non", "Oui"))
        mode_paiement = st.selectbox("Mode de paiement", ["espèce", "en ligne"])

        if st.button("S'inscrire"):
            success = evenement_service.inscrire_utilisateur(
                id_event=int(id_event),
                id_utilisateur=st.session_state.utilisateur.id_utilisateur,
                boit=boit_input == "Oui",
                mode_paiement=mode_paiement
            )
            if success:
                st.success("✅ Inscription réussie !")
            else:
                st.error("❌ Inscription échouée.")

    elif choix == "Déconnexion":
        st.session_state.utilisateur = None
        st.session_state.page = "menu"
        st.success("🔒 Déconnexion réussie.")

# --- Menu principal Streamlit ---
if st.session_state.page == "menu":
    st.title("Système de Gestion d'Événements")
    option = st.radio("Menu Principal", ["Créer un compte", "Connexion", "Quitter"])
    if option == "Créer un compte":
        creer_compte()
    elif option == "Connexion":
        connexion()
    elif option == "Quitter":
        st.write("👋 Au revoir !")
