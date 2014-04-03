#from Gui import *
from Gui2PlayerTest import *

#Runs the GUI version of the game
if __name__=="__main__":
	app = wx.App()
	gui = MainFrame()
	gui.Show()
	app.MainLoop()