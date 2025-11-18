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
                         id_event, id_bus_retour, id_bus_aller, created_at)
                        VALUES (%(code_reservation)s, %(boit)s, %(created_by)s, 
                                %(mode_paiement)s, %(id_event)s, 
                                %(id_bus_aller)s, %(id_bus_retour)s, %(created_at)s)
                        RETURNING code_reservation;
                        """,
                        {
                            "code_reservation": inscription.code_reservation,
                            "boit": inscription.boit,
                            "created_by": inscription.created_by,
                            "mode_paiement": inscription.mode_paiement,
                            "id_event": inscription.id_event,
                            "id_bus_aller": inscription.id_bus_aller,
                            "id_bus_retour": float(inscription.id_bus_retour),
                            "created_at": inscription.created_at,
                        },
                    )
                    code_reservation = cursor.fetchone()["code_reservation"]
                    inscription.code_reservation = code_reservation
                    return inscription

        except Exception as e:
            print(f"Erreur lors de la création de l'inscription : {e}")
            return None

    def get_by_field(self, field: str, value) ->  Inscription | None:
        """Retourne une Inscription selon un champ donné."""

        # Sécurité : liste blanche des champs autorisés
        allowed_fields = {"code_reservation", "boit", "created_by", "mode_paiement", 
                        "id_event", "id_bus_retour", "id_bus_aller", "created_at"}
        if field not in allowed_fields:
            raise ValueError(f"Champ non autorisé : {field}")

        query = f"SELECT * FROM inscription WHERE {field} = %s"

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (value,))
                row = cursor.fetchone()

                return Inscription.from_dict(row) if row else None


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
                               id_event, id_bus_aller, id_bus_retour, created_at
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
                            id_bus_aller=row["id_bus_aller"],
                            id_bus_retour=row["id_bus_retour"],
                            created_at=row["created_at"]
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

    def supprimer(self, inscription: Inscription) -> bool:
        """
        Supprime une inscription de la base de données.

        inscription : Objet Inscription à supprimer (doit contenir code_reservation)

        return : True si la suppression a réussi, False sinon.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM inscription
                        WHERE code_reservation = %(code_reservation)s;
                        """,
                        {"code_reservation": inscription.code_reservation},
                    )
                    return cursor.rowcount > 0

        except Exception as e:
            print(f"Erreur lors de la suppression de l'inscription : {e}")
            return False
