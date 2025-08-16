# Testing-Environment Game Hub

This repository provides a simple Python game hub built with [Pygame](https://www.pygame.org/). It includes a landing page where you can select from available games. The first bundled game is the classic **Snake** which supports both keyboard controls and USB controllers like the Sony DualShock 3.

## Requirements
- Python 3
- Pygame

Install dependencies using:

```bash
pip install pygame
```

## Usage
Run the hub with:

```bash
python gamehub.py
```

Use the arrow keys or a connected controller to navigate the menu. Select *Snake* to start the game. During the game, control the snake with either the keyboard or the controller's D-pad/analog stick. After a game over, press Enter or any controller button to return to the hub.

The hub is designed to make it easy to add more games in the future by appending them to the `games` list in `gamehub.py`.
