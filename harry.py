import os, csv

class HarryExt:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.master = ownerComp

		# self.ActivateExecs(0)
		
		self.StackList = None
		self.CuedStackName = None
		self.CurrStackName = None
		self.CurrStack = None
		self.CuedSlideNum = None
		self.CurrSlideNum = None
		self.PrevSlideNum = None
		self.PrevOSC = {'A': None, 'B': None, 'C': None, 'D': None, 'E': None}
		self.English = 0

		self.RefreshStacks()

		self.CueStack(self.StackList[0])
		self.LoadStack(0)

		self.UpdateFonts()

		return

	def RefreshStacks(self):
		stackfiles = [f for f in os.listdir("./stacks") if f.endswith('.csv')]
		stacklist = sorted([s[:-4] for s in stackfiles])

		self.master.par.Cuedstack.menuNames = stacklist
		self.master.par.Cuedstack.menuLabels = stacklist
		self.StackList = stacklist

		if self.CurrStackName in self.StackList:
			self.CueStack(self.CurrStackName)
			self.LoadStack(self.CurrSlideNum)
			#if self.CurrSlideNum is not None:
			#	self.CueSlide(self.CurrSlideNum)
			#	self.LoadSlide()

		print('REFRESHED STACKS')
		print(stacklist)

		return

	def CueStack(self, stackname):
		self.CuedStackName = stackname
		self.master.par.Cuedstack = stackname
		print('CUED STACK '+stackname)
		return

	def LoadStack(self, slidenum):
		stackname = self.CuedStackName
		file = open('./stacks/'+stackname+'.csv', encoding='utf8')
		reader = csv.reader(file)
		next(reader) # skip header
		stack = [['','','','','']]+[row for row in reader]
		self.CurrStack = stack

		self.CurrStackName = self.CuedStackName


		print('LOADED STACK '+stackname)
		print(stack)

		# Cue the next stack
		cuestackname = self.StackList[(self.StackList.index(self.CurrStackName) + 1) % len(self.StackList)]
		self.CueStack(cuestackname)

		self.master.par.Cuedslide.max = len(stack)-1
		self.master.par.Cuedslide.normMax = len(stack)-1

		# Cue and load slide 0
		self.master.par.Cuedslide = slidenum	
		self.CueSlide(slidenum)
		self.LoadSlide()

		return

	def CueSlide(self, slidenum):
		self.CuedSlideNum = slidenum
		self.DisplayPreview()

		self.DisplayInfo()
		print('CUED SLIDE '+str(slidenum))
		return

	def LoadSlide(self):
		self.PrevSlideNum = self.CurrSlideNum
		self.CurrSlideNum = self.CuedSlideNum
		self.DisplayOutput()

		self.DisplayInfo()
		print('LOADED SLIDE '+str(self.CurrSlideNum))

		# Cue the next slide
		nextslide = (self.CurrSlideNum+1) % len(self.CurrStack)
		self.master.par.Cuedslide = nextslide # this triggers CueSlide
		self.CueSlide(nextslide)
		return

	def DisplayInfo(self):
		op('preview/info/text').par.text = 'CURRENT STACK: '+self.CurrStackName+'\nCUED SLIDE: '+str(self.CuedSlideNum)+'   CURRENT SLIDE: '+str(self.CurrSlideNum)


	def DisplayPreview(self):
		slidenum = self.CuedSlideNum
		if slidenum is not None:
			text = ''
			if self.English==0:
				text = self.CurrStack[slidenum][4]
			else:
				text = self.CurrStack[slidenum][3]
			self.master.store('previewText', text)
		return

	def DisplayOutput(self):
		slidenum = self.CurrSlideNum
		if slidenum is not None:
			text = ''
			if self.English==0:
				text = self.CurrStack[slidenum][4]
			else:
				text = self.CurrStack[slidenum][3]
			self.master.store('outputText', text)
		return

	def UpdateFonts(self):
		if self.English == 1:
			op('preview/slide/text').par.font = self.master.par.Englishfont
			op('output/text').par.font = self.master.par.Englishfont
		else:
			op('preview/slide/text').par.font = self.master.par.Foreignfont
			op('output/text').par.font = self.master.par.Foreignfont
		return

	def ReceiveOSC(self, bus, msg):
		print(bus, msg)

		media = msg[0]
		pos = msg[1]
		prev = self.PrevOSC
		print(prev)
		margin = self.master.par.Trackingmargin

		if prev is None or prev[0] != media or abs(prev[1]-pos) > margin:
			self.PrevOSC[bus] = msg
			return

		if self.CurrStackName is None: return

		stack = self.CurrStack
		select = [s for s in stack if s[0]==bus and s[1]==media and s[2]>prev[1] and s[2]<=pos]
		print(bus, media, prev[1], pos, select)

		if select != []:
			slide = select[0]
			if slide != self.CurrSlideNum:
				self.CueSlide(slide)
				self.LoadSlide()

		self.PrevOSC[bus] = msg

		# bus = array[0]
		# media = array[1]
		# pos = array[2]
		

		# stack = self.CurrStack
		# selected = None


		# for i in range(0, len(stack)):
		# 	slide = stack[i]
		# 	if slide[0] == bus and int(slide[1]) == media:
		# 		target = float(slide[2])
		# 		margin = 0.1
		# 		if pos >= target-margin and pos <= target+margin
		# 			selected = i
		# 			break
		# 	else:
		# 		continue
		# if selected is not None and selected != self.CurrSlideNum:
		# 	self.CueSlide(selected)
		# 	self.LoadSlide()
		# self.PrevOSC = array

		return


