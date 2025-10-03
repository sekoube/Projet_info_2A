class Utilisateur:
    " Définit les informations de connection et les caractéristiques d'un utilisateur " 

    def __init__(self, id_utilisateur =  None, pseudo, nom, prenom, email, mdp):

        """ Constructeur de la classe Utilisateur 

        Param
        -----
        param id_utilisateur: int ou None - Identifiant auto-généré par la BDD
        param pseudo : str - Pseudonyme que l'utilisateur se donne (unique, peut servir d'identifiant de connexion)
        param nom: str - Nom  de l'utilisateur
        param prénom: str - prénom de l'utilisateur
        param email: str - Adresse email (unique, peut servir d'identifiant de connexion)
        param mdp: str - hash du mot de passe

        return : aucun retour
        -----

        """
    
        self.id_utilisateur = id_utilisateur
        self.pseudo = pseudo
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mdp = mdp  # Valeur hachée (gérée par AuthService)
 
    
    def __repr__(self):
        """
        Représentation utile pour le debug.
        """
        return f"<Utilisateur id={self.id_utilisateur}, email={self.email}>"
