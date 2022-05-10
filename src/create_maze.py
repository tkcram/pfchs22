from . import create_equipment
from . import create_monster
# import monster_test
import json, random, requests

def pathfinder(row,column):
	global criticalPath
	global currentPath
	global maze
	global mazeSize

	pathwayCell = str(row) + "-" + str(column)
	currentPath.append(pathwayCell)
	if len(currentPath) > len(criticalPath):
		criticalPath = currentPath.copy()
	cell = maze[row][column]
	cell['seen'] = True
	checkedSides = []
	while len(checkedSides) < 4:
		check = random.randint(1,4)
		if check not in checkedSides:
			checkedSides.append(check)
			newRow = 0
			newColumn = 0
			match check: #Find adjacent cell
				case 1: #Move up
					if row == 0:
						continue
					else:
						newRow = row - 1
						newColumn = column 
				case 2: #Move right
					if column == mazeSize - 1:
						continue
					else:
						newRow = row
						newColumn = column + 1
				case 3: #Move down
					if row == mazeSize - 1:
						continue
					else:
						newRow = row + 1
						newColumn = column 
				case 4: #Move Left
					if column == 0:
						continue
					else:
						newRow = row
						newColumn = column - 1
			newCell = maze[newRow][newColumn]
			if newCell['seen'] != True:
				match check:
					case 1: #Ceiling current, floor new
						cell['doors'][0] = 1
						newCell['doors'][2] = 1
					case 2: #Right current, left new
						cell['doors'][1] = 1
						newCell['doors'][3] = 1
					case 3: #Floor current, ceiling new
						cell['doors'][2] = 1
						newCell['doors'][0] = 1
					case 4: #Left current, right new
						cell['doors'][3] = 1
						newCell['doors'][1] = 1
				pathfinder(newRow,newColumn)
	currentPath.pop()

def createMaze(size,entranceRow,entranceColumn,level):
	url = "https://www.dnd5eapi.co"

	monsterSearch = url + "/api/monsters/?challenge_rating=" + level
	monsterSearchData = json.loads(requests.get(monsterSearch).text)
	monsterCount = monsterSearchData['count']
	monsterList = {}


	global maze
	global mazeSize
	global currentPath
	global criticalPath
	
	mazeSize = int(size)
	currentPath = []
	criticalPath = []

	maze = [None]*mazeSize
	for row in range(mazeSize):
		maze[row] = [None]*mazeSize
		for column in range(mazeSize):
			maze[row][column] = {
				'special': "",
				'seen': False,
				'doors': [0,0,0,0], #Top, Right, Bottom, Left
			}
			if  not (row == entranceRow and column == entranceColumn):
				monsterRoll = random.randint(1,20)
				if monsterRoll > 10:
					monsterRandom = random.randint(0,monsterCount-1)
					monsterName = monsterSearchData['results'][monsterRandom]['index']
					if monsterName not in monsterList:
						monsterList[monsterName] = create_monster.generator(monsterName)
					if monsterList[monsterName]['actions']:
						maze[row][column]['monster'] = monsterList[monsterName]

				lootRoll = random.randint(1,20)
				lootBonus = 1
				if lootRoll == 20:
					lootRoll = random.randint(1,20)
					lootBonus = 1
					if lootRoll == 20:
						lootRoll = random.randint(1,20)
						lootBonus = 2
						if lootRoll == 20:
							lootRoll = random.randint(1,20)
							lootBonus = 3
							if lootRoll == 20:
								maze[row][column]['loot'] = 'God Mode'
							else:
								lootGet = create_equipment.createLoot(lootRoll,lootBonus)
								maze[row][column]['loot'] = lootGet
						else:
							lootGet = create_equipment.createLoot(lootRoll,lootBonus)
							maze[row][column]['loot'] = lootGet
					else:
						lootGet = create_equipment.createLoot(lootRoll,lootBonus)
						maze[row][column]['loot'] = lootGet				
				else:
					lootGet = create_equipment.createLoot(lootRoll,lootBonus)
					maze[row][column]['loot'] = lootGet

	pathfinder(int(entranceRow),int(entranceColumn))

	criticalPathEnd = criticalPath[len(criticalPath)-1].split('-')
	endRow = int(criticalPathEnd[0])
	endColumn = int(criticalPathEnd[1])

	maze[int(entranceRow)][int(entranceColumn)]['special'] = 'entrance'
	maze[endRow][endColumn]['special'] = 'exit'

	return json.dumps(maze)

# Export maze as JSON
# with open('maze.json','w') as out:
# 	json.dump(maze,out,indent=2)

# # Export Maze as HTML
# from xml.etree.ElementTree import Element, SubElement, ElementTree
# html = Element('html')
# head = SubElement(html,'head')
# body = SubElement(html,'body')
# mazeDiv = SubElement(body, 'div')
# for row in range(totalRows):
# 	rowDiv = SubElement(mazeDiv,'div style="display: flex;"')
# 	for column in range(totalColumns):
# 		styledDiv = 'div style="margin: 0; box-sizing: border-box; height: 10px;width: 10px;'
# 		if maze[row][column]['doors'][0]==0: 			
# 			styledDiv += "border-top: 0.5px solid black;"
# 		if maze[row][column]['doors'][1]==0: 			
# 			styledDiv += "border-right: 0.5px solid black;"
# 		if maze[row][column]['doors'][2]==0: 			
# 			styledDiv += "border-bottom: 0.5px solid black;"
# 		if maze[row][column]['doors'][3]==0: 		
# 			styledDiv += "border-left: 0.5px solid black;"
# 		if row == entranceRow and column == entranceColumn:
# 			styledDiv += "background-color: green;" 
# 		if row == endRow and column == endColumn:
# 			styledDiv += "background-color: red;"
# 		styledDiv += '"'
# 		cellDiv = SubElement(rowDiv,styledDiv)
# 		cellDiv.text = " "
# ElementTree(html).write('test.html')