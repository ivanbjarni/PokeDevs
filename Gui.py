import subprocess
import tempfile
import wx
import sys
import os
import time
import threading
import wx.lib.agw.gradientbutton as GB
import wx.lib.scrolledpanel as scrolled
import random
from AI import *
from constants import *

# Define notification events for threads
EVT_ANIM_ID = wx.NewId()

def EVT_ANIM(win, func):
	win.Connect(-1, -1, EVT_ANIM_ID, func)
 
class AnimEvent(wx.PyEvent):
    def __init__(self, id, dx, dy, moveY, done):
		wx.PyEvent.__init__(self)
		self.SetEventType(EVT_ANIM_ID)
		self.id = id
		self.dx = dx
		self.dy = dy
		self.moveY = moveY
		self.done = done

# A worker thread that handles long running task so the GUI doesn't stop functioning
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

	def run(self):
		if self.animation == 'animation1':
			self.animation1()
		elif self.animation == 'bar':
			self.bar()
		elif self.animation == 'wait1':
			self.wait(1)
		elif self.animation == 'wait2':
			self.wait(-1)

	def animation1(self):
		forward = True
		while(self.i < self.j):
			time.sleep(0.01)
			if forward:
				dx = random.randint(1, 41) - 20
				dy = random.randint(1, 21) - 10

				self.anim.append([dx, dy])
				wx.PostEvent(self.wxObject, AnimEvent(self.id, dx, dy, -1, False))

				if self.i > 0:
					self.i -= 1
				else:
					forward = False
			else:
				dx, dy = self.anim.pop()

				wx.PostEvent(self.wxObject, AnimEvent(self.id, -dx, -dy, -1, False))
				self.i += 1

	def bar(self):
		if self.i < self.j:
			while self.i < self.j:
				time.sleep(0.005)
				self.i += 1
				wx.PostEvent(self.wxObject, AnimEvent(self.id, 0, 1, self.i, False))
				#self.i += 1
		else:
			while self.i > self.j:
				time.sleep(0.005)
				self.i -= 1
				wx.PostEvent(self.wxObject, AnimEvent(self.id, 0, -1, self.i, False))
				#self.i -= 1

	def wait(self, i):
		if i != -1:
			waitingTime = random.randint(1,3)
			time.sleep(waitingTime)
			try:
				wx.PostEvent(self.wxObject, AnimEvent(self.id, 0, 0, -1, True))
			except:
				'Program exited'
		else:
			waitingTime = 1
			time.sleep(waitingTime)
			try:
				wx.PostEvent(self.wxObject, AnimEvent(self.id, 0, -1, -1, True))
			except:
				'Program exited'

# A drawable panel that contains the Playing Area
class GamePanel(wx.ScrolledWindow):
	def __init__(self, parent, id, size=wx.DefaultSize):
		# This needs to be a scrolled window even though it doesn't scroll
		wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=(1060, 560), style=wx.SUNKEN_BORDER)
		self.SetDoubleBuffered(True)

		self.isMyTurn = True 		# Determines wheather you can move cards around
		self.hasDrawnPoke = False 	# Determines wheather you have drawn a pokemon this round
		self.canDrawInv = False 	# Determines wheather you can drag an inventory card
		self.hasDrawnInv = False 	# Determines wheather you have drawn an inventory card this round
		self.hitradius = 5			# How many pixels you can be "off" when trying to click on something
		self.objids = []			# ID's of movable objects on the screen
		self.countCPUpokemon = 0 	# Count how many pokemon CPU has drawn
		self.pdc = wx.PseudoDC()	# For drawing to the panel
		self.dragid = -1 			# ID for currently chosen object
		self.playerChosenID = -1 	# ID for player's currently chosen object
		self.CPUChosenID = -1 		# ID for CPU's currently chosen object
		self.graveyardID = -1 		# ID of pokemon in graveyard
		self.playerHealthID = -1 	# ID for players healthbar
		self.playerStaminaID = -1 	# ID for players stamina bar
		self.CPUHealthID = -1 		# ID for CPU health bar
		self.CPUStaminaID = -1 		# ID for CPU stamina bar
		self.winId = -1 			# ID for text that displays when you win
		self.loosId = -1 			# ID for text that displays when you loose
		self.movable = {}			# Dict of wheather or not a card can be moved by player, by id
		self.origpos = {}			# Dict of original position of bitmaps by id
		self.cards = {}				# Dict of cards by id
		self.cardsCPU = [] 			# List of CPU cards
		self.cardType = {} 			# Dict of card types by id
		self.backsides = {} 		# Dict of backside ids to link backsides to cards
		self.backsidesInv = {} 		# Dict of inventory backside ids to link to inventory cards
		self.backsidesCPU = {} 		# Dict of CPU backsides
		self.slot = {} 				# Dict of slot number for cards by id 
		self.invSlot = {} 			# Dict of slot number for inventory cards by
		self.slotCPU = {}			# Dict of slot number for CPU cards by id
		self.anim = []				# List of moves for animations
		self.lastpos = (0,0)		# Lates position of the mouse while dragging
		self.startpos = (0,0)		# Position of the mouse when clicked
		self.backsideBmp = None		# Bitmap of the backside of a pokemon card
		self.backsideInvBmp = None 	# Bitmap of the backside of an inventory card

		wx.Log.SetLogLevel(0) # remove this and fix images

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

	# Sets the bitmap for card
	def setImage(self, card):
		name = card.name.replace(' ', '').replace('.', '')
		try:
			image = wx.Image('images/Pokecards/' + name + '.jpg', wx.BITMAP_TYPE_ANY)
			image = image.Scale(116, 165, wx.IMAGE_QUALITY_HIGH)
			card.bitmap = image.ConvertToBitmap()
		except:
			print 'Failed to load card: ' + str(name)

	# Sets the bitmap for card
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

	#Handles mouse events
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

		# Move object back to original position if left button is realeased or the mouse leaves the panel
		elif event.LeftUp() or event.Leaving():
			if self.dragid != -1:
				dx = event.GetX()
				dy = event.GetY()

				if self.cardType[self.dragid] == 'Pokemon': 
					if self.inPlayerChosenArea(dx, dy) and self.playerChosenID != self.dragid and self.playerChosenID == self.graveyardID:
						# Switch currently chosen pokemon out for a new one 
						x = self.startpos[0] - self.lastpos[0] - self.origpos[self.dragid][0] + 119
						y = self.startpos[1] - self.lastpos[1] - self.origpos[self.dragid][1] + 195
						self.GetParent().attackPanel.setLabels(self.cards[self.dragid])
						slot = self.slot[self.dragid]
						tx = -106 + slot * 127
						ty = 189
						#if not self.pdc.GetIdGreyedOut(self.playerChosenID):
						if self.playerChosenID != self.graveyardID:
							self.moveItem(self.playerChosenID, tx, ty)
							self.slot[self.playerChosenID] = slot
	#					else:
						self.slot[self.playerChosenID] = -1
						self.moveItem(self.dragid, x, y)
						self.slot[self.dragid] = -1 ######################
						self.origpos[self.playerChosenID] = [13 + slot * 127, 384]
						self.playerChosenID = self.dragid
						self.GetParent().game.players[0].mainCard = self.cards[self.dragid]
						self.GetParent().updateStatus()
						self.GetParent().game.textLog.append('You put out ' + self.GetParent().game.players[0].mainCard.name + '\n')
						self.updatePlayerHp()
						self.updatePlayerStamina()
					else:
						x = self.startpos[0] - self.lastpos[0]
						y = self.startpos[1] - self.lastpos[1]
						self.moveItem(self.dragid, x, y)
						if self.inPlayerChosenArea(dx, dy):
							self.GetParent().game.textLog.append('You can not switch out your pokemon')

				elif self.cardType[self.dragid] == 'Backside':
					slot = self.findEmptySlot(self.slot)
					if self.inPlayerHandArea(dx, dy) and slot != -1 and not self.hasDrawnPoke:
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
						self.moveItem(self.dragid, 0, -1000)
						self.invSlot[self.dragid] = -1
						self.GetParent().game.players[0].use(self.cards[self.dragid], self.GetParent().game.textLog)
						self.updatePlayerHp()
						self.updatePlayerStamina()
					elif self.inCPUChosenArea(dx, dy):
						self.moveItem(self.dragid, 0, -1000)
						self.invSlot[self.dragid] = -1
						self.GetParent().game.players[1].use(self.cards[self.dragid], self.GetParent().game.textLog)
						self.updateCPUHp()
						self.updateCPUStamina()
					else:
						x = self.startpos[0] - self.lastpos[0]
						y = self.startpos[1] - self.lastpos[1]
						self.moveItem(self.dragid, x, y)
				self.dragid = -1
				self.GetParent().logPanel.updateLog()

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

	def inPlayerChosenArea(self, dx, dy):
		return  (110 < dx and dx < 245) and (376 > dy and dy > 182)

	def inCPUChosenArea(self, dx, dy):
		return (535 < dx and dx < 717) and (376 > dy and dy > 182)
	
	def inPlayerHandArea(self, dx, dy):
		return (3 < dx and dx < 778) and (555 > dy and dy > 308)

	def inPlayerInvArea(self, dx, dy):
		return (782 < dx and dx < 917) and (552 > dy and dy > 3)

	def findCard(self, id):
		for card in self.cards.iteritems():
			if id == card[0]:
				return card[1]

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

	def moveItem(self, id, x, y):
		r = self.pdc.GetIdBounds(id)
		self.pdc.TranslateId(id, x, y)
		r2 = self.pdc.GetIdBounds(id)
		r = r.Union(r2)
		r.Inflate(4, 4)
		self.offsetRect(r)
		self.RefreshRect(r, False)

	def moveItemToGraveyard(self, id, x, y):
		if self.graveyardID != -1:
			self.moveItem(self.graveyardID, 0, -1000)
			self.pdc.SetIdGreyedOut(self.graveyardID)
		self.graveyardID = id
		self.moveItem(self.graveyardID, x, y)

	def updateDisplay(self, msg):
		if msg.moveY != -1:
			self.origpos[msg.id][1] = msg.moveY
		if not msg.done:
			self.moveItem(msg.id, msg.dx, msg.dy)
			self.Update()
		elif msg.done and msg.dy != -1:
			self.GetParent().CPUAction()
		else:
			self.isMyTurn = True
			self.GetParent().attackPanel.enableAll()
			self.GetParent().game.turn += 1
			self.GetParent().updateStatus()

	# Usage: g.animation(self, isPlayer)
	# Pre  : isPlayer is a boolean value that determines if the players or the
	#		 CPU's pokemon should be "shaken"
	# Post : if isPlayer == True player's currently chosen pokemon is "shaken"
	#		 otherwise the CPU's currently chosen pokemon is "shaken"
	def animation1(self, isPlayer):
		if isPlayer:
			id = self.playerChosenID
		else:
			id = self.CPUChosenID

		anim = Worker(self, id, 10, 11, 'animation1')

	#	def updatePlayerHP(self, card):
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

	def updatePlayerHp(self):
		hp = self.updateBar(self.playerHealthID, self.cards[self.playerChosenID], 'health')
		if hp == 0:
			self.GetParent().game.players[1].points += 1
			self.GetParent().game.textLog.append(self.cards[self.playerChosenID].name + ' fainted\n')
			self.moveItemToGraveyard(self.playerChosenID, 812, 185)
			self.slot[self.playerChosenID] = -1

	def updatePlayerStamina(self):
		stamina = self.updateBar(self.playerStaminaID, self.cards[self.playerChosenID], 'stamina')

	def updateCPUHp(self):
		hp = self.updateBar(self.CPUHealthID, self.cards[self.CPUChosenID], 'health')
		if hp == 0:
			self.GetParent().game.players[0].points += 1
			self.GetParent().game.textLog.append(self.cards[self.CPUChosenID].name + ' fainted\n')
			self.moveItemToGraveyard(self.CPUChosenID, 387, 185)
			self.slotCPU[self.CPUChosenID] = -1

	def updateCPUStamina(self):
		stamina = self.updateBar(self.CPUStaminaID, self.cards[self.CPUChosenID], 'stamina')

	# Updates the playing area
	def onPaint(self, event):
		dc = wx.BufferedPaintDC(self)
		self.PrepareDC(dc)
		dc.Clear()
		rgn = self.GetUpdateRegion()
		r = rgn.GetBox()
		self.pdc.DrawToDCClipped(dc, r)

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

	def switchCPUpokemon(self, card):
		if self.cardsCPU:
			id = self.findID(card)
			bid = self.findBacksideCPU(id)
			self.slotCPU[bid] = -1
			self.CPUChosenID = id
			self.moveItem(id, 744, 395)
			self.moveItem(bid, 0, -1000)
			self.Update()

	def findID(self, card):
		for id in self.cards.iteritems():
			if card == id[1]:
				return id[0]

	def findBacksideCPU(self, id):
		for bid in self.backsidesCPU.iteritems():
			if id == bid[1]:
				return bid[0]

	def drawItem(self, dc, id, bitmap, x, y, w, h):
		dc.DrawBitmap(bitmap, x, y, True)
		dc.SetIdBounds(id, wx.Rect(x, y, w, h))
		self.objids.append(id)

	def drawBar(self, dc, x, y, w, h, color):
		# draw the bar outline
		pen = wx.Pen('#000000', 1)
		brush = wx.Brush('#FFFF66')
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

	# Draws the inital playing area
	def doDrawing(self, dc, player, CPU):
		dc.BeginDrawing()
		try:
			background = wx.Bitmap("images/pokematBasic.png")
		except:
			print 'Failed to load backround image'
		dc.DrawBitmap(background, 0, 0)

		pen = wx.Pen('#435353', 2)
		brush = wx.Brush('#A8B8B8')
		dc.SetPen(pen)
		dc.SetBrush(brush)

		player1pokePanel = wx.Rect(3, 380, 775, 175)
		player2pokePanel = wx.Rect(3, 3, 775, 175)
		player1invPanel = wx.Rect(782, 3, 135, 552)
#		player2invPanel = wx.Rect(782, 3, 135, 275)
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
#		dc.DrawRoundedRectangleRect(player2invPanel, 10)
		dc.DrawRoundedRectangleRect(player2chosenPanel, 10)
		brush = wx.Brush('#435353')
		dc.SetBrush(brush)
		dc.DrawRoundedRectangleRect(inventoryDeckPanel, 10)
		dc.DrawRoundedRectangleRect(cardDeckPanel, 10)
		dc.DrawRoundedRectangleRect(graveyardPanel, 10)

		self.playerHealthID = self.drawBar(dc, 90, 182, 10, 193, '#DB3340')

		self.CPUHealthID = self.drawBar(dc, 680, 182, 10, 193, '#DB3340')

		self.playerStaminaID = self.drawBar(dc, 70, 182, 10, 193, '#28ABE3')

		self.CPUStaminaID = self.drawBar(dc, 700, 182, 10, 193, '#28ABE3')

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

		id = wx.NewId()
		dc.SetId(id)
		self.drawItem(dc, id, CPU.deck.cards[0].bitmap, 544, 195, w, h)
		self.movable[id] = False
		self.cards[id] = CPU.deck.cards[0]
		self.slotCPU[id] = -1
		self.CPUChosenID = id


		for i in range(1, 10):
			id = wx.NewId()
			dc.SetId(id)
			self.drawItem(dc, id, player.deck.cards[i].bitmap, -200, -200, w, h)
			self.movable[id] = True
			self.cardType[id] = 'Pokemon'
			self.cards[id] = player.deck.cards[i]
			self.slot[id] = -1

			bid = wx.NewId()
			dc.SetId(bid)
			self.drawItem(dc, bid, self.backsideBmp, 931, 195, w, h)
			self.movable[bid] = True
			self.cardType[bid] = 'Backside'
			self.backsides[bid] = id

			id = wx.NewId()
			dc.SetId(id)
			self.drawItem(dc, id, CPU.deck.cards[i].bitmap, -200, -200, w, h)
			self.movable[id] = False
			self.cards[id] = CPU.deck.cards[i]
			self.slotCPU[id] = -1
			self.cardsCPU.append(CPU.deck.cards[i])

			bid = wx.NewId()
			dc.SetId(bid)
			self.drawItem(dc, bid, self.backsideBmp, -200, -200, w, h)
			self.movable[bid] = False
			self.backsidesCPU[bid] = id

		for i in range(0, 100):
			id = wx.NewId()
			dc.SetId(id)
			self.drawItem(dc, id, player.invdeck.invCards[i].bitmap, -200, -200, w, h)
			self.movable[id] = True
			self.cardType[id] = 'Inventory'
			self.cards[id] = player.invdeck.invCards[i]
			self.invSlot[id] = -1

			bid = wx.NewId()
			dc.SetId(bid)
			self.drawItem(dc, bid, self.backsideInvBmp, 931, 10, w, h)
			self.movable[bid] = True
			self.cardType[bid] = 'InvBackside'
			self.backsidesInv[bid] = id

		id = wx.NewId()
		dc.SetId(id)
		font = wx.Font(pointSize=100, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD)
		dc.SetFont(font)
		dc.SetTextForeground('#FF00FF')
		text = 'YOU WIN!'
		dc.DrawText(text, -200, -200)
		r = wx.Rect(-200, -200, 1000, 200)
		r.Inflate(2,2)
		dc.SetIdBounds(id, r)
		self.winId = id
		self.movable[id] = False
		self.objids.append(id)

		id = wx.NewId()
		dc.SetId(id)
		dc.SetFont(font)
		dc.SetTextForeground('#0000FF')
		text = 'YOU LOOSE!'
		dc.DrawText(text, -200, -200)
		r = wx.Rect(-200, -200, 1000, 200)
		r.Inflate(2,2)
		dc.SetIdBounds(id, r)
		self.looseId = id
		self.movable[id] = False
		self.objids.append(id)

		dc.EndDrawing()

# A panel that holds the names and HP of currently chosen pokemon
class StatusPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, size=(1200, 100))

		self.vbox = wx.BoxSizer(wx.VERTICAL)
		self.vbox1 = wx.BoxSizer(wx.VERTICAL)
		self.vbox2 = wx.BoxSizer(wx.VERTICAL)
		self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)

		self.pokemon1name = wx.StaticText(self, label='Player', style=wx.ALIGN_LEFT)
		self.pokemon1hp = wx.StaticText(self, label='HP: ---', style=wx.ALIGN_LEFT)
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

	# Usage: c.setPlayerPokemonInfo(card)
	# Pre  : card is the currently chosen card of the player
	# Post : The pokemon name and hp labels have been set to the values given
	#        on the card.
	def setPlayerPokemonInfo(self, card):
		self.Freeze()
		self.pokemon1name.SetLabel(card.name)
#		self.pokemon1hp.SetLabel('HP: ' + str(card.health))
		self.Layout()
		self.Thaw()

	# Usage: c.setCPUPokemonInfo(card)
	# Pre  : card is the currently chosen card of the CPU
	# Post : The pokemon name and hp labels have been set to the values given
	#        on the card.
	def setCPUPokemonInfo(self, card):
		self.Freeze()
		self.pokemon2name.SetLabel(card.name)
		self.pokemon2hp.SetLabel('HP: ' + str(card.health))
		self.Layout()
		self.Thaw()

	# Usage: c.setHpPlayer(hp)
	# Pre  : hp is the current hp of the players chosen pokemon
	# Post : The player pokemon hp label has been set to 'HP: ' + hp
	def setHpPlayer(self, hp):
		self.pokemon1hp.SetLabel('HP:' + str(hp))
		self.Layout()

	# Usage: c.setHpCPU(hp)
	# Pre  : hp is the current hp of ther CPU's chosen pokemon
	# Post : The CPU pokemon hp label has been set to 'HP: ' + hp
	def setHpCPU(self, hp):
		self.pokemon2hp.SetLabel('HP: ' + str(hp))
		self.Layout()

# A panel that holds 4 attack buttons
class AttackPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, size=(1064, 200))

		self.SetBackgroundColour('#435353')

		self.vbox = wx.BoxSizer(wx.VERTICAL)
		self.hbox = wx.BoxSizer(wx.HORIZONTAL)

		self.attackButtons = []

		# Some different variations of buttons, don't know what looks best

		# This button looks nicer than the generic button but I'm not 100% sure it's compatable with
		# other operating systems than windows
		# The label also doesn't center on this button if it is multiline
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

		self.passButton = GB.GradientButton(self, -1, label='Pass', size=(120, 100))
		self.passButton.SetTopStartColour(wx.Colour(168, 184, 184))
		self.passButton.SetTopEndColour(wx.Colour(70, 89, 89))
		self.passButton.SetBottomStartColour(wx.Colour(66, 82, 82))
		self.passButton.SetPressedTopColour(wx.Colour(88, 110, 110))
		self.passButton.SetPressedBottomColour(wx.Colour(54, 43, 43))
		self.passButton.SetFont(wx.Font(pointSize=18, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD))
		self.hbox.Add(self.passButton, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP, border=10)
		self.passButton.Bind(wx.EVT_BUTTON, lambda event: self.attack(-1, True))
		self.passButton.Bind(wx.EVT_MOUSE_EVENTS, self.onMousePass)

		self.vbox.Add(self.hbox, flag=wx.ALL|wx.ALIGN_CENTER, border=10)
		self.SetSizer(self.vbox)

	def attack(self, num, passTurn):
		self.disableAll()
		self.GetParent().gamePanel.isMyTurn = False
		self.GetParent().playerAction(num, passTurn)

	def onMouseBtn(self, event, btnNr):
		if event.Moving():
			attack = self.GetParent().game.players[0].mainCard.attacks[btnNr]
			self.GetParent().infoPanel.setAttackInfo(attack)
		event.Skip()

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
		self.passButton.SetTopStartColour(wx.Colour(66, 82, 82))
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

class MainFrame(wx.Frame):
	def __init__(self, game):
		wx.Frame.__init__(self, None, title="Pokemon", size=(1290, 725), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
		self.SetBackgroundColour('#435353')		
		self.vbox1 = wx.BoxSizer(wx.VERTICAL)
		self.vbox2 = wx.BoxSizer(wx.VERTICAL)
		self.hbox = wx.BoxSizer(wx.HORIZONTAL)

		self.game = game

		self.menuBar = wx.MenuBar()
		self.infoPanel = infoPanel(self)
		#self.statusPanel = StatusPanel(self)
		self.gamePanel = GamePanel(self, wx.ID_ANY)
		self.attackPanel = AttackPanel(self)
		self.logPanel = LogPanel(self)
		self.statusBar = self.CreateStatusBar()

		self.fileMenu = wx.Menu()
		m_exit = self.fileMenu.Append(wx.ID_EXIT, "&Exit\tAlt+X", "Close window and exit program.")
		#Helpmenu:
		m_help = self.fileMenu.Append(wx.ID_HELP, "&Help\tAlt+H", "Read instructions for this awesome pokemon game!")
		self.Bind(wx.EVT_MENU, self.OnHelp, m_help)
		


		self.menuBar.Append(self.fileMenu, "&File")
		self.Bind(wx.EVT_MENU, self.onQuit, m_exit)

		self.SetMenuBar(self.menuBar)

		self.updateStatus()

		#self.vbox.Add(self.statusPanel, 0, flag=wx.EXPAND)
		self.vbox1.Add(self.gamePanel, 0, flag=wx.EXPAND)
		self.vbox1.Add(self.attackPanel, 0, flag=wx.EXPAND)
		self.vbox2.Add(self.infoPanel, 0, flag=wx.EXPAND)
		self.vbox2.Add(self.logPanel, 0, flag=wx.EXPAND)
		self.hbox.Add(self.vbox1, 0, flag=wx.EXPAND)
		self.hbox.Add(self.vbox2, 0, flag=wx.EXPAND)

		self.SetAutoLayout(True)
		self.SetSizer(self.hbox)
		self.Layout()
		self.Centre()

	def OnHelp(self, event):
		helpw = HelpFrame()
		helpw.Show()

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
		player1str = player1.name + ': hp: ' + str(player1.health) + ' st: ' + str(player1.stamina) + ' stun: ' + str(player1.stun)
		player2str = player2.name + ': hp: ' + str(player2.health) + ' st: ' + str(player2.stamina) + ' stun: ' + str(player2.stun)
		inv = 'Can draw inventory: ' + canInv
		turn = 'Turn: ' + str(self.game.turn)
		self.statusBar.SetStatusText(score + '   |   ' + player1str + '   |   ' + player2str + '   |   ' + turn + '   |   ' + inv)

	def playerAction(self, attackNum, passTurn):
	#	self.game.turn += 1
		self.game.turnCount += 1
		self.gamePanel.hasDrawnInv = False
		self.gamePanel.hasDrawnPoke = False
		if not passTurn:
			if self.game.players[0].attack(attackNum, self.game.players[1], self.game.textLog):
				self.gamePanel.animation1(True)
				self.gamePanel.updateCPUHp()
				self.gamePanel.updateCPUStamina()
		else:
			self.game.textLog.append('You passed your turn\n')
		self.game.players[0].mainCard.applyEffects()
		self.gamePanel.updatePlayerHp()
		self.gamePanel.updatePlayerStamina()
		self.updateStatus()
		if not self.checkWin():
			worker = Worker(self.gamePanel, -1, 0, 0, 'wait1')

	def CPUAction(self):
		self.game.turnCount += 1
		self.game.draw(self.game.players[1])
		self.gamePanel.addCPUpokemon()
		if self.game.drawInvQuest():
			self.game.drawInv(self.game.players[1])
		if self.game.players[1].mainCard.isDead():
			newCard = self.game.chooseCardAI(self.game.players[1], self.game.players[0])
			self.game.players[1].mainCard = newCard
			self.game.textLog.append('Opponent put out ' + newCard.name + '\n')
			self.gamePanel.switchCPUpokemon(newCard)
			time.sleep(1)
		if self.game.chooseAttackAI(self.game.players[1], self.game.players[0]):
			self.gamePanel.animation1(False)
			self.gamePanel.updatePlayerHp()
		self.game.players[1].mainCard.applyEffects()
		self.gamePanel.updateCPUHp()
		self.gamePanel.updateCPUStamina()
		if not self.checkWin():
			worker = Worker(self.gamePanel, 0, 0, 1, 'wait2')

	def checkWin(self):
		if self.game.players[0].points >= pointsToWin:
			self.gamePanel.isMyTurn = False
			self.gamePanel.moveItem(self.gamePanel.winId, 400, 400)
			self.gamePanel.Update()
			self.updateStatus()
			return True
		elif self.game.players[1].points >= pointsToWin:
			self.gamePanel.isMyTurn = False
			self.gamePanel.moveItem(self.gamePanel.looseId, 400, 400)
			self.gamePanel.Update()
			self.updateStatus()
			return True
		return False
	def onQuit(self, event):
		self.Close()

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
		with open("instructions.txt") as myFile:
			data = myFile.read()

		self.help.SetLabel(data)
		
		
