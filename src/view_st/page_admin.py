import streamlit as st
from datetime import datetime
from service.evenement_service import EvenementService
from service.inscription_service import InscriptionService
from service.bus_service import BusService
from business_object.bus import Bus

def page_admin(utilisateur, evenement_service: EvenementService, inscription_service: InscriptionService):
    """
    Page admin Streamlit : gestion des événements et des bus.
    """
    st.subheader(f"Espace Admin - {utilisateur.pseudo}")

    bus_service = BusService()

    option = st.radio("Options", [
        "Voir les événements disponibles",
        "Créer un événement",
        "Créer un bus",
        "Déconnexion"
    ])

    # ---- OPTION 1 : Voir les événements ----
    if option == "Voir les événements disponibles":
        evenements = evenement_service.get_evenements_disponibles()
        if not evenements:
            st.info("Aucun événement disponible pour le moment.")
        else:
            for evt in evenements:
                places_restantes = (
                    evt.capacite_max - len(evt.inscriptions)
                    if hasattr(evt, "inscriptions")
                    else evt.capacite_max
                )
                st.write(
                    f"ID: {evt.id_event}, Titre: {evt.titre}, Lieu: {evt.lieu}, "
                    f"Date: {evt.date_evenement}, Places restantes: {places_restantes}"
                )

    # ---- OPTION 2 : Créer un événement ----
    elif option == "Créer un événement":
        st.markdown("### Création d’un nouvel événement")
        titre = st.text_input("Titre de l'événement", key="evt_titre")
        lieu = st.text_input("Lieu de l'événement", key="evt_lieu")
        date_str = st.text_input("Date de l'événement (YYYY-MM-DD)", key="evt_date")
        capacite_str = st.text_input("Capacité maximale", key="evt_capacite")
        description = st.text_area("Description (optionnel)", key="evt_desc")
        tarif_str = st.text_input("Tarif (optionnel, par défaut 0.00)", key="evt_tarif")

        if st.button("Créer l'événement", key="btn_creer_evt"):
            try:
                date_evenement = datetime.strptime(date_str, "%Y-%m-%d").date()
                capacite_max = int(capacite_str)
                tarif = float(tarif_str) if tarif_str else 0.00
                nouvel_evenement = evenement_service.creer_evenement(
                    titre=titre,
                    lieu=lieu,
                    date_evenement=date_evenement,
                    capacite_max=capacite_max,
                    created_by=utilisateur.id_utilisateur,
                    description_evenement=description,
                    tarif=tarif
                )
                if nouvel_evenement:
                    st.success(f"✅ Événement '{titre}' créé avec succès ! (ID: {nouvel_evenement.id_event})")
                else:
                    st.error("❌ La création de l'événement a échoué.")
            except ValueError as e:
                st.error(f"❌ Erreur dans les données saisies : {e}")

    # ---- OPTION 3 : Créer un bus ----
    elif option == "Créer un bus":
        st.markdown("### Création d’un bus")

        evenements = evenement_service.get_evenements_disponibles()
        if not evenements:
            st.warning("❌ Aucun événement disponible, impossible de créer un bus.")
            return

        evt_options = {f"{evt.id_event} - {evt.titre}": evt.id_event for evt in evenements}
        id_event = st.selectbox("Sélectionner un événement", list(evt_options.keys()))
        id_event_val = evt_options[id_event]

        sens_input = st.radio("Sens du trajet", ["Aller", "Retour"])
        sens = sens_input == "Aller"
        description = st.text_input("Description du bus (optionnel)", key="bus_desc")
        heure_str = st.text_input("Heure de départ (HH:MM)", key="bus_heure")
        capacite_str = st.text_input("Capacité maximale du bus", key="bus_capacite")

        if st.button("Créer le bus", key="btn_creer_bus"):
            try:
                heure_depart = datetime.strptime(heure_str, "%H:%M").time()
                capacite = int(capacite_str)
                bus = Bus(
                    id_bus=None,
                    id_event=id_event_val,
                    sens=sens,
                    description=description,
                    heure_depart=heure_depart,
                    capacite_max=capacite
                )
                nouveau_bus = bus_service.creer_bus(bus, utilisateur)
                if nouveau_bus:
                    st.success(f"✅ Bus créé avec succès pour l'événement {id_event_val} !")
                else:
                    st.error("❌ La création du bus a échoué.")
            except ValueError as e:
                st.error(f"❌ Erreur dans les données saisies : {e}")
            except PermissionError as e:
                st.error(f"🚫 {e}")
            except Exception as e:
                st.error(f"⚠️ Erreur inattendue : {e}")

    # ---- OPTION 4 : Déconnexion ----
    elif option == "Déconnexion":
        st.session_state.utilisateur = None
        st.session_state.page = "menu"
        st.info("🔒 Déconnexion réussie.")
