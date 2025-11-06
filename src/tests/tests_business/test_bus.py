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
    'params, sens_attendu',
    [
        (
            {'id_event': '1234', 'sens': "Aller", 'description': ["direct"], 'heure_depart': "10:00"},
            True
        ),
        (
            {'id_event': '5678', 'sens': "Retour", 'description': ["Bruz"], 'heure_depart': "18:30"},
            False
        ),
    ]
)
def test_bus_creation_valide(params, sens_attendu):
    """Vérifie la création correcte des bus et l'assignation des attributs"""
    bus_cour = Bus(**params)
    
    # Vérifie que les attributs correspondent aux paramètres
    assert bus_cour.id_event == params['id_event']
    assert bus_cour.sens == sens_attendu  # Vérifie le booléen
    assert bus_cour.description == params['description']
    
    # Vérifie que l'heure de départ est bien un datetime
    assert isinstance(bus_cour.heure_depart, datetime)
    
    # Vérifie que l'heure correspond à celle entrée
    heure_attendue = datetime.strptime(params['heure_depart'], "%H:%M")
    assert bus_cour.heure_depart.hour == heure_attendue.hour
    assert bus_cour.heure_depart.minute == heure_attendue.minute
    
    # Vérifie que id_bus est None par défaut
    assert bus_cour.id_bus is None

