from business_object.utilisateur import Utilisateur
from service.utilisateur_service import UtilisateurService  # Assure-toi que le chemin est correct

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

def connexion_terminal(service: UtilisateurService):
    print("\n=== Connexion ===")
    email = input("Email : ")
    mot_de_passe = input("Mot de passe : ")
    utilisateur = service.authentifier(email, mot_de_passe)
    if utilisateur:
        print(f"Bienvenue {utilisateur.pseudo} !")
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
