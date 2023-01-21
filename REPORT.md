# Rapport du Projet Web (aka Projet Oueb)

## Code source et adresse du serveur

Code source : [github.com/NathanFallet/ProjetOueb](https://github.com/NathanFallet/ProjetOueb)

Adresse du serveur : [projet-oueb.fr](https://projet-oueb.fr/)

## Choix effectués

Travail en groupe grâce à un git hébergé sur GitHub. Création d’issues, de branches et de Pull Requests pour chaque contribution, afin de collaborer efficacement.

Utilisation de Bootstrap pour la création des pages html.

Utilisation du système d’authentification/utilisateurs intégré à Django, afin de bénéficier du système de session (cookies etc…) ainsi que de sa sécurité (chiffrement des mots de passe etc…)

Création d’une API JSON avec appels via JavaScript, afin de rendre le site plus dynamique, et éviter de rafraichir la page.

Rafraichissement des messages chaque seconde avec Ajax, à défaut de pouvoir utiliser des WebSockets pour envoyer/recevoir des nouveaux messages.

Remplacement des requêtes PUT par des requêtes POST, car Django ne décode pas le body pour les requêtes PUT (ce qui est dommage).

Pour quitter une conversation, il y a deux cas : si on est le propriétaire d’une conversation (le rôle “owner”), ça la supprime. On considère que la personne qui a crée la conversation doit toujours y être sinon la conversation n’a pas lieu d’être. Pour les autres, que ce soit les membres ou les admins, ils quitteront la conversation sans conséquence, c’est-à-dire que la conversation ainsi que ses messages seront toujours dans la conversation.

## Difficultés rencontrées

**Déploiement :** prendre un VPS, un nom de domaine, configurer apache et les DNS n’a pas été un soucis, mais le déploiement de Django en production a été un peu fastidieux.

**Utilisation de l’ORM de Django :** l’ORM (Object Relational Mapping) de Django permet de gagner beaucoup de temps, mais semble ne pas permettre une personnalisation complète des requêtes. Une requête SQL avec un JOIN entre deux tables qui ne sont pas liés par une clé n’est pas directement accessible.

**Utilisation de toLocateString :** les dates étant au format JSON, il a fallu faire un formatage de ces dernières. Il y a énormément de fonctions sur le formatage de date, trouver la fonction la plus pertinente parmi toutes les fonctions proposées était complexe. 

**Url dans JavaScript :** lors d’une requête Ajax, l’url était parfois non trouvée par Django. Ce n’est qu’en vérifiant du côté du serveur que l’on a compris l’erreur : le serveur voulait une url qui finissait par un “/“.
