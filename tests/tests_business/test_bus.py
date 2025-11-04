import re
import pytest
from datetime import datetime
import sys
import os
from bus import Bus
# Chemin du projet racine (2 niveaux au-dessus du fichet test)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

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
