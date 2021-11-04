embed
<drac2>
argv = &ARGS&
args = argparse(argv)
char = character()

bet = int(args.last("bet", 10))

GAMES = [
  "Dice Set",
  "Dragonchess Set",
  "Playing Card Set",
  "Three-Dragon Ante Set"
]

base_adv = args.adv(boolwise=True)
base_d20 = "2d20kh1" if base_adv is True else "2d20kl1" if base_adv is False else "1d20"

exp_tools = char.cvars["eTools"].split(", ") if char and "eTools" in char.cvars else []
pro_tools = char.cvars["pTools"].split(", ") if char and "pTools" in char.cvars else []
game = ([g for g in exp_tools + pro_tools if g in GAMES] + [None])[0]
game_pro = 2 if game in exp_tools else 1 if game in pro_tools else 0
checks = [
  ["Wisdom (Insight)", char.skills.insight.d20(base_adv=base_adv) if char else base_d20] if not char or char.skills.insight.prof >= game_pro else [f"Wisdom ({game})", f"{char.skills.wisdom.d20(base_adv=base_adv)}+{game_pro*char.stats.prof_bonus}[{game}]"],
  ["Charisma (Deception)", char.skills.deception.d20(base_adv=base_adv) if char else base_d20] if not char or char.skills.deception.prof >= game_pro else [f"Charisma ({game})", f"{char.skills.charisma.d20(base_adv=base_adv)}+{game_pro*char.stats.prof_bonus}[{game}]"],
  ["Charisma (Intimidation)", char.skills.intimidation.d20(base_adv=base_adv) if char else base_d20] if not char or char.skills.deception.prof >= game_pro else [f"Charisma ({game})", f"{char.skills.charisma.d20(base_adv=base_adv)}+{game_pro*char.stats.prof_bonus}[{game}]"],
]

fields = ""
successes = 0
game_round = 1
for name, dice in checks:
  dc_roll = vroll("2d10+5")
  check_roll = vroll(dice)
  success = check_roll.total >= dc_roll.total
  if success:
    successes += 1
  fields += f"""-f "Game {game_round}|**DC**: {dc_roll}
**{name}**: {check_roll}; {"Success!" if success else "Failure!"}" """
  game_round += 1

fields += f"""-f "Cost|{bet}gp|inline" """

if successes == 0:
  fields += f"""-f "Debt|{bet}gp|inline" """
else:
  fields += f"""-f "Winnings|{int(bet * 2 if successes > 2 else bet * 1.5 if successes > 1 else bet / 2)}gp|inline" """

</drac2>
-title "Downtime Activity: Gambling"
{{fields}}
-footer "!gamble | kbsletten#5710"
-color <color> -thumb <image>
