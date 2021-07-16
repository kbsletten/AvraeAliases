embed
<drac2>
args = argparse(&ARGS&)

char = character()

dc = int(args.last("dc", 11))
n = int(args.last("n", 1))
base_adv = args.adv(boolwise=True)
fields = ""
failures = 0

for _ in range(0, n):
  save = char.saves.get("con") if char else None
  save_roll = vroll(save.d20(base_adv=base_adv) if save else "2d20kh1" if base_adv == True else "2d20kl1" if base_adv == False else "1d20")
  fields += f"""-f "DC {dc}|{save_roll} {"success" if save_roll.total >= dc else "failure"}" """
  if save_roll.total < dc:
    failures += 1
  dc += 1

if char:
  char.create_cc_nx("Exhaustion", minVal=0, maxVal=6, reset='long', dispType='bubble', reset_by=1, desc="Some special abilities and environmental hazards, such as starvation and the long-term effects of freezing or scorching temperatures, can lead to a special condition called exhaustion. Exhaustion is measured in six levels. An effect can give a creature one or more levels of exhaustion, as specified in the effect's description.")
  char.mod_cc("Exhaustion", -failures)
  fields += f"""-f "Exhaustion|{char.cc_str("Exhaustion")}{f" (-{failures})" if failures else ""}" """
</drac2>
-title "{{name}} makes a Forced March!"
{{fields}}
-footer "!march | kbsletten#5710"
-color <color> -thumb <image>
