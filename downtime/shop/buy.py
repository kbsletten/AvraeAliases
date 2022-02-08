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
rarity = ([r for r in ["legendary", "very", "rare", "uncommon"] if r in argv] + ["common"])[0]
minor = "minor" in argv and rarity != "common"
weeks = ceil({
  "legendary": 50,
  "very": 25,
  "rare": 10,
  "uncommon": 2,
  "common": 1
}[rarity] * (0.5 if minor else 1))
cost_expr = ({
  "legendary": "2d6 * 25000",
  "very": "(1d4 + 1) * 10000",
  "rare": "2d10 * 1000",
  "uncommon": "1d6 * 100",
  "common": "(1d6 + 1) * 10"
}[rarity])
cost = vroll(f"({cost_expr})/2" if minor else cost_expr)
cc = f"{'Minor ' if minor else ''}{RARITY[rarity]} Shopping"

char = character()
base_adv = args.adv(boolwise=True)
craft_expr = "+".join([char.skills.persuasion.d20(base_adv=base_adv)] + bonus)

fields = ""

char.create_cc_nx(cc, minVal=0)
char.mod_cc(cc, -weeks)
fields += f"""-f "{cc}|{char.cc_str(cc)} (-{weeks})" """

</drac2>
-title "Downtime Activity: Magic Item Shopping"
-f "Meta|**Rarity**: {{RARITY[rarity]}}
**Weeks**: {{weeks}} workweek{{"s" if weeks != 1 else ""}}
**Cost**: {{cost}}gp"
{{fields}}
-footer "!shop | kbsletten#5710"
-color <color> -thumb <image>
