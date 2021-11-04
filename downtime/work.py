embed
<drac2>
argv = &ARGS&
args = argparse(argv)
char = character()

base_adv = args.adv(boolwise=True)
base_d20 = "2d20kh1" if base_adv is True else "2d20kl1" if base_adv is False else "1d20"

INT_TOOLS = [
  "Alchemist's Supplies",
  "Brewer's Supplies",
  "Calligrapher's Supplies",
  "Carpenter's Tools",
  "Cartographer's Tools",
  "Cobbler's Tools",
  "Cook's Utensils",
  "Glassblower's Tools",
  "Jeweler's Tools",
  "Leatherworker's Tools",
  "Mason's Tools",
  "Painter's Supplies",
  "Potter's Tools",
  "Smith's Tools",
  "Tinker's Tools",
  "Weaver's Tools",
  "Woodcarver's Tools"
]
CHA_TOOLS = [
  "Bagpipes",
  "Drum",
  "Dulcimer",
  "Flute",
  "Lute",
  "Lyre",
  "Horn",
  "Pan flute",
  "Shawm",
  "Viol"
]

exp_tools = char.cvars["eTools"].split(", ") if char and "eTools" in char.cvars else []
pro_tools = char.cvars["pTools"].split(", ") if char and "pTools" in char.cvars else []

tool = ([g for g in exp_tools + pro_tools if g in INT_TOOLS] + [None])[0]
tool_pro = 2 if tool in exp_tools else 1 if tool in pro_tools else 0
inst = ([g for g in exp_tools + pro_tools if g in CHA_TOOLS] + [None])[0]
inst_pro = 2 if inst in exp_tools else 1 if inst in pro_tools else 0

checks = [
  ("Strength (Athletics)", char.skills.athletics.value),
  ("Dexterity (Acrobatics)", char.skills.acrobatics.value),
  ("Charisma (Performance)", char.skills.performance.value),
  ("Wisdom (Survival)", char.skills.survival.value),
  (f"Intelligence ({tool})" if tool else "Intelligence", char.skills.intelligence.value + char.stats.prof_bonus * tool_pro),
  (f"Charisma ({inst})" if inst else "Charisma", char.skills.charisma.value + char.stats.prof_bonus * inst_pro)
]

work_check = None
for check_name, modifier in checks:
  if work_check is None or modifier > work_check[1]:
    work_check = (check_name, modifier)

check_name, modifier = work_check
work_roll = vroll(f"{base_d20}+{modifier}")

reward = 2
if work_roll.total > 20:
  reward = 50
elif work_roll.total >= 15:
  reward = 20
elif work_roll.total >= 10:
  reward = 10
</drac2>
-title "Downtime Activity: Work"
-f "{{check_name}}|{{work_roll}}"
-f "Reward|{{reward}}gp"
-footer "!work | kbsletten#5710"
-color <color> -thumb <image>
