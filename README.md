# Planet Lander Game
A simple 'Lunar Lander' inspired game written in Python utilizing the python Arcade framework. 

Written as the final for CNM CIS 1250: Python 1

# Installation


1) Download the repository to your computer

2) navigate to the downloaded directory and create a python virtual environment

   `python -m venv venv`

3) Activate the venv
   1) Linux and Mac: `source venv/bin/activate`
   2) Windows: `Scripts/activate.bat`
      1) Please note I have not tested this on windows. I got the answer on sourcing the venv from a quick stack overflow check.

4) Use `pip` to install `requirements.txt`, this will download the arcade package to the virtual environment:

   `pip install -r requirements.txt`

6) Run the game using `python PlanetLander.py`

# Updating settings.py

I have hard-coded screen height and width into the game. 
If you find the options to be ill suited to your screen, change the constants within this file

I also have included a "difficulty" setting.
If you find it too easy or hard to land on the planets safely you can change this setting. A lower number is harder.

# Playing the Game

The goal of the game is to safely land your Lander on the surface of another planet, having to fight the planet's pull of gravity so that you do not crash.
Be careful with those thrusters though, you don't want to accidentally leave orbit and be stranded in space!

Use the space bar to toggle your thrusters on and off.

