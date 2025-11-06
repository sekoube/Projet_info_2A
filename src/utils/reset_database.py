import os
import logging
import dotenv
from unittest import mock

# Imports corrigés, selon la structure actuelle de ton projet
from utils.log_decorator import log
from utils.singleton import Singleton
from dao.db_connection import DBConnection

from service.joueur_service import JoueurService


class ResetDatabase(metaclass=Singleton):
    """
    Réinitialisation de la base de données
    """

    @log
    def lancer(self, test_dao=False):
        """Lancement de la réinitialisation des données.
        Si test_dao = True : réinitialisation des données de test
        """
        if test_dao:
            mock.patch.dict(os.environ, {"POSTGRES_SCHEMA": "projet_test_dao"}).start()
            pop_data_path = "data/pop_db_test.sql"
        else:
            pop_data_path = "data/pop_db.sql"

        dotenv.load_dotenv()

        schema = os.environ["POSTGRES_SCHEMA"]

        # Création du schema
        create_schema = f"DROP SCHEMA IF EXISTS {schema} CASCADE; CREATE SCHEMA {schema};"

        # Lecture des fichiers SQL
        with open("data/init_db.sql", encoding="utf-8") as f:
            init_db_as_string = f.read()

        with open(pop_data_path, encoding="utf-8") as f:
            pop_db_as_string = f.read()

        # Exécution SQL
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(create_schema)
                    cursor.execute(init_db_as_string)
                    cursor.execute(pop_db_as_string)
        except Exception as e:
            logging.info(e)
            raise

        # Appliquer le hashage des mots de passe à chaque joueur
        joueur_service = JoueurService()
        for j in joueur_service.lister_tous(inclure_mdp=True):
            joueur_service.modifier(j)

        return True


if __name__ == "__main__":
    ResetDatabase().lancer()
    ResetDatabase().lancer(True)
