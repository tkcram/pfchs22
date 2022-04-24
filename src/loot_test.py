import json, math, random, re, requests

url = 'https://www.dnd5eapi.co'

def itemAdd(item, inventoryList):
	print('adding item',item['equipment']['index'])
	itemURL = item['equipment']['url']
	quantity = item['quantity']
	characteritemRequest = requests.get(url + itemURL)
	characteritemData = json.loads(characteritemRequest.text)
	itemName = characteritemData['index']
	itemType = characteritemData['equipment_category']['index']

	if itemType in inventoryList:
		if itemName not in inventoryList[itemType]: 
			if itemName != 'net':
				item = {}
				if itemType == 'weapon': # For Weapons
					props = []
					for prop in characteritemData['properties']:
						props.append(prop['index'])

					item = {
						itemName: {
							'base-damage': {characteritemData['damage']['damage_type']['index']: characteritemData['damage']['damage_dice']},
							'damage': {characteritemData['damage']['damage_type']['index']: characteritemData['damage']['damage_dice']},
							'category':characteritemData['weapon_category'],
							'range': characteritemData['weapon_range'],
							'properties': props,
							'quantity': quantity,
							'equipped': False
						}
					}
				elif itemType == 'armor': # For armor
					acBase = characteritemData['armor_class']['base']
					item = {
						itemName: {
							'base-ac': acBase,
							'ac': acBase,
							'category':characteritemData['armor_category'],
							'quantity': quantity,
							'equipped': False
						}
					}
				inventoryList[itemType].update(item)
		else:
			inventoryList[itemType][itemName]['quantity'] += quantity
	return inventoryList

def createLoot(roll,bonus):
	lootCategories = ["potion",
				"simple-melee-weapons",
				"simple-ranged-weapons",
				"martial-melee-weapons",
				"martial-ranged-weapons",
				"light-armor",
				"medium-armor",
				"heavy-armor",
				"shields"
				]
	if roll > 10:
		lootList = {'weapon': {},
			'armor': {},
			'consumable': {}}
		lootUrl = url+"/api/equipment-categories/"+lootCategories[19-roll]
		lootSearchData = json.loads(requests.get(lootUrl).text)
		lootCount = len(lootSearchData['equipment'])
		lootRandom = random.randint(0,lootCount-1)
		lootName = lootSearchData['equipment'][lootRandom]['index']
		lootFormat = {'equipment':lootSearchData['equipment'][lootRandom],
						'quantity': 1}
		print('Map loot add')
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
				print('potion get')

		print(roll,lootList)
		return lootList


