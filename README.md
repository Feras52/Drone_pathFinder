
# Drone Delivery Pathfinder

## Introduction

Système de simulation interactif en Python qui démontre le calcul de chemin optimal pour la livraison par drone. Basée sur l'algorithme A*, l'application permet aux utilisateurs de concevoir des environnements en grille personnalisés avec différents types de terrain (obstacles, zones interdites et terrain difficile) et visualise comment un drone navigue d'un point de départ à une destination en empruntant l'itinéraire le plus efficace.

----------

## Technologies Utilisées

-   **Python** — Langage de programmation principal
    
-   **Pygame** — Bibliothèque graphique pour le rendu de la grille, des éléments d'interface et de l'animation du drone
    
-   **Heapq (Bibliothèque Standard Python)** — Implémentation de la file de priorité pour l'algorithme A*
    
-   **Programmation Orientée Objet (POO)** — Architecture modulaire avec des classes distinctes pour Grid, Cell, Node, AStar, UIManager et Visualizer
    

----------

## Fonctionnalités

-   **Éditeur de Grille Interactif** — Interface de clic pour placer des points de départ, des destinations, des obstacles, des zones interdites et du terrain difficile sur la grille.
    
-   **Redimensionnement Dynamique de la Grille** — Ajustez les dimensions de la grille (5x5 jusqu'à 100x100) à l'aide de curseurs interactifs.
    
-   **Calcul de Chemin A*** — Exécution de l'algorithme de calcul de chemin optimal qui trouve le chemin le moins coûteux en tenant compte des poids du terrain.
    
-   **Types de Terrain** — Plusieurs types de cellules avec des coûts différents :
    
-   Cellules vides (coût : 1)
    
-   Obstacles (infranchissables)
    
-   Zones interdites (zones militaires infranchissables)
    
-   Terrain difficile (coût : 3 — consommation d'énergie élevée)
    
-   **Visualisation du Calcul de Chemin** — Visualisation animée montrant :
    
-   Mise en surbrillance jaune des nœuds explorés pendant la recherche
    
-   Mise en surbrillance violette du chemin optimal final
    
-   Animation du drone se déplaçant fluidement le long du chemin découvert
    
-   **Génération Aléatoire de Carte** — Génération automatique d'environnements aléatoires avec des obstacles et différents types de terrain.
    
-   **Métriques de Performance** — Affichage du coût du chemin et du nombre de nœuds explorés
    

----------

## Processus de Développement

1.  **Planification du Projet & Conception de l'Algorithme** — Début par la recherche et la compréhension de l'algorithme de calcul de chemin A* (formule f = g + h), puis planification de l'architecture globale avec des composants modulaires
    
2.  **Implémentation de l'Algorithme Principal** — Construction de la classe AStar avec la boucle de recherche principale, la fonction heuristique (distance de Manhattan), la comparaison des nœuds pour la file de priorité et la reconstruction du chemin
    
3.  **Développement du Système de Grille** — Création des classes Grid et Cell pour gérer un environnement de grille 2D avec différents types de cellules, des vérifications de navigabilité et la détection des voisins (déplacement à 4 directions)
    
4.  **Mise en Place du Cadre d'Interface Utilisateur** — Implémentation de UIManager avec le système de boutons, la sélection d'outil et les contrôles de curseurs pour le redimensionnement dynamique de la grille ; création des classes Button et NumSlider pour les contrôles interactifs
    
5.  **Moteur de Visualisation** — Développement de la classe Visualizer pour le rendu de la grille, le dessin des types de cellules avec des textures/couleurs personnalisées, l'affichage des nœuds explorés avec animation et le tracé du chemin final
    
6.  **Animation du Drone** — Ajout d'une animation fluide du drone lors de ses déplacements
    
7.  **Boucle Principale de l'Application** — Intégration de tous les composants dans la classe DronePathfinderApp avec la gestion des événements, la gestion des états, la boucle de jeu et le contrôle des FPS
    
8.  **Finitions & Perfectionnement** — Ajout d'images personnalisées pour le drone et les icônes, implémentation d'une visualisation avec code couleur, création d'une section de guide rapide
    

----------

## Ce que J'ai Appris

-   **Maîtrise de l'Algorithme A*** — Compréhension approfondie de la recherche basée sur les heuristiques, de l'importance du choix des heuristiques appropriées (distance de Manhattan pour la grille) et de la façon dont f = g + h équilibre le coût d'exploration avec la proximité de l'objectif
    
-   **Patrons de Conception Orientés Objet** — Application de l'encapsulation et de la modularité en séparant les préoccupations (logique de grille, algorithme, visualisation, interface) en classes indépendantes qui communiquent de manière claire
    
-   **Conception d'Interface Utilisateur Interactive** — Conception de contrôles intuitifs pour des actions complexes (sélection d'outil, manipulation de grille, exécution d'algorithme) avec retour visuel via des états de survol et des indicateurs actifs
    

----------

## Ce qui Peut Être Amélioré

-   **Déplacement à 8 Directions** — Étendre le déplacement à 4 directions (haut/bas/gauche/droite) à 8 directions incluant les diagonales avec des calculs de distance appropriés
    
-   **Recherche Bidirectionnelle** — Implémenter l'A* bidirectionnel (recherche simultanément depuis le départ et l'objectif) pour de meilleures performances sur les grandes grilles
    
-   **Fonctionnalité Sauvegarder/Charger** — Ajouter la possibilité de sauvegarder les configurations de grille personnalisées et de les charger ultérieurement pour les tests
    
-   **Agents Multiples** — Étendre le système pour prendre en charge plusieurs drones effectuant simultanément un calcul de chemin avec évitement de collisions
    
-   **Visualisation 3D** — Passer à des graphismes 3D (en utilisant Pygame 3D ou un autre moteur 3D) pour des scénarios de livraison par drone plus réalistes
    

----------

## Comment Exécuter le Projet

**Prérequis :**

-   Python 3.6 ou supérieur installé sur votre système
    
-   Gestionnaire de paquets pip
    

**Étapes d'Installation :**

1.  **Accédez au répertoire du projet :**
    
2.  **Installez les dépendances :**
    

```bash

pip install pygame


```

3.  **Lancez l'application :**
    

**Guide de Démarrage Rapide (Après le Lancement) :**

1.  Sélectionnez un outil dans la barre latérale gauche :

-   "Set Start" — Marquer le point de départ (vert)
    
-   "Set End" — Marquer la destination (bleu)
    
-   "Add Obstacle" — Placer des murs/obstacles (gris foncé)
    
-   "Difficult Zone" — Marquer un terrain à coût élevé (orange)
    

2.  Cliquez sur la grille pour placer l'élément sélectionné
    
3.  Ajustez la taille de la grille à l'aide des curseurs "grid x" et "grid y" si désiré
    
4.  Cliquez sur "Run A*" pour exécuter l'algorithme de calcul de chemin
    
5.  Observez la visualisation :
    

-   Les cellules jaunes montrent les nœuds explorés
    
-   Le chemin violet indique l'itinéraire optimal
    
-   Le drone animé suit le chemin
    

6.  Utilisez les boutons supplémentaires :

-   "Clear Grid" — Réinitialiser à une grille vide
    
-   "Random Map" — Générer automatiquement un environnement aléatoire

