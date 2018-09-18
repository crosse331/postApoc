from pynput import keyboard
import time
import random as rnd

Hardness = 0
class MainScreen:
	Field = []
	Objects = []

	def __init__(self):
		for i in range(Size.y):
			for j in range(Size.x):
				self.Field.append(' ')
		self.Objects = []
				
	def __str__(self):
		result=""

		for i in range(Size.y):
			for j in range(Size.x):
				self.Field[i*Size.x+j] = '_'

		for obj in self.Objects:
			self.Field[obj.pos.y*Size.x+obj.pos.x] = obj.symbol

		for i in range(Size.y):
			for j in range(Size.x):
				result+=self.Field[i*Size.x+j]
			result+='\n'
		
		return result

	def AddObject(self, obj):
		self.Objects.append(obj)

	def RemoveObject(self, obj):
		self.Objects.remove(obj)

	def Update(self):
		for i in self.Objects:
			i.Logic()

		for i in self.Objects:
			for j in self.Objects:
				if i != j and i.pos == j.pos:
					if i.IsDead():
						self.Objects.remove(i)
					if j.IsDead():
						self.Objects.remove(j)

	def CreateShoot(self, pos, dir):
		tmpPos = Vector(0, 0)
		tmpPos.copyFrom(pos)
		tmpPos+=dir
		shoot = Shoot(tmpPos, dir, 10)
		self.Objects.append(shoot)

		#return shoot

	def IsEnemyClose(self, pos):
		for i in self.Objects:
			if i.pos.y > pos.y and i.pos.x == pos.x and self.Field[i.pos.y*Size.x+i.pos.x] == "W":
				return True

		return False


class Vector:
	x = 0
	y = 0
	
	def __init__(self, posX, posY):
		self.x = posX
		self.y = posY

	def __add__(self, other):
		tmp = Vector(self.x, self.y)
		tmp.x+=other.x
		tmp.y+=other.y

		return tmp

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def copyFrom(self, other):
		self.x = other.x
		self.y = other.y

class Object:
	pos = Vector(0,0)
	symbol = '?'

	delay = 1
	counter = 0

	def TryToMove(self, dir):
		if self.pos.x + dir.x < 0 or self.pos.x+dir.x > Size.x-1 or self.pos.y+dir.y < 0 or self.pos.y+dir.y > Size.y-1:
			return

		self.pos.x += dir.x
		self.pos.y += dir.y

	def Logic(self):
		a=0

	def IsDead(self):
		return True

			
	
class Player(Object):
	
	def __init__(self):
		self.symbol = 'M'

		self.pos = Vector(15, Size.y-1)
		
	def Input(self, char):
		if char == 'a':
			self.TryToMove(Vector(-1, 0))
		elif char == 'd':
			self.TryToMove(Vector(1, 0))
		elif char == 'm':
			screen.CreateShoot(self.pos, Vector(0, -1))




class Enemy(Object):

	horzDelay = 0
	vertDelay = 0
	isBottom = False

	def __init__(self):
		self.symbol = "W"

	def __init__(self, pos):
		self.symbol = "W"
		self.delay = 20
		self.pos = pos

	def Logic(self):
		self.counter+=1
		if self.counter >= self.delay - Hardness:
			if not screen.IsEnemyClose(self.pos):
				if rnd.randint(0, 10) < 8:
					screen.CreateShoot(self.pos, Vector(0,1))
			self.counter = 0


class Shoot(Object):

	direction = Vector(0, 0)

	def __init__(self):
		self.symbol = "|"

	def __init__(self, pos, dir, dly):

		self.direction = dir
		self.delay = dly
		self.pos = pos
		self.symbol = "|"


	def Logic(self):
		self.counter+=1
		if self.counter >= self.delay - Hardness/2:
			tmpPos = Vector(0, 0)
			tmpPos.copyFrom(self.pos)
			self.TryToMove(self.direction)
			if tmpPos == self.pos:
				screen.RemoveObject(self)
			self.counter = 0


class Defence(Object):

	hp = 5

	def __init__(self, pos):
		self.symbol = "D"
		self.pos = pos
		self.hp = 5

	def IsDead(self):
		self.hp -= 1
		if self.hp <= 0:
			return True
		else:
			return False

Size = Vector(30, 20)
screen = MainScreen()

player = Player()
screen.AddObject(player)



kDef = 5
for i in range(kDef):

	screen.AddObject(Defence(Vector(3+i*6, Size.y-4)))
	screen.AddObject(Defence(Vector(3 + i * 6, Size.y - 3)))
	screen.AddObject(Defence(Vector(4 + i * 6, Size.y - 4)))
	screen.AddObject(Defence(Vector(4 + i * 6, Size.y - 3)))

Score = 0

def on_press(key):
	char = ''
	try:
		char = key.char
	except AttributeError:
		char = key

	#if char == 'q':
	#	exit()
	player.Input(char)

enemies = []

def InitEnemies():
	for i in range(5):
		for j in range(11):
			enemies.append(Enemy(Vector(3 + j * 2, 5 + i * 2)))
			screen.AddObject(enemies[len(enemies) - 1])
			if i == 4:
				enemies[len(enemies) - 1].isBottom = True

InitEnemies()

listener = keyboard.Listener(on_press = on_press)
listener.start()

globalCounter = 0
delay = 20


horzDirection = 1

def Main():

	horzDirection = 1
	globalCounter = 0
	delay = 20
	Score = 0
	Hardness = 0

	while True:
		
		time.sleep(1./20)

		screen.Update()

		globalCounter+=1
		if globalCounter >= delay - Hardness:
			globalCounter=0
			horzDirection *= NeedToChangeDir()
			for en in enemies:
				en.TryToMove(Vector(horzDirection, 0))



		PrintScreen()
		print("Score: " + str(Score))

		if not screen.Objects.__contains__(player):
			break

		for en in enemies:
			if not screen.Objects.__contains__(en):
				enemies.remove(en)
				Score+=100
				tmp = Score/1000
				if Hardness<19:
					Hardness = int(tmp)
					if Hardness>18:
						Hardness = 18

		if len(enemies) == 0:
			InitEnemies()

	print("Game Over! Your Score is {0}".format(Score))

def NeedToChangeDir():
	for en in enemies:
		if en.pos.x == 1 or en.pos.x == Size.x-2:
			return -1

	return 1

def PrintScreen():

	global Score
	print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
	print(screen)
	
	
Main()