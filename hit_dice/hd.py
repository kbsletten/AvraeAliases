embed
<drac2>
HIT_DICE = load_json(get_gvar("1498d2ca-cbb5-448a-acaf-e67c8b0213e8"))

argv = &ARGS&
args = argparse(argv)
char = character()

con_mod = char.stats.get_mod("con")
hd_max = {
  12: 0,
  10: 0,
  8: 0,
  6: 0,
}
hd_val = {
  12: 0,
  10: 0,
  8: 0,
  6: 0,
}
hd_used = {
  12: 0,
  10: 0,
  8: 0,
  6: 0,
}

for name, level in char.levels:
  die = HIT_DICE[name] if name in HIT_DICE else None
  if not die:
    continue
  hd_max[die] += level

fields = ""

for die, num in hd_max.items():
  cc = f"Hit Dice (d{die})"
  cc_val = char.get_cc(cc) if char.cc_exists(cc) else 0
  cc_max = char.get_cc_max(cc) if char.cc_exists(cc) else 0
  if num > cc_max:
    cc_val += num - cc_max
    char.create_cc(cc, minVal=0, maxVal=num, reset='none')
    char.set_cc(cc, cc_val)
    fields += f"""-f "Creating {cc}|{char.cc_str(cc)} (was {cc_max})" """
  hd_max[die] = max(hd_max[die], cc_max)
  hd_val[die] = cc_val

lastindex = ([i for i, arg in enumerate(argv) if arg and arg.startswith("-")] + [len(argv)])[0]
for command in argv[:lastindex]:
  num, _, die = command.partition("d")
  num = int(num) if num.isdigit() else 0
  if not num:
    continue
  die = int(die) if die.isdigit() else 0
  if not die:
    die = ([die for die, val in hd_val.items() if val] + [None])[0]
  if not die:
    die = ([die for die, val in hd_max.items() if val] + [None])[0]
  cc = f"Hit Dice (d{die})"
  cc_val = char.get_cc(cc) if char.cc_exists(cc) else 0
  if cc_val < num:
    fields += f"""-f "Using {num}d{die}|Unable to use {num} hit dice, had {cc_val}" """
    continue
  if args.adv() == 1:
    hd_roll = vroll("+".join(f"2d{die}kh1+{con_mod}" for _ in range(num)))
  elif args.adv() == -1:
    hd_roll = vroll("+".join(f"2d{die}kl1+{con_mod}" for _ in range(num)))
  else:
    hd_roll = vroll("+".join(f"d{die}+{con_mod}" for _ in range(num)))
  old_hp = char.hp
  char.modify_hp(hd_roll.total, overflow=False)
  char.mod_cc(cc, -num)
  hd_val[die] -= num
  hd_used[die] += num
  hp_diff = char.hp - old_hp
  fields += f"""-f "Using {num}d{die}|{hd_roll}
{char.name} {char.hp_str()} (+{hp_diff})" """

if any([die for die, num in hd_used.items() if num]):
  bonus = args.join("b", "+")
  if bonus:
    bonus_roll = vroll(bonus)
    old_hp = char.hp
    char.modify_hp(bonus_roll.total, overflow=False)
    hp_diff = char.hp - old_hp
    fields += f"""-f "Bonus|{bonus_roll}
{char.name} {char.hp_str()} (+{hp_diff})" """

</drac2>
-title "{{char.name}}{{" uses Hit Dice" if lastindex > 0 else "'s Hit Dice"}}"
{{fields}}
{{"\n".join([f"""-f "Hit Dice (d{hd})|{char.cc_str(f"Hit Dice (d{hd})")}{f" (-{hd_used[hd]})" if hd_used[hd] else ""}|inline" """ for hd, max in hd_max.items() if max > 0])}}
-footer "!hd | kbsletten#5710"
-color <color> -thumb <image>
