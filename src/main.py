"""
Point d'entrée principal de l'application de gestion d'événements.
Lance l'interface utilisateur et initialise les services.
"""

from view.menu_principal import MenuPrincipal
from dao.db_connection import DBConnection

def main():
    """
    Fonction principale qui démarre l'application.
    """
    print("=" * 60)
    print("   BIENVENUE - Système de Gestion d'Événements")
    print("=" * 60)

    # Vérifier la connexion à la base de données
    try:
        with DBConnection().connection as conn:
            print("✓ Connexion à la base de données réussie")
    except Exception as e:
        print(f"✗ Erreur de connexion à la base de données : {e}")
        return

    # Lancer le menu principal
    menu = MenuPrincipal()
    menu.afficher()

if __name__ == "__main__":
    main()
