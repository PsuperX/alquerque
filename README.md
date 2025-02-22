# Alquerque Minimax

## Implemented

- board state evaluation
- minimax search algorithm for best move with limited depth
- alpha-beta search tree pruning
- minimax search using a transposition table
- support for different players/AIs
- game result stats

## How to use
(Tested using python 3.10.6)

In a terminal run the following commands
``` bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 main.py
```

In the main menu select with AI each player should use.
Once the AIs have been selected the 'Start' button will appear.

Non-human AIs play automatically

When using human moves click on one of the green hightlighted pieces and then the place you want the piece to move to.

If the window is too big the size of the window can be adjusted in [constants.py](constants.py) "CELL_SIZE" field.

[test.py](test.py) contains examples on how to use the program without a gui.
The example creates a tournment between all implemented algorithms with different settings.
