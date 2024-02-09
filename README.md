**<h2>Starfinder Random Generator Scripts</h2>** 

**computer_random.py** \
*Invocation:  python computer_random.py --tier=3 --complexity=2* \
  --tier:         The tier of the computer. This should be a number between 1 and 10 per the computer rules. The higher the tier the more countermeasure nodes there will be. \
  --complexity:   How complex you want the resulting architecture to be. The higher you set this number the more nodes there will be. Additional nodes will be mostly empty nodes. Default=2


**loot_random.py** \
*Invocation:  python loot_random.py --cr=5 --players=7* \
  --cr:           The CR of the encounter. The higher this is the higher the level of loot that will be found and the more total worth. Items found will be between CR-5 and CR+2. \
  --players:      The number of players in the encounter. The higher this is the higher the total worth of the loot generated, but does not affect the level of items found. Default=7 


**ship_random.py** \
*Invocation:  python ship_random.py --max_tier=5 --exclude=D,T* \
  --max_tier:      The highest tier of ship to generate. The generator will try to generate as high of a tier ship as it can, but intentional limitations mean that it won't always generate a ship of the maximum tier. \
  --exclude:       comma separated list of characters indicating what ship sizes to ignore when generating. Sizes are the first letter of each size such as D=Diminutive, T=Tiny, etc
