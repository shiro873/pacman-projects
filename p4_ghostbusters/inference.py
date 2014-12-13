# inference.py
# ------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
import random
import busters
import game

class InferenceModule:
  """
  An inference module tracks a belief distribution over a ghost's location.
  This is an abstract class, which you should not modify.
  """
  
  ############################################
  # Useful methods for all inference modules #
  ############################################
  
  def __init__(self, ghostAgent):
    "Sets the ghost agent for later access"
    self.ghostAgent = ghostAgent
    self.index = ghostAgent.index

  def getJailPosition(self):
     return (2 * self.ghostAgent.index - 1, 1)
    
  def getPositionDistribution(self, gameState):
    """
    Returns a distribution over successor positions of the ghost from the given gameState.
    
    You must first place the ghost in the gameState, using setGhostPosition below.
    """
    ghostPosition = gameState.getGhostPosition(self.index) # The position you set
    actionDist = self.ghostAgent.getDistribution(gameState)
    dist = util.Counter()
    for action, prob in actionDist.items():
      successorPosition = game.Actions.getSuccessor(ghostPosition, action)
      dist[successorPosition] = prob
    return dist
  
  def setGhostPosition(self, gameState, ghostPosition):
    """
    Sets the position of the ghost for this inference module to the specified
    position in the supplied gameState.
    """
    conf = game.Configuration(ghostPosition, game.Directions.STOP)
    gameState.data.agentStates[self.index] = game.AgentState(conf, False)
    return gameState
  
  def observeState(self, gameState):
    "Collects the relevant noisy distance observation and pass it along."
    distances = gameState.getNoisyGhostDistances()
    if len(distances) >= self.index: # Check for missing observations
      obs = distances[self.index - 1]
      self.observe(obs, gameState)
      
  def initialize(self, gameState):
    "Initializes beliefs to a uniform distribution over all positions."
    # The legal positions do not include the ghost prison cells in the bottom left.
    self.legalPositions = [p for p in gameState.getWalls().asList(False) if p[1] > 1]   
    self.initializeUniformly(gameState)
    
  ######################################
  # Methods that need to be overridden #
  ######################################
  
  def initializeUniformly(self, gameState):
    "Sets the belief state to a uniform prior belief over all positions."
    pass
  
  def observe(self, observation, gameState):
    "Updates beliefs based on the given distance observation and gameState."
    pass
  
  def elapseTime(self, gameState):
    "Updates beliefs for a time step elapsing from a gameState."
    pass
    
  def getBeliefDistribution(self):
    """
    Returns the agent's current belief state, a distribution over
    ghost locations conditioned on all evidence so far.
    """
    pass

class ExactInference(InferenceModule):
  """
  The exact dynamic inference module should use forward-algorithm
  updates to compute the exact belief function at each time step.
  """
  
  def initializeUniformly(self, gameState):
    "Begin with a uniform distribution over ghost positions."
    self.beliefs = util.Counter()
    for p in self.legalPositions: self.beliefs[p] = 1.0
    self.beliefs.normalize()
  
  def observe(self, observation, gameState):
    """
    Updates beliefs based on the distance observation and Pacman's position.
    
    The noisyDistance is the estimated manhattan distance to the ghost you are tracking.
    
    The emissionModel below stores the probability of the noisyDistance for any true 
    distance you supply.  That is, it stores P(noisyDistance | TrueDistance).

    self.legalPositions is a list of the possible ghost positions (you
    should only consider positions that are in self.legalPositions).

    A correct implementation will handle the following special case:
      *  When a ghost is captured by Pacman, all beliefs should be updated so
         that the ghost appears in its prison cell, position self.getJailPosition()

         You can check if a ghost has been captured by Pacman by
         checking if it has a noisyDistance of None (a noisy distance
         of None will be returned if, and only if, the ghost is
         captured).
         
    """
    noisyDistance = observation
    emissionModel = busters.getObservationDistribution(noisyDistance)
    pacmanPosition = gameState.getPacmanPosition()
    
    #print "NOISY DISTANCE", noisyDistance
    #print "EMISSION MODEL", emissionModel
    #print "PACMAN POSITION", pacmanPosition
    
    "*** YOUR CODE HERE ***"
    # Replace this code with a correct observation update
    # Be sure to handle the jail.
    allPossible = self.beliefs
    for p in self.legalPositions:
      trueDistance = util.manhattanDistance(p, pacmanPosition)
      if emissionModel[trueDistance] > 0:
      	allPossible[p] = allPossible[p]*emissionModel[trueDistance]
      else:
      	allPossible[p] = 0
    allPossible.normalize()
        
    "*** YOUR CODE HERE ***"
    self.beliefs = allPossible
    
  def elapseTime(self, gameState):
    """
    Update self.beliefs in response to a time step passing from the current state.
    
    The transition model is not entirely stationary: it may depend on Pacman's
    current position (e.g., for DirectionalGhost).  However, this is not a problem,
    as Pacman's current position is known.

    In order to obtain the distribution over new positions for the
    ghost, given its previous position (oldPos) as well as Pacman's
    current position, use this line of code:

      newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, oldPos))

    Note that you may need to replace "oldPos" with the correct name
    of the variable that you have used to refer to the previous ghost
    position for which you are computing this distribution.

    newPosDist is a util.Counter object, where for each position p in self.legalPositions,
    
    newPostDist[p] = Pr( ghost is at position p at time t + 1 | ghost is at position oldPos at time t )

    (and also given Pacman's current position).  You may also find it useful to loop over key, value pairs
    in newPosDist, like:

      for newPos, prob in newPosDist.items():
        ...

    As an implementation detail (with which you need not concern
    yourself), the line of code above for obtaining newPosDist makes
    use of two helper methods provided in InferenceModule above:

      1) self.setGhostPosition(gameState, ghostPosition)
          This method alters the gameState by placing the ghost we're tracking
          in a particular position.  This altered gameState can be used to query
          what the ghost would do in this position.
      
      2) self.getPositionDistribution(gameState)
          This method uses the ghost agent to determine what positions the ghost
          will move to from the provided gameState.  The ghost must be placed
          in the gameState with a call to self.setGhostPosition above.
    """
    
    "*** YOUR CODE HERE ***"
    # Remove this return call
    newBeliefs = util.Counter()
    for oldPos in self.legalPositions:
    	newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, oldPos))
    	for newPos, prob in newPosDist.items():
    		#print "oldPos: ", oldPos, "oldBelief", self.beliefs[oldPos], " newPos: ", newPos, " prob: ", prob
    		newBeliefs[newPos] += self.beliefs[oldPos] * prob
    		#print "new belief", newBeliefs[newPos]
    newBeliefs.normalize()
    
    self.beliefs = newBeliefs

  def getBeliefDistribution(self):
    return self.beliefs
