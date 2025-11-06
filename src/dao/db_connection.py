# dao/db_connection.py
import os
import dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from src.utils.singleton import Singleton


class DBConnection(metaclass=Singleton):
    """
    Classe de connexion à la base de données
    Elle permet de n'ouvrir qu'une seule et unique connexion
    """

    def __init__(self):
        """Ouverture de la connexion"""
        dotenv.load_dotenv()

        self.__connection = psycopg2.connect(
            host=os.environ["POSTGRES_HOST"],
            port=os.environ["POSTGRES_PORT"],
            database=os.environ["POSTGRES_DATABASE"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            options=f"-c search_path={os.environ['POSTGRES_SCHEMA']}",
            cursor_factory=RealDictCursor,
        )

        self.__connection.autocommit = True

    @property
    def connection(self):
        return self.__connection

# tests/test_utilisateur.py
from src.dao.db_connection import DBConnection
from datetime import datetime

def test_ajout_utilisateur():
    try:
        conn = DBConnection().connection
        with conn.cursor() as cursor:
            # Exemple d'insertion
            cursor.execute("""
                INSERT INTO projet.utilisateur (nom, prenom, email, mot_de_passe, role)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_utilisateur;
            """, ("Dupont", "Alice", "alice.test@example.com", "motdepasse123", False))

            id_utilisateur = cursor.fetchone()["id_utilisateur"]
            print(f"[OK] Utilisateur inséré avec ID : {id_utilisateur}")

            # Vérification : récupérer l'utilisateur ajouté
            cursor.execute("SELECT * FROM projet.utilisateur WHERE id_utilisateur = %s;", (id_utilisateur,))
            utilisateur = cursor.fetchone()
            print("Données récupérées :", utilisateur)

    except Exception as e:
        print("[ERREUR] Impossible d'ajouter l'utilisateur :", e)

if __name__ == "__main__":
    test_ajout_utilisateur()
