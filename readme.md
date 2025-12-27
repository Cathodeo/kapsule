# kapsule

WIP reimplementation (again) of **xmonka**, the card/monster battler I tried before in Elixir, Ruby and FastBasic.  
This time in Python.

Right now it's a prototype focused on the core systems:  
monsters, deck building, turn flow, hand management, attacks.

The goal is to get a fully playable CLI version first, without graphics.  
Once the battle loop and card interactions feel solid enough, the plan is to move to a Pygame UI.

## Current state

- Monster roster generation working (randomized teams, one active)
- Turn system and basic actions in place
- Deck + hand logic being implemented

## Next steps

- Finish card draw / play flow
- Connect attacks and boosters to real effects
- Make it fully playable end-to-end in terminal
- After that, start the graphical UI with Pygame

## Running

```bash
python3 main.py
