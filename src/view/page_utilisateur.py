from business_object.utilisateur import Utilisateur
from service.utilisateur_service import UtilisateurService
from service.evenement_service import EvenementService
from service.inscription_service import InscriptionService
from service.bus_service import BusService
import getpass

def page_utilisateur(utilisateur, evenement_service: EvenementService, inscription_service: InscriptionService, bus_service: BusService):
    """
    Sous-boucle pour un utilisateur connecté.
    Permet de lister les événements, de s'inscrire, d'annuler une inscription via son code de réservation,
    et de consulter ses inscriptions.
    """
    while True:
        print("\n=== Espace Utilisateur ===")
        print("1. Voir les événements disponibles")
        print("2. S'inscrire à un événement")
        print("3. Annuler une inscription")
        print("4. Voir mes inscriptions")
        print("5. Déconnexion")
        choix = input("Choisissez une option : ").strip()

        # ---------------- Option 1 : Voir les événements ----------------
        if choix == "1":
            evenements = evenement_service.get_evenement_by("statut", "en_cours")
            if not evenements:
                print("Aucun événement disponible pour le moment.")
                continue

            print("\nÉvénements disponibles :")
            for evt in evenements:
                # Calcul des places restantes
                inscriptions = inscription_service.get_inscription_by("id_event", evt.id_event)
                places_restantes = evt.capacite_max - len(inscriptions) if inscriptions else evt.capacite_max
                print(
                    f"- ID: {evt.id_event}, Titre: {evt.titre}, Lieu: {evt.lieu}, "
                    f"Date: {evt.date_event}, Places restantes: {places_restantes}"
                )

        # ---------------- Option 2 : S'inscrire ----------------

        elif choix == "2":
            id_event = input("Entrez l'ID de l'événement : ").strip()
            boit_input = input("Consommez-vous de l'alcool ? (oui/non) : ").strip().lower()
            boit = boit_input == "oui"
            mode_paiement = input("Mode de paiement (espèce/en ligne) : ").strip().lower()

            # 🔹 Affichage des bus disponibles avant la saisie
            print("\nBus Aller disponibles :")
            bus_aller_disponibles = bus_service.get_bus_by("sens", "ALLER")
            if bus_aller_disponibles:
                for bus in bus_aller_disponibles:
                    inscriptions_bus_aller = inscription_service.get_inscription_by("id_bus_aller", int(bus.id_bus))
                    places_restantes = bus.capacite_max - len(inscriptions_bus_aller)
                    print(f"- ID: {bus.id_bus}, Places restantes: {places_restantes}")
            else:
                print("Aucun bus Aller disponible.")

            print("\nBus Retour disponibles :")
            bus_retour_disponibles = bus_service.get_bus_by("sens", "RETOUR")
            if bus_retour_disponibles:
                for bus in bus_retour_disponibles:
                    inscriptions_bus_retour = inscription_service.get_inscription_by("id_bus_retour", int(bus.id_bus))
                    places_restantes = bus.capacite_max - len(inscriptions_bus_retour)
                    print(f"- ID: {bus.id_bus}, Places restantes: {places_restantes}")
            else:
                print("Aucun bus Retour disponible.")

            # 🔹 Saisie des bus
            id_bus_a = input("Entrez l'ID du bus Aller : ").strip()
            id_bus_r = input("Entrez l'ID du bus Retour : ").strip()

            try:
                id_event_int = int(id_event)
                id_bus_aller_int = int(id_bus_a) if id_bus_a else None
                id_bus_retour_int = int(id_bus_r) if id_bus_r else None
            except ValueError:
                print("❌ ID d'événement ou de bus invalide. Annulation de l'inscription.")
                continue


            # Récupération de l'événement
            evenement = evenement_service.get_evenement_by("id_event", id_event_int)
            if not evenement:
                print("❌ Événement introuvable.")
                continue
            if isinstance(evenement, list):
                evenement = evenement[0]
            nom_evenement = evenement.titre

            # 🔹 Vérification bus Aller
            if id_bus_aller_int:
                bus_aller = bus_service.get_bus_by("id_bus", id_bus_aller_int)
                if not bus_aller or bus_aller[0].sens != "ALLER":
                    print("❌ Bus Aller invalide.")
                    continue
                inscriptions_bus_aller = inscription_service.get_inscription_by("id_bus_aller", id_bus_aller_int)
                if len(inscriptions_bus_aller) >= bus_aller[0].capacite_max:
                    print("❌ Bus Aller complet. Inscription impossible.")
                    continue

            # 🔹 Vérification bus Retour
            if id_bus_retour_int:
                bus_retour = bus_service.get_bus_by("id_bus", id_bus_retour_int)
                if not bus_retour or bus_retour[0].sens != "RETOUR":
                    print("❌ Bus Retour invalide.")
                    continue
                inscriptions_bus_retour = inscription_service.get_inscription_by("id_bus_retour", id_bus_retour_int)
                if len(inscriptions_bus_retour) >= bus_retour[0].capacite_max:
                    print("❌ Bus Retour complet. Inscription impossible.")
                    continue

            # Création de l'inscription
            success = inscription_service.creer_inscription(
                id_event=id_event_int,
                boit=boit,
                mode_paiement=mode_paiement,
                created_by=utilisateur.id_utilisateur,
                nom_event=nom_evenement,
                id_bus_aller=id_bus_aller_int,
                id_bus_retour=id_bus_retour_int,
            )

            if success:
                print("✅ Inscription réussie !")
            else:
                print("❌ Inscription échouée.")


        # ---------------- Option 5 : Déconnexion ----------------
        elif choix == "5":
            print("🔒 Déconnexion...")
            break

        # ---------------- Option 3 : Annuler une inscription ----------------
        elif choix == "3":
            print("\n=== Annulation d'une inscription ===")
            code_reservation = input("Entrez le code de réservation à annuler : ").strip()
            if not code_reservation:
                print("❌ Code de réservation vide. Annulation.")
                continue

            confirmation = input(
                f"⚠️ Confirmez-vous l'annulation de l'inscription avec le code '{code_reservation}' ? (oui/non) : "
            ).strip().lower()
            if confirmation != "oui":
                print("❌ Annulation de la suppression.")
                continue

            try:
                resultat = inscription_service.supprimer_inscription(code_reservation, utilisateur.id_utilisateur)
                if resultat:
                    print(f"✅ Inscription avec le code '{code_reservation}' supprimée avec succès.")
                else:
                    print(f"❌ La suppression a échoué pour le code '{code_reservation}'.")
            except ValueError as ve:
                print(f"❌ Erreur : {ve}")
            except PermissionError as pe:
                print(f"🚫 Permission refusée : {pe}")
            except Exception as e:
                print(f"⚠️ Erreur inattendue lors de la suppression : {e}")

        # ---------------- Option 4 : Voir mes inscriptions ----------------
        elif choix == "4":
            print("\n=== Mes inscriptions ===")
            inscriptions = inscription_service.get_inscription_by("created_by", utilisateur.id_utilisateur)
            if not inscriptions:
                print("ℹ️ Vous n'êtes inscrit à aucun événement pour le moment.")
                continue

            for ins in inscriptions:
                print(
                    f"- Code: {ins.code_reservation}, Événement: {ins.nom_event}, ID: {ins.id_event}, "
                    f"Bus Aller: {ins.id_bus_aller}, Bus Retour: {ins.id_bus_retour}"
                )

        else:
            print("❌ Option invalide, réessayez.")
