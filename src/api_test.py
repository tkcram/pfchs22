from . import loot_test
import json, random, re, requests, math

#*****Initialise*****
#Variables
url = 'https://www.dnd5eapi.co'

#API
raceData = json.loads(requests.get(f'{url}/api/races').text)
classData = json.loads(requests.get(f'{url}/api/classes').text)
backgroundData = json.loads(requests.get(f'{url}/api/backgrounds').text)

def createCharacter(startLevel):
	#Character
	character = {
		'details': {},
		'stats': {
			'raw': {},
			'mod': {},
			'saves': {},
			'profs': {}
		},
		'skills':{},
		'inventory': {
			'weapon': {},
			'armor': {},
			'consumable': {}
		},
		'combat': {
			'weilding':{}
		},
		'spellcasting': {
			'spells':{}
		}
	}

	#*****Details*****
	#Variables
	charDetails = character['details']

	raceSelect = random.randint(0,raceData['count']-1)
	charRace = raceData['results'][raceSelect]['index']
	charSubrace = None

	classSelect = random.randint(0,classData['count']-1)
	charClass = classData['results'][classSelect]['index']
	print(charClass)

	backgroundSelect = random.randint(0,backgroundData['count']-1)
	charBackground = backgroundData['results'][backgroundSelect]['index']

	charAlignment = random.choice(['Lawful','Neutral','Chaotic']) + ' ' + random.choice(['Good','Neutral','Evil'])
	if charAlignment == 'Neutral Neutral':
		charAlignment = 'True Neutral'

	#API
	characterRaceData = json.loads(requests.get(f'{url}/api/races/{charRace}').text)
	characterClassData = json.loads(requests.get(f'{url}/api/classes/{charClass}').text)
	characterBackgroundData = json.loads(requests.get(f'{url}/api/backgrounds/{charBackground}').text)

	#Working
	if characterRaceData['subraces']:
		subraceSelect = random.randint(0, len(characterRaceData['subraces']) - 1)
		charSubrace = characterRaceData['subraces'][subraceSelect]['index']
		subraceURL = characterRaceData['subraces'][subraceSelect]['url']
		characterSubraceData = json.loads(requests.get(url + subraceURL).text)

	if characterClassData['subclasses']:
		subclassSelect = random.randint(0, len(characterClassData['subclasses']) - 1)
		charSubclass = characterClassData['subclasses'][subclassSelect]['index']
		subclassUrl = characterClassData['subclasses'][subclassSelect]['url']
		characterSubclassData = json.loads(requests.get(url + subclassUrl).text)

	#Character
	charDetails['entity'] = 'hero'
	charDetails['race'] = charRace
	charDetails['subrace'] = charSubrace
	charDetails['class'] = charClass
	charDetails['subclass'] = charSubclass
	charDetails['background'] = charBackground
	charDetails['level'] = 0
	charDetails['proficiency'] = 0
	charDetails['alignment'] = charAlignment
	charDetails['features'] = []

	#*****Stats*****
	#Variables
	statList = ['str','dex','con','int','wis','cha']
	charStatBase = character['stats']['raw']
	charStatMod = character['stats']['mod']
	charStatSave = character['stats']['saves']
	charStatProf = character['stats']['profs']
	charStatBonus = {}

	#Functions
	def statCalc():
		for stat in statList:
			charStatMod[stat] = math.floor((charStatBase[stat] - 10)/2) 
			charStatSave[stat]  = charStatMod[stat]
			if 'saves' in charStatProf[stat]:
				charStatSave[stat] += charDetails['proficiency']

	#Workings
	for raceStatBonus in characterRaceData['ability_bonuses']:
		stat = raceStatBonus['ability_score']['index']
		statBonus = raceStatBonus['bonus']
		charStatBonus[stat] = statBonus

	if charSubrace != None:
		for subraceStatBonus in characterSubraceData['ability_bonuses']:
			stat = subraceStatBonus['ability_score']['index']
			statBonus = subraceStatBonus['bonus']
			charStatBonus[stat] = statBonus

	#Character
	for stat in statList:
		statRoll = random.randint(1,6) + random.randint(1,6) + random.randint(1,6)
		charStatBase[stat] = statRoll
		charStatProf[stat] = []
		if stat in charStatBonus:
			charStatBase[stat] += charStatBonus[stat] 

	for save in characterClassData['saving_throws']:
		charStatProf[save['index']].append('saves')
	# statCalc()

	#*****Skills*****
	#Variables
	skillAbilities = {
		'acrobatics': 'dex', 
		'animal-handling': 'wis', 
		'arcana': 'int', 
		'athletics': 'str', 
		'deception': 'cha', 
		'history': 'int', 
		'insight': 'wis', 
		'intimidation': 'cha', 
		'investigation': 'int', 
		'medicine': 'wis', 
		'nature': 'int', 
		'perception': 'wis', 
		'performance': 'cha', 
		'persuasion': 'cha', 
		'religion': 'int', 
		'sleight-of-hand': 'dex', 
		'stealth': 'dex', 
		'survival': 'wis'
	}
	charSkills = character['skills']

	profOffset = 0
	if charClass == 'monk':
		profOffset = 2

	backgroundProfs = len(characterBackgroundData['starting_proficiencies'])
	classProfs = characterClassData['proficiency_choices'][profOffset]['choose']
	totalProfs = backgroundProfs + classProfs
	charSkillProfs = []

	#Functions
	def skillCalc():
		for skillName in charSkills: 
			skillMod = skillAbilities[skillName] 
			charSkills[skillName] = charStatMod[skillMod]
			if skillName in charSkillProfs: 
				charSkills[skillName] += charDetails['proficiency']
				if skillName not in charStatProf[skillMod]:
					charStatProf[skillMod].append(skillName)


	#Workings
	for proficiency in characterBackgroundData['starting_proficiencies']: #Background Proficiencies
		charSkillProfs.append(proficiency['index'][6:])

	while len(charSkillProfs) < totalProfs: #Class Proficiencies
		print('New Prof')
		# print(charRace,charClass)
		profList = characterClassData['proficiency_choices'][profOffset]['from']
		profNumber = random.randint(0,len(profList)-1)
		profTry = profList[profNumber]['index'][6:]
		if profTry not in charSkillProfs:
			charSkillProfs.append(profTry)

	#JSON
	for skill in skillAbilities: # Skills
		charSkills[skill] = 0

	#*****Equipment*****
	#Variables
	charInventory = character['inventory']
	charWeapons = charInventory['weapon']
	charArmor = charInventory['armor']
	fullEquipmentList = []

	#Functions
	def getEquipmentOptions(equipmentOptions):
		equipmentOptionsRequest = requests.get(url + equipmentOptions['url'])
		equipmentOptionsData = json.loads(equipmentOptionsRequest.text)

		options = []
		for equipment in equipmentOptionsData['equipment']:
			options.append({
				'equipment': equipment,
				'quantity': 1
			})
		return options

	def getEquipment(items, count):
		chosenItems = []
		for x in range(count):
			choice = random.randint(0, len(items) - 1)
			chosenItems.append(items[choice])
		itemsToAdd = []
		key = 0
		while key < len(chosenItems):
			print('New Item')
			item = chosenItems[key]
			if item.get('equipment'):
				itemsToAdd.append(item) # add to the end of the list
			elif item.get('0'):
				for subItem in item.values():
					chosenItems.append(subItem) # add to the end of the list
			elif item.get('equipment_option'):
				equipmentOptions = getEquipmentOptions(item['equipment_option']['from']['equipment_category'])
				optionItemsToAdd = getEquipment(equipmentOptions, item['equipment_option']['choose'])
				itemsToAdd += optionItemsToAdd # join the two lists
			key += 1
		return itemsToAdd

	def equipmentCalc(): #Need to change so it lists damage types
		damageBonus = charStatMod['str']
		for weapon in charWeapons:
			if 'thrown' in charWeapons[weapon]['properties']:
				damageBonus = charStatMod['dex']
			if 'finesse' in charWeapons[weapon]['properties']:
				damageBonus = max(charStatMod['str'],charStatMod['dex'])
			if charWeapons[weapon]['range'] == 'Ranged':
				damageBonus = charStatMod['dex']

			for damageType in charWeapons[weapon]['base-damage']:
				baseDamage = charWeapons[weapon]['base-damage'][damageType]
				if damageBonus < 0:
					charWeapons[weapon]['damage'][damageType] = baseDamage + str(damageBonus)
				else:
					charWeapons[weapon]['damage'][damageType] = baseDamage + "+" + str(damageBonus)

				charWeapons[weapon]['bonus'] = damageBonus + charDetails['proficiency']

		for armor in charArmor:
			baseAC = charArmor[armor]['base-ac']
			if charArmor[armor]['category'] == 'Light':
				charArmor[armor]['ac'] = baseAC + charStatMod['dex']
			elif charArmor[armor]['category'] == 'Medium':
				charArmor[armor]['ac'] = baseAC + min(2,charStatMod['dex'])
			else:
				charArmor[armor]['ac'] = baseAC

	#Workings
	for equipment in characterClassData['starting_equipment']:
		fullEquipmentList.append(equipment)

	for equipment in characterClassData['starting_equipment_options']: 
		itemList = getEquipment(equipment['from'], equipment['choose'])
		fullEquipmentList += itemList 

	for equipment in fullEquipmentList:
		loot_test.itemAdd(equipment,charInventory)

	randomWeapon = random.choice(list(charWeapons))
	weaponChoice = charWeapons[randomWeapon]
	weaponChoice['equipped'] = True

	for armor in charArmor:
		charArmor[armor]['equipped'] = True

	#*****Combat*****
	#Variables
	charCombat = character['combat']
	hitDie = int(characterClassData['hit_die'])

	#Functions

	def combatCalc():
		maxHP = 0
		if 'hp-max' in charCombat.keys():
			maxHP = charCombat['hp-max']  

		maxHP += (random.randint(1,hitDie) + charStatMod['con'])

		if maxHP < 1:
			maxHP = 1

		ac = 10+charStatMod['dex']

		charCombat['ac'] = ac
		charCombat['hp-max'] = maxHP
		charCombat['hp-current'] = maxHP
		charCombat['initiative'] = charStatMod['dex']
		charCombat['passive-perception'] = 10 + charSkills['perception']

	#Character
	charCombat['weilding']['weapon'] = randomWeapon
	charCombat['hit-die'] = hitDie
	charCombat['actions'] = {}

	#*****Level Up*****
	#Variables
	charFeatures = charDetails['features']
	charSpells = character['spellcasting']
	charActions = charCombat['actions']

	#API
	levelData = json.loads(requests.get(url + characterClassData['class_levels']).text)
	#Functions
	def levelUp(newLevel):
		currentLevel = charDetails['level']
		charDetails['level'] = newLevel
		levelSpecific = levelData[newLevel-1]
		charDetails['proficiency'] = levelSpecific["prof_bonus"]

		#Features
		for level in levelData[currentLevel:newLevel:1]:
			for feature in level['features']:
				feaureName = feature['name'].split(' (')
				if feaureName[0] not in charFeatures:
					charFeatures.append(feaureName[0])

				if feaureName[0] == 'Ability Score Improvement':
					asiSplit = random.getrandbits(1)
					if asiSplit:
						charStatBase[random.choice(statList)] += 1
						charStatBase[random.choice(statList)] += 1
					else:
						charStatBase[random.choice(statList)] += 2
		#Spellcasting
		if 'spellcasting' in levelSpecific.keys():
			spellAbility = characterClassData['spellcasting']['spellcasting_ability']['index']
			levelSpecific['spellcasting']['ability'] = spellAbility
			spellList = charSpells['spells']

			if 'cantrips_known' not in charSpells:
				charSpells['cantrips_known'] = 0
			if 'spells_known' not in charSpells:
				charSpells['spells_known'] = 0

			cantsKnown = charSpells['cantrips_known']
			spellsKnown = charSpells['spells_known']

			if 'cantrips_known' in levelSpecific['spellcasting']:
				charSpells['cantrips_known'] = levelSpecific['spellcasting']['cantrips_known']
			if 'spells_known' in levelSpecific['spellcasting']:
				charSpells['spells_known'] = levelSpecific['spellcasting']['spells_known']

			cantsTotal = charSpells['cantrips_known']
			spellsTotal = charSpells['spells_known'] - spellsKnown

			charSpells['spell_slots'] = {}
			maxSpell = 0
			for field in levelSpecific['spellcasting']:
				fieldSplit = field.split('_')
				if len(fieldSplit) > 2:
					spellsSlotsTotal = levelSpecific['spellcasting'][field]
					charSpells['spell_slots'][fieldSplit[3]] = spellsSlotsTotal
					if spellsSlotsTotal > 0:
						maxSpell = int(fieldSplit[3])

			cantsData = json.loads(requests.get(f'{url}/api/classes/{charClass}/levels/0/spells').text)

			if '0' not in spellList:
				spellList['0'] = []

			while len(spellList['0']) < cantsTotal:
				print('New Cantrip')
				cantSelect = random.randint(0,cantsData['count']-1)
				cantChoice = cantsData['results'][cantSelect]['index']
				if cantChoice not in spellList['0']:
					spellList['0'].append(cantChoice)

			if maxSpell not in spellList:
				spellList[maxSpell] = []

			spellData = json.loads(requests.get(f'{url}/api/classes/{charClass}/levels/{maxSpell}/spells').text)

			if maxSpell > 0:
				while spellData['count'] == len(spellList[maxSpell]):
					maxSpell -= 1
					spellData = json.loads(requests.get(f'{url}/api/classes/{charClass}/levels/{maxSpell}/spells').text)

			for newSpell in range(spellsTotal):
				searchList = spellList[maxSpell]
				spellSelect = random.randint(0,spellData['count']-1)
				spellChoice = spellData['results'][spellSelect]['index']
				while spellChoice in searchList:
					print('New Spell')
					spellSelect = random.randint(0,spellData['count']-1)
					spellChoice = spellData['results'][spellSelect]['index']
				spellList[maxSpell].append(spellChoice)

		#Class specific
		for specificFeature in levelSpecific['class_specific']:
			actionCount = levelSpecific['class_specific'][specificFeature]
			charActions[specificFeature] = actionCount

		#Recalc
		statCalc()
		skillCalc()
		equipmentCalc()
		combatCalc()
	#Workings

	#Character
	#*****Actions*****
	#Variables
	#API
	#Functions
	#Workings
	#Character

	#*****Export*****
	for level in range(int(startLevel)):
		levelUp(int(level)+1)

	# print(character)
	return json.dumps(character)

# print(createCharacter(18))

# for test in range(50):
# 	level = random.randint(1,20)
# 	character = createCharacter(level)
# 	filename = f'{test}.json'
# 	with open(filename,'w') as out:
# 		json.dump(character,out,indent=2)