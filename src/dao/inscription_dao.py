from dao.db_connection import DBConnection

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

    def compter_par_evenement(self, id_evenement: int) -> int:
        """
        Retourne le nombre d'inscriptions pour un événement donné.
        """
        with DBConnection().connection as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT COUNT(*) 
                FROM inscription 
                WHERE id_evenement = ?
                """,
                (id_evenement,)
            )
            resultat = cursor.fetchone()
            return resultat[0] if resultat else 0
