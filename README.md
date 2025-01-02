# 🎮 SkyHop

Un jeu de plateforme inspiré de Doodle Jump, développé avec Pygame.

## 📋 Description

SkyHop est un jeu de plateforme vertical où vous devez sauter de plateforme en plateforme pour monter le plus haut possible. Collectez des power-ups pour améliorer vos capacités et évitez de tomber !

### 🎯 Fonctionnalités

- **Plateformes dynamiques** : Différents types de plateformes (normales, mobiles)
- **Power-ups** :
  - 🚀 **Super Saut** : Augmente la hauteur de saut (x3)
  - 🔄 **Double Saut** : Permet de sauter deux fois (dure 10 secondes)
  - ⬆️ **Propulsion** : Vous propulse vers le haut (+10)
- **Score** : Système de points basé sur la hauteur atteinte
- **Indicateurs visuels** : Affichage des power-ups actifs et leur durée

## 🎮 Contrôles

- **←/→** : Se déplacer à gauche/droite
- **↑** : Double saut (si activé)
- **ESPACE** : Recommencer après une défaite
- **ESC** : Quitter le jeu

## 🛠️ Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/Arcadiastyx/SkyHop.git
cd SkyHop
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Lancez le jeu :
```bash
python main.py
```

## 📦 Prérequis

- Python 3.8+
- Pygame 2.5.2

## 🎨 Structure du Projet

```
SkyHop/
├── src/
│   ├── entities/
│   │   ├── player.py    # Classe du joueur
│   │   ├── platform.py  # Classes des plateformes
│   │   └── powerup.py   # Classes des power-ups
│   ├── game/
│   │   ├── game.py      # Logique principale du jeu
│   │   └── constants.py # Constantes et configuration
├── assets/
│   ├── sprites/         # Images des sprites
│   └── sky.jpg         # Image de fond
├── main.py             # Point d'entrée du jeu
└── requirements.txt    # Dépendances Python
```

## 🎯 Objectif

Montez le plus haut possible en sautant de plateforme en plateforme. Utilisez les power-ups à votre avantage pour atteindre des hauteurs vertigineuses !

## 🏆 Score

Votre score augmente en fonction de la hauteur atteinte. Les power-ups peuvent vous aider à atteindre des scores plus élevés.

## 💡 Astuces

- Utilisez le double saut avec parcimonie
- Les power-ups se cumulent !
- Gardez un œil sur la durée restante des power-ups
- Les plateformes mobiles peuvent être utiles pour atteindre des endroits difficiles

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
