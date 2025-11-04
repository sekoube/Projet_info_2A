"""
Module implémentant le pattern Singleton via une métaclasse.
Le Singleton garantit qu'une classe n'a qu'une seule instance dans toute l'application.
"""


class Singleton(type):
    """
    Métaclasse implémentant le pattern Singleton.
    
    Toute classe utilisant cette métaclasse ne pourra avoir qu'une seule instance.
    Les appels ultérieurs au constructeur retourneront toujours la même instance.
    
    Utilisation:
    ------------
    class MaClasse(metaclass=Singleton):
        def __init__(self):
            # Votre code ici
            pass
    
    # Première instanciation : crée l'objet
    obj1 = MaClasse()
    
    # Deuxième instanciation : retourne le même objet
    obj2 = MaClasse()
    
    # obj1 et obj2 sont la même instance
    assert obj1 is obj2  # True
    """
    
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        """
        Contrôle la création d'instances.
        Si une instance existe déjà, la retourne.
        Sinon, en crée une nouvelle et la stocke.
        
        cls: La classe à instancier
        *args, **kwargs: Arguments du constructeur
        
        return: L'instance unique de la classe
        """
        if cls not in cls._instances:
            # Première instanciation : crée l'objet
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        
        return cls._instances[cls]
    
    @classmethod
    def reset_instances(cls):
        """
        Réinitialise toutes les instances (utile pour les tests).
        À utiliser avec précaution en production.
        """
        cls._instances.clear()