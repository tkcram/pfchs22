# Programming for Cultural Heritage - Spring '22

This repo contains the backend scripts for the PFCH final project (available in the 'src' folder). This includes two primary scripts, create_character.py and create_maze.py, as well as create_equipment (needed for both primary files) and create_monster (needed for create_maze)

This project was created as the backend for https://puis22.netlify.app/, as a project in pursuit of an MS-DAV at the Pratt Institute. Read the full report /here/

These scripts are deisgned to pull from https://www.dnd5eapi.co and their exports and functionality are outlined below.

## create_character.py
This script is designed to create a random DnD 5e character. This includes class, race, starting statistics, and equipment. 

Given a single numeric input < 20, it creates a level 0 character, and iteratively levels it up the the input value. It then exports the character as a JSON string. 
The 6 keys are: 
- 'details' which lists race and class data; 
- 'stats' which provides character statistics, modifiers, and saves; 
- 'skills' which lists the characters skills; 
- 'inventory' which lists character weapons and armor. *Note: other equipment types are not available at this time.*
- 'combat' which lists hit-points, armor-class, combat abilities, and related stats;
- 'spellcasting' which lists spell known and spell slots. 

Note that all abilities are only listed by name, and no information is provided as to what they do. Additionally, some class abilities (such as a Warlocks Eldritch Invocations) are currently unavailable.

## create_maze.py
This script creates a randomly generated maze based off of four inputs: 
- Size: number
- Entrance Row: number
- Entrance Column: number
- Monster Level: number

The maze is generated using a randomised depth first dearch algorithm, creating a maze of size Size and begining at the entrance row/column (that it marks as the entrance).
It also logs the longest possible path through the maze, and places an 'exit' marker at the end of the path.
Once the maze is generated, the script goes through each non entrance/exit cell and randomly determines if it should contain either equipment or monsters. If it does, then it calls the appropriate script to populate the cell.
In the case of creating a monster, it uses the Monster Level variable that was passed in during initialisation to create a monster with the requisite strength.

## create_equipment.py
This script containts two functions, createLoot and itemAdd. 

createLoot calls the API to generate a random weapon, shield, or potion, and passes it to the latter. 

itemAdd takes an item and an inventory list and transforms the given items into a specific form, adding them to the inventory list.

This is called by the create_character.py script for a character's starting equipment, and by create_maze.py script to populate the maze with equipment.

## create_monster.py
This script takes a numberic input as a parameter, and returns a random monster of that level formatted in the same fashion as create_character. However, compared to create_character, monsters have more definitive statistics and are less prone to random variance.

At this time several features, such as multi-attack, and not listed in the monster statistics

## Running the script
There are three ways to interact with these files: Via the frontend, via the endpoint, or by directly running the project files.

The frontend is a small webgame, available at:
https://puis22.netlify.app/

Endpoints are available at:
https://pfchs22.herokuapp.com/createMaze/{size}/{eRow}/{eCol}/{mLevel}
https://pfchs22.herokuapp.com/createCharacter/{level}

If you want to run the scripts locally, place all four files into a folder and call "python3 {script}" to run. create_character.py requires create_equipment.py, and create_maze.py requires create_equipment.py and create_monster.py. create_monster.py can also be run by itself.
Note that the import statement may need altering to reflect the local nature, and example export statements are available. 
