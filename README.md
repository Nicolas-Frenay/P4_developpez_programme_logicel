# 4_Développez_un_programme_logiciel_en_Python
# Projet 4 : Développez un programme logiciel en Python

Le projet final comporte 3 fichiers python :
- Centre_echencs.py : fichier principale, gérant le front-end et l'affichage du menu. A lancer pour exectuer le programme.
- control.py : fichier contenant le back-end de l'application.
- data_base : fichier gérant la base de donnée utilisant TinyDB.

Vous trouverez deux branches sur github :

La branche "master" comporte le projet final.

La branche "with_json_loading" comporte des fichiers supplémentaires.

Joueurs.json et tournois.json servent à charger plus simplement les informations d'un tournois et de joueurs, pour 
faciliter les testes.

Le code du projet final est toujours present, mais commenté, et quelques instructions ont été rajoutées pour charger les 
informations depuis les fichiers *.json.

Le dossier Tournois contient 2 dossiers : interrpompus et terminés. Interrompus contient le fichier *.json d'un tournois
 non terminé, et Terminés contient le fichier d'un tournois complet. Ils servent pour faciliter les testes de generation
 de rapports.



## Instructions :


1) Installation python :
- Allez sur [https://www.python.org/downloads/](url) , et télécharger la dernière version de python, puis lancez le fichier 
  téléchargé pour l'installer.

2) Télécharger le code :
- Sur le repository github, cliquez sur le bouton "Code", puis "Download ZIP".
- Ensuite décompressez le fichier dans votre dossier de travail.

3) creation environnement virtuel :
- Ouvrez un terminal, puis allez dans votre dossier de travail avec la commande cd.
- Dans le terminal, tapez : ``` python3 -m venv env ```

4) Activer l'environnement virtuel :
  - Si vous êtes sous mac ou linux :
    - tapez : ```source env/bin/activate ```
  - Si vous êtes sous windows :
    - tapez ```env/Scripts/activate.bat```

5) Installation des modules nécessaires :
- dans le terminal, tapez : ```pip install -r requirements.txt```

6) lancer le script :
- dans le terminal tapez : ```python3 Centre_echecs.py```

7)Pour fermer l'environnement virtuel :
- Dans le terminal, tapez : ```deactivate ```


## Validation Flak8 :
- Depuis le terminal, rendez vous dans votre dossier de travail.
- Tappez ```flake8 --format=html --htmldir=flake-report```
- Dans le dossier flake-report nouvellement créé, lancer index.html dans votre navigateur pour voir le rapport d'erreur.

(Attention, flake fera un rapport de tous les fichiers presents dans le dossier, y compris ceux du dossier ENV, je 
conseille de copier les seuls fichiers à analyser dans un dossier à part, et de lancer l'analyse depuis celui-ci, afin 
d'eviter des rapport sur des fichiers "non-python").



## Utilisation :


Le programme affiche un menu textuel dans la fenetre de terminal, taper simplement le chiffre correspondant à votre 
choix, puis appuyer sur la touche <entrée> pour valider.

Dans les cas ou vous créez un nouveau tournois, ou que vous modifiez les informations d'un joueurs, tapez les informations
demandées, puis appuyez sur <entrée>.


