import json, math, random, re, requests

url = 'https://www.dnd5eapi.co'

def itemAdd(item, inventoryList):
	print('adding item',item['equipment']['index'])
	itemURL = item['equipment']['url']
	quantity = item['quantity']
	characterItemRequest = requests.get(url + itemURL)
	characterItemData = json.loads(characterItemRequest.text)
	itemName = characterItemData['index']
	itemType = characterItemData['equipment_category']['index']

	if itemType in inventoryList:
		if itemName not in inventoryList[itemType]: 
			if itemName != 'net':
				item = {}
				if itemType == 'weapon': # For Weapons
					props = []
					for prop in characterItemData['properties']:
						props.append(prop['index'])

					item = {
						itemName: {
							'base-damage': {characterItemData['damage']['damage_type']['index']: characterItemData['damage']['damage_dice']},
							'damage': {characterItemData['damage']['damage_type']['index']: characterItemData['damage']['damage_dice']},
							'category':characterItemData['weapon_category'],
							'range': characterItemData['weapon_range'],
							'properties': props,
							'quantity': quantity,
							# 'equipped': False
						}
					}
				elif itemType == 'armor': # For armor
					acBase = characterItemData['armor_class']['base']
					item = {
						itemName: {
							'base-ac': acBase,
							'ac': acBase,
							'category':characterItemData['armor_category'],
							'quantity': quantity,
							# 'equipped': False
						}
					}
				inventoryList[itemType].update(item)
		else:
			inventoryList[itemType][itemName]['quantity'] += quantity
	return inventoryList

	def createLoot(roll,bonus):
	lootCategories = ["stat-potion",
				"health-potion",
				"simple-melee-weapons",
				"simple-ranged-weapons",
				"martial-melee-weapons",
				"martial-ranged-weapons",
				"light-armor",
				"medium-armor",
				"heavy-armor",
				"shields"
				]
	if roll > 9:
		lootList = {'weapon': {},
			'armor': {},
			'consumable': {}}
		lootType = lootCategories[19-roll]
		if lootType == "stat-potion":
			potionStat = random.choice(['str','dex','con','int','wis','cha'])
			lootName = f'{potionStat}-potion'
			lootList['consumable'][lootName] = {'bonus': 0,
											'quantity': 1,
											'category': 'stat',
											'stat': potionStat}

		elif lootType == "health-potion":
			lootName = 'healing-potion'
			lootList['consumable'][lootName] = {'bonus': 0,
								'quantity': 1,
								'category': 'healing'}
		else: 
			lootUrl = url+"/api/equipment-categories/"+lootType
			lootSearchData = json.loads(requests.get(lootUrl).text)
			lootCount = len(lootSearchData['equipment'])
			lootRandom = random.randint(0,lootCount-1)
			lootName = lootSearchData['equipment'][lootRandom]['index']
			lootFormat = {'equipment':lootSearchData['equipment'][lootRandom],
							'quantity': 1}

			itemAdd(lootFormat,lootList)

		if bonus > 0:
			if lootList['weapon']:
				for damageType in lootList['weapon'][lootName]['damage']:
					lootList['weapon'][lootName]['base-damage'][damageType] += f'+{bonus}'
					lootList['weapon'][lootName]['damage'][damageType] += f'+{bonus}'
			elif lootList['armor']:
				lootList['armor'][lootName]['base-ac'] += bonus
				lootList['armor'][lootName]['ac'] += bonus
			elif lootList['consumable']:
				lootList['consumable'][lootName]['bonus'] += bonus
		print(roll,lootList)
		return lootList


