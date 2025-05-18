# projet-elec3_g5_2025
Repository contenant les fichiers du RaspBerry Pi Pico pour le projet d'électronique 2025 du groupe 5.

## Comment lancer le code ?

Simplement brancher le Pico avec un câble adapté à votre ordinateur, ouvrir Thonny en lancer l'exécution du fichier "main.py".

## Structure de fichiers

Voici la structure actuelle des fichiers :
.
├── ap_templates
│   ├── configured.html
│   ├── index.html
│   ├── redirect.html
│   └── template.html
├── assets
│   ├── app.css
│   ├── app.js
│   ├── back.png
│   ├── key.png
│   ├── logo.png
│   └── question.png
├── Experiments
│   ├── button_test.py
│   ├── main_github.py
│   ├── reset_leds.py
│   ├── test_HC.py
│   ├── wifi_test_2.py
│   └── wifi_test.py
├── main.py
├── phew
│   ├── dns.py
│   ├── __init__.py
│   ├── logging.py
│   ├── server.py
│   └── template.py
├── README.md
├── reset_wifi.py
├── safety.py
├── send_data.py
└── victim_counter.py

### ap_templates/

Contient les fichiers HTML du faux portail de connexion qui sont desservis par le serveur web.

### assets/

D'autres assets du faux portail de connexion.

### Experiments/

Contient des fichiers pour effectuer différents tests.

**button_test.py** : Pour tester le fonctionnement du bouton poussoir sur le PCB.
**main_github.py** : A servi de "au cas où ça foire sur le vrai main", il ne sert à rien.
**reset_leds.py** : Pour éteindre les trois leds quand elles restent allumées après arrêt du code principal.
**test_HC.py** : Script de test pour le capteur de proximité.
**wifi_test_2.py** : Version améliorée de wifi_test.py par ChatGPT.
**wifi_test.py** : Script pour tester une connexion à un réseau Wi_fi.

### phew/

Contient les fichiers du serveur web phew.

### main.py

Fichier principal à exécuter.

### reset_wifi.py

Fichier à exécuter pour réinitialiser les interfaces wifi du Pico. Est également utilisé comme module par main.py.

### safety.py

Module de main.py. Contient toutes les fonctions utilisées par les capteurs et composants assurant la sécurité du dispositif.

### send_data.py

Module contenant la fonction qui enverra les données capturées sur la base de données.

### victim_counter.py

Contient toutes les fonctions sollicitées pour l'affichage du nombre de victimes sur les afficheurs à segments. Est également utilisé comme module.