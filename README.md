The Pacman Projects
===================

### Intro
Back in 2011, I took the original Introduction to Artificial Intelligence online course taught by Peter Norving and Sebastian Thrun. I thoroughly enjoyed all the AI theory we learnt but I desperately needed to apply those to solve problems. That's when I found out about [The Pacman Projects](http://ai.berkeley.edu/project_overview.html) by the [University of California, Berkeley](http://berkeley.edu/).

![Animated gif pacman game](http://ai.berkeley.edu/images/pacman_game.gif)

### Project 1: Search in Pacman
From the [project 1 page](http://ai.berkeley.edu/search.html): *In this project, your Pacman agent will find paths through his maze world, both to reach a particular location and to collect food efficiently. You will build general search algorithms and apply them to Pacman scenarios.*

Some sample scenarios to try with are:

```
$ cd pacman-projects/p1_search

$ python pacman.py -l bigMaze -p SearchAgent -a fn=dfs -z .5
$ python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5

$ python pacman.py -l openMaze -p SearchAgent -a fn=dfs -z .5
$ python pacman.py -l openMaze -p SearchAgent -a fn=bfs -z .5

$ python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
$ python pacman.py -l mediumDottedMaze -p StayEastSearchAgent
$ python pacman.py -l mediumScaryMaze -p StayWestSearchAgent

$ python pacman.py -l trickySearch -p SearchAgent -a fn=bfs,prob=FoodSearchProblem
$ python pacman.py -l trickySearch -p SearchAgent -a fn=astar,prob=FoodSearchProblem,heuristic=foodHeuristic
```

### Project 3: Reinforcement Learning
From the [project 3 page](http://ai.berkeley.edu/reinforcement.html): *In this project, you will implement value iteration and Q-learning. You will test your agents first on Gridworld (from class), then apply them to a simulated robot controller (Crawler) and Pacman.*

Some sample scenarios to try with are:

```
$ cd pacman-projects/p3_reinforcement_learning

$ python gridworld.py -a q -k 100 
$ python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumGrid
$ python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumClassic
```

### Project 4: Ghostbusters
From the [project 4 page](http://ai.berkeley.edu/tracking.html): *Pacman spends his life running from ghosts, but things were not always so. Legend has it that many years ago, Pacman's great grandfather Grandpac learned to hunt ghosts for sport. However, he was blinded by his power and could only track ghosts by their banging and clanging.*

*In this project, you will design Pacman agents that use sensors to locate and eat invisible ghosts. You'll advance from locating single, stationary ghosts to hunting packs of multiple moving ghosts with ruthless efficiency.*

Some sample scenarios to try with are:

```
$ cd pacman-projects/p4_ghostbusters

$ python busters.py
$ python busters.py -p GreedyBustersAgent -l bigHunt
```

### Author
The solutions to the problems originally posted at the Pacman project site were developed by Ramón Argüello ([@monchote](https://github.com/monchote)) back in 2011.
