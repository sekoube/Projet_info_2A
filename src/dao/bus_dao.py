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
    def get_by_field(self, field: str, value) -> Bus | None:
        """Retourne un Bus selon un champ donné."""

        # Sécurité : liste blanche des champs autorisés
        allowed_fields = {"id_bus", "id_event", "sens, description", "heure_depart", "capacite_max"}
        if field not in allowed_fields:
            raise ValueError(f"Champ non autorisé : {field}")

        query = f"SELECT * FROM bus WHERE {field} = %s"

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (value,))
                row = cursor.fetchone()

                return Bus.from_dict(row) if row else None


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
