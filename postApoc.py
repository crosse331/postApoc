#Первый прототип

import random as rnd
import math
import numpy
print("Данная игра про выживание в постапокалипсисе (многое еще не реализовано), графона тоже нету, т.к. прототип")
print("P - игрок, E - враг, W - стена, D - дверь, Q - закрытая дверь(нужен ключ), 0 - пустое место, K - переход на след. уровень, k - ключ для Q, m - аптечка, восстанавливает 3 хп, движение происходит с помощью набора w/a/s/d + Enter для движения вверх, влево, вправо, вниз соответственно, атаковать врага - дивжение в его сторону, враг атакует двигаясь на игрока")
input("Нажмите Enter, что бы продолжить")

Field = [[] for i in range(6)]
for i in range(6):
		for j in range(6):
			Field[i].append('0')
			
Actions = ['a','d','w','s']
Items = ['k','K','m']
QuestItems = ['K']

class Player:
	x = 0
	y = 0
	
	Hp = 10
	MaxHp = 10
	Shoots = 2
	MaxShoots = 6
	
	Score = 0
	
	inventory = []
	
	def __init__(self):
		self.x = 0
		self.y = 0
	
	def SecureTryToMove(self,_x = 0,_y = 0):
		if (self.x+_x<0 or self.x+_x>5 or self.y+_y<0 or self.y+_y>5):
			return
		if Interact(self.y+_y, self.x+_x) == 1:
			Field[self.y][self.x] = '0'
			self.x+=_x
			self.y+=_y
			Field[self.y][self.x] = 'P'
			self.Score-=1
			
	def __str__(self):
		result = "Игрок: ХП:%s/%s,Заряды:%s/%s"%(self.Hp,self.MaxHp,self.Shoots,self.MaxShoots)
		result+='\n'
		result+= "Инвентарь: " + str(self.inventory) + '\n'
		result+= "Ваш счет: " + str(self.Score)
		
		return result
		
	def UpdateLogic(self):
		if self.Shoots<self.MaxShoots:
			if self.UseItemFromInv('p') == 1:
				self.Shoots+=1
				
		if self.inventory.count('K')>0:
			self.inventory.remove('K')
			StartNewLevel()
		if self.Hp<7 and self.inventory.count('m')>0:
			self.inventory.remove('m')
			self.Hp+=3
		
	def AddToInv(self,item):
		self.inventory.append(item)
		self.Score+=3
		self.inventory.sort()
		
	def UseItemFromInv(self,item):
		if self.inventory.count(item) == 0:
			return 0
		else:
			self.inventory.remove(item)
			return 1

class Enemy:
	hp=3
	x=0
	y=0
	
	isSeePlayer = 0
	
	def __init__(self,_x,_y):
		self.x = _x
		self.y = _y
	
	def RandomMove(self):
		_x = rnd.randint(-1,1)
		_y = 0
		if _x == 0:
			_y = rnd.randint(-1,1)
		if (self.x+_x<0 or self.x+_x>5 or self.y+_y<0 or self.y+_y>5):
			return
		if EnemyInteract(self.y+_y, self.x+_x,self) == 1:
			Field[self.y][self.x] = '0'
			self.x+=_x
			self.y+=_y
			Field[self.y][self.x] = 'E'
			
	def Move(self,_x,_y):
		if (self.x+_x<0 or self.x+_x>5 or self.y+_y<0 or self.y+_y>5):
			return
		if EnemyInteract(self.y+_y, self.x+_x,self) == 1:
			Field[self.y][self.x] = '0'
			self.x+=_x
			self.y+=_y
			Field[self.y][self.x] = 'E'
		
	def MoveToPlayer(self):
		_x = player.x-self.x
		_y = player.y-self.y
		if _x != 0:
			self.Move(numpy.sign(_x),0)
		elif _y != 0:
			self.Move(0,numpy.sign(_y))
			
	def CheckPlayer(self):
		if math.sqrt((player.x-self.x)**2 + (player.y-self.y)**2)<2:
			self.isSeePlayer = 1
		else:
			self.isSeePlayer = 0
		
	def UpdateLogic(self):
		self.CheckPlayer()
		if self.isSeePlayer == 0:
			self.RandomMove()
		else:
			self.MoveToPlayer()
			
		
			
			
		
player = Player()
enemies = []
		
def StartNewLevel():
	player.x=0
	player.y=0
	player.Score+=10
	Clear()
	GenerateField()
		
def DrawWorld():
	#Должно быть приблизительно 19 строк для нормального обновления экрана
	print("\n\n\n")#\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
	print(str(player))
	print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
	
	global Field
	
	for i in range(6):
		for j in range(6):
			if Field[i][j] == 'P':
				Field[i][j] = '0'
			if Field[i][j] == 'E':
				Field[i][j] = '0'
	
	Field[player.y][player.x] = 'P'
	for i in enemies:
		Field[i.y][i.x] = 'E'
	
	for i in range(6):
		for j in range(6):
			#if math.sqrt((player.x-j)**2 + (player.y - i)**2)<2.5:
				print(Field[i][j],end='')
			#else:
			#	print(' ',end = '')
		print()
		
def Interact(y,x):
	global Field

	a = -1
	try:
		a = Items.index(Field[y][x])
	except ValueError:
		a = -1
		
	if a>=0:
		player.AddToInv(Items[a])
		Field[y][x] = '0'
		return 1
	
	if Field[y][x] == '0':
		return 1
	elif Field[y][x] == 'D':
		Field[y][x] = '0'
		return 0
	elif Field[y][x] == 'Q':
		if player.UseItemFromInv('k') == 1:
			Field[y][x] = '0'
	elif Field[y][x] == 'E':
		e = FindEnemy(y,x)
		if type(e) is Enemy:
			e.hp-=1
	else:
		return 0
		
def FindEnemy(y,x):
	for e in enemies:
		if e.y == y and e.x == x:
			return e

def EnemyInteract(y,x,enemy):
	if Field[y][x] == '0':
		return 1
	elif Field[y][x] == 'P':
		player.Hp-=1
		#enemy.hp-=1
		return 0
	else:
		return 0

def GenerateField():
	a = rnd.randint(0,2)
	
	needToBeSpawned = ['K']
	numOfFloor = 0
	
	if a == 0:
		startx = rnd.randint(1,3)
		starty = rnd.randint(1,3)
		for i in range(starty,starty+3):
			for j in range(startx,startx+3):
				if i == starty or i == starty+2 or j == startx or j == startx+2:
					Field[i][j] = 'W'
					if i == starty+1 and j != startx+2:
						if rnd.randint(0,1) == 0:
							Field[i][j] = 'D'
						else:
							Field[i][j] = 'Q'
							needToBeSpawned.append('k')
				else:
					Field[i][j] = 'FF'
					numOfFloor+=1
	

	if a == 1:
		startx = rnd.randint(1,2)
		starty = rnd.randint(1,2)
		for i in range(starty,starty+4):
			for j in range(startx,startx+4):
				if i == starty or i == starty+3 or j == startx or j == startx+3:
					Field[i][j] = 'W'
					if i == starty+1 and j != startx+3:
						if rnd.randint(0,1) == 0:
							Field[i][j] = 'D'
						else:
							Field[i][j] = 'Q'
							needToBeSpawned.append('k')
				else:
					Field[i][j] = 'FF'
					numOfFloor+=1
		
	numOfAddectiveItems = rnd.randint(0,2)
	for i in range(numOfAddectiveItems):
		needToBeSpawned.append(Items[rnd.randint(0,len(Items)-1)])
		
	for i in needToBeSpawned:
		count = 0
		while(1):
			a = rnd.randint(0,5)
			b = rnd.randint(0,5)
			if a == 0 and b == 0:
				continue
			if QuestItems.count(i)>0 and numOfFloor>0:
				if Field[a][b] == 'FF':
					Field[a][b] = str(i)
					break
			else:
				if Field[a][b] == '0':
					Field[a][b] = str(i)
					break
					
			count+=1
			if count>100:
				break
	
	for i in range(6):
		for j in range(6):
			if Field[i][j] == 'FF':
				Field[i][j] = '0'
				
				
	c = rnd.randint(0,3)
	for i in range(c):
		count = 0
		while(1):
			a = rnd.randint(0,5)
			b = rnd.randint(0,5)
			if a == 0 and b == 0:
				continue
			if Field[a][b] == '0':
				enemies.append(Enemy(b,a))
				break
			count+=1
			if count>100:
				break
			
def Clear():
	global Field
	for i in range(6):
		for j in range(6):
			Field[i][j] = '0'
			
	enemies.clear()

def Command(d):
	if d == 0:
		player.SecureTryToMove(_x = -1, _y = 0)
	elif d == 1:
		player.SecureTryToMove(_x = 1,_y = 0)
	elif d == 2:
		player.SecureTryToMove(_x = 0,_y = -1)
	else:
		player.SecureTryToMove(_x = 0,_y = 1)
			
Clear()
GenerateField()
DrawWorld()

while (1):
	player.UpdateLogic()
	for e in enemies:
		if e.hp>0:
			e.UpdateLogic()
		else:
			enemies.remove(e)
			player.Score+=10
	DrawWorld()
	inp = str(input())
	try:
		ind = Actions.index(inp)
	except ValueError:
		ind = -1
	if ind>=0:
		Command(ind)
