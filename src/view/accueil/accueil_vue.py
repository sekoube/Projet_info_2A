from business_object.utilisateur import Utilisateur
from service.utilisateur_service import UtilisateurService  # Assure-toi que le chemin est correct
from service.evenement_service import EvenementService

def creer_compte_terminal(service: UtilisateurService):
    print("\n=== Création de compte ===")
    pseudo = input("Pseudo : ")
    nom = input("Nom : ")
    prenom = input("Prénom : ")
    email = input("Email : ")
    mot_de_passe = input("Mot de passe : ")
    role_input = input("Compte admin ? (oui/non) : ").lower()
    role = True if role_input == "oui" else False

    service.creer_compte(pseudo, nom, prenom, email, mot_de_passe, role)

def creer_event_terminal(service : EvenementService):
    print("\n=== Création d'un évènement")
    titre = input("Titre : ")
    lieu = input("Lieu : ")
    date_evenement = input("Date : ")
    capacite_max = input("Capacité max :")
    created_by = input("Entrez votre identifiant :")
    description_event = input("Description évènement :")
    tarif = input("tarif :")

    service.creer_evenement(titre, lieu, date_evenement, capacite_max, created_by, description_event, tarif)


def connexion_terminal(service: UtilisateurService):
    print("\n=== Connexion ===")
    email = input("Email : ")
    mot_de_passe = input("Mot de passe : ")
    utilisateur = service.authentifier(email, mot_de_passe)
    if utilisateur:
        print(f"Bienvenue {utilisateur.pseudo} !")
        print("\n=== Menu de l'utilisateur ===")
        if UtilisateurService.is_admin():
            print("1. Créer un évènement")
            print("2. S'inscrire à un évènement")
            print("3. Se désinscrire d'un évènement")
            print("4. Supprimer un évènement")
            print("5. Supprimer un utilisateur")
            print("6. Suppremer son compte")
            print("7. Se déconnecter")
        else:
            print("2. S'inscrire à un évènement")
            print("3. Se désinscrire d'un évènement")
            print("6. Suppremer son compte")
            print("7. Se déconnecter")
        
        if choix==1:
            creer_event_terminal(service)

    else:
        print("Échec de la connexion.")

def menu():
    service = UtilisateurService()
    while True:
        print("\n=== Menu Principal ===")
        print("1. Créer un compte")
        print("2. Connexion")
        print("3. Quitter")
        choix = input("Choisissez une option : ")

        if choix == "1":
            creer_compte_terminal(service)
        elif choix == "2":
            connexion_terminal(service)
        elif choix == "3":
            print("Au revoir !")
            break
        else:
            print("Option invalide, réessayez.")

if __name__ == "__main__":
    menu()