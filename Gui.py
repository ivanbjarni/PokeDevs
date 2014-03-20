#	TODO:
#		- Add info panel, to display info on pokemon/attacks/inventory items when hovered over
#		- Add "menubar" where you can choose help, exit, some other things maybe
#		- Maybe add a healthbar to either drawing area(gamePanel) or the statusPanel instead of just showing numbers for HP
#		- Choose which type of buttons to use
#		- Maybe choose some better colors for some things
#		- Hook everything up to the actual gameplay!!


import wx
import sys
import os
import time
import wx.lib.agw.gradientbutton as GB

# A drawable panel that contains the Playing Area
class GamePanel(wx.ScrolledWindow):
	def __init__(self, parent, id, size=wx.DefaultSize):
		wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=(1200, 650), style=wx.SUNKEN_BORDER)
		self.SetDoubleBuffered(True)

		self.hitradius = 5			# How many pixels you can be "off" when trying to click on something
		self.objids = []			# ID's of movable objects on the screen
		self.pdc = wx.PseudoDC()	# For drawing to the panel
		self.dragid = -1 			# ID of currently chosen object
		self.lastdragid = -1 		# ID of last chosen object
		self.origpos = {}			# Dictionary of original position of bitmaps based on id
		self.lastpos = (0,0)		# Lates position of the mouse while dragging
		self.startpos = (0,0)		# Position of the mouse when clicked

		self.Bind(wx.EVT_PAINT, self.onPaint)
		self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)
		self.Bind(wx.EVT_MOUSE_EVENTS, self.onMouse)

	def setupPanel(self, player, CPU):
		for card in player.deck.cards:
			self.setImage(card)

		for card in CPU.deck.cards:
			self.setImage(card)

		self.doDrawing(self.pdc, player, CPU)

	# Sets the bitmap for card
	def setImage(self, card):
		name = card.name.replace(' ', '').replace('.', '')
		image = wx.Image('images/Pokecards/' + str(card.name) + '.jpg', wx.BITMAP_TYPE_ANY)
		image = image.Scale(122, 175, wx.IMAGE_QUALITY_HIGH)
		card.bitmap = image.ConvertToBitmap()
	
	# Sets the right coordinates for a scrollable area if the area has been scrolled
	# Our area will never scroll so this will probably be changed/deleted
	def convertEventCoords(self, event):
		xView, yView = self.GetViewStart()
		xDelta, yDelta = self.GetScrollPixelsPerUnit()
		return (event.GetX() + (xView * xDelta),
			event.GetY() + (yView * yDelta))

	# Offsets a rectangle based on where you are placed on a scrollable area, 
	# Our area will never scroll so this will probably be changed/deleted
	def offsetRect(self, r):
		xView, yView = self.GetViewStart()
		xDelta, yDelta = self.GetScrollPixelsPerUnit()
		r.OffsetXY(-(xView*xDelta),-(yView*yDelta))

	#Handles mouse events
	# -------- Will be changed somewhat when it has been connected to the actual game -----
	def onMouse(self, event):
		# If the left button is pressed, grab the object that the mouse was over and
		# save the old coordinates where it was placed
		if event.LeftDown():
			x,y = self.convertEventCoords(event)
			l = self.pdc.FindObjects(x, y, self.hitradius)
			for id in l:
				if not self.pdc.GetIdGreyedOut(id):
					self.dragid = id
					self.lastpos = (event.GetX(), event.GetY())
					self.startpos = self.lastpos
					break

		# Right click is currently only used for testing purposes
		elif event.RightDown():
			#x,y = self.ConvertEventCoords(event)
			#l = self.pdc.FindObjects(x, y, self.hitradius)
			#if l:
			#	self.pdc.SetIdGreyedOut(l[0], not self.pdc.GetIdGreyedOut(l[0]))
			#	r = self.pdc.GetIdBounds(l[0])
			#	r.Inflate(4, 4)
			#	self.OffsetRect(r)
			#	self.RefreshRect(r, False)
			
			dx,dy = 100, 100
			if self.lastdragid != -1:
#				dx,dy = 100,100
				loopCPU = 10
				start = time.time()

				while(loopCPU != 0):
					time.sleep(0.005)
					x,y = self.lastpos
					dx = -5
					dy = -5

					self.moveItem(self.lastdragid, dx, dy)

					self.Update()
					loopCPU -= 1
				self.lastpos = (event.GetX(), event.GetY())

		# If dragging an object, move it relative to mouse movements
		elif event.Dragging():
			if self.dragid != -1:
				x,y = self.lastpos
				
				dx = event.GetX() - x
				dy = event.GetY() - y

				self.moveItem(self.dragid, dx, dy)
				self.lastpos = (event.GetX(), event.GetY())

		# Move object back to original position if left button is realeased or the mouse leaves the panel
		# TODO: Move object to allowed area if dropped over that area
		elif event.LeftUp() or event.Leaving():
			if self.dragid != -1:
				self.lastdragid = self.dragid

				dx = event.GetX()
				dy = event.GetY()

				if self.dropArea(dx, dy):
					x = self.startpos[0] - self.lastpos[0] - self.origpos[self.lastdragid][0] + 321
					y = self.startpos[1] - self.lastpos[1] - self.origpos[self.lastdragid][1] + 236
				else:
					x = self.startpos[0] - self.lastpos[0]
					y = self.startpos[1] - self.lastpos[1]

				self.moveItem(self.lastdragid, x, y)

				self.dragid = -1

		#elif event.Moving():
		#	print 'ok'
	
	def moveItem(self, id, x, y):
		r = self.pdc.GetIdBounds(id)
		self.pdc.TranslateId(id, x, y)
		r2 = self.pdc.GetIdBounds(id)
		r = r.Union(r2)
		r.Inflate(4, 4)
		self.offsetRect(r)
		self.RefreshRect(r, False)


	def dropArea(self, dx, dy):
		return  (300 < dx and dx < 465) and (435 > dy and dy > 215)

	# Updates the drawing area
	def onPaint(self, event):
		dc = wx.BufferedPaintDC(self)
		self.PrepareDC(dc)
		dc.Clear()
		rgn = self.GetUpdateRegion()
		r = rgn.GetBox()
		self.pdc.DrawToDCClipped(dc, r)

	# Draws the inital drawing area
	def doDrawing(self, dc, player, CPU):
		dc.BeginDrawing()
		background = wx.Bitmap("images/pokematBasic.png")
		dc.DrawBitmap(background, 0, 0)
		pen = wx.Pen('#435353', 2)
		brush = wx.Brush('#708B8B')
		dc.SetPen(pen)
		dc.SetBrush(brush)

		player1pokePanel = wx.Rect(190, 445, 805, 195)
		player2pokePanel = wx.Rect(190, 5, 805, 195)
		player1invPanel = wx.Rect(15, 70, 160, 570)
		player2invPanel = wx.Rect(1010, 5, 160, 570)
		player1chosenPanel = wx.Rect(300, 215, 165, 220)
		player2chosenPanel = wx.Rect(730, 215, 165, 220)
		dc.DrawRoundedRectangleRect(player1pokePanel, 10)
		dc.DrawRoundedRectangleRect(player2pokePanel, 10)
		dc.DrawRoundedRectangleRect(player1invPanel, 10)
		dc.DrawRoundedRectangleRect(player2invPanel, 10)
		dc.DrawRoundedRectangleRect(player1chosenPanel, 10)
		dc.DrawRoundedRectangleRect(player2chosenPanel, 10)

		w, h = player.deck.cards[0].bitmap.GetSize()
		for i in range(0, 6):
			id = wx.NewId()
			dc.SetId(id)
			x = 195 + i * 134
			y = 452
			dc.DrawBitmap(player.deck.cards[i].bitmap, x, y, True)
			dc.SetIdBounds(id, wx.Rect(x, y, w, h))
			self.origpos[id] = [x, y]
			self.objids.append(id)

		dc.EndDrawing()

# A panel that holds the names and HP of currently chosen pokemon
class StatusPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, size=(1200, 80))

		self.vbox = wx.BoxSizer(wx.VERTICAL)
		self.vbox1 = wx.BoxSizer(wx.VERTICAL)
		self.vbox2 = wx.BoxSizer(wx.VERTICAL)
		self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)

		self.pokemon1name = wx.StaticText(self, label='Pikachu', style=wx.ALIGN_LEFT)
		self.pokemon1hp = wx.StaticText(self, label='HP: 100', style=wx.ALIGN_LEFT)
		font = wx.Font(pointSize=24, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD)
		self.pokemon1name.SetFont(font)
		self.pokemon1hp.SetFont(font)
		self.pokemon1name.SetForegroundColour('#CCCCCC')
		self.pokemon1hp.SetForegroundColour('#CCCCCC')
		self.vbox1.Add(self.pokemon1name, flag=wx.ALIGN_CENTER, border=10)
		self.vbox1.Add(self.pokemon1hp, flag=wx.ALIGN_CENTER, border=10)
		self.hbox1.Add(self.vbox1, flag=wx.ALIGN_LEFT|wx.TOP, border=10)

		self.hbox1.AddSpacer((630,0))

		self.pokemon2name = wx.StaticText(self, label='Onyx', style=wx.ALIGN_RIGHT)
		self.pokemon2hp = wx.StaticText(self, label='HP: 100', style=wx.ALIGN_RIGHT)
		font = wx.Font(pointSize=24, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD)
		self.pokemon2name.SetFont(font)
		self.pokemon2hp.SetFont(font)
		self.pokemon2name.SetForegroundColour('#CCCCCC')
		self.pokemon2hp.SetForegroundColour('#CCCCCC')
		self.vbox2.Add(self.pokemon2name, flag=wx.ALIGN_CENTER, border=10)
		self.vbox2.Add(self.pokemon2hp, flag=wx.ALIGN_CENTER, border=10)
		self.hbox1.Add(self.vbox2, flag=wx.ALIGN_RIGHT|wx.TOP, border=10)

		self.vbox.Add(self.hbox1, flag=wx.ALIGN_CENTER, border=10)
		self.SetSizer(self.vbox)

	# Usage: c.setNamePlayer(name)
	# Pre  : name is the name of the players currently chosen pokemon
	# Post : The player pokemon label has been changed to name
	def setNamePlayer(self, name):
		self.pokemon1name.SetLabel(name)
		self.Layout()

	# Usage: c.setHpPlayer(hp)
	# Pre  : hp is the current hp of the players chosen pokemon
	# Post : The player pokemon hp label has been set to 'HP: ' + hp
	def setHpPlayer(self, hp):
		self.pokemon1hp.SetLabel('HP:' + str(hp))
		self.Layout()

	# Usage: c.setNameCPU(name)
	# Pre  : name is the name of the CPU's currently chosen pokemon
	# Post : The CPU pokemon label has been changed to name
	def setNameCPU(self, name):
		self.pokemon2name.SetLabel(name)
		self.Layout()

	# Usage: c.setHpCPU(hp)
	# Pre  : hp is the current hp of ther CPU's chosen pokemon
	# Post : The CPU pokemon hp label has been set to 'HP: ' + hp
	def setHpCPU(self, hp):
		self.pokemon2hp.SetLabel('HP: ' + str(hp))
		self.Layout()

# A panel that holds 4 attack buttons
class ControlPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, size=(1200, 200))

		self.SetBackgroundColour('#435353')

		self.vbox = wx.BoxSizer(wx.VERTICAL)
		self.hbox = wx.BoxSizer(wx.HORIZONTAL)

		# Some different variations of buttons, don't know what looks best

		# This button looks nicer than the generic button but I'm not 100% sure it's compatable with
		# other operating systems than windows
		# The label also doesn't center on this button if it is multiline
		self.attackButton1 = GB.GradientButton(self, -1, label='Attack\n'.center(5) + '25/25'.center(5), size=(200, 100))
		#self.attackButton1.SetTopStartColour(wx.Colour('#A8B8B8'))
		self.attackButton1.SetTopStartColour(wx.Colour(168, 184, 184))
		self.attackButton1.SetTopEndColour(wx.Colour(70, 89, 89))
		self.attackButton1.SetBottomStartColour(wx.Colour(66, 82, 82))
		self.attackButton1.SetPressedTopColour(wx.Colour(88, 110, 110))
		self.attackButton1.SetPressedBottomColour(wx.Colour(54, 43, 43))
		self.attackButton1.SetFont(wx.Font(pointSize=18, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD))
		self.hbox.Add(self.attackButton1, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP, border=10)
#		self.attackButton1.Bind(wx.EVT_BUTTON, lambda event: attack())

		self.attackButton2 = GB.GradientButton(self, -1, label='Attack', size=(200, 100))
		self.attackButton2.SetTopStartColour(wx.Colour(168, 184, 184))
		self.attackButton2.SetBottomStartColour(wx.Colour(66, 82, 82))
		self.attackButton2.SetPressedTopColour(wx.Colour(88, 110, 110))
		self.attackButton2.SetPressedBottomColour(wx.Colour(54, 43, 43))
		self.attackButton2.SetFont(wx.Font(pointSize=18, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD))
		self.hbox.Add(self.attackButton2, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP, border=10)
#		self.attackButton2.Bind(wx.EVT_BUTTON, lambda event: attack())

		self.attackButton3 = wx.Button(self, label='Attack\n25/25', size=(200, 100))
		self.attackButton3.SetFont(wx.Font(pointSize=18, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD))
		self.hbox.Add(self.attackButton3, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP, border=10)
#		self.attackButton3.Bind(wx.EVT_BUTTON, lambda event: attack())

		self.attackButton4 = wx.Button(self, label='Attack', size=(200, 100))
		self.attackButton4.SetFont(wx.Font(pointSize=18, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD))
		self.hbox.Add(self.attackButton4, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP, border=10)
#		self.attackButton4.Bind(wx.EVT_BUTTON, lambda event: attack())

		self.vbox.Add(self.hbox, flag=wx.ALL|wx.ALIGN_CENTER, border=10)
		self.SetSizer(self.vbox)

	# Usage: c.setAttackLabels(card)
	# Pre  : card is Card
	# Post : the labels on the attack buttons have been updated to the 
	#        attacks on card
	def setAttackLabels(self, card):
		self.freeze()
		self.attackButton1.SetLabel(card.attacks[0].name)
		self.attackButton2.SetLabel(card.attacks[1].name)
		self.attackButton3.SetLabel(card.attacks[2].name)
		self.attackButton4.SetLabel(card.attacks[3].name)
		self.Layout()
		self.Thaw()

	# Usage: c.disableAll()
	# Post : all of the attack buttons have been disabled
	def disableAll(self):
		self.attackButton1.Disable()
		self.attackButton2.Disable()
		self.attackButton3.Disable()
		self.attackButton4.Disable()

	# Usage: c.enableAll()
	# Post : all of the attack buttons have been enabled
	def enableAll(self):
		self.attackButton1.Enable()
		self.attackButton2.Enable()
		self.attackButton3.Enable()
		self.attackButton4.Enable()

class MainFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, title="Pokemon", size=(1200, 880))
		self.SetBackgroundColour('#435353')		
		self.vbox = wx.BoxSizer(wx.VERTICAL)
		self.hbox = wx.BoxSizer(wx.HORIZONTAL)

		self.statusPanel = StatusPanel(self)
		self.gamePanel = GamePanel(self, wx.ID_ANY)
		self.controlPanel = ControlPanel(self)

		self.vbox.Add(self.statusPanel, 0, flag=wx.EXPAND)
		self.vbox.Add(self.gamePanel, 0, flag=wx.EXPAND)
		self.vbox.Add(self.controlPanel, 0, flag=wx.EXPAND)

		self.SetAutoLayout(True)
		self.SetSizer(self.vbox)
		self.Layout()
		self.Centre()

if __name__=="__main__":
    app = wx.App()
    gui = MainFrame()
    gui.Show()
    app.MainLoop()
#    MainFrame().Show()
#    app.MainLoop()

