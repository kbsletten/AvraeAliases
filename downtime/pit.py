embed
<drac2>
HIT_DICE = {
  "Artificer": 8,
  "Barbarian": 12,
  "Bard": 8,
  "Cleric": 8,
  "Druid": 8,
  "Fighter": 10,
  "Monk": 8,
  "Paladin": 10,
  "Ranger": 10,
  "Rogue": 8,
  "Sorcerer": 6,
  "Warlock": 8,
  "Wizard": 6,
}

argv = &ARGS&
args = argparse(argv)
char = character()

base_adv = args.adv(boolwise=True)
base_d20 = "2d20kh1" if base_adv is True else "2d20kl1" if base_adv is False else "1d20"

hit_die = 6
if char:
  for name, level in char.levels:
    die = HIT_DICE[name] if name in HIT_DICE else None
    if not die:
      continue
    if die > hit_die:
      hit_die = die

replace = [
  ["max(dexterityMod, strengthMod)", str(max(char.stats.get_mod("dex"), char.stats.get_mod("str")))],
  ["dexterityMod", str(char.stats.get_mod("dex"))],
  ["strengthMod", str(char.stats.get_mod("str"))],
  ["proficiencyBonus", str(char.stats.prof_bonus)]
]

best_attack = None
attack_bonus = -10
for attack in char.attacks if char else []:
  bonus = attack.raw["automation"][0]["effects"][0]["attackBonus"] if "effects" in attack.raw["automation"][0] and "attackBonus" in attack.raw["automation"][0]["effects"][0] else "0"
  for key, value in replace:
    bonus = bonus.replace(key, value)
  bonus = vroll(bonus).total
  if bonus > attack_bonus:
    best_attack = attack.name
    attack_bonus = bonus

replace_attack = [best_attack, f"{base_d20}+{attack_bonus}"] if best_attack else None

replace_athletics = any(kw in argv for kw in ["athletics", "ath"])
replace_acrobatics = any(kw in argv for kw in ["acrobatics", "acr"])
replace_constitution = any(kw in argv for kw in ["constitution", "con"])

checks = [
  (replace_attack if replace_athletics else None) or ["Athletics", char.skills.athletics.d20(base_adv=base_adv) if char else base_d20],
  (replace_attack if replace_acrobatics else None) or ["Acrobatics", char.skills.acrobatics.d20(base_adv=base_adv) if char else base_d20],
  (replace_attack if replace_constitution else None) or ["Constitution", char.skills.constitution.d20(base_adv=base_adv) + f"+1d{hit_die}" if char else base_d20]
]

fields = ""
successes = 0
fight_round = 1
for name, dice in checks:
  dc_roll = vroll("2d10+5")
  check_roll = vroll(dice)
  success = check_roll.total >= dc_roll.total
  if success:
    successes += 1
  fields += f"""-f "Round {fight_round}|**DC**: {dc_roll}
**{name}**:{check_roll}; {"Success!" if success else "Failure!"}" """
  fight_round += 1

fields += f"""-f "Reward|{200 if successes > 2 else 100 if successes > 1 else 50 if successes else 0}gp" """

</drac2>
-title "Downtime Pit Fighting"
{{fields}}
-footer "!pit | kbsletten#5710"
-color <color> -thumb <image>
