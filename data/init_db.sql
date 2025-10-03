DROP SCHEMA IF EXISTS projet CASCADE;
CREATE SCHEMA projet;

CREATE TABLE projet.utilisateur (
    id_utilisateur SERIAL PRIMARY KEY,
    pseudo         VARCHAR(50),
    nom            VARCHAR(50),
    prenom         VARCHAR(50),
    email          VARCHAR(100) UNIQUE,
    mot_de_passe   VARCHAR(100),
    role           VARCHAR(20) 
                                );

-- Création de la table admin
CREATE TABLE projet.administrateur (
    id_admin      SERIAL PRIMARY KEY,
    id_utilisateur INT NOT NULL UNIQUE,
    FOREIGN KEY (id_utilisateur) 
        REFERENCES projet.utilisateur(id_utilisateur) 
        ON DELETE CASCADE
);  -- si on supprimes un utilisateur dans utilisateur, alors la ligne correspondante est automatiquement supprimée dans admin

-- Création de la table evenement
CREATE TABLE projet.evenement (
    id_event                SERIAL PRIMARY KEY,
    titre                   VARCHAR(100) NOT NULL,
    description_evenement   TEXT,
    lieu                    VARCHAR(100) NOT NULL,
    date_evenement          DATE NOT NULL,
    capacite_max            INT CHECK (capacite_max > 0), -- on refuse la création d'un évènement vide
    created_by              INT NOT NULL REFERENCES projet.utilisateur(id_utilisateur) ON DELETE CASCADE,
    created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tarif                   NUMERIC(10,2) CHECK (tarif >= 0)
);

-- Création de la table bus
CREATE TABLE projet.bus (
    id_bus                  SERIAL PRIMARY KEY,
    date_evenement          DATE NOT NULL,
    sens                    VARCHAR(6),
    arrets                  VARCHAR(50),
    capacite_max            INT NOT NULL,
    evenement               INT NOT NULL REFERENCES projet.evenement(id_event) ON DELETE CASCADE,
    created_by              INT NOT NULL REFERENCES projet.administrateur(id_admin),
-- participants est elle même une liste, faire une table d'association ?
)
