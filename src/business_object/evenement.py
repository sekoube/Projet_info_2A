from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
import re


class Evenement:
    """
    Classe métier représentant un événement de l'application.
    Cette classe contient uniquement la logique métier et les attributs de l'entité.
    """

    def __init__(
        self,
        titre: str = "",
        lieu: str = "",
        date_evenement: Optional[date] = None,
        capacite_max: int = 0,
        created_by: Optional[int] = None,
        id_event: Optional[int] = None,
        description_evenement: str = "",
        created_at: Optional[datetime] = None,
        tarif: float = 0.00
    ):
        """
        Constructeur de la classe Evenement.

        titre: Titre de l'événement (max 100 caractères)
        lieu: Lieu de l'événement (max 100 caractères)
        date_evenement: Date de l'événement
        capacite_max: Capacité maximale de participants
        created_by: ID de l'utilisateur créateur (FK vers utilisateur)
        id_event: Identifiant unique de l'événement (auto-incrémenté en base)
        description_evenement: Description détaillée de l'événement
        created_at: Date de création de l'événement
        tarif: Tarif de participation à l'événement
        """

        # ========================== VALIDATIONS ==========================
        if not titre or titre.strip() == "":
            raise ValueError("Le titre ne peut pas être vide")
        if len(titre) > 100:
            raise ValueError("Le titre ne peut pas dépasser 100 caractères")

        if not lieu or lieu.strip() == "":
            raise ValueError("Le lieu ne peut pas être vide")
        if len(lieu) > 100:
            raise ValueError("Le lieu ne peut pas dépasser 100 caractères")

        if date_evenement is None:
            raise ValueError("La date de l'événement est obligatoire")
        if not isinstance(date_evenement, date):
            raise ValueError("La date de l'événement doit être un objet date")

        if capacite_max <= 0:
            raise ValueError("La capacité maximale doit être supérieure à 0")
        if not isinstance(capacite_max, int):
            raise ValueError("La capacité maximale doit être un entier")

        if created_by is None:
            raise ValueError("L'ID du créateur est obligatoire")
        if not isinstance(created_by, int) or created_by <= 0:
            raise ValueError("L'ID du créateur doit être un entier positif")

        if tarif < 0:
            raise ValueError("Le tarif ne peut pas être négatif")
        # =================================================================

        self.id_event = id_event
        self.titre = titre
        self.description_evenement = description_evenement
        self.lieu = lieu
        self.date_evenement = date_evenement
        self.capacite_max = capacite_max
        self.created_by = created_by
        self.created_at = created_at or datetime.now()
        self.tarif = Decimal(str(tarif))

        # Relations (non persistées directement en DB, gérées via tables de liaison)
        self.inscriptions: List = []  # Liste des objets Inscription
        self.bus_aller = None  # Objet Bus (sens=True)
        self.bus_retour = None  # Objet Bus (sens=False)
        self.createur = None  # Objet Utilisateur (si chargé depuis la DB)

    # ************************ Méthodes ***********************************************

    def inscrire(
        self,
        utilisateur,
        boit: bool,
        mode_paiement: str,
        id_bus_aller: Optional[int] = None,
        id_bus_retour: Optional[int] = None
    ) -> bool:
        """
        Inscrit un utilisateur à l'événement.
        Crée un objet Inscription avec les informations nécessaires.

        utilisateur: Objet Utilisateur à inscrire
        boit: Si l'utilisateur consomme de l'alcool
        mode_paiement: Mode de paiement choisi
        id_bus_aller: ID du bus aller (optionnel)
        id_bus_retour: ID du bus retour (optionnel)

        return: True si inscription réussie, False sinon
        ------
        """
        if self.est_complet():
            print(
                f"Impossible d'inscrire {utilisateur.nom} {utilisateur.prenom}. "
                f"Capacité maximale atteinte ({self.capacite_max})."
            )
            return False

        # Vérifier si l'utilisateur n'est pas déjà inscrit
        if any(
            insc.id_utilisateur == utilisateur.id_utilisateur
            for insc in self.inscriptions
        ):
            print(f"{utilisateur.nom} {utilisateur.prenom} est déjà inscrit.")
            return False

        # Créer une nouvelle inscription (à persister en DB)
        from inscription import Inscription  # Import local pour éviter la circularité

        nouvelle_inscription = Inscription(
            id_utilisateur=utilisateur.id_utilisateur,
            id_event=self.id_event,
            boit=boit,
            mode_paiement=mode_paiement,
            id_bus_aller=id_bus_aller,
            id_bus_retour=id_bus_retour,
        )

        self.inscriptions.append(nouvelle_inscription)
        print(f"{utilisateur.nom} {utilisateur.prenom} est inscrit à {self.titre}.")
        return True

    def desinscrire(self, utilisateur) -> bool:
        """
        Désinscrit un utilisateur de l'événement.

        utilisateur: Objet Utilisateur à désinscrire

        return: True si désinscription réussie, False sinon
        ------
        """
        for insc in self.inscriptions:
            if insc.id_utilisateur == utilisateur.id_utilisateur:
                self.inscriptions.remove(insc)
                print(
                    f"{utilisateur.nom} {utilisateur.prenom} est désinscrit de {self.titre}."
                )
                return True

        print(
            f"{utilisateur.nom} {utilisateur.prenom} n'est pas inscrit à cet événement."
        )
        return False

    def places_disponibles(self) -> int:
        """
        Retourne le nombre de places disponibles.

        return: Nombre de places restantes
        ------
        """
        return self.capacite_max - len(self.inscriptions)

    def est_complet(self) -> bool:
        """
        Vérifie si l'événement est complet.

        return: True si aucune place disponible
        ------
        """
        return len(self.inscriptions) >= self.capacite_max

    def ajouter_bus(self, bus) -> None:
        """
        Ajoute un bus à l'événement (aller ou retour selon le sens).

        bus: Objet Bus à associer à l'événement
        ------
        """
        if bus.sens:  # True = aller
            self.bus_aller = bus
        else:  # False = retour
            self.bus_retour = bus

    def get_participants(self) -> List:
        """
        Retourne la liste des utilisateurs inscrits.
        Note: Nécessite de charger les objets Utilisateur depuis la DB.

        return: Liste des objets Utilisateur inscrits
        ------
        """
        return [
            insc.utilisateur
            for insc in self.inscriptions
            if hasattr(insc, "utilisateur")
        ]

    def taux_remplissage(self) -> float:
        """
        Calcule le taux de remplissage de l'événement en pourcentage.

        return: Pourcentage de places occupées (0.0 à 100.0)
        ------
        """
        if self.capacite_max == 0:
            return 0.0
        return (len(self.inscriptions) / self.capacite_max) * 100

    def est_passe(self) -> bool:
        """
        Vérifie si l'événement est déjà passé.

        return: True si la date de l'événement est antérieure à aujourd'hui
        ------
        """
        return self.date_evenement < date.today()

    def resume(self) -> str:
        """
        Retourne un résumé textuel de l'événement.
        Utile pour affichage dans les listes ou interfaces.

        return: str -> "Titre - Date à Lieu (participants/capacité)"
        ------
        """
        return (
            f"{self.titre} - {self.date_evenement} à {self.lieu} "
            f"({len(self.inscriptions)}/{self.capacite_max} participants) - {self.tarif}€"
        )

    def __repr__(self):
        """Représentation technique de l'objet"""
        return (
            f"<Evenement #{self.id_event} - {self.titre} "
            f"({self.date_evenement} à {self.lieu})>"
        )

    def __str__(self):
        """Représentation textuelle lisible"""
        return self.resume()

    def to_dict(self) -> dict:
        """
        Transforme l'objet en dictionnaire pour échange avec les autres couches.
        Utilisé pour la sérialisation (API, DAO, etc.)

        return: Dictionnaire contenant tous les attributs
        ------
        """
        return {
            "id_event": self.id_event,
            "titre": self.titre,
            "description_evenement": self.description_evenement,
            "lieu": self.lieu,
            "date_evenement": self.date_evenement.isoformat() if self.date_evenement else None,
            "capacite_max": self.capacite_max,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "tarif": str(self.tarif),
            "places_disponibles": self.places_disponibles(),
            "est_complet": self.est_complet(),
            "taux_remplissage": self.taux_remplissage(),
        }

    @staticmethod
    def from_dict(data: dict) -> "Evenement":
        """
        Transformation d'un dict (provenant de la DAO ou de l'API) vers un objet métier.

        data: Dictionnaire contenant les champs d'un événement

        return: Instance de Evenement
        ------
        """
        # Conversion de la date si elle est en format string
        date_evenement = data.get("date_evenement")
        if isinstance(date_evenement, str):
            date_evenement = datetime.fromisoformat(date_evenement).date()

        created_at = data.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)

        return Evenement(
            id_event=data.get("id_event"),
            titre=data.get("titre", ""),
            description_evenement=data.get("description_evenement", ""),
            lieu=data.get("lieu", ""),
            date_evenement=date_evenement,
            capacite_max=data.get("capacite_max", 0),
            created_by=data.get("created_by"),
            created_at=created_at,
            tarif=data.get("tarif", 0.00),
        )
