from World import World
from Position import Position
from Organisms import Grass, Sheep, Lynx, Antelope
import os

if __name__ == '__main__':
    pyWorld = World(10, 10)

    pyWorld.addOrganism(Grass(position=Position(xPosition=9, yPosition=9), world=pyWorld))
    pyWorld.addOrganism(Grass(position=Position(xPosition=1, yPosition=1), world=pyWorld))
    pyWorld.addOrganism(Sheep(position=Position(xPosition=2, yPosition=2), world=pyWorld))

    while True: # the game continues forever, and not for an maximum of 50 rounds
        os.system('cls' if os.name == 'nt' else 'clear') # allows the board to refresh in the same place
        print(pyWorld)
        if pyWorld.plagueTurns > 0:
            print(f">>> PLAGA AKTYWNA (Pozostało tur: {pyWorld.plagueTurns}) <<<")
        
        print("Opcje:")
        print("[Enter] Nastepna tura")
        print("[p] Wywolaj plage")
        print("[a] Dodaj organizm")
        print("[q] Wyjdz")
        
        choice = input("Wybierz akcje: ")

        if choice == 'q':
            break
        elif choice == 'p':
            pyWorld.triggerPlague()
        elif choice == 'a':
            xStr = input("Podaj X: ")
            yStr = input("Podaj Y: ")
            typeStr = input("Typ (S=Sheep, G=Grass, R=Lynx, A=Antelope): ")
            
            if xStr.isdigit() and yStr.isdigit(): # convert digit text to integers
                x, y = int(xStr), int(yStr)
                pos = Position(xPosition=x, yPosition=y)
                
                if pyWorld.positionOnBoard(pos) and pyWorld.getOrganismFromPosition(pos) is None:
                    if typeStr == 'S': pyWorld.addOrganism(Sheep(position=pos, world=pyWorld))
                    elif typeStr == 'G': pyWorld.addOrganism(Grass(position=pos, world=pyWorld))
                    elif typeStr == 'R': pyWorld.addOrganism(Lynx(position=pos, world=pyWorld))
                    elif typeStr == 'A': pyWorld.addOrganism(Antelope(position=pos, world=pyWorld))
                else:
                    input("Blad: Pozycja zajeta lub poza plansza. [Enter]")
        else:
            pyWorld.makeTurn()