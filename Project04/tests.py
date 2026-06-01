import pytest
from World import World
from Position import Position
from Organisms.Grass import Grass
from Organisms.Sheep import Sheep
from Organisms.Lynx import Lynx
from Organisms.Antelope import Antelope
from ActionEnum import ActionEnum

# ==============================================================================
# PLAGUE AND WORLD LOGIC
# ==============================================================================

def test_plague_halves_life():
	"""Checks if the plaugue correctly reduces life by half."""
	world = World(10, 10)
	sheep = Sheep(position=Position(xPosition=0, yPosition=0), world=world)
	sheep.liveLength = 20
	world.addOrganism(sheep)

	world.triggerPlague()

	assert sheep.liveLength == 10
	assert world.plagueTurns == 2


def test_manual_addition_logic():
	"""Checks if manual addition of an organism works correctly."""
	world = World(10, 10)
	pos = Position(xPosition=5, yPosition=5)
	
	assert world.getOrganismFromPosition(pos) is None
	world.addOrganism(Lynx(position=pos, world=world))
	
	org = world.getOrganismFromPosition(pos)
	assert org is not None
	assert org.sign == 'R'


def test_world_sorting_by_initiative():
	"""Checks is the world properly sorts organism by initiative in descending order."""
	world = World(5, 5)
	grass = Grass(position=Position(xPosition=0, yPosition=0), world=world)
	antelope = Antelope(position=Position(xPosition=1, yPosition=1), world=world)
	lynx = Lynx(position=Position(xPosition=2, yPosition=2), world=world)

	world.addOrganism(grass)
	world.addOrganism(antelope)
	world.addOrganism(lynx)

	assert world.organisms[0].sign == 'R'
	assert world.organisms[1].sign == 'A'
	assert world.organisms[2].sign == 'G'


# ==============================================================================
# INTERACTIONS BETWEEN LYNX AND ANTELOPE
# ==============================================================================

def test_lynx_attacks_and_kills_antelope():
	"""Lynx attacks antelope and should kill it."""
	world = World(2, 1)
	lynx = Lynx(position=Position(xPosition=0, yPosition=0), world=world)
	antelope = Antelope(position=Position(xPosition=1, yPosition=0), world=world)
	
	world.addOrganism(lynx)
	world.addOrganism(antelope)

	actions = lynx.move()
    # if it does not find anything, returns none. Otherwise, searches for the action of deleting a.organism.
	remove_action = next((a for a in actions if a.action == ActionEnum.A_REMOVE and a.organism == antelope), None)
	
	assert remove_action is not None


def test_lynx_attacks_stronger_antelope():
	"""Lynx attacks a stronger Antelope and should lose and die."""
	world = World(2, 1)
	lynx = Lynx(position=Position(xPosition=0, yPosition=0), world=world)
	antelope = Antelope(position=Position(xPosition=1, yPosition=0), world=world)
	antelope.power = 10
	
	world.addOrganism(lynx)
	world.addOrganism(antelope)

	actions = lynx.move()
	remove_action = next((a for a in actions if a.action == ActionEnum.A_REMOVE and a.organism == lynx), None)
	
	assert remove_action is not None


def test_antelope_flees_from_lynx():
	"""Antelope sees lynx and flees 2 squares in the opposite direction."""
	world = World(10, 10)
	antelope = Antelope(position=Position(xPosition=5, yPosition=5), world=world)
	lynx = Lynx(position=Position(xPosition=4, yPosition=5), world=world)
	
	world.addOrganism(antelope)
	world.addOrganism(lynx)

	actions = antelope.move()
	move_action = next((a for a in actions if a.action == ActionEnum.A_MOVE), None)
	
	assert move_action is not None
	assert move_action.position is not None
	assert move_action.position.x == 7
	assert move_action.position.y == 5


def test_antelope_attacks_when_cannot_flee():
	"""Antelope is in the corner of the map, and cannot flee, so it desperately attacks!"""
	world = World(10, 10)
	antelope = Antelope(position=Position(xPosition=0, yPosition=0), world=world)
	lynx = Lynx(position=Position(xPosition=1, yPosition=0), world=world)
	
	world.addOrganism(antelope)
	world.addOrganism(lynx)

	actions = antelope.move() # gets the battle plan of the antelope (does not change position yet)
	move_action = next((a for a in actions if a.action == ActionEnum.A_MOVE), None) # searches for the action when an animal wants to change its coordinates
	
	assert move_action is not None
	assert move_action.position is not None
    # The move action should target the coordinates of Lynx
	assert move_action.position.x == 1 
	assert move_action.position.y == 0


# ==============================================================================
# BEHAVIOUR AND MOVEMENT OF ANTELOPE
# ==============================================================================

def test_antelope_flees_diagonal():
	"""Checks escape route of Antelope when Lynx is on a diogonal."""
	world = World(10, 10)
	antelope = Antelope(position=Position(xPosition=5, yPosition=5), world=world)
	lynx = Lynx(position=Position(xPosition=4, yPosition=4), world=world)
	
	world.addOrganism(antelope)
	world.addOrganism(lynx)

	actions = antelope.move()
	move_action = next((a for a in actions if a.action == ActionEnum.A_MOVE), None)
	
	assert move_action is not None
	assert move_action.position is not None
	assert move_action.position.x == 7
	assert move_action.position.y == 7


def test_antelope_normal_movement_no_lynx():
	"""When there is no Lynx, antelope acts like a sheep"""
	world = World(2, 1)
	antelope = Antelope(position=Position(xPosition=0, yPosition=0), world=world)
	world.addOrganism(antelope)

	actions = antelope.move()
	move_action = next((a for a in actions if a.action == ActionEnum.A_MOVE), None)
	
	assert move_action is not None
	assert move_action.position is not None
	assert move_action.position.x == 1
	assert move_action.position.y == 0


def test_position_equality_logic():
	"""Simply checks if Positions objects correctly compare their coordinates."""
	p1 = Position(xPosition=4, yPosition=2)
	p2 = Position(xPosition=4, yPosition=2)
	p3 = Position(xPosition=1, yPosition=2)

	assert p1 == p2
	assert p1 != p3


# ==============================================================================
# AGING, PROPAGATION AND ROUNDS
# ==============================================================================

def test_lynx_power_increases_every_turn():
	"""Checks if the power of Lynx is incremented by 1 each round."""
	world = World(5, 5)
	lynx = Lynx(position=Position(xPosition=0, yPosition=0), world=world)
	world.addOrganism(lynx)
	
	initial_power = lynx.power
    # We need to make Pylance sure that the value is not None
	assert initial_power is not None
	
	world.makeTurn()
	
	assert lynx.power == initial_power + 1


def test_lynx_dies_of_old_age():
	"""Checks if the lynx dies if his liveLength drops below 1."""
	world = World(5, 5)
	lynx = Lynx(position=Position(xPosition=0, yPosition=0), world=world)
	lynx.liveLength = 1
	world.addOrganism(lynx)

	world.makeTurn()

	assert len(world.organisms) == 0


def test_antelope_dies_of_old_age():
	"""Checks if antelope dies of old age after its life finishes."""
	world = World(5, 5)
	antelope = Antelope(position=Position(xPosition=0, yPosition=0), world=world)
	antelope.liveLength = 1
	world.addOrganism(antelope)

	world.makeTurn()

	assert len(world.organisms) == 0


def test_lynx_reproduction_logic():
	"""Lynx has enough power and free square nearby, so it should reproduce."""
	world = World(2, 2)
	lynx = Lynx(position=Position(xPosition=0, yPosition=0), world=world)
	lynx.power = 14
	world.addOrganism(lynx)

	actions = lynx.action()
	add_action = next((a for a in actions if a.action == ActionEnum.A_ADD), None)
	
	assert add_action is not None
	assert lynx.power == 7.0


def test_antelope_reproduction_logic():
	"""Antelope has enough power and free square nearby, so it should reproduce."""
	world = World(2, 2)
	antelope = Antelope(position=Position(xPosition=0, yPosition=0), world=world)
	antelope.power = 6
	world.addOrganism(antelope)

	actions = antelope.action()
	add_action = next((a for a in actions if a.action == ActionEnum.A_ADD), None)
	
	assert add_action is not None
	assert antelope.power == 3.0