embed
<drac2>
argv = &ARGS&
args = argparse(argv)
char = character()

dc = int(args.last("dc", 10))
loot = 1000 if dc >= 25 else 200 if dc >= 20 else 100 if dc >= 15 else 50

base_adv = args.adv(boolwise=True)
base_d20 = "2d20kh1" if base_adv is True else "2d20kl1" if base_adv is False else "1d20"

stealth_check = vroll(char.skills.stealth.d20(base_adv=base_adv) if char else base_d20)
dexterity_check = vroll("+".join(x for x in [
  char.skills.dexterity.d20(base_adv=base_adv) if char else base_d20,
  str(char.stats.prof_bonus) if char and "pTools" in char.cvars and "thieves" in char.cvars["pTools"].lower() else ""
] if x))
pick_ability = None
pick_skill = None
for ability, skill in [("Intelligence (Investigation)", char.skills.investigation), ("Wisdom (Perception)", char.skills.perception), ("Charisma (Deception)", char.skills.deception)]:
  if not pick_skill or skill.value > pick_skill.value:
    pick_ability = ability
    pick_skill = skill
skill_check = vroll(pick_skill.d20(base_adv=base_adv) if pick_skill else base_d20)

stealth_success = stealth_check.total >= dc
dexterity_success = dexterity_check.total >= dc
skill_success = skill_check.total >= dc

successes = (1 if stealth_success else 0) + (1 if dexterity_success else 0) + (1 if skill_success else 0)

</drac2>
-title "Downtime Activity: Crime"
-f "Meta|**DC**:{{dc}}
**Loot**: {{loot}}gp|inline"
-f "Cost|25gp|inline"
-f "Dexterity (Stealth)|{{stealth_check}}"
-f "Dexterity (Thieves' Tools)|{{dexterity_check}}"
-f "{{pick_ability}}|{{skill_check}}"
{{f"""-f "Failure|You must pay a fee of {loot}gp and spend {loot/25} weeks in jail." """ if successes == 0 else ""}}
{{f"""-f "Failure|You manage to escape." """ if successes == 1 else ""}}
{{f"""-f "Mixed|You manage to get half the loot, {int(loot/2)}gp." """ if successes == 2 else ""}}
{{f"""-f "Success|You earn {loot}gp." """ if successes == 3 else ""}}
-footer "!crime | kbsletten#5710"
-color <color> -thumb <image>
