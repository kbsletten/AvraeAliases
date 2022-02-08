embed
<drac2>
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
weeks = int(args.last("weeks", 1))
rarity = ([r for r in ["legendary", "very", "rare", "uncommon"] if r in argv] + ["common"])[0]
minor = "minor" in argv and rarity != "common"
dc = {
  "legendary": 30,
  "very": 25,
  "rare": 20,
  "uncommon": 15,
  "common": 10
}[rarity]
cost = int({
  "legendary": 1000,
  "very": 400,
  "rare": 100,
  "uncommon": 50,
  "common": 25
}[rarity] * weeks * (0.5 if minor else 1.0))
cc = f"{'Minor ' if minor else ''}{RARITY[rarity]} Shopping"

char = character()
base_adv = args.adv(boolwise=True)
craft_expr = "+".join([char.skills.persuasion.d20(base_adv=base_adv)] + bonus)

progress = 0

fields = ""

for i in range(0, weeks):
  craft_roll = vroll(craft_expr)
  success = 2 if craft_roll.total >= dc else 1
  fields += f"""-f "Week {i+1}|**Charisma (Persuasion)**: {craft_roll}{"; Success!" if success > 1 else ""}
**Progress**: {success} week{"s" if success > 1 else ""}" """
  progress += success

char.create_cc_nx(cc, minVal=0)
char.mod_cc(cc, progress)
fields += f"""-f "{cc}|{char.cc_str(cc)} (+{progress})" """

</drac2>
-title "Downtime Activity: Magic Item Shopping"
-f "Meta|**Rarity**: {{RARITY[rarity]}}
**Weeks**: {{weeks}} workweek{{"s" if weeks != 1 else ""}}
**DC**: {dc}
**Cost**: {{cost}}gp"
{{fields}}
-footer "!shop | kbsletten#5710"
-color <color> -thumb <image>
