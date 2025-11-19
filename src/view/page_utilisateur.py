from business_object.utilisateur import Utilisateur
from service.utilisateur_service import UtilisateurService
from service.evenement_service import EvenementService
from service.inscription_service import InscriptionService
import getpass


def page_utilisateur(utilisateur, evenement_service: EvenementService, inscription_service: InscriptionService):
    """
    Sous-boucle pour un utilisateur connecté.
    Permet de lister les événements, de s'inscrire et d'annuler une inscription via son code de réservation.
    """
    while True:
        print("\n=== Espace Utilisateur ===")
        print("1. Voir les événements disponibles")
        print("2. S'inscrire à un événement")
        print("3. Déconnexion")
        print("4. Annuler une inscription (code de réservation)")  # ← nouvelle option
        choix = input("Choisissez une option : ").strip()

        if choix == "1":
            evenements = evenement_service.get_evenement_by("statut", "en_cours")
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

        elif choix == "2":
            id_event = input("Entrez l'ID de l'événement : ").strip()
            boit_input = input("Consommez-vous de l'alcool ? (oui/non) : ").strip().lower()
            boit = boit_input == "oui"
            mode_paiement = input("Mode de paiement (espèce/en ligne) : ").strip().lower()
            nom_evenement = input("Entrez le nom de l'événement : ").strip()
            id_bus_a = input("Entrez l'ID du bus Aller : ").strip()
            id_bus_r = input("Entrez l'ID du bus Retour : ").strip()

            # Conversion éventuelle des IDs en int si nécessaire
            try:
                id_event_int = int(id_event)
            except ValueError:
                print("ID d'événement invalide. Annulation de l'inscription.")
                continue

            # si tes services attendent des int pour les bus, convertir aussi :
            try:
                id_bus_aller_int = int(id_bus_a) if id_bus_a != "" else None
                id_bus_retour_int = int(id_bus_r) if id_bus_r != "" else None
            except ValueError:
                print("ID de bus invalide. Annulation de l'inscription.")
                continue

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

        elif choix == "3":
            print("🔒 Déconnexion...")
            break

        elif choix == "4":
            # Annulation d'une inscription à partir du code de réservation
            print("\n=== Annulation d'une inscription ===")
            code_reservation = input("Entrez le code de réservation à annuler : ").strip()
            if not code_reservation:
                print("❌ Code de réservation vide. Annulation.")
                continue

            # Demande de confirmation (sécurité UX)
            confirmation = input(f"⚠️ Confirmez-vous l'annulation de l'inscription avec le code '{code_reservation}' ? (oui/non) : ").strip().lower()
            if confirmation != "oui":
                print("❌ Annulation de la suppression.")
                continue

            # Appel du service — la méthode doit accepter un code_reservation (str)
            try:
                resultat = inscription_service.supprimer_inscription(code_reservation, utilisateur.id_utilisateur)

                if resultat:
                    print(f"✅ Inscription avec le code '{code_reservation}' supprimée avec succès.")
                else:
                    # Si la méthode retourne False, on affiche un message générique
                    print(f"❌ La suppression a échoué pour le code '{code_reservation}'.")
            except ValueError as ve:
                print(f"❌ Erreur : {ve}")
            except PermissionError as pe:
                print(f"🚫 Permission refusée : {pe}")
            except Exception as e:
                # Cas inattendu — utile pour debug
                print(f"⚠️ Erreur inattendue lors de la suppression : {e}")

        else:
            print("❌ Option invalide, réessayez.")
