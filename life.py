embed
<drac2>
death_rolls = []
parents_roll = vroll("1d100")
parents = "You know who your parents are or were." if parents_roll.total <= 95 else "You know who your parents are or were."
birth_roll = vroll("1d100")
birth_table = [
  (50, "Home"),
  (55, "Home of a family friend"),
  (63, "Home of a healer or midwife"),
  (65, "Carriage, cart, or wagon"),
  (68, "Barn, shed, or other outbuilding"),
  (70, "Cave"),
  (72, "Field"),
  (74, "Forest"),
  (77, "Temple"),
  (78, "Battlefield"),
  (80, "Alley or street"),
  (82, "Brothel, tavern, or inn"),
  (84, "Castle, keep, tower, or palace"),
  (85, "Sewer or rubbish heap"),
  (88, "Among people of a different race"),
  (91, "On board a boat or a ship"),
  (93, "In a prison or in the headquarters of a secret organization"),
  (95, "In a sage’s laboratory"),
  (96, "In the Feywild"),
  (97, "In the Shadowfell"),
  (98, "On the Astral Plane or the Ethereal Plane"),
  (99, "On an Inner Plane of your choice"),
  (100, "On an Outer Plane of your choice"),
]
birth = [x[1] for x in birth_table if birth_roll.total <= x[0]][0]
siblings_roll = vroll("1d10")
siblings = vroll("0" if siblings_roll.total <= 2 else "1d3" if siblings_roll.total <= 4 else "1d4+1" if siblings_roll.total <= 6 else "1d6+2" if siblings_roll.total <= 8 else "1d8+3")
order_roll = vroll("2d6")
order = "Twin, triplet, or quadruplet" if order_roll.total == 2 else "Older" if order_roll.total <= 7 else "Younger"
family_roll = vroll("1d100")
family_table = [
  (1, "None", True, True),
  (2, "Institution, such as an asylum", True, True),
  (3, "Temple", True, True),
  (5, "Orphanage", True, True),
  (7, "Guardian", True, True),
  (15, "Paternal or maternal aunt, uncle, or both; or extended family such as a tribe or clan", True, True),
  (25, "Paternal or maternal grandparent(s)", True, True),
  (35, "Adoptive family (same or different race)", True, True),
  (55, "Single father or stepfather", False, True),
  (75, "Single mother or stepmother", True, False),
  (100, "Mother and father", False, False),
]
family = [x for x in family_table if family_roll.total <= x[0]][0]
parent_fates_rolls = [vroll("1d4"), vroll("1d4")]
parent_fates_table = [
  ("Your parent died (roll on the Cause of Death supplemental table).", True),
  ("Your parent was imprisoned, enslaved, or otherwise taken away.", False),
  ("Your parent abandoned you.", False),
  ("Your parent disappeared to an unknown fate.", False),
]
parent_fates = [parent_fates_table[x.total-1] for x in parent_fates_rolls]
father = parent_fates[0][0] if family[2] else None
mother = parent_fates[1][0] if family[3] else None
if parent_fates[0][1] and family[2]:
  death_rolls += [("Father", vroll("1d12"))]
if parent_fates[1][1] and family[3]:
  death_rolls += [("Mother", vroll("1d12"))]
lifestyle_roll = vroll("3d6")
lifestyle_table = [
  (3, "Wretched", -40),
  (5, "Squalid", -20),
  (8, "Poor", -10),
  (12, "Modest", 0),
  (15, "Comfortable", 10),
  (17, "Wealthy", 20),
  (18, "Aristocratic", 40)
]
lifestyle = [x for x in lifestyle_table if lifestyle_roll.total <= x[0]][0]
home_roll = vroll(f"1d100+{lifestyle[2]}")
home_table = [
  (0, "On the streets"),
  (20, "Rundown shack"),
  (30, "No permanent residence; you moved around a lot"),
  (40, "Encampment or village in the wilderness"),
  (50, "Apartment in a rundown neighborhood"),
  (70, "Small house"),
  (90, "Large house"),
  (110, "Mansion"),
  (140, "Palace or castle")
]
home = [x for x in home_table if home_roll.total <= x[0]][0]
deaths = ""
death_table = [
  "Unknown",
  "Murdered",
  "Killed in battle",
  "Accident related to class or occupation",
  "Accident unrelated to class or occupation",
  "Natural causes, such as disease or old age",
  "Apparent suicide",
  "Torn apart by an animal or a natural disaster",
  "Consumed by a monster",
  "Executed for a crime or tortured to death",
  "Bizarre event, such as being hit by a meteorite, struck down by an angry god, or killed by a hatching slaad egg"
]
for name, death_roll in death_rolls:
  deaths += f"""-f "Death ({name})|{death_table[death_roll.total-1]}" """
</drac2>
-title "This is Your Life"
-f "Parents|{{parents}}"
-f "Birthplace|{{birth}}"
-f "Siblings|{{siblings.total}}"
{{f"""-f "Birth Order|{order}" """ if siblings.total > 0 else ""}}
-f "Family|{{family[1]}}"
{{f"""-f "Father|{father}" """ if father else ""}}
{{f"""-f "Mother|{mother}" """ if mother else ""}}
-f "Lifestyle|{{lifestyle[1]}}"
-f "Home|{{home[1]}}"
{{deaths}}
-footer "!life | kbsletten#5710"
-color <color>
