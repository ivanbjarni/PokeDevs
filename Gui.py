import subprocess
import tempfile
import wx
import sys
import os
import time
import threading
import wx.lib.agw.gradientbutton as GB
import random

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
			waitingTime = random.randint(2,5)
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
		self.hitradius = 5			# How many pixels you can be "off" when trying to click on something
		self.objids = []			# ID's of movable objects on the screen
		self.countCPUpokemon = 0 	# Count how many pokemon CPU has drawn
		self.pdc = wx.PseudoDC()	# For drawing to the panel
		self.dragid = -1 			# ID for currently chosen object
		self.playerChosenID = -1 	# ID for player's currently chosen object
		self.CPUChosenID = -1 		# ID for CPU's currently chosen object
		self.playerHealthID = -1 	# ID for players healthbar
		self.playerStaminaID = -1 	# ID for players stamina bar
		self.CPUHealthID = -1 		# ID for CPU health bar
		self.CPUStaminaID = -1 		# ID for CPU stamina bar
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
				if not self.pdc.GetIdGreyedOut(id) and self.movable[id] and self.isMyTurn:
					self.dragid = id
					self.lastpos = (event.GetX(), event.GetY())
					self.startpos = self.lastpos
					break

		# Right click is currently only used for testing purposes
		elif event.RightDown():
			x,y = self.convertEventCoords(event)
			l = self.pdc.FindObjects(x, y, self.hitradius)
			if l:
				self.pdc.SetIdGreyedOut(l[0], not self.pdc.GetIdGreyedOut(l[0]))
				r = self.pdc.GetIdBounds(l[0])
				r.Inflate(4, 4)
				self.offsetRect(r)
				self.RefreshRect(r, False)
			
			dx,dy = 100, 100
			if self.playerChosenID != -1:
#				dx,dy = 100,100
				loopCPU = 10
				start = time.time()

				while(loopCPU != 0):
					time.sleep(0.005)
					x,y = self.lastpos
					dx = -5
					dy = -5

					self.moveItem(self.playerChosenID, dx, dy)

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
		elif event.LeftUp() or event.Leaving():
			if self.dragid != -1:
				dx = event.GetX()
				dy = event.GetY()

				if self.cardType[self.dragid] == 'Pokemon': 
					if self.inPlayerChosenArea(dx, dy) and self.playerChosenID != self.dragid:
						# Switch currently chosen pokemon out for a new one 
						x = self.startpos[0] - self.lastpos[0] - self.origpos[self.dragid][0] + 119
						y = self.startpos[1] - self.lastpos[1] - self.origpos[self.dragid][1] + 195
						self.GetParent().attackPanel.setLabels(self.cards[self.dragid])
						slot = self.slot[self.dragid]
						tx = -106 + slot * 127
						ty = 189
						if not self.pdc.GetIdGreyedOut(self.playerChosenID):
							self.moveItem(self.playerChosenID, tx, ty)
							self.slot[self.playerChosenID] = slot
						else:
							self.slot[self.playerChosenID] = -1
						self.moveItem(self.dragid, x, y)
						self.slot[self.dragid] = -1 ######################
						self.origpos[self.playerChosenID] = [13 + slot * 127, 384]
						self.playerChosenID = self.dragid
						self.GetParent().game.players[0].mainCard = self.cards[self.dragid]
						self.updatePlayerHp()
						self.updatePlayerStamina()
					else:
						x = self.startpos[0] - self.lastpos[0]
						y = self.startpos[1] - self.lastpos[1]
						self.moveItem(self.dragid, x, y)

				elif self.cardType[self.dragid] == 'Backside':
					slot = self.findEmptySlot(self.slot)
					if self.inPlayerHandArea(dx, dy) and slot != -1:
						id = self.backsides[self.dragid]
						x = 213 + slot * 127
						y = 584
						self.moveItem(id, x, y)
						self.origpos[id] = [x-200, y-200]
						self.slot[id] = slot
						self.moveItem(self.dragid, 0, -1000)
						#self.GetParent().game.players[0].hand.cards.append(self.cards[id])
					else:
						x = self.startpos[0] - self.lastpos[0]
						y = self.startpos[1] - self.lastpos[1]
						self.moveItem(self.dragid, x, y)

				elif self.cardType[self.dragid] == 'InvBackside':
					slot = self.findEmptyInvSlot()
					if self.inPlayerInvArea(dx, dy) and slot != -1:
						id = self.backsidesInv[self.dragid]
						x = 991
						y = 215 + slot * 180
						self.moveItem(id, x, y)
						self.invSlot[id] = slot
						self.moveItem(self.dragid, 0, -1000)
						self.GetParent().game.drawInv(self.GetParent().game.players[0])
					else:
						x = self.startpos[0] - self.lastpos[0]
						y = self.startpos[1] - self.lastpos[1]
						self.moveItem(self.dragid, x, y)

				elif self.cardType[self.dragid] == 'Inventory':
					if self.inPlayerChosenArea(dx, dy):
						self.moveItem(self.dragid, 0, -1000)
						self.invSlot[self.dragid] = -1
						self.GetParent().game.players[0].use(self.cards[self.dragid])
						self.updatePlayerHp()
						self.updatePlayerStamina()
					else:
						x = self.startpos[0] - self.lastpos[0]
						y = self.startpos[1] - self.lastpos[1]
						self.moveItem(self.dragid, x, y)
				self.dragid = -1

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

	def updateDisplay(self, msg):
		if msg.moveY != -1:
			self.origpos[msg.id][1] = msg.moveY
		if not msg.done:
			self.moveItem(msg.id, msg.dx, msg.dy)
			self.Update()
		elif msg.done and msg.dy != -1:
			#self.isMyTurn = True
			#self.GetParent().attackPanel.enableAll()
			self.GetParent().CPUAction()
		else:
			self.isMyTurn = True
			self.GetParent().attackPanel.enableAll()

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
		loopCPU = 10
#		forward = True

		anim = Worker(self, id, 10, 11, 'animation1')

	'''while(loopCPU < 11):
			time.sleep(0.01)
			if forward:
				dx = random.randint(1, 41) - 20
				dy = random.randint(1, 21) - 10

				self.anim.append([dx, dy])

				self.moveItem(id, dx, dy)

				self.Update()
				if loopCPU > 0:
					loopCPU -= 1
				else:
					forward = False
			else:
				dx, dy = self.anim.pop()

				self.moveItem(id, -dx, -dy)

				loopCPU += 1'''

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

		'''if currentY < endY:
			while currentY < endY:
				time.sleep(0.01)
				self.moveItem(bar, 0, 1)
				self.origpos[bar][1] += 1
				currentY += 1
				self.Update()
		else:
			while currentY > endY:
				time.sleep(0.01)
				self.moveItem(bar, 0, -2)
				self.origpos[bar][1] -= 2
				currentY -= 2
				self.Update()'''

		return hp

	def updatePlayerHp(self):
		hp = self.updateBar(self.playerHealthID, self.cards[self.playerChosenID], 'health')
		print 'playerhp: ' + str(hp)
		if hp == 0:
			self.pdc.SetIdGreyedOut(self.playerChosenID)
			self.moveItem(self.playerChosenID, 812, 185)
			self.slot[self.playerChosenID] = -1

	def updatePlayerStamina(self):
		stamina = self.updateBar(self.playerStaminaID, self.cards[self.playerChosenID], 'stamina')

	def updateCPUHp(self):
		hp = self.updateBar(self.CPUHealthID, self.cards[self.CPUChosenID], 'health')
		print 'CPUhp: ' + str(hp)
		if hp == 0:
			self.pdc.SetIdGreyedOut(self.CPUChosenID)
			self.moveItem(self.CPUChosenID, 387, 185)
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
			print 'ok===================================================='
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

	def findID(self, card):
		for id in self.cards.iteritems():
			if card == id[1]:
				return id[0]

	def findBacksideCPU(self, id):
		for bid in self.backsidesCPU.iteritems():
			if id == bid[1]:
				return bid[0]


#	def switchCPUpokemon(self):

	def drawItem(self, dc, id, bitmap, x, y, w, h):
		dc.DrawBitmap(bitmap, x, y, True)
		dc.SetIdBounds(id, wx.Rect(x, y, w, h))
#		self.origpos[id] = [x, y]
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
#		dc.EndDrawing()

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
		#	print id
			bid = wx.NewId()
			dc.SetId(bid)
			self.drawItem(dc, bid, self.backsideBmp, -200, -200, w, h)
			self.movable[bid] = False
			self.backsidesCPU[bid] = id
			print bid
		#	print id

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

		dc.EndDrawing()		

'''		for i in range(0, 6):
			id = wx.NewId()
			dc.SetId(id)
			x = 13 + i * 127
			y = 384
			self.movable[id] = True
			self.drawItem(dc, id, player.deck.cards[i].bitmap, x, y, w, h)
			self.cards[id] = player.deck.cards[i]

		dc.EndDrawing()
''''''
		for i in range(1, 6):
			id = wx.NewId()
			dc.SetId(id)
			x = 195 + i * 134
			y = 15
			self.movable[id] = False
			self.drawItem(dc, id, CPU.deck.cards[i].bitmap, x, y, w, h)
			self.cards[id] = CPU.deck.cards[i]

			# Draw the backside of a card over the CPU card 
			id = id * 2
			dc.SetId(id)
			self.movable[id] = False
			self.drawItem(dc, id, self.backsideBmp, x, y, w, h)

		id = wx.NewId()
		dc.SetId(id)
		x = 750
		y = 236
		self.movable[id] = False
		self.cards[id] = CPU.deck.cards[0]
		self.drawItem(dc, id, CPU.deck.cards[0].bitmap, x, y, w, h)
'''
#		self.GetParent().statusPanel.setCPUPokemonInfo(CPU.deck.cards[0])

#		dc.EndDrawing()

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
		wx.Panel.__init__(self, parent, size=(1200, 200))

		self.SetBackgroundColour('#435353')

		self.vbox = wx.BoxSizer(wx.VERTICAL)
		self.hbox = wx.BoxSizer(wx.HORIZONTAL)

		# Some different variations of buttons, don't know what looks best

		# This button looks nicer than the generic button but I'm not 100% sure it's compatable with
		# other operating systems than windows
		# The label also doesn't center on this button if it is multiline
		self.attackButton1 = GB.GradientButton(self, -1, label='---', size=(200, 100))
		#self.attackButton1.SetTopStartColour(wx.Colour('#A8B8B8'))
		self.attackButton1.SetTopStartColour(wx.Colour(168, 184, 184))
		self.attackButton1.SetTopEndColour(wx.Colour(70, 89, 89))
		self.attackButton1.SetBottomStartColour(wx.Colour(66, 82, 82))
		self.attackButton1.SetPressedTopColour(wx.Colour(88, 110, 110))
		self.attackButton1.SetPressedBottomColour(wx.Colour(54, 43, 43))
		self.attackButton1.SetFont(wx.Font(pointSize=18, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD))
		self.hbox.Add(self.attackButton1, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP, border=10)
		self.attackButton1.Bind(wx.EVT_BUTTON, lambda event: self.attack(0))
		self.attackButton1.Bind(wx.EVT_MOUSE_EVENTS, self.onMouse1)

		self.attackButton2 = GB.GradientButton(self, -1, label='---', size=(200, 100))
		self.attackButton2.SetTopStartColour(wx.Colour(168, 184, 184))
		self.attackButton2.SetTopEndColour(wx.Colour(70, 89, 89))
		self.attackButton2.SetBottomStartColour(wx.Colour(66, 82, 82))
		self.attackButton2.SetPressedTopColour(wx.Colour(88, 110, 110))
		self.attackButton2.SetPressedBottomColour(wx.Colour(54, 43, 43))
		self.attackButton2.SetFont(wx.Font(pointSize=18, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD))
		self.hbox.Add(self.attackButton2, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP, border=10)
		self.attackButton2.Bind(wx.EVT_BUTTON, lambda event: self.attack(1))
		self.attackButton2.Bind(wx.EVT_MOUSE_EVENTS, self.onMouse2)

		self.attackButton3 = GB.GradientButton(self, -1, label='---', size=(200, 100))
		self.attackButton3.SetTopStartColour(wx.Colour(168, 184, 184))
		self.attackButton3.SetTopEndColour(wx.Colour(70, 89, 89))
		self.attackButton3.SetBottomStartColour(wx.Colour(66, 82, 82))
		self.attackButton3.SetPressedTopColour(wx.Colour(88, 110, 110))
		self.attackButton3.SetPressedBottomColour(wx.Colour(54, 43, 43))
		self.attackButton3.SetFont(wx.Font(pointSize=18, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD))
		self.hbox.Add(self.attackButton3, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP, border=10)
		self.attackButton3.Bind(wx.EVT_BUTTON, lambda event: self.attack(2))
		self.attackButton3.Bind(wx.EVT_MOUSE_EVENTS, self.onMouse3)

		self.attackButton4 = GB.GradientButton(self, -1, label='---', size=(200, 100))
		self.attackButton4.SetTopStartColour(wx.Colour(168, 184, 184))
		self.attackButton4.SetTopEndColour(wx.Colour(70, 89, 89))
		self.attackButton4.SetBottomStartColour(wx.Colour(66, 82, 82))
		self.attackButton4.SetPressedTopColour(wx.Colour(88, 110, 110))
		self.attackButton4.SetPressedBottomColour(wx.Colour(54, 43, 43))
		self.attackButton4.SetFont(wx.Font(pointSize=18, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD))
		self.hbox.Add(self.attackButton4, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP, border=10)
		self.attackButton4.Bind(wx.EVT_BUTTON, lambda event: self.attack(3))
		self.attackButton4.Bind(wx.EVT_MOUSE_EVENTS, self.onMouse4)

		self.vbox.Add(self.hbox, flag=wx.ALL|wx.ALIGN_CENTER, border=10)
		self.SetSizer(self.vbox)

	def attack(self, num):
		self.disableAll()
		self.GetParent().gamePanel.isMyTurn = False
		self.GetParent().playerAction(num)

	def onMouse1(self, event):
		if event.Moving():
			attack = self.GetParent().game.players[0].mainCard.attacks[0]
			self.GetParent().infoPanel.setAttackInfo(attack)
		event.Skip()

	def onMouse2(self, event):
		if event.Moving():
			attack = self.GetParent().game.players[0].mainCard.attacks[1]
			self.GetParent().infoPanel.setAttackInfo(attack)
		event.Skip()

	def onMouse3(self, event):
		if event.Moving():
			attack = self.GetParent().game.players[0].mainCard.attacks[2]
			self.GetParent().infoPanel.setAttackInfo(attack)
		event.Skip()

	def onMouse4(self, event):
		if event.Moving():
			attack = self.GetParent().game.players[0].mainCard.attacks[3]
			self.GetParent().infoPanel.setAttackInfo(attack)
		event.Skip()

	# Usage: c.setAttackLabels(card)
	# Pre  : card is Card
	# Post : the labels on the attack buttons have been updated to the 
	#        attacks on card
	def setLabels(self, card):
		self.Freeze()
		self.attackButton1.SetLabel(card.attacks[0].name)
		self.attackButton2.SetLabel(card.attacks[1].name)
		self.attackButton3.SetLabel(card.attacks[2].name)
		self.attackButton4.SetLabel(card.attacks[3].name)
		self.Layout()
		self.Thaw()

	# Usage: c.disableAll()
	# Post : all of the attack buttons have been disabled
	def disableAll(self):
		self.Freeze()
		self.attackButton1.Disable()
		self.attackButton2.Disable()
		self.attackButton3.Disable()
		self.attackButton4.Disable()
		self.attackButton1.SetTopStartColour(wx.Colour(66, 82, 82))
		self.attackButton2.SetTopStartColour(wx.Colour(66, 82, 82))
		self.attackButton3.SetTopStartColour(wx.Colour(66, 82, 82))
		self.attackButton4.SetTopStartColour(wx.Colour(66, 82, 82))
		self.Thaw()

	# Usage: c.enableAll()
	# Post : all of the attack buttons have been enabled
	def enableAll(self):
		self.Freeze()
		self.attackButton1.Enable()
		self.attackButton2.Enable()
		self.attackButton3.Enable()
		self.attackButton4.Enable()
		self.attackButton1.SetTopStartColour(wx.Colour(168, 184, 184))
		self.attackButton2.SetTopStartColour(wx.Colour(168, 184, 184))
		self.attackButton3.SetTopStartColour(wx.Colour(168, 184, 184))
		self.attackButton4.SetTopStartColour(wx.Colour(168, 184, 184))
		self.Thaw()

# Displays info
class infoPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, size=(220, 725))
		self.SetDoubleBuffered(True)

		self.vbox = wx.BoxSizer(wx.VERTICAL)
		self.vbox1 = wx.BoxSizer(wx.VERTICAL)
		self.vboxatt = wx.BoxSizer(wx.VERTICAL)
		self.hboxHealth = wx.BoxSizer(wx.HORIZONTAL)
		self.hboxStamina = wx.BoxSizer(wx.HORIZONTAL)
		titlefont = wx.Font(pointSize=22, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD)
		font = wx.Font(pointSize=18, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD)
		fc = '#CCCCCC'

		self.name = wx.StaticText(self, label='Name', style=wx.ALIGN_LEFT)
		self.name.SetFont(titlefont)
		self.name.SetForegroundColour(fc)
		self.vbox1.Add(self.name, flag=wx.ALIGN_CENTER, border=10)


		self.currentHP =  wx.StaticText(self, label='currentHP', style=wx.ALIGN_LEFT)
		self.currentHP.SetFont(font)
		self.currentHP.SetForegroundColour(fc)

		self.maxHP =  wx.StaticText(self, label='maxHP', style=wx.ALIGN_LEFT)
		self.maxHP.SetFont(font)
		self.maxHP.SetForegroundColour(fc)

		self.hboxHealth.Add(self.currentHP, flag=wx.ALIGN_CENTER, border=10)
		self.hboxHealth.Add(self.maxHP, flag=wx.ALIGN_CENTER, border=10)

		self.vbox1.Add(self.hboxHealth, flag=wx.ALIGN_LEFT, border=10)
#
		self.stamina = wx.StaticText(self, label='Stamina', style=wx.ALIGN_LEFT)
		self.stamina.SetFont(font)
		self.stamina.SetForegroundColour(fc)
		self.vbox.Add(self.stamina, flag=wx.ALIGN_CENTER, border=10)
#		

		self.currentStamina = wx.StaticText(self, label='currentStamina', style=wx.ALIGN_LEFT)
		self.currentStamina.SetFont(font)
		self.currentStamina.SetForegroundColour(fc)

		self.maxStamina = wx.StaticText(self, label='maxStamina', style=wx.ALIGN_LEFT)
		self.maxStamina.SetFont(font)
		self.maxStamina.SetForegroundColour(fc)

		self.hboxStamina.Add(self.currentStamina, flag=wx.ALIGN_CENTER, border=10)
		self.hboxStamina.Add(self.maxStamina, flag=wx.ALIGN_CENTER, border=10)

		self.vbox.Add(self.hboxStamina, flag=wx.ALIGN_CENTER, border=10)

		self.vbox1.Add(self.vbox, flag=wx.ALIGN_LEFT, border=10)

		self.attacks = wx.StaticText(self, label='ATTACKS:', style=wx.ALIGN_LEFT)
		self.attacks.SetFont(font)
		self.attacks.SetForegroundColour(fc)
		self.vbox1.Add(self.attacks, flag=wx.ALIGN_LEFT, border=10)

		self.attack1 = wx.StaticText(self, label='ATTACK1', style=wx.ALIGN_LEFT)
		self.attack1.SetFont(font)
		self.attack1.SetForegroundColour(fc)
		self.vboxatt.Add(self.attack1, flag=wx.ALIGN_LEFT, border=10)

		self.attack2 = wx.StaticText(self, label='ATTACK2', style=wx.ALIGN_LEFT)
		self.attack2.SetFont(font)
		self.attack2.SetForegroundColour(fc)
		self.vboxatt.Add(self.attack2, flag=wx.ALIGN_LEFT, border=10)

		self.attack3 = wx.StaticText(self, label='ATTACK3', style=wx.ALIGN_LEFT)
		self.attack3.SetFont(font)
		self.attack3.SetForegroundColour(fc)
		self.vboxatt.Add(self.attack3, flag=wx.ALIGN_LEFT, border=10)

		self.attack4 = wx.StaticText(self, label='ATTACK4', style=wx.ALIGN_LEFT)
		self.attack4.SetFont(font)
		self.attack4.SetForegroundColour(fc)
		self.vboxatt.Add(self.attack4, flag=wx.ALIGN_LEFT, border=10)

		self.vbox1.Add(self.vboxatt, flag=wx.ALIGN_LEFT, border=10)

		self.type = wx.StaticText(self, label='Type', style=wx.ALIGN_LEFT)
		self.type.SetFont(font)
		self.type.SetForegroundColour(fc)
		self.vbox1.Add(self.type, flag=wx.ALIGN_LEFT, border=10)

		self.weakness = wx.StaticText(self, label='Weakness', style=wx.ALIGN_LEFT)
		self.weakness.SetFont(font)
		self.weakness.SetForegroundColour(fc)
		self.vbox1.Add(self.weakness, flag=wx.ALIGN_LEFT, border=10)

		self.resistance = wx.StaticText(self, label='Resistance', style=wx.ALIGN_LEFT)
		self.resistance.SetFont(font)
		self.resistance.SetForegroundColour(fc)
		self.vbox1.Add(self.resistance, flag=wx.ALIGN_LEFT, border=10)

		self.SetSizer(self.vbox1)

	# Usage: c.setPokeInfo(card)
	# Pre  : card is Card
	# Post : the labels on the infoPanel has been updated to the 
	#        info on card
	def setPokeInfo(self, pcard):
		self.Freeze()
		self.name.SetLabel('-'+str(pcard.name)+'-')
		self.currentHP.SetLabel(' HP:' + str(pcard.health) + '/')
		self.maxHP.SetLabel(str(pcard.healthMax))
		self.stamina.SetLabel(' Stamina:')
		self.currentStamina.SetLabel(' ' + str(pcard.stamina) + '/')
		self.maxStamina.SetLabel(' ' + str(pcard.staminaMax))
		self.attacks.SetLabel(' Attacks: ')
		self.attack1.SetLabel(' -' + str(pcard.attacks[0]))
		self.attack2.SetLabel(' -' + str(pcard.attacks[1]))
		self.attack3.SetLabel(' -' + str(pcard.attacks[2]))
		self.attack4.SetLabel(' -' + str(pcard.attacks[3]))
		self.type.SetLabel(' Type: ' + str(pcard.poketype).title())
		self.weakness.SetLabel(' Wkn: ' + str(pcard.weakness).title())
		self.resistance.SetLabel(' Res: ' + str(pcard.resistance).title())
		self.Layout()
		self.Thaw()


	# Usage: c.setAttackInfo(attack)
	# Pre  : card is Attack
	# Post : the labels on the infoPanel have been updated to the 
	#        attack info which is on attack
	def setAttackInfo(self, attack):
		self.Freeze()
		self.name.SetLabel('-' + str(attack.name) + '-')
		self.currentHP.SetLabel(' Damage: ' + str(attack.damage))
		self.maxHP.SetLabel('')
		self.stamina.SetLabel(' St. cost: ' + str(attack.staminaCost))
		self.currentStamina.SetLabel(' HP cost: ' + str(attack.healthCost))
		self.maxStamina.SetLabel('')
		self.attacks.SetLabel(' Stun: ' + str(attack.stun))
		self.attack1.SetLabel(' Type: ' + str(attack.poketype).title())
		self.attack2.SetLabel('')
		self.attack3.SetLabel('')
		self.attack4.SetLabel('')
		self.type.SetLabel('')
		self.weakness.SetLabel('')
		self.resistance.SetLabel('')
		self.Layout()
		self.Thaw()


	# Usage: c.setInventoryInfo(icard)
	# Pre  : card is invCard
	# Post : the labels on the infoPanel has  been updated to the 
	#        info on icard
	def setInventoryInfo(self, icard):
		self.Freeze()
		self.name.SetLabel('-' + str(icard.name) + '-')
		if(icard.health == 0):
			self.currentHP.SetLabel(' No HP boost')
		else:
			self.currentHP.SetLabel(' HP boost: ' + str(icard.health))
		if(icard.stamina == 0):
			self.maxHP.SetLabel(' No stamina boost ')
		else:
			self.maxHP.SetLabel(' Stamina boost: ' + str(icard.stamina))
		if(icard.stun):
			self.stamina.SetLabel(' Stun off')
			#self.currentStamina.SetLabel('Stun off')
			if(icard.damageBoost != 0):
				self.currentStamina.SetLabel(' Damage boost: ' + str(icard.damageBoost))
				#self.maxStamina.SetLabel('Damage boost: ' + str(icard.damageBoost))
		else:
			if(icard.damageBoost == 0):
				self.stamina.SetLabel('')
				self.currentStamina.SetLabel('')
				
			else:
				self.currentStamina.SetLabel('Damage boost: ' + str(icard.damageBoost))
		self.maxStamina.SetLabel('')
		self.attacks.SetLabel('')
		self.attack1.SetLabel('')
		self.attack2.SetLabel('')
		self.attack3.SetLabel('')
		self.attack4.SetLabel('')
		self.type.SetLabel('')
		self.weakness.SetLabel('')
		self.resistance.SetLabel('')
		self.Layout()
		self.Thaw()

class LogPanel(wx.ScrolledWindow):
	def __init__(self, parent):
		# This needs to be a scrolled window even though it doesn't scroll
		wx.ScrolledWindow.__init__(self, parent, size=(1060, 560), style=wx.SUNKEN_BORDER)
		self.SetDoubleBuffered(True)

		
	#	with tempfile.TemporaryFile() as tempf:
	#		proc = subprocess.Popen(['echo', 'a', 'b'], stdout=tempf)
	#		proc.wait()
	#		tempf.seek(0)
   	#		print tempf.read()



class MainFrame(wx.Frame):
	def __init__(self, game):
		wx.Frame.__init__(self, None, title="Pokemon", size=(1300, 725))
		self.SetBackgroundColour('#435353')		
		self.vbox = wx.BoxSizer(wx.VERTICAL)
		self.hbox = wx.BoxSizer(wx.HORIZONTAL)

		self.game = game

		self.menuBar = wx.MenuBar()
		self.infoPanel = infoPanel(self)
		#self.statusPanel = StatusPanel(self)
		self.gamePanel = GamePanel(self, wx.ID_ANY)
		self.attackPanel = AttackPanel(self)

		self.fileMenu = wx.Menu()
		m_exit = self.fileMenu.Append(wx.ID_EXIT, "&Exit\tAlt+X", "Close window and exit program.")
		self.menuBar.Append(self.fileMenu, "&File")
		self.Bind(wx.EVT_MENU, self.onQuit, m_exit)

		self.SetMenuBar(self.menuBar)

		#self.vbox.Add(self.statusPanel, 0, flag=wx.EXPAND)
		self.vbox.Add(self.gamePanel, 0, flag=wx.EXPAND)
		self.vbox.Add(self.attackPanel, 0, flag=wx.EXPAND)
		self.hbox.Add(self.infoPanel, 0, flag=wx.EXPAND)
		self.hbox.Add(self.vbox, 0, flag=wx.EXPAND)

		self.SetAutoLayout(True)
		self.SetSizer(self.hbox)
		self.Layout()
		self.Centre()

	def playerAction(self, attackNum):
		self.game.turn += 1
		self.game.turnCount += 1
		if self.game.players[0].attack(attackNum, self.game.players[1]):
			self.gamePanel.animation1(True)
			self.gamePanel.updateCPUHp()
			self.gamePanel.updateCPUStamina()
			self.gamePanel.updatePlayerHp()
			self.gamePanel.updatePlayerStamina()

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
			self.gamePanel.switchCPUpokemon(newCard)
			time.sleep(0.5)
		if self.game.chooseAttackAI(self.game.players[1], self.game.players[0]):
			self.game.players[1].mainCard.applyEffects()
			self.gamePanel.animation1(False)
			self.gamePanel.updatePlayerHp()
		self.gamePanel.updateCPUHp()
		self.gamePanel.updateCPUStamina()
		worker = Worker(self.gamePanel, 0, 0, 1, 'wait2')

	def onQuit(self, event):
		self.Close()
