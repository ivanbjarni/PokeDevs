import subprocess
import tempfile
import wx
import wx.media
import sys
import os
import time
import threading
import wx.lib.agw.gradientbutton as GB
import wx.lib.scrolledpanel as scrolled
import random
from AI import *
from constants import *
from Presets import *
from Player import *
from Deck import *
from Inventory import *
from InvDeck import *
from Main import *

# Define notification event for threads
EVT_ANIM_ID = wx.NewId()

def EVT_ANIM(win, func):
	win.Connect(-1, -1, EVT_ANIM_ID, func)

class AnimEvent(wx.PyEvent):
    def __init__(self, id, dx, dy, moveY, done, barFinished):
		wx.PyEvent.__init__(self)
		self.SetEventType(EVT_ANIM_ID)
		self.id = id
		self.dx = dx
		self.dy = dy
		self.moveY = moveY
		self.done = done
		self.barFinished = barFinished

# A worker thread that handles long running task so the GUI doesn't freeze up
class Worker(threading.Thread):
	def __init__(self, wxObject, id, i, j, animation):
		threading.Thread.__init__(self)
		self.wxObject = wxObject
		self.id = id
		self.i = i
		self.j = j
		self.animation = animation
		self.anim = []
		self.start()

	# run the thread
	def run(self):
		if self.animation == 'animation1':
			self.animation1()
		elif self.animation == 'bar':
			self.bar()
		elif self.animation == 'wait1':
			self.wait(1)
		elif self.animation == 'wait2':
			self.wait(2)
		elif self.animation == 'wait3':
			self.wait(3)

	# animates a pokemon attack movement
	def animation1(self):
		forward = True
		while(self.i < self.j):
			time.sleep(0.01)
			if forward:
				dx = random.randint(1, 41) - 20
				dy = random.randint(1, 21) - 10

				self.anim.append([dx, dy])
				try:
					wx.PostEvent(self.wxObject, AnimEvent(self.id, dx, dy, -1, False, False))
				except:
					print 'Program exited'

				if self.i > 0:
					self.i -= 1
				else:
					forward = False
			else:
				dx, dy = self.anim.pop()

				try:
					wx.PostEvent(self.wxObject, AnimEvent(self.id, -dx, -dy, -1, False, False))
				except:
					print 'Program exited'

				self.i += 1

	# Updates health/statusbars by animating it's movements
	def bar(self):
		if self.i < self.j:
			while self.i < self.j:
				time.sleep(0.005)
				self.i += 1

				try:
					wx.PostEvent(self.wxObject, AnimEvent(self.id, 0, 1, self.i, False, False))
				except:
					print 'Program exited'
		else:
			while self.i > self.j:
				time.sleep(0.005)
				self.i -= 1
				try:
					wx.PostEvent(self.wxObject, AnimEvent(self.id, 0, -1, self.i, False, False))
				except:
					print 'Program exited'
		try:
			wx.PostEvent(self.wxObject, AnimEvent(self.id, 0, 0, -1, False, True))
		except:
			print 'Program exited'


	#Waits a certain amount of time and then enables Player to perform actions
	def wait(self, i):
		if i == 1:
			waitingTime = random.randint(1,3)
			time.sleep(waitingTime)
			try:
				wx.PostEvent(self.wxObject, AnimEvent(self.id, 0, 0, -1, True, False))
			except:
				'Program exited'
		elif i == 2:
			waitingTime = 1
			time.sleep(waitingTime)
			try:
				wx.PostEvent(self.wxObject, AnimEvent(self.id, 0, -1, -1, True, False))
			except:
				'Program exited'
		elif i == 3:
			waitingTime = 1.8
			time.sleep(waitingTime)
			try:
				wx.PostEvent(self.wxObject, AnimEvent(self.id, 0, -1, -1, True, False))
			except:
				'Program exited'

# A drawable panel that contains the Playing Area
class GamePanel(wx.ScrolledWindow):
	def __init__(self, parent, id, size=wx.DefaultSize):
		# This needs to be a scrolled window even though it doesn't scroll
		wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=(1060, 560), style=wx.SUNKEN_BORDER)
		self.SetDoubleBuffered(True)

		self.isMyTurn = True 		 # Determines wheather you can move cards around
		self.hasDrawnPoke = False 	 # Determines wheather you have drawn a pokemon this round
		self.canDrawInv = False 	 # Determines wheather you can drag an inventory card
		self.hasDrawnInv = False 	 # Determines wheather you have drawn an inventory card this round
		self.CPUselfdestruct = False # Deterermines wheather CPU killed itself last turn
		self.isPlayerStunned = False # Determines wheather player is stunned
		self.isCPUStunned = False 	 # Determines wheather CPU is stunned
		self.hitradius = 5			 # How many pixels you can be "off" when trying to click on something
		self.objids = []			 # ID's of movable objects on the screen
		self.countCPUpokemon = 0 	 # Count how many pokemon CPU has drawn
		self.pdc = wx.PseudoDC()	 # For drawing to the panel
		self.dragid = -1 			 # ID for currently chosen object
		self.playerChosenID = -1 	 # ID for player's currently chosen object
		self.CPUChosenID = -1 		 # ID for CPU's currently chosen object
		self.graveyardID = -1 		 # ID of pokemon in graveyard
		self.playerHealthID = -1 	 # ID for players healthbar
		self.playerStaminaID = -1 	 # ID for players stamina bar
		self.CPUHealthID = -1 		 # ID for CPU health bar
		self.CPUStaminaID = -1 		 # ID for CPU stamina bar
		self.playerStunnedID = -1 	 # ID for player stunned sign
		self.CPUStunnedID = -1 		 # ID for CPU stunned sign
		self.winId = -1 			 # ID for text that displays when you win
		self.loseId = -1 			 # ID for text that displays when you loose
		self.movable = {}			 # Dict of wheather or not a card can be moved by player, by id
		self.origpos = {}			 # Dict of original position of bitmaps by id
		self.cards = {}				 # Dict of cards by id
		self.cardsCPU = [] 			 # List of CPU cards
		self.cardType = {} 			 # Dict of card types by id
		self.backsides = {} 		 # Dict of backside ids to link backsides to cards
		self.backsidesInv = {} 		 # Dict of inventory backside ids to link to inventory cards
		self.backsidesCPU = {} 		 # Dict of CPU backsides
		self.slot = {} 				 # Dict of slot number for cards by id 
		self.invSlot = {} 			 # Dict of slot number for inventory cards by
		self.slotCPU = {}			 # Dict of slot number for CPU cards by id
		self.anim = []				 # List of moves for animations
		self.lastpos = (0,0)		 # Latest position of the mouse while dragging
		self.startpos = (0,0)		 # Position of the mouse when clicked
		self.backsideBmp = None		 # Bitmap of the backside of a pokemon card
		self.backsideInvBmp = None 	 # Bitmap of the backside of an inventory card

		wx.Log.SetLogLevel(0) # remove this and fix images

	# Loads the bitmaps for the players and CPUs cards, and initializes the playing area 
	def setupPanel(self, player, CPU):
		for card in player.deck.cards:
			self.setImage(card)

		for card in player.invdeck.invCards:
			self.setInvImage(card)

		for card in CPU.deck.cards:
			self.setImage(card)

		self.setBacksideBmp()
		self.setBacksideInvBmp()

		self.doDrawing(self.pdc, player, CPU)

		self.Bind(wx.EVT_PAINT, self.onPaint)
		self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)
		self.Bind(wx.EVT_MOUSE_EVENTS, self.onMouse)

		EVT_ANIM(self, self.updateDisplay)

	# Sets the bitmap for a pokemon card
	def setImage(self, card):
		name = card.name.replace(' ', '').replace('.', '')
		try:
			image = wx.Image('images/Pokecards/' + name + '.jpg', wx.BITMAP_TYPE_ANY)
			image = image.Scale(116, 165, wx.IMAGE_QUALITY_HIGH)
			card.bitmap = image.ConvertToBitmap()
		except:
			print 'Failed to load card: ' + str(name)

	# Sets the bitmap for and inventory card
	def setInvImage(self, card):
		name = card.name.replace(' ', '').replace('.', '')
		try:
			image = wx.Image('images/Inventorycards/' + name + '.png', wx.BITMAP_TYPE_ANY)
			image = image.Scale(116, 165, wx.IMAGE_QUALITY_HIGH)
			card.bitmap = image.ConvertToBitmap()
		except:
			print 'Failed to load card: ' + str(name)

	# Sets the bitmap for the backside of a pokemon card
	def setBacksideBmp(self):
		try:
			image = wx.Image('images/Pokecards/Backside.jpg', wx.BITMAP_TYPE_ANY)
			image = image.Scale(116, 165, wx.IMAGE_QUALITY_HIGH)
			self.backsideBmp = image.ConvertToBitmap()
		except:
			print 'Failed to load backside card'

	# Sets the bitmap for the backside of an inventory card
	def setBacksideInvBmp(self):
		try:
			image = wx.Image('images/Inventorycards/invBackside.png', wx.BITMAP_TYPE_ANY)
			image = image.Scale(116, 165, wx.IMAGE_QUALITY_HIGH)
			self.backsideInvBmp = image.ConvertToBitmap()
		except:
			print 'Failed to load inventory backside card'
	
	# Sets the right coordinates the area
	def convertEventCoords(self, event):
		xView, yView = self.GetViewStart()
		xDelta, yDelta = self.GetScrollPixelsPerUnit()
		return (event.GetX() + (xView * xDelta),
			event.GetY() + (yView * yDelta))

	# Offsets a rectangle based on where you are placed
	def offsetRect(self, r):
		xView, yView = self.GetViewStart()
		xDelta, yDelta = self.GetScrollPixelsPerUnit()
		r.OffsetXY(-(xView*xDelta),-(yView*yDelta))

	# Handles mouse events
	def onMouse(self, event):
		# If the left button is pressed, grab the object that the mouse was over and
		# save the old coordinates where it was placed
		if event.LeftDown():
			x,y = self.convertEventCoords(event)
			l = self.pdc.FindObjects(x, y, self.hitradius)
			for id in l:
				if not self.pdc.GetIdGreyedOut(id) and self.movable[id] and self.isMyTurn and id != self.graveyardID:
					self.dragid = id
					self.lastpos = (event.GetX(), event.GetY())
					self.startpos = self.lastpos
					break

		# If dragging an object, move it relative to mouse movements
		elif event.Dragging():
			if self.dragid != -1:
				x,y = self.lastpos
				
				dx = event.GetX() - x
				dy = event.GetY() - y

				self.moveItem(self.dragid, dx, dy)
				self.lastpos = (event.GetX(), event.GetY())

		# If an object is released either move it back to it's original position or if it is in an allowed area
		# do the corresponding action for the object
		elif event.LeftUp() or event.Leaving():
			if self.dragid != -1:
				dx = event.GetX()
				dy = event.GetY()

				if self.cardType[self.dragid] == 'Pokemon': 
					if self.inPlayerChosenArea(dx, dy) and self.playerChosenID != self.dragid and (self.playerChosenID == self.graveyardID or self.CPUselfdestruct):
						# Switch currently chosen pokemon out for a new one 
						x = self.startpos[0] - self.lastpos[0] - self.origpos[self.dragid][0] + 119
						y = self.startpos[1] - self.lastpos[1] - self.origpos[self.dragid][1] + 195
						self.GetParent().attackPanel.setLabels(self.cards[self.dragid])
						slot = self.slot[self.dragid]
						tx = -106 + slot * 127
						ty = 189
						if self.playerChosenID != self.graveyardID:
							self.moveItem(self.playerChosenID, tx, ty)
							self.slot[self.playerChosenID] = slot
						self.slot[self.playerChosenID] = -1
						self.moveItem(self.dragid, x, y)
						self.slot[self.dragid] = -1
						self.origpos[self.playerChosenID] = [13 + slot * 127, 384]
						self.playerChosenID = self.dragid
						self.GetParent().game.players[0].mainCard = self.cards[self.dragid]
						self.GetParent().updateStatus()
						self.GetParent().game.textLog.append('You put out ' + self.GetParent().game.players[0].mainCard.name + '\n')
						self.GetParent().attackPanel.disableAll() 
						worker = Worker(self, 0, 0, 1, 'wait3') # Enables attack buttons again in 1.8 seconds so that the healthbar has time to finish animating
						self.updatePlayerHp()
						self.updatePlayerStamina()
						self.CPUselfdestruct = False
					else:
						x = self.startpos[0] - self.lastpos[0]
						y = self.startpos[1] - self.lastpos[1]
						self.moveItem(self.dragid, x, y)
						if self.inPlayerChosenArea(dx, dy):
							self.GetParent().game.textLog.append('You can not switch out your pokemon')

				elif self.cardType[self.dragid] == 'Backside':
					slot = self.findEmptySlot(self.slot)
					if self.inPlayerHandArea(dx, dy) and slot != -1 and not self.hasDrawnPoke:
						# Draw a new pokecard
						id = self.backsides[self.dragid]
						x = 213 + slot * 127
						y = 584
						self.moveItem(id, x, y)
						self.origpos[id] = [x-200, y-200]
						self.slot[id] = slot
						self.moveItem(self.dragid, 0, -1000)
						self.GetParent().game.draw(self.GetParent().game.players[0])
						self.hasDrawnPoke = True
					else:
						x = self.startpos[0] - self.lastpos[0]
						y = self.startpos[1] - self.lastpos[1]
						self.moveItem(self.dragid, x, y)
						if self.hasDrawnPoke:
							self.GetParent().game.textLog.append('You can only draw one pokemon each round\n')

				elif self.cardType[self.dragid] == 'InvBackside':
					slot = self.findEmptyInvSlot()
					if self.inPlayerInvArea(dx, dy) and slot != -1 and self.canDrawInv and not self.hasDrawnInv:
						# Draw a new inventory card
						id = self.backsidesInv[self.dragid]
						x = 991
						y = 215 + slot * 180
						self.moveItem(id, x, y)
						self.invSlot[id] = slot
						self.moveItem(self.dragid, 0, -1000)
						self.hasDrawnInv = True
						self.GetParent().game.drawInv(self.GetParent().game.players[0])
					else:
						x = self.startpos[0] - self.lastpos[0]
						y = self.startpos[1] - self.lastpos[1]
						self.moveItem(self.dragid, x, y)
						self.GetParent().game.textLog.append('You can not draw Inventory things now\n')
						if self.hasDrawnInv:
							self.GetParent().game.textLog.append('You can only draw one inventory card each 3 turns\n')

				elif self.cardType[self.dragid] == 'Inventory':
					if self.inPlayerChosenArea(dx, dy):
						# Use an inventory card
						self.moveItem(self.dragid, 0, -1000)
						self.invSlot[self.dragid] = -1
						self.GetParent().game.players[0].use(self.cards[self.dragid], self.GetParent().game.textLog)
						self.GetParent().updateStatus()
						self.updatePlayerHp()
						self.updatePlayerStamina()
					elif self.inCPUChosenArea(dx, dy):
						# Use an inventory card on CPU
						self.moveItem(self.dragid, 0, -1000)
						self.invSlot[self.dragid] = -1
						self.GetParent().game.players[1].use(self.cards[self.dragid], self.GetParent().game.textLog)
						self.updateCPUHp(False)
						self.updateCPUStamina()
					else:
						x = self.startpos[0] - self.lastpos[0]
						y = self.startpos[1] - self.lastpos[1]
						self.moveItem(self.dragid, x, y)
				self.dragid = -1
				self.GetParent().logPanel.updateLog()

		# Update info panel if hovering over a card
		elif event.Moving():
			x,y = self.convertEventCoords(event)
			l = self.pdc.FindObjects(x, y, self.hitradius)
			for id in l:
				card = self.findCard(id)
				if card:
					if hasattr(card, 'poketype'):
						self.GetParent().infoPanel.setPokeInfo(card)
					else:
						self.GetParent().infoPanel.setInventoryInfo(card)

	# Returns True if (dx, dy) is in players chosen pokemon area, 
	# otherwise False
	def inPlayerChosenArea(self, dx, dy):
		return  (110 < dx and dx < 245) and (376 > dy and dy > 182)

	# Returns True if (dx, dy) is in CPU's chosen pokemon area, 
	# otherwise False
	def inCPUChosenArea(self, dx, dy):
		return (535 < dx and dx < 717) and (376 > dy and dy > 182)
	
	# Returns True if (dx, dy) is in players pokepanel area, 
	# otherwise False
	def inPlayerHandArea(self, dx, dy):
		return (3 < dx and dx < 778) and (555 > dy and dy > 308)

	# Returns True if (dx, dy) is in players chosen inventory area, 
	# otherwise False
	def inPlayerInvArea(self, dx, dy):
		return (782 < dx and dx < 917) and (552 > dy and dy > 3)

	# Finds a card by its id
	def findCard(self, id):
		for card in self.cards.iteritems():
			if id == card[0]:
				return card[1]


	# Finds an empty slot in Players/CPU's pokepanel
	# if no slot is available -1 is returned
	def findEmptySlot(self, slot):
		i = {
			'0': True,
			'1': True,
			'2': True,
			'3': True,
			'4': True,
			'5': True,
		}
		for j in slot.iteritems():
			if j[1] == 5:
				i['5'] = False
			if j[1] == 4:
				i['4'] = False
			if j[1] == 3:
				i['3'] = False
			if j[1] == 2:
				i['2'] = False
			if j[1] == 1:
				i['1'] = False
			if j[1] == 0:
				i['0'] = False

		for k in range(0, 6):
			if i[str(k)]:
				return k
		return -1		

	# Finds an empty inventory slot on the players inventory panel
	# if no slot is available it -1 is returned
	def findEmptyInvSlot(self):
		i = {
			'0': True,
			'1': True,
			'2': True,
		}
		for j in self.invSlot.iteritems():
			if j[1] == 2:
				i['2'] = False
			if j[1] == 1:
				i['1'] = False
			if j[1] == 0:
				i['0'] = False

		for k in range(0, 3):
			if i[str(k)]:
				return k
		return -1

	# Moves item id by (x, y)
	def moveItem(self, id, x, y):
		r = self.pdc.GetIdBounds(id)
		self.pdc.TranslateId(id, x, y)
		r2 = self.pdc.GetIdBounds(id)
		r = r.Union(r2)
		r.Inflate(4, 4)
		self.offsetRect(r)
		self.RefreshRect(r, False)

	# Moves a card bitmap to the graveyard
	def moveItemToGraveyard(self, id, x, y):
		if self.graveyardID != -1:
			self.moveItem(self.graveyardID, 0, -1000)
		self.graveyardID = id
		self.moveItem(self.graveyardID, x, y)

	# if isPlayer == True the players pokemon is "shaken" on the screen
	# else the CPU's pokemon is "shaken"
	def animation1(self, isPlayer):
		if isPlayer:
			id = self.playerChosenID
		else:
			id = self.CPUChosenID

		anim = Worker(self, id, 10, 11, 'animation1')

	# Updates a health/stamina bar and returns the health/stamina that is left
	def updateBar(self, bar, card, type):
		if type == 'health':
			hp = card.health
			maxhp = card.healthMax
		else:
			hp = card.stamina
			maxhp = card.staminaMax
		if hp > maxhp:
			hp = maxhp
		movement = 193 - (float(hp) / float(maxhp) * 193)
		origY = self.origpos[bar][0]
		currentY = self.origpos[bar][1]

		if hp <= 0: 
			hp = 0

		endY = origY + movement

		worker = Worker(self, bar, currentY, endY, 'bar')

		return hp

	# Update the Players healthbar, if the players chosen pokemon is dead it is 
	# moved to the graveyard and the CPU's score is increased by 1
	def updatePlayerHp(self):
		hp = self.updateBar(self.playerHealthID, self.cards[self.playerChosenID], 'health')
		if hp == 0:
			self.GetParent().game.players[1].points += 1
			self.GetParent().game.textLog.append(self.cards[self.playerChosenID].name + ' fainted\n')
			self.moveItemToGraveyard(self.playerChosenID, 812, 185)
			self.slot[self.playerChosenID] = -1

	# Update the Players stamina bar
	def updatePlayerStamina(self):
		stamina = self.updateBar(self.playerStaminaID, self.cards[self.playerChosenID], 'stamina')

	# Add the Players stunned sign
	def setPlayerStunned(self):
		if not self.isPlayerStunned: 
			self.moveItem(self.playerStunnedID, 450, 390)
			self.isPlayerStunned = True

	# Remove the Players stunned sign
	def setPlayerNotStunned(self):
		if self.isPlayerStunned:
			self.moveItem(self.playerStunnedID, -450, -390)
			self.isPlayerStunned = False

	# Updates the CPU's healthbar, if its chosen pokemon is dead it is moved to 
	# the graveyard and the Players score is increased by 1
	def updateCPUHp(self, selfKill):
		if not selfKill:
			hp = self.updateBar(self.CPUHealthID, self.cards[self.CPUChosenID], 'health')
		else:
			hp = 0

		if hp == 0:
			self.GetParent().game.players[0].points += 1
			self.GetParent().game.textLog.append(self.cards[self.CPUChosenID].name + ' fainted\n')
			self.moveItemToGraveyard(self.CPUChosenID, 387, 185)
			self.slotCPU[self.CPUChosenID] = -1

	# Update the CPU's stamina bar
	def updateCPUStamina(self):
		stamina = self.updateBar(self.CPUStaminaID, self.cards[self.CPUChosenID], 'stamina')

	# Add the CPU's stunned sign
	def setCPUStunned(self):
		if not self.isCPUStunned:
			self.moveItem(self.CPUStunnedID, 705, 390)
			self.isCPUStunned = True

	# Remove the CPU's stunned sign
	def setCPUNotStunned(self):
		if self.isCPUStunned:
			self.moveItem(self.CPUStunnedID, -705, -390)
			self.isCPUStunned = False

	# For when the CPU draws a pokemon, adds the corresponding backside to its pokepanel
	def addCPUpokemon(self):
		if self.cardsCPU and self.findEmptySlot(self.slotCPU) != -1 and self.countCPUpokemon < 10:
			card = self.cardsCPU.pop()
			self.cardsCPU.insert(0, card)
			id = self.findID(card)
			bid = self.findBacksideCPU(id)
			slot = self.findEmptySlot(self.slotCPU)
			self.slotCPU[bid] = slot
			self.countCPUpokemon += 1
			self.origpos[bid] = [10 + slot * 127, 6]
			self.moveItem(bid, 210 + slot * 127, 206)

	# Switch out CPU's chosen pokemon, removes the backside from CPU's pokepanel and puts
	# and puts the corresponding card in its chosen area
	def switchCPUpokemon(self, card):
		if self.cardsCPU:
			id = self.findID(card)
			bid = self.findBacksideCPU(id)
			self.slotCPU[bid] = -1
			self.CPUChosenID = id
			self.moveItem(id, 744, 395)
			self.moveItem(bid, 0, -1000)
			self.Update()

	# Find the id of a card
	def findID(self, card):
		for id in self.cards.iteritems():
			if card == id[1]:
				return id[0]

	# find the backside of a CPU card
	def findBacksideCPU(self, id):
		for bid in self.backsidesCPU.iteritems():
			if id == bid[1]:
				return bid[0]

	# displays the Win sign 
	def setWinSign(self):
		self.moveItem(self.winId, 510, 480)

	# displays the Lose sign
	def setLoseSign(self):
		self.moveItem(self.loseId, 510, 480)

	# for drawing a bitmap
	def drawItem(self, dc, id, bitmap, x, y, w, h):
		dc.DrawBitmap(bitmap, x, y, True)
		dc.SetIdBounds(id, wx.Rect(x, y, w, h))
		self.objids.append(id)

	# for drawing health/stamina bars, returns the bars id
	def drawBar(self, dc, x, y, w, h, color):
		# draw the bar outline
		pen = wx.Pen('#000000', 1)
		brush = wx.Brush('#F0D84E')
		dc.SetPen(pen)
		dc.SetBrush(brush)
		tempid = wx.NewId()
		dc.SetId(tempid)
		outline = wx.Rect(x, y, w, h)
		dc.DrawRectangleRect(outline)
		outline.Inflate(pen.GetWidth(), pen.GetWidth())
		dc.SetIdBounds(tempid, outline)
		self.movable[tempid] = False

		# draw the bar itself
		id = wx.NewId()
		dc.SetId(id)
		brush = wx.Brush(color)
		dc.SetBrush(brush)
		dc.SetPen(pen)
		bar = wx.Rect(x, y, w, h)
		dc.DrawRectangleRect(bar)
		bar.Inflate(pen.GetWidth(), pen.GetWidth())
		dc.SetIdBounds(id, bar)
		self.movable[id] = False
		self.origpos[id] = [y, y]		# The x value never changes, keep track of original and current y values

		return id

	# Handles ANIM events
	def updateDisplay(self, msg):
		if msg.moveY != -1:
			self.origpos[msg.id][1] = msg.moveY
		
		if not msg.done:
			self.moveItem(msg.id, msg.dx, msg.dy)
			self.Update()
		elif msg.done and msg.dy != -1:
			self.GetParent().CPUAction()
		elif not msg.barFinished:
			self.isMyTurn = True
			self.GetParent().attackPanel.enableAll()
			self.GetParent().game.turn += 1
			self.GetParent().updateStatus()

	# Updates the playing area
	def onPaint(self, event):
		dc = wx.BufferedPaintDC(self)
		self.PrepareDC(dc)
		dc.Clear()
		rgn = self.GetUpdateRegion()
		r = rgn.GetBox()
		self.pdc.DrawToDCClipped(dc, r)

	# Draws the inital playing area
	def doDrawing(self, dc, player, CPU):
		dc.BeginDrawing()
		try:
			background = wx.Bitmap("images/pokematBasic.png")
		except:
			print 'Failed to load backround image'

		try:
			stunned = wx.Bitmap("images/stunnedStatus2.png")
		except:
			print 'Failed to load stunned image'

		try:
			winSign = wx.Bitmap("images/youWinV1.png")
		except:
			print 'Failed to load win image'

		try:
			loseSign = wx.Bitmap("images/youLoseV1.png")
		except:
			print 'Failed to load lose image'		

		dc.DrawBitmap(background, 0, 0)

		pen = wx.Pen('#435353', 2)
		brush = wx.Brush('#A8B8B8')
		dc.SetPen(pen)
		dc.SetBrush(brush)

		# Make panels for cards
		player1pokePanel = wx.Rect(3, 380, 775, 175)
		player2pokePanel = wx.Rect(3, 3, 775, 175)
		player1invPanel = wx.Rect(782, 3, 135, 552)
		player1chosenPanel = wx.Rect(110, 182, 135, 193)
		player2chosenPanel = wx.Rect(535, 182, 135, 193)
		inventoryDeckPanel = wx.Rect(922, 3, 135, 181)
		cardDeckPanel = wx.Rect(922, 188, 135, 181)
		graveyardPanel = wx.Rect(922, 373, 135, 181)
		dc.DrawRoundedRectangleRect(player1pokePanel, 10)
		dc.DrawRoundedRectangleRect(player1invPanel, 10)
		dc.DrawRoundedRectangleRect(player1chosenPanel, 10)
		brush = wx.Brush('#708B8B')
		dc.SetBrush(brush)
		dc.DrawRoundedRectangleRect(player2pokePanel, 10)
		dc.DrawRoundedRectangleRect(player2chosenPanel, 10)
		brush = wx.Brush('#435353')
		dc.SetBrush(brush)
		dc.DrawRoundedRectangleRect(inventoryDeckPanel, 10)
		dc.DrawRoundedRectangleRect(cardDeckPanel, 10)
		dc.DrawRoundedRectangleRect(graveyardPanel, 10)

		# Make health- and stamina bars
		self.playerHealthID = self.drawBar(dc, 90, 182, 10, 193, '#DB3340')
		self.CPUHealthID = self.drawBar(dc, 680, 182, 10, 193, '#DB3340')
		self.playerStaminaID = self.drawBar(dc, 70, 182, 10, 193, '#28ABE3')
		self.CPUStaminaID = self.drawBar(dc, 700, 182, 10, 193, '#28ABE3')

		# A yellow line to hide healthbars when they move
		id = wx.NewId()
		dc.SetId(id)
		pen = wx.Pen('#FFFFFF', 1)
		brush = wx.Brush('#FFFF66')
		dc.SetPen(pen)
		dc.SetBrush(brush)
		yellowLine = wx.Rect(60, 375, 680, 195)
		dc.DrawRectangleRect(yellowLine)
		yellowLine.Inflate(pen.GetWidth(), pen.GetWidth())
		dc.SetIdBounds(id, yellowLine)
		self.movable[id] = False

		# Player pokemon panel, must be drawn after healthbars so they don't go over it
		id = wx.NewId()
		dc.SetId(id)
		pen = wx.Pen('#435353', 2)
		brush = wx.Brush('#A8B8B8')
		dc.SetPen(pen)
		dc.SetBrush(brush)
		player1pokePanel = wx.Rect(3, 380, 775, 175)
		dc.DrawRoundedRectangleRect(player1pokePanel, 10)
		player1pokePanel.Inflate(pen.GetWidth(), pen.GetWidth())
		dc.SetIdBounds(id, player1pokePanel)
		self.movable[id] = False

		w, h = player.deck.cards[0].bitmap.GetSize()

		# Players starting card
		id = wx.NewId()
		dc.SetId(id)
		self.drawItem(dc, id, player.deck.cards[0].bitmap, 119, 195, w, h)
		self.movable[id] = True
		self.cardType[id] = 'Pokemon'
		self.cards[id] = player.deck.cards[0]
		self.slot[id] = -1
		self.origpos[id] = [13, 384]
		self.playerChosenID = id
		self.GetParent().attackPanel.setLabels(self.cards[id])

		# CPU starting card
		id = wx.NewId()
		dc.SetId(id)
		self.drawItem(dc, id, CPU.deck.cards[0].bitmap, 544, 195, w, h)
		self.movable[id] = False
		self.cards[id] = CPU.deck.cards[0]
		self.slotCPU[id] = -1
		self.CPUChosenID = id


		for i in range(1, 10):
			# Players pokecards, put offscreen initially
			id = wx.NewId()
			dc.SetId(id)
			self.drawItem(dc, id, player.deck.cards[i].bitmap, -200, -200, w, h)
			self.movable[id] = True
			self.cardType[id] = 'Pokemon'
			self.cards[id] = player.deck.cards[i]
			self.slot[id] = -1

			# Players deck, backsides of pokecards
			bid = wx.NewId()
			dc.SetId(bid)
			self.drawItem(dc, bid, self.backsideBmp, 931, 195, w, h)
			self.movable[bid] = True
			self.cardType[bid] = 'Backside'
			self.backsides[bid] = id

			# Computers pokecards, put offscreen initially
			id = wx.NewId()
			dc.SetId(id)
			self.drawItem(dc, id, CPU.deck.cards[i].bitmap, -200, -200, w, h)
			self.movable[id] = False
			self.cards[id] = CPU.deck.cards[i]
			self.slotCPU[id] = -1
			self.cardsCPU.append(CPU.deck.cards[i])

			# Backsides of computers pokecards, put offscreen initially
			bid = wx.NewId()
			dc.SetId(bid)
			self.drawItem(dc, bid, self.backsideBmp, -200, -200, w, h)
			self.movable[bid] = False
			self.backsidesCPU[bid] = id

		for i in range(0, 100):
			# Players inventory cards, put offscreen initially
			id = wx.NewId()
			dc.SetId(id)
			self.drawItem(dc, id, player.invdeck.invCards[i].bitmap, -200, -200, w, h)
			self.movable[id] = True
			self.cardType[id] = 'Inventory'
			self.cards[id] = player.invdeck.invCards[i]
			self.invSlot[id] = -1

			# Backsides of players inventory cards
			bid = wx.NewId()
			dc.SetId(bid)
			self.drawItem(dc, bid, self.backsideInvBmp, 931, 10, w, h)
			self.movable[bid] = True
			self.cardType[bid] = 'InvBackside'
			self.backsidesInv[bid] = id

		w, h = stunned.GetSize()

		# Stunned sign for player
		id = wx.NewId()
		dc.SetId(id)
		self.drawItem(dc, id, stunned, -200, -200, w, h)
		self.movable[id] = False
		self.playerStunnedID = id

		# Stunned sign for CPU
		id = wx.NewId()
		dc.SetId(id)
		self.drawItem(dc, id, stunned, -200, -200, w, h)
		self.movable[id] = False
		self.CPUStunnedID = id

		w, h = winSign.GetSize()

		# Sign that appears when you win
		id = wx.NewId()
		dc.SetId(id)
		self.drawItem(dc, id, winSign, -400, -400, w, h)
		self.winId = id
		self.movable[id] = False
		self.objids.append(id)

		# Sign that appears when you loose
		id = wx.NewId()
		dc.SetId(id)
		self.drawItem(dc, id, loseSign, -400, -400, w, h)
		self.loseId = id
		self.movable[id] = False
		self.objids.append(id)

		dc.EndDrawing()

# A panel that holds 4 attack buttons and a pass button
class AttackPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, size=(1064, 200))

		self.SetBackgroundColour('#435353')

		self.vbox = wx.BoxSizer(wx.VERTICAL)
		self.hbox = wx.BoxSizer(wx.HORIZONTAL)

		self.attackButtons = []

		for i in xrange(0,4):
			element = GB.GradientButton(self, -1, label='---', size=(200, 100))
			self.attackButtons.insert(i,element)
			self.attackButtons[i].SetTopStartColour(wx.Colour(168-30*i, 184, 184))
			self.attackButtons[i].SetTopEndColour(wx.Colour(70-10*i, 89, 89))
			self.attackButtons[i].SetBottomStartColour(wx.Colour(66-10*i, 82, 82))
			self.attackButtons[i].SetPressedTopColour(wx.Colour(88, 110, 110))
			self.attackButtons[i].SetPressedBottomColour(wx.Colour(54, 43, 43))
			self.attackButtons[i].SetFont(wx.Font(pointSize=18, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD))
			self.attackButtons[i].Bind(wx.EVT_BUTTON, lambda event, index=i: self.attack(index, False))
			self.attackButtons[i].Bind(wx.EVT_MOUSE_EVENTS, lambda event, index=i: self.onMouseBtn(event,index))
			self.hbox.Add(self.attackButtons[i], flag=wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP, border=10)

		#Then we create the pass button a bit differently
		self.passButton = GB.GradientButton(self, -1, label='Pass', size=(120, 100))
		self.passButton.SetTopStartColour(wx.Colour(168, 184, 184))
		#self.passButton.SetTopStartColour(wx.Colour(212, 0, 0)) #
		#self.passButton.SetTopEndColour(wx.Colour(70, 89, 89))
		self.passButton.SetTopEndColour(wx.Colour(120, 0, 0)) #
		#self.passButton.SetBottomStartColour(wx.Colour(66, 82, 82))
		self.passButton.SetBottomStartColour(wx.Colour(112, 0, 0)) #
		self.passButton.SetBottomEndColour(wx.Colour(80, 0, 0)) #
		#self.passButton.SetPressedTopColour(wx.Colour(88, 110, 110))
		self.passButton.SetPressedTopColour(wx.Colour(120, 10, 10)) #
		#self.passButton.SetPressedBottomColour(wx.Colour(54, 43, 43))
		self.passButton.SetPressedBottomColour(wx.Colour(100, 0, 0)) #
		self.passButton.SetFont(wx.Font(pointSize=18, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD))
		self.hbox.Add(self.passButton, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP, border=10)
		self.passButton.Bind(wx.EVT_BUTTON, lambda event: self.attack(-1, True))
		self.passButton.Bind(wx.EVT_MOUSE_EVENTS, self.onMousePass)

		self.vbox.Add(self.hbox, flag=wx.ALL|wx.ALIGN_CENTER, border=10)
		self.SetSizer(self.vbox)

	#when you press one of the attack buttons
	def attack(self, num, passTurn):
		self.disableAll()
		self.GetParent().gamePanel.isMyTurn = False
		self.GetParent().playerAction(num, passTurn)
		self.setLabels(self.GetParent().game.players[0].mainCard)

	#When you hover over attack button with index btnNr
	def onMouseBtn(self, event, btnNr):
		if event.Moving():
			attack = self.GetParent().game.players[0].mainCard.attacks[btnNr]
			self.GetParent().infoPanel.setAttackInfo(attack)
		event.Skip()

	#When you hover over the pass button
	def onMousePass(self, event):
		if event.Moving():
			self.GetParent().infoPanel.setPassInfo()
		event.Skip()

	# Usage: c.setAttackLabels(card)
	# Pre  : card is Card
	# Post : the labels on the attack buttons have been updated to the 
	#        attacks on card
	def setLabels(self, card):
		self.Freeze()
		self.attackButtons[0].SetLabel(card.attacks[0].name)
		self.attackButtons[1].SetLabel(card.attacks[1].name)
		self.attackButtons[2].SetLabel(card.attacks[2].name)
		self.attackButtons[3].SetLabel(card.attacks[3].name)
		self.Layout()
		self.Thaw()

	# Usage: c.disableAll()
	# Post : all of the attack buttons have been disabled
	def disableAll(self):
		self.Freeze()
		self.attackButtons[0].Disable()
		self.attackButtons[1].Disable()
		self.attackButtons[2].Disable()
		self.attackButtons[3].Disable()
		self.passButton.Disable()
		self.attackButtons[0].SetTopStartColour(wx.Colour(66, 82, 82))
		self.attackButtons[1].SetTopStartColour(wx.Colour(66, 82, 82))
		self.attackButtons[2].SetTopStartColour(wx.Colour(66, 82, 82))
		self.attackButtons[3].SetTopStartColour(wx.Colour(66, 82, 82))
		#self.passButton.SetTopStartColour(wx.Colour(66, 82, 82))
		self.passButton.SetTopStartColour(wx.Colour(112, 0, 0))
		self.Thaw()

	# Usage: c.enableAll()
	# Post : all of the attack buttons have been enabled
	def enableAll(self):
		self.Freeze()
		self.attackButtons[0].Enable()
		self.attackButtons[1].Enable()
		self.attackButtons[2].Enable()
		self.attackButtons[3].Enable()
		self.passButton.Enable()
		self.attackButtons[0].SetTopStartColour(wx.Colour(168, 184, 184))
		self.attackButtons[1].SetTopStartColour(wx.Colour(168, 184, 184))
		self.attackButtons[2].SetTopStartColour(wx.Colour(168, 184, 184))
		self.attackButtons[3].SetTopStartColour(wx.Colour(168, 184, 184))
		self.passButton.SetTopStartColour(wx.Colour(168, 184, 184))
#		self.passButton.SetTopStartColour(wx.Colour(112, 0, 0))
		self.Thaw()

# Displays info
class infoPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, size=(220, 370))
		self.SetDoubleBuffered(True)

		self.vbox = wx.BoxSizer(wx.VERTICAL)
		self.vbox1 = wx.BoxSizer(wx.VERTICAL)
		self.vboxatt = wx.BoxSizer(wx.VERTICAL)
		self.hboxTooltip = wx.BoxSizer(wx.HORIZONTAL)
		self.hboxStamina = wx.BoxSizer(wx.HORIZONTAL)
		titlefont = wx.Font(pointSize=22, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD)
		font = wx.Font(pointSize=17, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD)
		fc = '#CCCCCC'

		self.name = wx.StaticText(self, label='Name', style=wx.ALIGN_LEFT)
		self.name.SetFont(titlefont)
		self.name.SetForegroundColour(fc)
		self.vbox1.Add(self.name, flag=wx.ALIGN_CENTER, border=10)

		self.tooltip = wx.StaticText(self, label='tooltip', style=wx.ALIGN_LEFT)
		self.tooltip.SetFont(font)
		self.tooltip.SetForegroundColour(fc)

		self.hboxTooltip.Add(self.tooltip, flag=wx.ALIGN_CENTER, border=10)
		self.vbox1.Add(self.hboxTooltip, flag=wx.ALIGN_LEFT, border=10)

		self.SetSizer(self.vbox1)

		self.name.SetLabel('')
		self.tooltip.SetLabel('')

	# Usage: c.setPokeInfo(card)
	# Pre  : card is Card
	# Post : the labels on the infoPanel has been updated to the 
	#        info on card
	def setPokeInfo(self, pcard):
		self.Freeze()
		self.name.SetLabel('-'+str(pcard.name)+'-')
		self.tooltip.SetLabel(pcard.getInfo())
		self.Layout()
		self.Thaw()

	# Usage: c.setAttackInfo(attack)
	# Pre  : card is Attack
	# Post : the labels on the infoPanel have been updated to the 
	#        attack info which is on attack
	def setAttackInfo(self, attack):
		self.Freeze()
		self.name.SetLabel('-' + str(attack.name) + '-')
		self.tooltip.SetLabel(attack.getInfo())
		self.Layout()
		self.Thaw() 

	# Usage: c.setPassInfo()
	# Pre  : card is Attack
	# Post : the labels on the infoPanel have been updated to indicate that 
	#		 player wants to pass on his turn
	def setPassInfo(self):
		self.Freeze()
		self.name.SetLabel('- Pass -')
		self.tooltip.SetLabel('If you prefer\nnot to attack\nyour enemy you\ncan pass on\nyour turn.')
		self.Layout()
		self.Thaw() 

	# Usage: c.setInventoryInfo(icard)
	# Pre  : card is invCard
	# Post : the labels on the infoPanel has  been updated to the 
	#        info on icard
	def setInventoryInfo(self, icard):
		self.Freeze()
		self.name.SetLabel('-' + icard.getName() + '-')
		self.tooltip.SetLabel(icard.getInfo())
		self.Layout()
		self.Thaw()

# A panel that displays information about the events that are occurring during gameplay
class LogPanel(scrolled.ScrolledPanel):
	def __init__(self, parent):
		wx.ScrolledWindow.__init__(self, parent, size=(220, 300), style=wx.RAISED_BORDER)
		self.SetBackgroundColour('#151A1A')
		self.SetDoubleBuffered(True)
		self.SetAutoLayout(1) 
		self.SetupScrolling(scroll_x=False, scroll_y=True, scrollToTop=False)

		self.vbox = wx.BoxSizer(wx.VERTICAL)
		self.numMsg = 0

		self.font = wx.Font(pointSize=12, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD)
		self.fc = '#CCCCCC'
		
		self.SetSizer(self.vbox)

	# Adds new information to the log
	def updateLog(self):
		self.Freeze()
		length = len(self.GetParent().game.textLog)
		for i in range(self.numMsg, length):
			text = wx.StaticText(self, label=self.GetParent().game.textLog[i], style=wx.EXPAND)
			text.SetFont(self.font)
			text.SetForegroundColour(self.fc)
			text.Wrap(self.GetSize().width-18)
			self.vbox.Add(text, flag=wx.EXPAND, border=10)
			self.numMsg += 1
		self.SetSizer(self.vbox)
		self.Layout()
		self.FitInside()
		self.Scroll(-1, self.GetVirtualSize()[1])
		self.Thaw()

# The main frame for the game
class MainFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, title="Pokemon", size=(1290, 725), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
		self.SetBackgroundColour('#435353')		
		#Create sizers
		self.vbox1 = wx.BoxSizer(wx.VERTICAL)
		self.vbox2 = wx.BoxSizer(wx.VERTICAL)
		self.hbox = wx.BoxSizer(wx.HORIZONTAL)
		self.gamePanelBox = wx.BoxSizer(wx.HORIZONTAL)
		#Load presets so we can put presets decks in menu
		presets = Presets()

		#Determines the difficulty setting
		self.difficulty = "computer"

		#Decks that human(hmn) and computer (cpu) want to use
		self.hmnDeck = "Random"
		self.cpuDeck = "Random"

		#Define menus and panels
		self.menuBar = wx.MenuBar()
		self.infoPanel = infoPanel(self)
		self.gamePanel = GamePanel(self, wx.ID_ANY)
		self.attackPanel = AttackPanel(self)
		self.logPanel = LogPanel(self)
		self.statusBar = self.CreateStatusBar()

		self.game = self.initGame()

		#Setup the menu
		self.fileMenu = wx.Menu()
		m_newGame = self.fileMenu.Append(wx.ID_ANY, "&New Game\tAlt+N", "Start a new game!")

		# Sub menu to choose difficulty
		m_difficulty = wx.Menu()
		m_diffHard = m_difficulty.AppendRadioItem(-1, "Hard")
		m_diffNormal = m_difficulty.AppendRadioItem(-1, "Normal")
		m_diffEasy = m_difficulty.AppendRadioItem(-1, "Easy")
		self.Bind(wx.EVT_MENU, self.OnChooseDifficulty, m_diffHard)
		self.Bind(wx.EVT_MENU, self.OnChooseDifficulty, m_diffNormal)
		self.Bind(wx.EVT_MENU, self.OnChooseDifficulty, m_diffEasy)

		#Sub menu for decks that  you might want to use
		m_yourDeck = wx.Menu()
		m_yourDeck.AppendRadioItem(-1, "Random")
		for key,val in presets.decks.iteritems():
			m_element = m_yourDeck.AppendRadioItem(-1, str(val.name))
			self.Bind(wx.EVT_MENU, self.OnNewSelectedYourDeck, m_element)
		
		#Sub menu for decks that you might want the computer to use
		m_enemDeck = wx.Menu()
		m_enemDeck.AppendRadioItem(-1, "Random")
		for key,val in presets.decks.iteritems():
			m_element = m_enemDeck.AppendRadioItem(-1, str(val.name))
			self.Bind(wx.EVT_MENU, self.OnNewSelectedEnemDeck, m_element)

		#Add sub menus to the filemenu
		self.fileMenu.AppendMenu(wx.ID_ANY, 'D&ifficulty', m_difficulty)
		self.fileMenu.AppendMenu(wx.ID_ANY, 'Y&our Deck', m_yourDeck)
		self.fileMenu.AppendMenu(wx.ID_ANY, 'E&nemy Deck', m_enemDeck)

		#We want to seperate newgame, yourdeck and enemy deck from help and exit 
		self.fileMenu.AppendSeparator()

		#Music options:
		m_music = wx.Menu()
		m_play = m_music.AppendRadioItem(-1, "Playing")
		m_mute = m_music.AppendRadioItem(-1, "Muted")
		self.Bind(wx.EVT_MENU, self.OnMuted, m_play)
		self.Bind(wx.EVT_MENU, self.OnMuted, m_mute)

		self.fileMenu.AppendMenu(wx.ID_ANY, "M&usic", m_music)


		#Helpmenu:
		m_help = self.fileMenu.Append(wx.ID_HELP, "&Help\tAlt+H", "Read instructions for this awesome pokemon game!")
		self.Bind(wx.EVT_MENU, self.OnHelp, m_help)

		#Exit button
		m_exit = self.fileMenu.Append(wx.ID_EXIT, "&Exit\tAlt+X", "Close window and exit program.")

		#PLayer for the music:

		self.player = wx.media.MediaCtrl(parent = self, szBackend=wx.media.MEDIABACKEND_WMP10)
		self.player.Load(r'PokemoanSong.wav')
		self.Bind(wx.media.EVT_MEDIA_LOADED, self.playSong)

		#loop the main song:
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.OnTimer)
		self.timer.Start(354000)

		#is the music on?
		self.isPlaying = True

		#add filemenu to the menubar and bind events
		self.menuBar.Append(self.fileMenu, "&File")
		self.Bind(wx.EVT_MENU, self.onQuit, m_exit)
		self.Bind(wx.EVT_MENU, self.OnNewGame, m_newGame)

		self.SetMenuBar(self.menuBar)

		self.updateStatus()

		self.gamePanelBox.Add(self.gamePanel, 0, flag=wx.EXPAND)
		self.vbox1.Add(self.gamePanelBox, 0, flag=wx.EXPAND)
		self.vbox1.Add(self.attackPanel, 0, flag=wx.EXPAND)
		self.vbox2.Add(self.infoPanel, 0, flag=wx.EXPAND)
		self.vbox2.Add(self.logPanel, 0, flag=wx.EXPAND)
		self.hbox.Add(self.vbox1, 0, flag=wx.EXPAND)
		self.hbox.Add(self.vbox2, 0, flag=wx.EXPAND)

		self.SetAutoLayout(True)
		self.SetSizer(self.hbox)
		self.Layout()
		self.Centre()
	
	def OnMuted(self, event):
		item = self.GetMenuBar().FindItemById(event.GetId())
		if item.GetText() == "Muted" :
			self.player.Pause()
			self.isPlaying = False
		elif item.GetText() == "Playing" :
			self.player.Play()
			self.isPlaying = True

	def playSong(self, event):
		self.player.Play()

	def OnTimer(self, event):
		if(self.isPlaying):
			self.player.Load(r'PokemoanSong.wav')
		
	
	# Initializes the game itself
	def initGame(self):
		presets = Presets()

		#create player 1 give him a hand, random mainCard and a random 10card deck
		p1 = Player("player1")
		p1.hand = Hand()
		p1.inv = Inventory()
		p1.deck = presets.gd(self.hmnDeck)
		p1.deck.shuffle()
		p1.invdeck = InvDeck()
		p1.mainCard = p1.deck.cards[0]
		for i in xrange(0,100):
			p1.invdeck.add(presets.getRandomInvCard())

		#create player 1 give him a hand, random mainCard and a random 10card deck
		p2 = Player(self.difficulty)
		p2.hand = Hand()
		p2.inv = Inventory()
		p2.deck = presets.gd(self.cpuDeck)
		p2.deck.shuffle()
		p2.invdeck = InvDeck()
		p2.mainCard = p2.deck.cards[0]
		for i in xrange(0,100):
			p2.invdeck.add(presets.getRandomInvCard())
		
		game = Main([p1, p2])
		self.gamePanel.setupPanel(p1, p2)

		return game

	#When difficulty radio button is pressed
	def OnChooseDifficulty(self, event):
		item = self.GetMenuBar().FindItemById(event.GetId())
		if item.GetText() == "Hard":
			self.difficulty = "computer"
		elif item.GetText() == "Normal":
			self.difficulty = "normalcomputer"
		elif item.GetText() == "Easy":
			self.difficulty = "easycomputer"

	#When yourdeck radio button is pressed
	def OnNewSelectedYourDeck(self, event):
		#get id of button pressed and set hmn deck to the value of that button (string)
		item = self.GetMenuBar().FindItemById(event.GetId())
		self.hmnDeck = item.GetText()

	#When enemy deck radio button is pressed
	def OnNewSelectedEnemDeck(self, event):
		#get id of button pressed and set cpu deck to the value of that button (string)
		item = self.GetMenuBar().FindItemById(event.GetId())
		self.cpuDeck = item.GetText()

	#when player presses the new game button
	def OnNewGame(self, event):	
		self.Freeze()
		self.game = self.initGame()
		self.game.textLog.append('--- New Game ---\n')
		self.gamePanel.Destroy()
		self.gamePanel = GamePanel(self, wx.ID_ANY)
		self.gamePanelBox.Add(self.gamePanel, 0, flag=wx.EXPAND)
		self.gamePanel.setupPanel(self.game.players[0], self.game.players[1])
		self.updateStatus()
		self.attackPanel.enableAll()
		self.Thaw()

	# Displays a help window
	def OnHelp(self, event):
		helpw = HelpFrame()
		helpw.Show()

	# Updates the status bar and some game information
	def updateStatus(self):
		self.logPanel.updateLog()
		drawInv = self.game.drawInvQuest()
		self.gamePanel.canDrawInv = drawInv
		if drawInv:
			canInv = 'Yes'
		else:
			canInv = 'No'
		score = 'Score: Player ' + str(self.game.players[0].points) + ' - ' + str(self.game.players[1].points) + ' CPU'
		player1 = self.game.players[0].mainCard
		player2 = self.game.players[1].mainCard
		player1str = player1.name + ': hp: ' + str(player1.health) + ' sta: ' + str(player1.stamina) + ' stun: ' + str(player1.stun)
		player2str = player2.name + ': hp: ' + str(player2.health) + ' sta: ' + str(player2.stamina) + ' stun: ' + str(player2.stun)
		inv = 'Can draw inventory: ' + canInv
		turn = 'Turn: ' + str(self.game.turn)
		self.statusBar.SetStatusText(score + '   |   ' + player1str + '   |   ' + player2str + '   |   ' + turn + '   |   ' + inv)
		
		if player1.stun:
			self.gamePanel.setPlayerStunned()
		else:
			self.gamePanel.setPlayerNotStunned()

		if player2.stun:
			self.gamePanel.setCPUStunned()
		else:
			self.gamePanel.setCPUNotStunned()

	# The player chooses an attack
	def playerAction(self, attackNum, passTurn):
		if self.game.players[0].mainCard.isDead():
			# if the player tries to attack with a dead pokemon
			self.game.textLog.append('You must choose a new pokemon!\n')
			self.attackPanel.enableAll()
			self.gamePanel.isMyTurn = True
			self.updateStatus()
			return
		if not passTurn:
			if self.game.players[0].attack(attackNum, self.game.players[1], self.game.textLog):
				# player attacks
				self.gamePanel.animation1(True)
				if not self.game.players[0].mainCard.isDead():
					# if player doesn't die from it's own attack
					self.gamePanel.updateCPUHp(False)
					self.gamePanel.updateCPUStamina()
				elif self.game.players[1].mainCard.isDead():
					# if player dies from its own attackand also kills the CPU's pokemon
					self.gamePanel.updateCPUHp(True)
			else:
				# if player doesn't have enough stamina for the chosen attack
				self.attackPanel.enableAll()
				self.gamePanel.isMyTurn = True
				self.updateStatus()
				return
		else:
			# the player passes its turn
			self.game.textLog.append('You passed your turn\n')
		self.game.turnCount += 1
		self.gamePanel.hasDrawnInv = False
		self.gamePanel.hasDrawnPoke = False
		self.game.players[0].mainCard.applyEffects()
		self.gamePanel.updatePlayerHp()
		self.gamePanel.updatePlayerStamina()
		self.updateStatus()
		if not self.checkWin():
			worker = Worker(self.gamePanel, -1, 0, 0, 'wait1')

		

	# The CPU performs an action
	def CPUAction(self):
		self.game.turnCount += 1
		self.game.draw(self.game.players[1])
		self.gamePanel.addCPUpokemon()
		if self.game.drawInvQuest():
			# draws an inventory card if it can
			self.game.drawInv(self.game.players[1])
		if self.game.players[1].mainCard.isDead():
			# choose a new pokemon to put out if the currently chosen one is dead
			newCard = self.game.chooseCardAI(self.game.players[1], self.game.players[0])
			self.game.players[1].mainCard = newCard
			self.game.textLog.append('Opponent put out ' + newCard.name + '\n')
			self.updateStatus()
			self.gamePanel.switchCPUpokemon(newCard)
			time.sleep(1)
		if not self.game.players[0].mainCard.isDead():
			# If the player's currently chosen pokemon isn't dead the CPU tries to attack it
			if self.game.chooseAttackAI(self.game.players[1], self.game.players[0]):
				# CPU attacks
				self.gamePanel.animation1(False)
				self.gamePanel.updatePlayerHp()
				if self.game.players[1].mainCard.isDead():
					# if the CPU kills itself with its attack it choose a new pokemon to put out
					newCard = self.game.chooseCardAI(self.game.players[1], self.game.players[0])
					self.gamePanel.updateCPUHp(True)
					self.gamePanel.CPUselfdestruct = True
					self.game.players[1].mainCard = newCard
					self.game.textLog.append('Opponent put out ' + newCard.name + '\n')
					self.gamePanel.switchCPUpokemon(newCard)
		self.game.players[1].mainCard.applyEffects()
		self.gamePanel.updateCPUHp(False)
		self.gamePanel.updateCPUStamina()
		if not self.checkWin():
			worker = Worker(self.gamePanel, 0, 0, 1, 'wait2')


	# Returns True if the game is won or lost, otherwise False
	def checkWin(self):
		if self.game.players[0].points >= pointsToWin:
			self.gamePanel.isMyTurn = False
			self.gamePanel.setWinSign()
			self.gamePanel.Update()
			self.updateStatus()
			return True
		elif self.game.players[1].points >= pointsToWin:
			self.gamePanel.isMyTurn = False
			self.gamePanel.setLoseSign()
			self.gamePanel.Update()
			self.updateStatus()
			return True
		return False

	# Exit the program
	def onQuit(self, event):
		self.Close()

# A window that displays game instructions
class HelpFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, title="Pokemon", size=(850, 725), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
		self.SetBackgroundColour('#435353')		
		self.vbox1 = wx.BoxSizer(wx.VERTICAL)
		self.help = wx.StaticText(self, label='help', style=wx.ALIGN_LEFT)
		font = wx.Font(pointSize=12, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD)
		self.help.SetFont(font)
		fc = '#CCCCCC'
		self.help.SetForegroundColour(fc)
		try:
			with open("instructions.txt") as myFile:
				data = myFile.read()
		except:
			data = 'Failed to load instructions'

		self.help.SetLabel(data)


