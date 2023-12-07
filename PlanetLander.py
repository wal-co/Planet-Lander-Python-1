"""
WalkerFinal.py
Programmer: Corey Walker
EMail: CWalker62@cnm.edu
Purpose: A simple game that simulates trying to safely land on other celestial
    bodies. This game was programmed to fulfill the requirements for CNM CIS1250
    Python 1.

The game settings are easily changed within the settings.py file and can be changed

TODO: Comment all code according to sylabus specifications
TODO: Add star sprites in the upper portion of planet and all around left orbit
TODO: Add a timer in the ui to see how long you take to land (or can stay in bounds)

"""
import arcade, arcade.gui, os

import planets
import scoreKeeping as sk
from settings import *


class InFlightView(arcade.View):
    '''
    InFlightView cotains the main game loop view and runs until:
        - lander sprite's y location is drawn at or below "ground level"
        - lander sprite's y location is drawn above the height of the screen
    '''
    def __init__(self, planet = planets.createNewMoon()):
        self.currentPlanet = planet
      
        # call the window's init method
        super().__init__()

    def setup(self):
        '''
        Paint the window the color of the world atmosphere. 

        Populate the world with two sets of sprites that will be "stacked" on 
        top of each other and update at the same rate. 
        
        Each sprite starts toward the top of the screen and starts falling
        '''
        arcade.set_background_color(self.currentPlanet.atmosphere_color)

        # Load lander without flame sprite and put it on the screen
        self.thrusterOffLanderList = arcade.SpriteList()
        spritePath = os.path.join('./Resources', 'lander_off.PNG')
        self.thrusterOffSprite = arcade.Sprite(spritePath, 0.1)
        self.thrusterOffSprite.center_x = SCREEN_WIDTH/2
        self.thrusterOffSprite.center_y = SCREEN_HEIGHT - self.thrusterOffSprite.height/2
        self.thrusterOffSprite.change_y = -1
        self.thrusterOffLanderList.append(self.thrusterOffSprite)


        # Load a lander with flame and put it on the screen
        self.thrusterOnLanderList = arcade.SpriteList()
        spritePath = os.path.join('./Resources', 'lander_on.PNG')
        self.thrusterOnSprite = arcade.Sprite(spritePath, 0.1)
        self.thrusterOnSprite.center_x = SCREEN_WIDTH/2
        self.thrusterOnSprite.center_y = SCREEN_HEIGHT - self.thrusterOnSprite.height/2
        self.thrusterOnSprite.change_y = -1
        self.thrusterOnLanderList.append(self.thrusterOnSprite)

        # make a list of lander sprite lists.
        self.landers = [self.thrusterOnLanderList, self.thrusterOffLanderList]


    def on_update(self, delta_time):
        '''
        Each time the game loop updates, the game checks the following scenerios:
            - The lander has already landed 
            - Thrusters activation state
            - If the lander has passed the ground
                - Updates lifetime stats if it has
        '''

        if not self.currentPlanet.is_landed:
            # Both sprites y-coords need to be updated at the same time
            if self.currentPlanet.thruster_on:
                for landerList in self.landers:
                    landerList[0].change_y = landerList[0].change_y + 0.1
            else:
                for landerList in self.landers:
                    landerList[0].change_y = landerList[0].change_y - self.currentPlanet.gravity

            # Check if the bottom of the sprite is at ground level (or past it)
            if self.thrusterOffSprite.center_y - self.thrusterOffSprite.height/2 < SCREEN_HEIGHT * .1:
                # Check if it was travelling too fast
                # TODO: move score saving into landedScreenView, it makes more sense to handle it there
                if self.thrusterOffSprite.change_y < - DIFFICULTY_SETTING:
                    # Update crash scores
                    try:
                        scores = sk.getCurrentScores()
                        total_crashed = scores.get('crashed')
                        total_crashed = str(int(total_crashed) + 1)
                        scores['crashed'] = total_crashed
                    except:
                        # The save file must be missing or corrupted
                        # Create new dict so a new save file can be made
                        scores = {'safe': '0',
                                  'crashed': '1',
                                  'left': '0'}
                    sk.updateScores(scores)
                    self.currentPlanet.is_crashed = True
                else:
                    # update safe score
                    try:
                        scores = sk.getCurrentScores()
                        total_safe = scores.get('safe')
                        total_safe = str(int(total_safe) + 1)
                        scores['safe'] = total_safe
                    except:
                        # The save file must be missing or corrupted
                        # Create new dict so a new save file can be made
                        scores = {'safe': '1',
                                  'crashed': '0',
                                  'left': '0'}
                    sk.updateScores(scores)

                # Stop the sprites from moving
                # this smooths out the animation transitioning to the end screen
                for landerList in self.landers:
                    landerList[0].change_y = 0
                self.currentPlanet.is_landed = True
            # Send them into outer space if they fly off the top of the screen
            elif self.thrusterOffSprite.center_y - self.thrusterOffSprite.height/2 > SCREEN_HEIGHT:
                gameview = flewHomeView(self.currentPlanet)
                self.window.show_view(gameview)
        else:
            # Go to the end game screen
            game_view = landedScreenView(self.currentPlanet)
            self.window.show_view(game_view)
        
        self.thrusterOffLanderList.update()
        self.thrusterOnLanderList.update()


    def on_key_press(self, key, modifiers):
        '''Toggle the thruster state when the spacebar is pressed'''
        if key == arcade.key.SPACE:
            self.currentPlanet.thruster_on = not self.currentPlanet.thruster_on
        

    
    def on_key_release(self, key, modifiers):
        '''Toggle thrusters off when spacebar is released'''
        if key == arcade.key.SPACE: self.currentPlanet.thruster_on = False

    def on_draw(self):
        '''render the screen'''
        self.clear()
        # Determine which lander sprite to draw
        if self.currentPlanet.thruster_on: self.thrusterOnLanderList.draw()
        else: self.thrusterOffLanderList.draw()
        # Draw a line for the ground
        arcade.draw_line(0, SCREEN_HEIGHT * .1, SCREEN_WIDTH, SCREEN_HEIGHT * .1,
                         self.currentPlanet.ground_color, 5)
        

class flewHomeView(arcade.View):
    '''
    flewHomeView is a fail condition end screen that animates the lander
        flying off into space and provides a button to take the user back
        to the main menu
    '''
    def __init__(self, planet= planets.createNewMoon()):
        self.currentPlanet = planet
        # Set up manager for gui elements
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Stlye for the button
        grey_button = {
            "font_color": arcade.csscolor.WHITE_SMOKE,
            "bg_color": arcade.csscolor.GRAY
        }
        self.v_box = arcade.gui.UIBoxLayout()
        play_again_button = arcade.gui.UIFlatButton(text="Main Menu", width=300, style=grey_button)
        play_again_button.on_click = self.show_main_menu
        self.v_box.add(play_again_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x='center',
                anchor_y='bottom',
                align_y=SCREEN_HEIGHT * .3,
                child=self.v_box)
        )

        
        # Load lander without flame sprite and put it on the bottom of the screen
        self.landerFlying = arcade.SpriteList()
        joinedPath = os.path.join('./Resources', 'lander_on.PNG')
        self.landerFlyingSprite = arcade.Sprite(joinedPath, 0.1)
        self.landerFlyingSprite.center_x = SCREEN_WIDTH/2
        self.landerFlyingSprite.center_y = SCREEN_HEIGHT - SCREEN_HEIGHT
        self.landerFlying.append(self.landerFlyingSprite)

        super().__init__()

    def on_show_view(self):
        '''
        Color the background and increment the 'left' value within scores.csv by 1
        '''
        arcade.set_background_color(arcade.color.BLACK)
        try:
            # Attempt to get existing scores
            scores = sk.getCurrentScores()
            total_left = scores.get('left')
            total_left = str(int(total_left) + 1)
            scores['left'] = total_left
        except:
            # The save file must be missing or corrupted
            # Create new dict so a new save file can be made
            scores = {'safe': '0',
                      'crashed': '0', 
                      'left': '1'}
        sk.updateScores(scores)

    def show_main_menu(self, event):
        '''Button method to go back to the menu screen'''
        start_view = startScreenView()
        self.window.show_view(start_view)

    def on_update(self, delta_time: float):
        '''Animate the lander flying off into space'''
        self.landerFlying[0].change_y = self.landerFlying[0].change_y +0.1
        self.landerFlying.update()

    def on_draw(self):
        '''
        Let the user know they failed to land and draw splash screen
        '''
        self.clear()
        # draw result splash
        arcade.draw_text("You Left Orbit", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                             arcade.csscolor.GRAY, font_size=24, anchor_x = 'center')
        self.landerFlying.draw()
        self.manager.draw()

class landedScreenView(arcade.View):
    '''
    A fail condition end screen shown when the sprite passes the y-axis 
    depicting the ground. The view decides which lander sprite to display 
    based on self.currentPlanet.is_crashed.

    Also provides a button to take the user back to the main menu
    '''
    def __init__(self, planet = planets.createNewMoon()):
        self.currentPlanet = planet
        # Set up manager for gui elements
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Stlye for the button
        grey_button = {
            "font_color": arcade.csscolor.WHITE_SMOKE,
            "bg_color": arcade.csscolor.GRAY
        }
        self.v_box = arcade.gui.UIBoxLayout()
        play_again_button = arcade.gui.UIFlatButton(text="Main Menu", width=300, style=grey_button)
        play_again_button.on_click = self.show_main_menu
        self.v_box.add(play_again_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x='center',
                anchor_y='bottom',
                align_y=SCREEN_HEIGHT * .3,
                child=self.v_box)
        )
        

        arcade.set_background_color(self.currentPlanet.atmosphere_color)

        
        # Load lander without flame sprite and put it on the screen
        self.landerSafe = arcade.SpriteList()
        joinedPath = os.path.join('./Resources', 'lander_off.PNG')
        self.landerSafeSprite = arcade.Sprite(joinedPath, 0.1)
        self.landerSafeSprite.center_x = SCREEN_WIDTH/2
        self.landerSafeSprite.center_y = SCREEN_HEIGHT * .1 + self.landerSafeSprite.height/2
        self.landerSafe.append(self.landerSafeSprite)


        # Load a crashed lander and put it on the screen
        self.landerCrashed = arcade.SpriteList()
        landerCrashedSource = 'lander_crashed.PNG'
        joinedPath = os.path.join('./Resources', landerCrashedSource)
        self.landerCrashedSprite = arcade.Sprite(joinedPath, 0.1)
        self.landerCrashedSprite.center_x = SCREEN_WIDTH/2
        self.landerCrashedSprite.center_y = SCREEN_HEIGHT * .1 + self.landerCrashedSprite.height/2
        self.landerCrashed.append(self.landerCrashedSprite)


        super().__init__()


    def show_main_menu(self, event):
        '''Button method to show the start screen'''
        start_view = startScreenView()
        self.window.show_view(start_view)

    def on_hide_view(self):
        '''
        Clears the GUI manager when leaving the view
        '''
        self.manager.clear()
        return super().on_hide_view()


    def on_draw(self):
        '''Determine which lander sprite to load based on 
        self.currentPlanet.is_crashed
        '''
        self.clear()
        # draw result splash
        arcade.draw_line(0, SCREEN_HEIGHT * .1, SCREEN_WIDTH, SCREEN_HEIGHT * .1, 
                         self.currentPlanet.ground_color, 5)
        # determine which lander and message to show 
        if self.currentPlanet.is_crashed:
            self.landerCrashed.draw()
            arcade.draw_text("You Crashed", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                             arcade.csscolor.GRAY, font_size=24, anchor_x = 'center')
        else:
            self.landerSafeSprite.draw()
            arcade.draw_text("You Landed safely", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                             arcade.csscolor.GRAY, font_size=24, anchor_x= 'center')

        # Draw menu button    
        self.manager.draw()


class startScreenView(arcade.View):
    '''
    The main menu screen shown at start as well as any time the user goes back 
    to the main menu.

    Contains:
        - Game Title
        - Game instructions
        - Buttons to launch the game in various planets
        - Lifetime play statistics for the user
    '''
    def __init__(self):
        super().__init__()
        # Set up manager for gui elements
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # vbox to hold the buttons
        self.v_box = arcade.gui.UIBoxLayout()
        
        # Create buttons for each planet and add them to the vbox
        start_moon_button = arcade.gui.UIFlatButton(text="Moon", width=100)
        start_moon_button.on_click = self.start_moon
        self.v_box.add(start_moon_button.with_space_around(bottom=10))

        start_mars_button = arcade.gui.UIFlatButton(text="Mars", width=100)
        start_mars_button.on_click = self.start_mars
        self.v_box.add(start_mars_button.with_space_around(bottom=10))

        start_jupiter_button = arcade.gui.UIFlatButton(text="Jupiter", width=100)
        start_jupiter_button.on_click = self.start_jupiter
        self.v_box.add(start_jupiter_button)

        # add the vbox to the gui manager
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x='center',
                anchor_y='center',
                child=self.v_box)
        )
    
    # Methods for the buttons
    def start_moon(self,event):
        # go to moon game view
        game_view = InFlightView(planets.createNewMoon())
        game_view.setup()
        self.window.show_view(game_view)

    def start_mars(self,event):
        # go to mars game view
        game_view = InFlightView(planets.createNewMars())
        game_view.setup()
        self.window.show_view(game_view)

    def start_jupiter(self,event):
        # go to jupiter game view
        game_view = InFlightView(planets.createNewJupiter())
        game_view.setup()
        self.window.show_view(game_view)

    def on_show_view(self):
        '''
        Set's up things that need to be done once everytime the view is loaded
            1) Retrieve the current scores
            2) Set the background
        '''
        try: 
            scoresDict = sk.getCurrentScores()
            self.total_safe = scoresDict.get('safe')
            self.total_crashed = scoresDict.get('crashed')
            self.total_left = scoresDict.get('left')
        except:
            self.total_safe = 'No Save File Found, one will be created for you'
            self.total_crashed = 'No Save File Found, one will be created for you'
            self.total_left = 'No Save File Found, one will be created for you' 
        arcade.set_background_color(arcade.color.SKY_BLUE)
        
    def on_hide_view(self):
        '''
        Clears the GUI manager when leaving the view
        '''
        self.manager.clear()
        return super().on_hide_view()

    def on_draw(self):
        '''
        Draw all of the elements of the menu screen
        '''
        
        self.clear()
        # Title
        arcade.draw_text("Planet Lander", 
                         self.window.width/2, self.window.height * .8,
                         arcade.color.BLACK, font_size=64, anchor_x='center')
        # Instructions
        arcade.draw_text("Use the Spacebar to fire your engine and land safely", 
                         self.window.width/2, self.window.height * 0.7, 
                         arcade.color.BLACK, font_size= 20, anchor_x='center')
        # Buttons gui manager
        self.manager.draw()
        # Lifetime score values
        arcade.draw_text("Lifetime Landings Statistics:",
                         self.window.width/2, self.window.height * 0.25, 
                         arcade.color.BLACK, 20, anchor_x = 'center')
        arcade.draw_text(f"Safe Landings: {self.total_safe}",
                         self.window.width/2, self.window.height * 0.2, 
                         arcade.color.FOREST_GREEN, font_size= 16,
                         anchor_x= 'center')
        arcade.draw_text(f"Crash Landings: {self.total_crashed}",
                         self.window.width/2, self.window.height * 0.15,
                         arcade.color.BARN_RED, font_size= 16,
                         anchor_x= 'center')
        arcade.draw_text(f"Left Orbit: {self.total_left}", 
                         self.window.width/2, self.window.height * 0.1,
                         arcade.color.DARK_GOLDENROD,font_size= 16, 
                         anchor_x= 'center')
    

def main():
    """
    Create a window based on settings imported from settings.py,
        load the main menu, and start arcade's game loop
    """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = startScreenView()
    window.show_view(start_view)
    arcade.run()


if __name__ == '__main__':
    main()
