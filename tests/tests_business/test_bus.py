import re
import pytest
from datetime import datetime
from business_object.bus import Bus


# ========================== Tests de levée d'erreurs ==========================
@pytest.mark.parametrize(
    'params, erreur, message_erreur',
    [
        ({'id_event': '', 'sens': 'Aller', 'description': ['Bruz'], 'heure_depart': "10:00"},
        ValueError, "L'identifiant de l'évènement doit être renseigné"),
        ({'id_event': '1234', 'sens': "", 'description': ['direct'], 'heure_depart': "10:00"},
        ValueError, "Le sens ne peut pas être vide"),
        ({'id_event': '1234', 'sens': 'vers ENSAI', 'description': ['direct'], 'heure_depart': "10:00"},
        ValueError, "Le sens doit être 'Aller' ou 'Retour'"),
        ({'id_event': '1234', 'sens': "Retour", 'description': [""], 'heure_depart': "10:00"},
        ValueError, "Les arrêts intermédiaires doivent être renseignés, sinon écrire ['direct']"),
    ]
)

def test_bus_erreurs(params, erreur, message_erreur):
    """Vérifie que les mauvaises valeurs lèvent les erreurs appropriées"""
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        Bus(**params)

# ========================== Tests de création valide ==========================
@pytest.mark.parametrize(
    'params',
    [
        {'id_event': '1234', 'sens': "Aller", 'description': ["direct"], 'heure_depart': "10:00"},
        {'id_event': '5678', 'sens': "Retour", 'description': ["Bruz"], 'heure_depart': "10:00"}    
    ]
)

def test_bus_creation_valide(params):
    """Vérifie la création correcte des bus et l'assignation des attributs"""
    bus_cour = Bus(**params)
    for key, value in params.items():
        assert getattr(bus_cour, key) == value
    # Vérifie que l'heure de départ est bien un datetime
    assert isinstance(bus_cour.heure_depart, datetime)


"""
@pytest.fixture
def bus_instance():
    return Bus(
        id_bus=200,
        id_event=111,
        sens="Retour",
        description="Bus de l'Ensai vers Chartres",
        heure_depart="18:45")


class TestBus:

    def test_bus_init(self, bus_instance):
        assert bus_instance.id_bus == 200
        assert bus_instance.id_event == 111
        assert bus_instance.sens == "Retour"
        assert bus_instance.description == "Bus de l'Ensai vers Chartres"
        assert bus_instance.heure_depart == "18:45"
"""