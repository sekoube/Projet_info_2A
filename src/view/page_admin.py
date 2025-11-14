from datetime import datetime
from service.utilisateur_service import UtilisateurService
from service.evenement_service import EvenementService
from service.inscription_service import InscriptionService
from service.bus_service import BusService
from business_object.bus import Bus


def page_admin(utilisateur, evenement_service: EvenementService, inscription_service: InscriptionService):
    """
    Sous-boucle pour un utilisateur connecté (admin).
    Permet de gérer les événements et les bus.
    """
    bus_service = BusService()

    while True:
        print("\n=== Espace Admin ===")
        print("1. Voir les événements disponibles")
        print("2. Créer un événement")
        print("3. Déconnexion")
        print("4. Créer un bus")  # 🔹 Nouvelle option
        print("5. Supprimer un événement")
        choix = input("Choisissez une option : ").strip()

        # ---- OPTION 1 : Liste des événements ----
        if choix == "1":
            evenements = evenement_service.get_evenements_disponibles()
            if not evenements:
                print("Aucun événement disponible pour le moment.")
            else:
                print("\nÉvénements disponibles :")
                for evt in evenements:
                    places_restantes = (
                        evt.capacite_max - len(evt.inscriptions)
                        if hasattr(evt, "inscriptions")
                        else evt.capacite_max
                    )
                    print(
                        f"- ID: {evt.id_event}, Titre: {evt.titre}, Lieu: {evt.lieu}, "
                        f"Date: {evt.date_event}, Places restantes: {places_restantes}"
                    )

        # ---- OPTION 2 : Création d’un nouvel événement ----
        elif choix == "2":
            print("\n=== Création d’un nouvel événement ===")
            titre = input("Titre de l'événement : ").strip()
            lieu = input("Lieu de l'événement : ").strip()
            date_str = input("Date de l'événement (format YYYY-MM-DD) : ").strip()
            capacite_str = input("Capacité maximale : ").strip()
            description = input("Description (optionnel) : ").strip()
            tarif_str = input("Tarif (optionnel, par défaut 0.00) : ").strip()

            # Validation des entrées
            try:
                date_event = datetime.strptime(date_str, "%Y-%m-%d").date()
                capacite_max = int(capacite_str)
                tarif = float(tarif_str) if tarif_str else 0.00
            except ValueError as e:
                print(f"❌ Erreur dans les données saisies : {e}")
                continue

            # Création via le service
            nouvel_evenement = evenement_service.creer_evenement(
                titre=titre,
                lieu=lieu,
                date_event=date_event,
                capacite_max=capacite_max,
                created_by=utilisateur.id_utilisateur,  # ID de l'admin
                description_event=description,
                tarif=tarif
            )

            if nouvel_evenement:
                print(f"✅ Événement '{titre}' créé avec succès ! (ID: {nouvel_evenement.id_event})")
            else:
                print("❌ La création de l'événement a échoué.")

        # ---- OPTION 3 : Déconnexion ----
        elif choix == "3":
            print("🔒 Déconnexion...")
            break

        # ---- OPTION 4 : Création d’un bus ----
        elif choix == "4":
            print("\n=== Création d’un bus ===")

            # Liste les événements pour que l'admin choisisse l’un d’eux
            evenements = evenement_service.get_evenements_disponibles()
            if not evenements:
                print("❌ Aucun événement disponible, impossible de créer un bus.")
                continue

            print("\nÉvénements disponibles :")
            for evt in evenements:
                print(f"- ID: {evt.id_event}, Titre: {evt.titre}, Date: {evt.date_event}")

            try:
                id_event = int(input("ID de l'événement associé : ").strip())
            except ValueError:
                print("❌ ID invalide.")
                continue

            sens_input = input("Sens du trajet (Aller / Retour) : ").strip().lower()

            if sens_input not in ["aller", "retour"]:
                print("❌ Valeur de sens invalide (‘Aller’ ou ‘Retour’ attendu).")
                continue

            # Normalisation pour l'envoyer à la classe Bus
            sens = sens_input.capitalize()   # → “Aller” ou “Retour”


            description = input("Description du bus (optionnel) : ").strip()
            heure_str = input("Heure de départ (format HH:MM) : ").strip()
            capacite_str = input("Capacité maximale du bus : ").strip()

            try:
                heure_depart = datetime.strptime(heure_str, "%H:%M").time()
                capacite = int(capacite_str)
            except ValueError as e:
                print(f"❌ Erreur dans les données saisies : {e}")
                continue

            # Création de l'objet Bus
            bus = Bus(
                id_bus=None,
                id_event=id_event,
                sens=sens,
                description=description,
                heure_depart=heure_depart,
                capacite_max=capacite
            )

            try:
                nouveau_bus = bus_service.creer_bus(bus, utilisateur)
                if nouveau_bus:
                    print(f"✅ Bus créé avec succès pour l'événement {id_event} !")
                else:
                    print("❌ La création du bus a échoué.")
            except PermissionError as e:
                print(f"🚫 {e}")
            except ValueError as e:
                print(f"❌ {e}")
            except Exception as e:
                print(f"⚠️ Erreur inattendue : {e}")

                # ---- OPTION 5 : Supprimer un événement ----
        elif choix == "5":
            print("\n=== Suppression d’un événement ===")

            # Récupérer les événements disponibles
            evenements = evenement_service.get_evenements_disponibles()
            if not evenements:
                print("❌ Aucun événement disponible à supprimer.")
                continue

            print("\nÉvénements disponibles :")
            for evt in evenements:
                print(f"- ID: {evt.id_event}, Titre: {evt.titre}, Date: {evt.date_event}")

            try:
                id_event = int(input("ID de l'événement à supprimer : ").strip())
            except ValueError:
                print("❌ ID invalide.")
                continue

            # Vérifier que l'événement existe
            evenement_a_supprimer = evenement_service.evenement_dao.get_by_id(id_event)
            if not evenement_a_supprimer:
                print(f"❌ L'événement avec l'ID {id_event} n'existe pas.")
                continue

            confirmation = input(
                f"⚠️ Êtes-vous sûr de vouloir supprimer l'événement '{evenement_a_supprimer.titre}' ? (oui/non) : "
            ).strip().lower()

            if confirmation != "oui":
                print("❌ Suppression annulée.")
                continue

            # Appel du service
            if evenement_service.supprimer_evenement(id_event):
                print(f"✅ Événement {id_event} supprimé avec succès.")
            else:
                print("❌ La suppression a échoué.")


        else:
            print("❌ Option invalide, réessayez.")
