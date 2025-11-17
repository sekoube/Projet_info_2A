from business_object.bus import Bus
from dao.db_connection import DBConnection


class BusDAO:
    """Accès aux données pour les bus."""

    @staticmethod
    def creer(bus: Bus) -> Bus:
        """Insère un nouveau bus dans la base de données."""
        query = """
            INSERT INTO bus (id_event, sens, description, heure_depart, capacite_max)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_bus;
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        bus.id_event,
                        bus.sens,
                        bus.description,
                        bus.heure_depart,
                        bus.capacite_max,
                    ),
                )
                bus.id_bus = cursor.fetchone()["id_bus"]
        return bus
    
    @staticmethod
    def get_by_event(id_event: int) -> Bus | None:
        """Recherche les bus affectés à un évènement."""
        query = "SELECT * FROM bus WHERE id_event = %s"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (id_event,))
                row = cursor.fetchone()
                if row:
                    return Bus.from_dict(row)
                return None

    def get_by_id(id_bus: int) -> Bus | None:
        """Recheche un bus d'après son identifiant"""
        query = "SELECT * FROM bus WHERE id_bus = %s"
        with DBConnection().connection as connection:
            with connection.cursor as cursor:
                cursor.execute(query, (id_bus,))
                row = cursor.fetchone()
                if row:
                    return Bus.from_dict(row)
                return None

    @staticmethod
    def lister_tous() -> list[Bus]:
        """Retourne tous les bus"""
        query = "SELECT * FROM bus ORDER BY id_event"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return [Bus.from_dict(row) for row in rows]
   
    @staticmethod
    def supprimer(id_bus: int) -> bool:
        """Supprime un bus par son ID."""
        query = "DELETE FROM bus WHERE id_bus = %s"
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (id_bus,))
                return cursor.rowcount > 0
