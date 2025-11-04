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
        pass
        # =================================================================

    # ************************ Méthodes ***********************************************

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