from dao.db_connection import DBConnection
from typing import Optional, List
from business_object.inscription import Inscription

class InscriptionDAO:

    def creer(self, inscription: Inscription) -> Optional[Inscription]:
        """
        Crée un nouvel événement en base de données.
        
        evenement: Objet Evenement à insérer (sans id_event)
        
        return: Evenement avec son id_event généré, ou None si échec
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO inscription 
                        (code_reservation, boit, created_by, mode_paiement, 
                         id_event, nom_event, id_bus_aller, id_bus_retour)
                        VALUES (%(code_reservation)s, %(boit)s, %(created_by)s, 
                                %(mode_paiement)s, %(id_event)s, %(nom_event)s, 
                                %(id_bus_aller)s, %(id_bus_retour)s)
                        RETURNING code_reservation;
                        """,
                        {
                            "code_reservation": inscription.code_reservation,
                            "boit": inscription.boit,
                            "created_by": inscription.created_by,
                            "mode_paiement": inscription.mode_paiement,
                            "id_event": inscription.id_event,
                            "nom_event": inscription.nom_event,
                            "id_bus_aller": inscription.id_bus_aller,
                            "id_bus_retour": float(inscription.id_bus_retour),
                        },
                    )
                    code_reservation = cursor.fetchone()["code_reservation"]
                    inscription.code_reservation = code_reservation
                    return inscription

        except Exception as e:
            print(f"Erreur lors de la création de l'inscription : {e}")
            return None

    def trouver_par_code_reservation(self, code_reservation: str) -> Optional[Inscription]:
        """
        Trouve une inscription par son code de réservation.
        
        code_reservation: Code de réservation à rechercher
        
        return: Objet Inscription trouvé, ou None si non trouvé
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT code_reservation, boit, created_by, mode_paiement,
                               id_event, nom_event, id_bus_aller, id_bus_retour
                        FROM inscription
                        WHERE code_reservation = %(code_reservation)s;
                        """,
                        {"code_reservation": code_reservation}
                    )
                    row = cursor.fetchone()
                    if row:
                        return Inscription(
                            code_reservation=row["code_reservation"],
                            boit=row["boit"],
                            created_by=row["created_by"],
                            mode_paiement=row["mode_paiement"],
                            id_event=row["id_event"],
                            nom_event=row["nom_event"],
                            id_bus_aller=row["id_bus_aller"],
                            id_bus_retour=row["id_bus_retour"]
                        )
                    return None
        except Exception as e:
            print(f"Erreur lors de la recherche de l'inscription : {e}")
            return None

    def get_by_event(self, id_event: int) -> List[Inscription]:
        """
        Trouve toutes les inscriptions pour un événement donné.
        
        id_evenement: ID de l'événement
        
        return: Liste des inscriptions trouvées
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT code_reservation, boit, created_by, mode_paiement,
                               id_event, nom_event, id_bus_aller, id_bus_retour
                        FROM inscription
                        WHERE id_event = %(id_event)s;
                        """,
                        {"id_event": id_event}
                    )
                    rows = cursor.fetchall()
                    return [
                        Inscription(
                            code_reservation=row["code_reservation"],
                            boit=row["boit"],
                            created_by=row["created_by"],
                            mode_paiement=row["mode_paiement"],
                            id_event=row["id_event"],
                            nom_event=row["nom_event"],
                            id_bus_aller=row["id_bus_aller"],
                            id_bus_retour=row["id_bus_retour"]
                        )
                        for row in rows
                    ]
        except Exception as e:
            print(f"Erreur lors de la recherche des inscriptions : {e}")
            return []

    def lister_toutes(self) -> List[Inscription]:
        """
        Liste toutes les inscriptions en base de données.
        
        return: Liste de toutes les inscriptions
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT code_reservation, boit, created_by, mode_paiement,
                               id_event, nom_event, id_bus_aller, id_bus_retour
                        FROM inscription;
                        """
                    )
                    rows = cursor.fetchall()
                    return [
                        Inscription(
                            code_reservation=row["code_reservation"],
                            boit=row["boit"],
                            created_by=row["created_by"],
                            mode_paiement=row["mode_paiement"],
                            id_event=row["id_event"],
                            nom_event=row["nom_event"],
                            id_bus_aller=row["id_bus_aller"],
                            id_bus_retour=row["id_bus_retour"]
                        )
                        for row in rows
                    ]
        except Exception as e:
            print(f"Erreur lors du listage des inscriptions : {e}")
            return []

    def compter_par_evenement(self, id_event: int) -> int:
        """
        Retourne le nombre d'inscriptions pour un événement donné.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT COUNT(*) as count
                        FROM inscription 
                        WHERE id_event = %(id_event)s;
                        """,
                        {"id_event": id_event}
                    )
                    resultat = cursor.fetchone()
                    return resultat["count"] if resultat else 0
        except Exception as e:
            print(f"Erreur lors du comptage des inscriptions : {e}")
            return 0