'''
Program: planets.py
Programmer: Corey Walker
EMail: cwalker62@cnm.edu
Date: Nov 30, 2023
Purpose: Creates a set of planet objects to be utilized by Planet Lander

Each Planet has:
        gravity -> float
        atmosphere_color -> (r,g,b)
        ground_color -> (r,g,b)

Each planet also initializes the state variables that will be used
        to track end conditions for that planet's game loop

TODO: Add a sun property for different sized sun sprite (represent closeness)
TODO: Move lander properties into their own class
'''
class Planet():
    def __init__(self,
                 gravity = 0,
                 atmosphere_color = (0,0,0), 
                 ground_color = (0, 0, 0) 
                ):
        self.gravity = gravity
        self.ground_color = ground_color
        self.atmosphere_color = atmosphere_color
        # The planet enviornment holds the lander state
        self.thruster_on = False
        self.is_landed = False
        self.is_crashed = False


def createNewMoon():
     '''
     Creates a new Planet object to simulate the moon

     While the moon isn't a planet, it has:
        - Low gravity
        - Pitch Black Space (no atmosphere)
        - A gray ground
     '''
     moon = Planet(0.03, (0,0,0), (50,50,50))
     return moon

def createNewMars():
     """
     Creates a new Planet object to simulate mars.

     Mars has:
        - Medium gravity
        - Dark Red atmosphere
        - Lighter red ground
     """
     mars = Planet(0.15, (40,0,0), (178,34,34))
     return mars

def createNewJupiter():
     """
     Creates a new Planet object to simulate mars.

     Jupiter has:
        - High gravity
        - Hazy green atmosphere
        - Light Brown ground
     """
     jupiter = Planet(0.5, (65,74,76), (152,116,86))
     return jupiter

if __name__ == '__main__':
     moon1 = createNewMoon()
     print(f"Moon1 crash status: {moon1.is_crashed}")
     moon2 = createNewMoon()
     print(f"Moon2 crash status: {moon2.is_crashed}")

     print(f"Crashing lander on moon1")
     moon1.is_crashed = True
     print(f"Moon1 crash status: {moon1.is_crashed}")
     print(f"Moon2 crash status: {moon2.is_crashed}")