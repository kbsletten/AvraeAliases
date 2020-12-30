embed
<drac2>
argv = &ARGS&
command = argv[0] if argv else "help"
rune_name = argv[1].lower() if argv and len(argv) > 1 else None
ignore = "-i" in argv
runes = [
  {
    "name": "Cloud Rune",
    "kw": ["cloud", "skye"],
    "img": "https://i.imgur.com/TuMkoKU.png",
    "lv": 3,
    "desc": """This rune emulates the deceptive magic used by some cloud giants. While wearing or carrying an object inscribed with this rune, you have advantage on Dexterity (Sleight of Hand) checks and Charisma (Deception) checks.
In addition, when you or a creature you can see within 30 feet of you is hit by an attack roll, you can use your reaction to invoke the rune and choose a different creature within 30 feet of you, other than the attacker. The chosen creature becomes the target of the attack, using the same roll. This magic can transfer the attack’s effects regardless of the attack’s range. Once you invoke this rune, you can’t do so again until you finish a short or long rest."""
  },
  {
    "name": "Fire Rune",
    "kw": ["fire", "ild"],
    "img": "https://i.imgur.com/nsBfhqZ.png",
    "lv": 3,
    "desc": """This rune’s magic channels the masterful craftsmanship of great smiths. While wearing or carrying an object inscribed with this rune, your proficiency bonus is doubled for any ability check you make that uses your proficiency with a tool.
In addition, when you hit a creature with an attack using a weapon, you can invoke the rune to summon fiery shackles: the target takes an extra 2d6 fire damage, and it must succeed on a Strength saving throw or be restrained for 1 minute. While restrained by the shackles, the target takes 2d6 fire damage at the start of each of its turns. The target can repeat the saving throw at the end of each of its turns, banishing the shackles on a success. Once you invoke this rune, you can’t do so again until you finish a short or long rest."""
  },
  {
    "name": "Frost Rune",
    "kw": ["frost", "ice", "ise"],
    "img": "https://i.imgur.com/aIbBWat.png",
    "lv": 3,
    "desc": """This rune’s magic evokes the might of those who survive in the wintry wilderness, such as frost giants. While wearing or carrying an object inscribed with this rune, you have advantage on Wisdom (Animal Handling) checks and Charisma (Intimidation) checks.
In addition, you can invoke the rune as a bonus action to increase your sturdiness. For 10 minutes, you gain a +2 bonus to all ability checks and saving throws that use Strength or Constitution. Once you invoke this rune, you can’t do so again until you finish a short or long rest."""
  },
  {
    "name": "Stone Rune",
    "kw": ["stone", "stein"],
    "img": "https://i.imgur.com/wrt5SJs.png",
    "lv": 3,
    "desc": """This rune’s magic channels the judiciousness associated with stone giants. While wearing or carrying an object inscribed with this rune, you have advantage on Wisdom (Insight) checks, and you have darkvision out to a range of 120 feet.
In addition, when a creature you can see ends its turn within 30 feet of you, you can use your reaction to invoke the rune and force the creature to make a Wisdom saving throw. Unless the save succeeds, the creature is charmed by you for 1 minute. While charmed in this way, the creature has a speed of 0 and is incapacitated, descending into a dreamy stupor. The creature repeats the saving throw at the end of each of its turns, ending the effect on a success. Once you invoke this rune, you can’t do so again until you finish a short or long rest."""
  },
  {
    "name": "Hill Rune",
    "kw": ["hill", "haug"],
    "img": "https://i.imgur.com/schZJMF.png",
    "lv": 7,
    "desc": """This rune’s magic bestows a resilience reminiscent of a hill giant. While wearing or carrying an object that bears this rune, you have advantage on saving throws against being poisoned, and you have resistance against poison damage.
In addition, you can invoke the rune as a bonus action, gaining resistance to bludgeoning, piercing, and slashing damage for 1 minute. Once you invoke this rune, you can’t do so again until you finish a short or long rest."""
  },
  {
    "name": "Storm Rune",
    "kw": ["storm", "uvar"],
    "img": "https://i.imgur.com/RugVmae.png",
    "lv": 7,
    "desc": """Using this rune, you can glimpse the future like a storm giant seer. While wearing or carrying an object inscribed with this rune, you have advantage on Intelligence (Arcana) checks, and you can’t be surprised as long as you aren’t incapacitated.
In addition, you can invoke the rune as a bonus action to enter a prophetic state for 1 minute or until you’re incapacitated. Until the state ends, when you or another creature you can see within 60 feet of you makes an attack roll, a saving throw, or an ability check, you can use your reaction to cause the roll to have advantage or disadvantage. Once you invoke this rune, you can’t do so again until you finish a short or long rest."""
  }
]

char = character()
name = char.name if char else name
proficiency_bonus = char.stats.prof_bonus if char else 2
fighter_level = char.levels.get("Fighter") if char else 0
subclass_json = load_json(char.cvars["subclass"]) if char and "subclass" in char.cvars else None
fighter_subclass = subclass_json["FighterLevel"] if subclass_json and "FighterLevel" in subclass_json else ""
runes_known = 0 if fighter_level < 3 or fighter_subclass != "Rune Knight" else 2 if fighter_level < 7 else 3 if fighter_level < 10 else 4 if fighter_level < 15 else 5
rune_max = 0 if fighter_level < 3 or fighter_subclass != "Rune Knight" else 1 if fighter_level < 15 else 2

rune = [rune for rune in runes if rune_name in rune["kw"]] if rune_name else []
rune = rune[0] if rune else None

char_runes = [rune["name"] for rune in runes if char.cc_exists(rune["name"])] if char else []
char_runes.sort()
char_has_rune = char.cc_exists(rune["name"]) if char and rune else False
char_rune = char.get_cc(rune["name"]) if char_has_rune else 0

title = ""
fields = ""
image = "<image>"

if command == "help":
  title = "Runes"
  rune_list = "; ".join(f'{rune["name"]} ({", ".join(rune["kw"])})' for rune in runes)
  if rune_name:
    if rune:
      title = f"""{rune["name"]}{f' ({rune["lv"]}th Level or Higher)' if rune["lv"] > 3 else ''}"""
      image = rune["img"]
      fields += f"""-f "Effect|{rune["desc"]}" """
    else:
      title = "Unknown Rune"
      fields += f"""-f "Invalid Rune|Supported runes are: {rune_list}" """
  else:
    fields += """-f "Usage|`!rune NAME` to activate it" """
    fields += f"""-f "Supported Runes|{rune_list}" """
if command == "pick":
  if char and rune:
    title = f'{name} picks the {rune["name"]}'
    if rune["name"] in char_runes:
      title = title.replace("picks", "already knows")
      fields += f"""-f "Effect|{rune["desc"]}" """
      fields += f"""-f "{rune["name"]}|{char.cc_str(rune["name"])}" """
    elif len(char_runes) >= runes_known:
      title = title.replace("picks", "cannot pick")
    elif fighter_level < rune["lv"]:
      title = title.replace("picks", "cannot pick")
      fields += f"""-f "Unmet Requirement|The {rune["name"]} is available to level {rune["lv"]} Rune Knights." """
    else:
      fields += f"""-f "Description|{rune["desc"]}" """
      char.create_cc(rune["name"], desc=rune["desc"], minVal=0, maxVal=rune_max, dispType='bubble', reset='long')
    char_runes = [rune["name"] for rune in runes if char.cc_exists(rune["name"])] if char else []
    char_runes.sort()
    fields += f"""-f "Runes Known ({len(char_runes)}/{runes_known})|{", ".join(char_runes or ["None"])}" """
  else:
    title = "Unknown Rune"
    fields += f"""-f "Invalid Rune|Supported runes are: {rune_list}" """

</drac2>
-title "{{title}}"
{{fields}}
-footer "Rune Knight | TCoE"
-color <color> -thumb {{image}}