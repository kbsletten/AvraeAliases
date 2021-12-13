embed
<drac2>
ABILITIES = {
  "Cobbler's Tools": "dex",
  "Glassblower's Tools": "dex",
  "Jeweler's Tools": "dex",
  "Leatherworker's Tools": "str",
  "Potter's Tools": "dex",
  "Smith's Tools": "str",
  "Tinker's Tools": "dex",
  "Weaver's Tools": "dex",
  "Woodcarver's Tools": "dex",
}
DESCRIPTIONS = {
  "dex": "Dexterity",
  "str": "Strength"
}
RARITY = {
  "legendary": "Legendary",
  "very": "Very Rare",
  "rare": "Rare",
  "uncommon": "Uncommon",
  "common": "Common"
}

argv = &ARGS&
args = argparse(argv)
bonus = args.get("b")
tool_name = argv[0].lower() if argv else ""
tool_name = ([a for a in ABILITIES.keys() if tool_name.lower() in a.lower()] + ["Cobbler's Tools"])[0]
weeks = int(args.last("weeks", 1))
rarity = ([r for r in ["legendary", "very", "rare", "uncommon"] if r in argv] + ["common"])[0]
minor = "minor" in argv
dc = {
  "legendary": 30,
  "very": 25,
  "rare": 20,
  "uncommon": 15,
  "common": 10
}[rarity]
cost = int({
  "legendary": 2000,
  "very": 800,
  "rare": 200,
  "uncommon": 100,
  "common": 50
}[rarity] * weeks * (0.5 if minor else 1.0))

char = character()
exp_tools = char.cvars["eTools"].split(", ") if char and "eTools" in char.cvars else []
pro_tools = char.cvars["pTools"].split(", ") if char and "pTools" in char.cvars else []

base_adv = args.adv(boolwise=True)
base_d20 = "2d20kh1" if base_adv is True else "2d20kl1" if base_adv is False else "1d20"

tool_pro = 2 if tool_name in exp_tools else 1 if tool_name in pro_tools else 0

ability = ABILITIES[tool_name]
modifier = char.stats.get_mod(ability) + char.stats.prof_bonus * tool_pro

craft_expr = "+".join([f"{base_d20}+{modifier}"] + bonus)

progress = 0

fields = ""

for i in range(0, weeks):
  craft_roll = vroll(craft_expr)
  success = 2 if craft_roll.total >= dc else 1
  fields += f"""-f "Week {i+1}|**{DESCRIPTIONS[ability]} ({tool_name})**: {craft_roll}{"; Success!" if success > 1 else ""}
**Progress**: {success} week{"s" if success > 1 else ""}" """
  progress += success

fields += f"""-f "Total|{progress} weeks" """

complications = [
  "Rumors swirl that what you’re working on is unstable and a threat to the community.",
  "Your tools are stolen, forcing you to buy new ones.",
  "A local wizard shows keen interest in your work and insists on observing you.",
  "A powerful noble offers a hefty price for your work and is not interested in hearing no for an answer.",
  "A dwarf clan accuses you of stealing its secret lore to fuel your work.",
  "A competitor spreads rumors that your work is shoddy and prone to failure."
]

complication = ""
for i in range(0, floor(weeks/5)):
  complications_roll = vroll("1d100")
  if complications_roll.total > 10:
    continue
  complication += f"""-f "Complication|{complications_roll}
||{complications[vroll(f"1d{len(complications)}").total - 1]}||" """
</drac2>
-title "Downtime Activity: Crafting an Item"
-f "Meta|**Rarity**: {{RARITY[rarity]}}
**Weeks**: {{weeks}} workweek{{"s" if weeks != 1 else ""}}
**DC**: {dc}
**Cost**: {{cost}}gp"
{{fields}}
{{complication}}
-footer "!craft | kbsletten#5710"
-color <color> -thumb <image>
