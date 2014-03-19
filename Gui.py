import wx
import sys
import os
import time

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
	from agw import gradientbutton as GB
	#bitmapDir = "bitmaps/"
except ImportError: # if it's not there locally, try the wxPython lib.
	import wx.lib.agw.gradientbutton as GB
#	bitmapDir = "agw/bitmaps/"


# A drawable panel that contains the Playing Area
class GamePanel(wx.ScrolledWindow):
	def __init__(self, parent, id, size=wx.DefaultSize):
		wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=(1200, 650), style=wx.SUNKEN_BORDER)
		self.SetDoubleBuffered(True)

		self.x = 0
		self.y = 0
		self.drawing = False
		self.hitradius = 5
		self.objids = []

		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)
		self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)

		self.image = wx.Image('images/alakazam.jpg', wx.BITMAP_TYPE_ANY)
		self.image = self.image.Scale(122, 175, wx.IMAGE_QUALITY_HIGH)
		self.bitmap = self.image.ConvertToBitmap()


		self.pdc = wx.PseudoDC()
		self.DoDrawing(self.pdc)

		self.dragid = -1
		self.lastdragid = -1
		self.lastpos = (0,0)
		self.startpos = (0,0)


		#self.image = wx.Image('alakazam.jpg', wx.BITMAP_TYPE_ANY)
		#self.grabbed = False
		#self.bitPanel = wx.Panel(self, pos=(100,100))
		#self.bitmap = self.image.ConvertToBitmap()
		#self.bitmap = wx.StaticBitmap(self.bitPanel, -1, self.bitmap, pos=(10, 10))
		#self.bitmap.Bind(wx.EVT_LEFT_DOWN, lambda event: self.setGrabbed())
		#self.bitmap.Bind(wx.EVT_LEFT_UP, lambda event: self.setReleased())
		#self.bitmap.Bind(wx.EVT_MOTION, self.dragImage)

#		self.vbox = wx.BoxSizer(wx.VERTICAL)
#		self.vbox.Add(self.bitPanel, 0, flag=wx.EXPAND)
		

#		self.SetSizer(self.vbox)
#		self.SetAutoLayout(1)
#		self.vbox.Fit(self)
#		self.Layout()
	
	def setImage(self, card):
		image = wx.Image('images/' + str(card.name) + '.jpg', wx.BITMAP_TYPE_ANY)
		image = image.Scale(122, 175, wx.IMAGE_QUALITY_HIGH)
		card.bitmap = image.ConvertToBitmap()
	
	def ConvertEventCoords(self, event):
		xView, yView = self.GetViewStart()
		xDelta, yDelta = self.GetScrollPixelsPerUnit()
		return (event.GetX() + (xView * xDelta),
			event.GetY() + (yView * yDelta))

	def OffsetRect(self, r):
		xView, yView = self.GetViewStart()
		xDelta, yDelta = self.GetScrollPixelsPerUnit()
		r.OffsetXY(-(xView*xDelta),-(yView*yDelta))

	def OnMouse(self, event):
		if event.LeftDown():
			#x = event.GetX() 
			#y = event.GetY()
			#self.ConvertEventCoords(event)
			x,y = self.ConvertEventCoords(event)
			l = self.pdc.FindObjects(x, y, self.hitradius)
			for id in l:
				if not self.pdc.GetIdGreyedOut(id):
					self.dragid = id
					self.lastpos = (event.GetX(), event.GetY())
					self.startpos = self.lastpos
					break
		elif event.RightDown():
			#x = event.GetX() 
			#y = event.GetY()
			#self.ConvertEventCoords(event)
			'''x,y = self.ConvertEventCoords(event)
			l = self.pdc.FindObjects(x, y, self.hitradius)
			if l:
				self.pdc.SetIdGreyedOut(l[0], not self.pdc.GetIdGreyedOut(l[0]))
				r = self.pdc.GetIdBounds(l[0])
				r.Inflate(4, 4)
				self.OffsetRect(r)
				self.RefreshRect(r, False)
			'''
			dx,dy = 100, 100
			if self.lastdragid != -1:
#				dx,dy = 100,100
				loopCPU = 10
				start = time.time()
				print self.lastpos

				while(loopCPU != 0):
					time.sleep(0.005)
					x,y = self.lastpos
					dx = -5
					dy = -5

					print "dx" + str(dx)
					print "dy" + str(dy)

					r = self.pdc.GetIdBounds(self.lastdragid)
					self.pdc.TranslateId(self.lastdragid, dx, dy)
					r2 = self.pdc.GetIdBounds(self.lastdragid)
					r = r.Union(r2)
					r.Inflate(4, 4)
					self.OffsetRect(r)
					self.RefreshRect(r, False)
				#	self.pdc.DrawToDc(self.pdc)
					self.Update()

					print loopCPU
			#		self.OnPaint(event)
					loopCPU -= 1
				self.lastpos = (event.GetX(), event.GetY())

		elif event.Dragging() or event.LeftUp():
			if self.dragid != -1:
				x,y = self.lastpos
				dx = event.GetX() - x
				dy = event.GetY() - y
				r = self.pdc.GetIdBounds(self.dragid)
				self.pdc.TranslateId(self.dragid, dx, dy)
				r2 = self.pdc.GetIdBounds(self.dragid)
				r = r.Union(r2)
				r.Inflate(4, 4)
				self.OffsetRect(r)
				self.RefreshRect(r, False)
				self.lastpos = (event.GetX(), event.GetY())
			if event.LeftUp():
				self.lastdragid = self.dragid

#				print self.startpos - self.lastpos
				x = self.startpos[0] - self.lastpos[0]
				y = self.startpos[1] - self.lastpos[1]

				r = self.pdc.GetIdBounds(self.lastdragid)
				self.pdc.TranslateId(self.lastdragid, x, y)
				r2 = self.pdc.GetIdBounds(self.lastdragid)
				r = r.Union(r2)
				r.Inflate(4, 4)
				self.OffsetRect(r)
				self.RefreshRect(r, False)

				self.dragid = -1

		#elif event.Moving():
		#	print 'ok'

	def OnPaint(self, event):
		dc = wx.BufferedPaintDC(self)
#		self.PrepareDC(dc)
#		bg = wx.Brush(self.GetBackgroundColour())
#		dc.SetBackground()
		dc.Clear()

#		xv, yv = self.GetViewStart()
		rgn = self.GetUpdateRegion()
		r = rgn.GetBox()
		self.pdc.DrawToDCClipped(dc, r)

	def DoDrawing(self, dc):
		dc.BeginDrawing()
		background = wx.Bitmap("images/pokematBasic.png")
		dc.DrawBitmap(background, 0, 0)
		pen = wx.Pen('#435353', 1)
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

		id = wx.NewId()
		dc.SetId(id)
		x = 195
		y = 450
		w, h = self.bitmap.GetSize()
		dc.DrawBitmap(self.bitmap, 195, 450, True)
		dc.SetIdBounds(id, wx.Rect(x, y, w, h))
		self.objids.append(id)
		dc.EndDrawing()


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
#		self.vbox.Add(self.hbox2, flag=wx.ALIGN_RIGHT, border=10)
		self.SetSizer(self.vbox)


class ControlPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, size=(1200, 200))

		self.SetBackgroundColour('#435353')

		self.vbox = wx.BoxSizer(wx.VERTICAL)
		self.hbox = wx.BoxSizer(wx.HORIZONTAL)

		self.attackButton1 = GB.GradientButton(self, -1, label='Attack', size=(200, 100))
#		self.attackButton1.Bind(wx.EVT_BUTTON, lambda event: attack())
		#self.attackButton1.SetTopStartColour(wx.Colour('#A8B8B8'))
		self.attackButton1.SetTopStartColour(wx.Colour(168, 184, 184))
		self.attackButton1.SetBottomStartColour(wx.Colour(66, 82, 82))
		self.attackButton1.SetFont(wx.Font(pointSize=18, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD))
		self.hbox.Add(self.attackButton1, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP, border=10)

		self.attackButton2 = wx.Button(self, label='Attack', size=(200, 100))
#		self.attackButton2.Bind(wx.EVT_BUTTON, lambda event: attack())
		self.attackButton2.SetFont(wx.Font(pointSize=18, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD))
		self.hbox.Add(self.attackButton2, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP, border=10)

		self.attackButton3 = wx.Button(self, label='Attack', size=(200, 100))
#		self.attackButton3.Bind(wx.EVT_BUTTON, lambda event: attack())
		self.attackButton3.SetFont(wx.Font(pointSize=18, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD))
		self.hbox.Add(self.attackButton3, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP, border=10)

		self.attackButton4 = wx.Button(self, label='Attack', size=(200, 100))
#		self.attackButton4.Bind(wx.EVT_BUTTON, lambda event: attack())
		self.attackButton4.SetFont(wx.Font(pointSize=18, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD))
		self.hbox.Add(self.attackButton4, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.TOP, border=10)

		self.vbox.Add(self.hbox, flag=wx.ALL|wx.ALIGN_CENTER, border=10)
		self.SetSizer(self.vbox)



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
    MainFrame().Show()
    app.MainLoop()

