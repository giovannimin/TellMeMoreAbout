# TellMeMoreAbout

![image](./assets/img/img_banniere.jpg)
[![Python](https://img.shields.io/pypi/pyversions/tensorflow.svg)](https://badge.fury.io/py/tensorflow)


Ce projet est un projet open source, qui a pour but de mettre en évidence des indicateurs de performance 
clés chez les joueurs de football.

L'**objectif principal** à terme est de pouvoir établir des rapports comparatifs des différents joueurs référencés. 

L'**objectif secondaire** est de proposer par une approche de clustering un panel de joueurs à profil fortement 
similaires en prenant en compte des paramètres de recherche *(fourchette d'âge, valeur marchande, championnat, KPI etc.)*.  

L'objectif pour les contributeurs de ce projet est de mettre à profit leurs compétences autour d'un projet orienté 
football, en parfaisant leurs compétences techniques, le tout en collaborant avec d'autres 
passionnés de la communauté sport technologies. 

Les idées pour orienter le projet sont les naturellement les bienvenues.

Pour les contributions, n'hésitez pas à regarder les besoins dans les 
**[Issues](https://github.com/giovannimin/TellMeMoreAbout/issues)** de ce repositories.

### Pour commencer
Pour utiliser ce projet en local :
- Cloner ce repositories avec la commande `git clone https://github.com/giovannimin/TellMeMoreAbout.git`

### Pré-requis
Pour installer les dépendances de ce projet : 2. `pip install requirements.txt`


### Utilisation
Ce projet est destiné à être utilisé via différents modes :
- Une [API](./src/api/app.py) mise a disposition `curl -o ${player_name}_report.png -X GET http://localhost:8000/status/${player_name}`
- Une utilisation locale via la CLI `python3 ./src/main.py $player_name`
- Une utilisation automatisée contrôlée par des bots [X | Twitter](https://twitter.com)
- Une application executable avec Docker `docker-compose -f TellMeMoreAbout/docker_app/docker-compose.yml up --build`


### Exemple d'utilisation 



### Sources des données
Les données utilisées sont issus de méthodes de scrapping. Les sources utilisées sont :
- **[FBRef](https://fbref.com/)** 
- **[TransferMarkt](https://www.transfermarkt.fr/)**

Les autres sources sont les bienvenues, que ce soit à partir d'API ou de données scrappées. 


#### Automatisation 
L'ensemble des actions automatisées sont recensés sur cette section. 
Vous pourrez les trouver dans le repertoire 
[workflows](https://github.com/giovannimin/TellMeMoreAbout/tree/main/.github/workflows). 
- [test.yml](https://github.com/giovannimin/TellMeMoreAbout/tree/main/.github/workflows/test.yml), 
cette action exécute l'ensemble des tests unitaires pytests lors de chaque push sur la branche principale. 
- 

#### Tests unitaires
Les tests unitaires sont exécutés automatiquement lors de chaque push sur la branche principale et les logs ajoutés dans le volume monté sur le conteneur. 
Pour les exécuter manuellement : `python3 -m pytest tests/`

N'hésitez pas à ajouter progressivement les tests unitaires des nouvelles fonctionnalités que vous ajoutez. 


### Contributions

Le projet accueille avec plaisir votre expertise et votre enthousiasme !
Les petites améliorations ou corrections sont toujours appréciées.
N'hésitez pas à soumettre de nouvelles idées de fonctionnalités. 

Pour contribuer au projet **[TellMeMoreAbout](https://github.com/giovannimin/TellMeMoreAbout)**. Vous pouvez :
- Examiner les demandes de **[Pull request](https://github.com/giovannimin/TellMeMoreAbout/pulls)**
- Prendre en charge les **[Issues](https://github.com/giovannimin/TellMeMoreAbout/issues)**
- Nous aider à maintenir les outils de ce projet 


Pour plus d'informations sur les façons dont vous pouvez contribuer à ce projet n'hésitez pas à poser des questions 
sur GitHub, en ouvrant une **[New Issue](https://github.com/giovannimin/TellMeMoreAbout/issues/new)** ou en laissant un message via la **[Discussion](https://github.com/giovannimin/TellMeMoreAbout/discussions/1)**.


Si vous avez besoin de plus d'information sur les contributions open-source,
**[ce guide](https://opensource.guide/how-to-contribute/)** explique pourquoi et comment vous impliquer.

#### Licence
[Apache License 2.0](license)