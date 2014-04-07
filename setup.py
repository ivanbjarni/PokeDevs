import sys
from cx_Freeze import setup, Executable


includefiles = ['Attack.py','analyzeTextFiles.py','Card.py','constants.py','Deck.py','Gui.py','Hand.py','initTextFiles.py','InvCard.py','Inventory.py','InvDeck.py','Main.py','Player.py','Presets.py','util.py']
includes = []
excludes = []
packages = []

setup(
	name = "pokemon",
	version = "0.1",
	description ="test",
	options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}}, 
	executables = [Executable("pokemon.py")] ,
)