import streamlit as st
from service.evenement_service import EvenementService
from service.inscription_service import InscriptionService

def page_utilisateur(utilisateur, evenement_service: EvenementService, inscription_service: InscriptionService):
    """
    Page utilisateur Streamlit : consultation et inscription aux événements.
    """
    st.subheader(f"Espace Utilisateur - {utilisateur.pseudo}")

    option = st.radio("Options", [
        "Voir les événements disponibles",
        "S'inscrire à un événement",
        "Déconnexion"
    ])

    # ---- OPTION 1 : Voir les événements disponibles ----
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

    # ---- OPTION 2 : S'inscrire à un événement ----
    elif option == "S'inscrire à un événement":
        st.markdown("### Inscription à un événement")
        evenements = evenement_service.get_evenements_disponibles()
        if not evenements:
            st.warning("Aucun événement disponible pour le moment.")
            return

        evt_options = {f"{evt.id_event} - {evt.titre}": evt.id_event for evt in evenements}
        id_event_key = st.selectbox("Sélectionnez un événement", list(evt_options.keys()))
        id_event = evt_options[id_event_key]

        boit_input = st.radio("Consommez-vous de l'alcool ?", ["Non", "Oui"])
        boit = boit_input == "Oui"
        mode_paiement = st.selectbox("Mode de paiement", ["espèce", "en ligne"])
        nom_evenement = st.text_input("Nom de l'événement (facultatif)")
        id_bus_aller = st.text_input("ID du bus Aller (facultatif)")
        id_bus_retour = st.text_input("ID du bus Retour (facultatif)")

        if st.button("S'inscrire"):
            try:
                id_bus_aller_val = int(id_bus_aller) if id_bus_aller else None
                id_bus_retour_val = int(id_bus_retour) if id_bus_retour else None

                success = inscription_service.creer_inscription(
                    id_event=int(id_event),
                    boit=boit,
                    mode_paiement=mode_paiement,
                    created_by=utilisateur.id_utilisateur,
                    nom_event=nom_evenement,
                    id_bus_aller=id_bus_aller_val,
                    id_bus_retour=id_bus_retour_val,
                )
                if success:
                    st.success("✅ Inscription réussie !")
                else:
                    st.error("❌ Inscription échouée.")
            except ValueError:
                st.error("❌ Les IDs d'événement ou de bus doivent être des nombres valides.")

    # ---- OPTION 3 : Déconnexion ----
    elif option == "Déconnexion":
        st.session_state.utilisateur = None
        st.session_state.page = "menu"
        st.info("🔒 Déconnexion réussie.")
