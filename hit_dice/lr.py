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

count = max(1, int(char.levels.total_level / 2))
for die, num in hd_max.items():
  cc = f"Hit Dice (d{die})"
  cc_val = char.get_cc(cc) if char.cc_exists(cc) else 0
  cc_max = char.get_cc_max(cc) if char.cc_exists(cc) else 0
  if num > cc_max:
    cc_val += num - cc_max
    char.create_cc(cc, minVal=0, maxVal=num, reset='none')
    char.set_cc(cc, cc_val)
    fields += f"""-f "Creating {cc}|{char.cc_str(cc)} (was {cc_max})" """
  if cc_val < cc_max:
    mod = min(count, cc_max - cc_val)
    char.mod_cc(cc, mod)
    count -= mod
    fields += f"""-f "{cc}|{char.cc_str(cc)} (+{mod})" """
  elif cc_max:
    fields += f"""-f "{cc}|{char.cc_str(cc)}" """
    </drac2>
-title "{{char.name}} recovers Hit Dice!"
-desc "At the end of a long rest, the character also regains spent Hit Dice, up to a number of dice equal to half of the character's total number of them (minimum of one die)."
{{fields}}
-footer "!hd lr | kbsletten#5710"
-color <color> -thumb <image>
