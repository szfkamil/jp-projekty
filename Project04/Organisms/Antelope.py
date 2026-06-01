from .Animal import Animal
from Action import Action
from ActionEnum import ActionEnum
from Position import Position
import random

class Antelope(Animal):

    # Polymorphism magic to create children
	def __init__(self, antelope=None, position=None, world=None):
		super(Antelope, self).__init__(antelope, position, world)

	def clone(self):
		return Antelope(self, None, None)

    # Override parameters
	def initParams(self):
		self.power = 4
		self.initiative = 3
		self.liveLength = 11
		self.powerToReproduce = 5
		self.sign = 'A'

    # The distinct instinct for the movement of the Antelope
	def move(self):
		result = []
		
		
		if self.world is None or self.position is None:
			return result

		world_ref = self.world
		current_pos = self.position
		
		neighbors = world_ref.getNeighboringPositions(current_pos)
		lynxFound = None

        # Scanning the surroundings to see if 'R' (lynx) is nearby
		for pos in neighbors:
			org = world_ref.getOrganismFromPosition(pos)
			if org is not None and org.sign == 'R':
				# Additional safeguard for Lynx's position to ensure proper coordinates
				if org.position is not None:
					lynxFound = org
					break

        # Check if R is found and if its position is safely defined
		if lynxFound is not None and lynxFound.position is not None:
			dx = current_pos.x - lynxFound.position.x
			dy = current_pos.y - lynxFound.position.y

            # Normalization of movement vectors
			fleeDx = 1 if dx > 0 else (-1 if dx < 0 else 0)
			fleeDy = 1 if dy > 0 else (-1 if dy < 0 else 0)

			fleeX = current_pos.x + (fleeDx * 2)
			fleeY = current_pos.y + (fleeDy * 2)
			fleePos = Position(xPosition=fleeX, yPosition=fleeY)

            # Antelope flees to the empty position
			if world_ref.positionOnBoard(fleePos) and world_ref.getOrganismFromPosition(fleePos) is None:
				result.append(Action(ActionEnum.A_MOVE, fleePos, 0, self))
				self.lastPosition = current_pos
			else: # Position is not on board, so antelope has to attack
				result.append(Action(ActionEnum.A_MOVE, lynxFound.position, 0, self)) # moves onto position of lynx
				self.lastPosition = current_pos
				result.extend(lynxFound.consequences(self)) # lynx and antelope fight
		else: # No lynx found, so antelope act like a sheep
			freePositions = world_ref.filterPositionsWithoutAnimals(neighbors)
			if freePositions:
				newPosition = random.choice(freePositions)
				result.append(Action(ActionEnum.A_MOVE, newPosition, 0, self))
				self.lastPosition = current_pos
				metOrganism = world_ref.getOrganismFromPosition(newPosition)
				if metOrganism is not None: # if the position has grass on it, it 'fights' it
					result.extend(metOrganism.consequences(self))

		return result