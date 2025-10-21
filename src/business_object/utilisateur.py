from datetime import datetime
from typing import Optional  # indiquer les types attendus pour les arguments, les attributs
import re  # pour vérifier la validité de l'adresse e-mail


class Utilisateur:
    """
    Classe métier représentant un utilisateur de l'application (administrateur ou participant).
    Cette classe contient uniquement la logique métier et les attributs de l'entité.
    """

    def __init__(
        self,
        id_utilisateur: Optional[int] = None,
        pseudo: str = "",
        nom: str = "",
        prenom: str = "",
        email: str = "",
        mot_de_passe: str = "",
        role: bool = False,
        date_creation: Optional[datetime] = None
    ):
        """
        Constructeur de la classe Utilisateur.

        id_utilisateur: Identifiant unique de l'utilisateur (auto-incrémenté en base)
        pseudo: Pseudonyme choisi par l'utilisateur
        nom: Nom de famille
        prenom: Prénom
        email: Adresse e-mail de l'utilisateur
        Mot de passe (hashé en base)
        role: Booléen indiquant si l'utilisateur est administrateur (True) ou participant (False)
        date_creation: Date de création du compte
        """

        # ========================== VALIDATIONS ==========================
        if not pseudo or pseudo.strip() == "":
            raise ValueError("Le pseudo ne peut pas être vide")
        if not nom or nom.strip() == "":
            raise ValueError("Le nom ne peut pas être vide")
        if not prenom or prenom.strip() == "":
            raise ValueError("Le prénom ne peut pas être vide")

        # Validation améliorée de l'email (via expression régulière)
        # Format attendu : texte@texte.domaine
        if not email or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            raise ValueError("L'adresse e-mail n'est pas valide")

        if not mot_de_passe or mot_de_passe.strip() == "":
            raise ValueError("Le mot de passe ne peut pas être vide")
        # =================================================================

        self.id_utilisateur = id_utilisateur
        self.pseudo = pseudo
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mot_de_passe = mot_de_passe
        self.role = role
        self.date_creation = date_creation or datetime.now()

    # ************************ Méthodes ***********************************************

    def identite(self) -> str:
        """
        Retourne une représentation de l'identité de l'utilisateur.
        utile pour héritage avec Administrateur

        return: str -> "Prénom Nom (pseudo)"
        ------
        """
        return f"{self.prenom} {self.nom} ({self.pseudo})"

    def email_valide(self) -> bool:
        """
        Vérifie la validité de l'adresse e-mail.

        return: True si l'e-mail semble valide
        ------
        """
        return "@" in self.email and "." in self.email
       
    def __repr__(self):
        """Représentation texte"""
        role_str = "Admin" if self.role else "Participant"
        return f"<Utilisateur #{self.id_utilisateur} - {self.pseudo} ({role_str})>"

    def to_dict(self) -> dict:
        """
        On transforme l'objet en dict pour échange avec les autres couches (service/DAO/API).
        """
        return {
            "id_utilisateur": self.id_utilisateur,
            "pseudo": self.pseudo,
            "nom": self.nom,
            "prenom": self.prenom,
            "email": self.email,
            "mot_de_passe": self.mot_de_passe,  # hash attendu
            "role": self.role,
            "date_creation": self.date_creation.isoformat(),
        }

    @staticmethod
    def from_dict(data: dict) -> "Utilisateur":
        """
        Transformation d'un dict (provenant de la DAO ou de l'API) vers un objet métier.
        data: Dictionnaire contenant les champs d'un utilisateur

        return: Instance de Utilisateur
        ------
        """
        return Utilisateur(
            id_utilisateur=data.get("id_utilisateur"),
            pseudo=data.get("pseudo", ""),
            nom=data.get("nom", ""),
            prenom=data.get("prenom", ""),
            email=data.get("email", ""),
            mot_de_passe=data.get("mot_de_passe", ""),
            role=data.get("role", False),
            date_creation=data.get("date_creation", datetime.now()),
        )
