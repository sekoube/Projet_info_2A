from datetime import datetime


class Inscription:
    _compteurs = {}

    """
    Classe métier représentant une inscription dans un evenement.
    Cette classe contient uniquement la logique métier et les attributs de l'entité.
    """

    def __init__(
    self,
    code_reservation : int,
    boit : bool = False,
    created_by: Optional[int] = None,
    mode_paiement : str = "",
    id_event : str = "",
    nom_event : str = "",
    id_bus_aller : str = "",
    id_bus_retour : str = ""
    
    ):

        """
        Constructeur de la classe Inscription.

        code_reservation: code de réservation créé lors de l'inscription
        boit: Booléen indiquant si l'utilisateur boit de l'alcool (True) ou non (False)
        created_by: ID de l'utilisateur créateur (FK vers utilisateur)
        mode de paiement: espèce ou en ligne
        id_event: identifiant de l'évenement associé à l'inscription
        nom_event: nom de l'évenement associé à l'inscription
        id_bus_aller: identifiant du bus aller choisi par l'utilisateur lors de l'inscription
        id_bus_retour: identifiant du bus retour choisi par l'utilisateur lors de l'inscription
        """

        if nom_event not in Inscription._compteurs:
            Inscription._compteurs[nom_event] = 0
        Inscription._compteurs[nom_event] += 1
        self.code_reservation = code_reservation
        self.boit = boit
        self.created_by = created_by
        self.mode_paiement = mode_paiement
        self.id_event = id_event
        self.nom_event = nom_event
        self.id_bus_aller = id_bus_aller
        self.id_bus_retour = id_bus_retour
        self.date_creation = datetime.now()
        # ========================== VALIDATIONS ==========================
        # Code de réservation : doit être un entier positif
        if not isinstance(code_reservation, int) or code_reservation <= 0:
            raise ValueError("Le code de réservation doit être un entier positif.")

        # Boit : doit être un booléen
        if not isinstance(boit, bool):
            raise TypeError("Le champ 'boit' doit être de type bool.")

        # created_by : ID utilisateur obligatoire
        if created_by is None:
            raise ValueError("L'attribut 'created_by' (ID utilisateur) est obligatoire.")
        if not isinstance(created_by, int) or created_by <= 0:
            raise ValueError("L'ID utilisateur doit être un entier positif.")

        # Mode de paiement : doit être soit 'espèce' soit 'en ligne'
        if mode_paiement not in ("espèce", "en ligne", ""):
            raise ValueError("Le mode de paiement doit être 'espèce', 'en ligne' ou vide.")

        # ID événement et nom événement : obligatoires
        if not id_event or not isinstance(id_event, str):
            raise ValueError("L'ID de l'événement est obligatoire et doit être une chaîne.")
        if not nom_event or not isinstance(nom_event, str):
            raise ValueError("Le nom de l'événement est obligatoire et doit être une chaîne.")

        # Bus aller/retour : doivent être des chaînes (même vides)
        if not isinstance(id_bus_aller, str):
            raise TypeError("L'identifiant du bus aller doit être une chaîne de caractères.")
        if not isinstance(id_bus_retour, str):
            raise TypeError("L'identifiant du bus retour doit être une chaîne de caractères.")
        # =================================================================

    # ************************ Méthodes ***********************************************
        def inscrire(self, evenement, utilisateur):
        """
        Inscrire un utilisateur à un événement.
        - Ajoute l'utilisateur à l'événement via evenement.inscrire()
        - Met à jour le compteur d'inscriptions
        """
        if evenement is None or utilisateur is None:
            raise ValueError("L'événement et l'utilisateur doivent être fournis.")

        if utilisateur.id_utilisateur in evenement.liste_inscrits:
            print(f"{utilisateur.nom} est déjà inscrit à {evenement.nom}.")
            return False

        evenement.inscrire(utilisateur)
        print(f"{utilisateur.nom} a été inscrit à l'événement {evenement.nom}.")
        return True

    def desinscrire(self, evenement, utilisateur):
        """
        Désinscrire un utilisateur d'un événement.
        - Retire l'utilisateur via evenement.desinscrire()
        - Met à jour le compteur
        """
        if evenement is None or utilisateur is None:
            raise ValueError("L'événement et l'utilisateur doivent être fournis.")

        if utilisateur.id_utilisateur not in evenement.liste_inscrits:
            print(f"{utilisateur.nom} n'est pas inscrit à {evenement.nom}.")
            return False

        evenement.desinscrire(utilisateur)
        print(f"{utilisateur.nom} a été désinscrit de l'événement {evenement.nom}.")
        return True

    def __repr__(self):
        """Représentation texte"""
        return f"<Inscription {self.created_by} - {self.nom_event}>"

    def to_dict(self) -> dict:
        """
        On transforme l'objet en dict pour échanger avec les autres couches (service/DAO/API).
        """
        return {
            "code_reservation": self.code_reservation,
            "boit": self.boit,
            "created_by": self.created_by,
            "mode_paiement": self.mode_paiement,
            "id_event": self.id_event,
            "nom_event": self.nom_event,
            "id_bus_aller": self.id_bus_aller,
            "id_bus_retour": self.id_bus_retour,
            "date_creation": self.date_creation.isoformat(),
        }

    @staticmethod
    def from_dict(data: dict) -> "Inscription":
        """
        Transformation d'un dict (provenant de la DAO ou de l'API) vers un objet métier.
        data: Dictionnaire contenant les champs d'une inscription

        return: Instance de Inscription
        ------
        """
        return Inscription(
            code_reservation=data.get("code_reservation"),
            boit=data.get("boit", False),
            created_by=data.get("created_by", ""),
            mode_paiement=data.get("mode_paiement", ""),
            id_event=data.get("id_event", ""),
            nom_event=data.get("nom_event", ""),
            id_bus_aller=data.get("id_bus_aller", ""),
            id_bus_retour=data.get("id_bus_retour", ""),
            date_creation=data.get("date_creation", datetime.now()),
        )