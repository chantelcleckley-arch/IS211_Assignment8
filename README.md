# IS211 Assignment 8 - Design Patterns

## Overview
This assignment expands the Pig Dice Game from Week 7 by
implementing the Factory and Proxy design patterns.

## Features
- Human versus human gameplay
- Human versus computer gameplay
- Computer versus computer gameplay
- Computer strategy that holds at the lesser of 25
  points or the points needed to reach 100
- Timed gameplay with a 60-second limit
- Winner determined by score when time expires

## Design Patterns

### Factory Pattern
The PlayerFactory class creates either a HumanPlayer
or ComputerPlayer based on the selected player type.

### Proxy Pattern
The TimedGameProxy class wraps the PigGame class
and adds a 60-second time limit.

## Running the Game

Human versus human:
python3 pig.py --player1 human --player2 human

Human versus computer:
python3 pig.py --player1 human --player2 computer

Computer versus computer:
python3 pig.py --player1 computer --player2 computer

Timed game:
python3 pig.py --player1 human --player2 computer --timed

## Testing
Run the tests using:
python3 -m unittest discover -v
