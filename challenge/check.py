embed
<drac2>
SKILLS = [
  "acrobatics",
  "animalHandling",
  "arcana",
  "athletics",
  "deception",
  "history",
  "insight",
  "intimidation",
  "investigation",
  "medicine",
  "nature",
  "perception",
  "performance",
  "persuasion",
  "religion",
  "sleightOfHand",
  "stealth",
  "survival",
  "strength",
  "dexterity",
  "constitution",
  "intelligence",
  "wisdom",
  "charisma"
]
NAMES = {
  "acrobatics": "Dexterity (Acrobatics)",
  "animalHandling": "Wisdom (Animal Handling)",
  "arcana": "Intelligence (Arcana)",
  "athletics": "Strength (Athletics)",
  "deception": "Charisma (Deception)",
  "history": "Intelligence (History)",
  "insight": "Wisdom (Insight)",
  "intimidation": "Charisma (Intimidation)",
  "investigation": "Intelligence (Investigation)",
  "medicine": "Wisdom (Medicine)",
  "nature": "Intelligence (Nature)",
  "perception": "Wisdom (Perception)",
  "performance": "Charisma (Performance)",
  "persuasion": "Charisma (Persuasion)",
  "religion": "Intelligence (Religion)",
  "sleightOfHand": "Dexterity (Sleight of Hand)",
  "stealth": "Dexterity (Stealth)",
  "survival": "Wisdom (Survival)",
  "strength": "Strength",
  "dexterity": "Dexterity",
  "constitution": "Constitution",
  "intelligence": "Intelligence",
  "wisdom": "Wisdom",
  "charisma": "Charisma"
}

argv = &ARGS&
args = argparse(argv)
check_skill = (argv[0] if argv else SKILLS[0]).lower()
check_skill = ([skill for skill in SKILLS if skill.lower().startswith(check_skill)] + [SKILLS[0]])[0]

init = combat()
config = load_json(init.get_metadata("skillChallenge")) if init and init.get_metadata("skillChallenge") else { "dc": 13, "goalSuccess": 6, "goalFailure": 3, "success": 0, "failure": 0, "log": [] }
char = character()
me = init.me if init else None
name = me.name if me else char.name if char else name

dc = int(args.last("dc", config["dc"]))
is_pro = "pro" in argv
is_exp = "exp" in argv
base_adv = args.adv(boolwise=True)
base_d20 = {True: "2d20kh1", None: "1d20", False: "2d20kl1"}[base_adv]
prof_bonus = me.stats.prof_bonus if me else char.stats.prof_bonus if char else 0
modifier = me.skills[check_skill] if me else char.skills[check_skill] if char else None
modifier_prof = modifier.prof if modifier else 0
additional_prof = 2 - modifier_prof if is_exp else 1 - modifier_prof if is_pro else 0
base_roll = f"""{base_d20}+{(modifier.value if modifier else 0) + additional_prof * prof_bonus}"""
bonus = args.get("b") + ([effect.effects["cb"] for effect in me.effects if "cb" in effect.effects] if me else [])

title = f"{name} makes a {NAMES[check_skill]} check!"
check_roll = vroll("+".join([base_roll] + bonus))
success = check_roll.total >= dc
result = "Success!" if success else "Failure!"
if success:
  config["success"] += 1
else:
  config["failure"] += 1
config["log"] = config["log"] + [{ "name": name, "roll": str(check_roll), "result": result }]

if init:
  init.set_metadata("skillChallenge", dump_json(config))
</drac2>
-title "{{title}}"
-f "Meta|**DC**: {{dc}}"
-f "{{NAMES[check_skill]}}|{{check_roll}}; {{result}}"
-f "Successes|{{config["success"]}}/{{config["goalSuccess"] or "None"}}{{" (+1)" if success else ""}}|inline"
-f "Failures|{{config["failure"]}}/{{config["goalFailure"] or "None"}}{{" (+1)" if not success else ""}}|inline"
-footer "!challenge check | kbsletten#5710"
-color <color> -thumb <image>
