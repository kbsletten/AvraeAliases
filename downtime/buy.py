embed
<drac2>
args = argparse(&ARGS&)
char = character()

weeks = max(1, int(args.last("weeks", 0)))
cost = floor(max(100, int(args.last("cost", 0)))/100)
bonus = min(weeks - 1 + cost - 1, 10)
dc = int(args.last("dc", 100))

base_adv = args.adv(boolwise=True)

persuasion_roll = vroll(
  "+".join(
    [(char.skills.persuasion.d20(base_adv=base_adv) if char else
      "2d20kh1" if base_adv is True else
      "2d20kl1" if base_adv is False else
      "1d20")] +
    args.get("b") +
    ([f"{bonus}[bonus]"] if bonus > 0 else []))
)

rewards = [r for r in [
  (1, "1d6", "A"),
  (6, "1d4", "B"),
  (11, "1d4", "C"),
  (16, "1d4", "D"),
  (21, "1d4", "E"),
  (26, "1d4", "F"),
  (31, "1d4", "G"),
  (36, "1d4", "H"),
  (41, "1d4", "I"),
] if r[0] <= min(dc, persuasion_roll.total)]

reward = rewards[len(rewards) - 1] if rewards else None
reward_roll = vroll(reward[1]) if reward else None
</drac2>
-title "Downtime Activity: Buying a Magic Item"
-f "Cost|{{cost*100}}gp|inline"
-f "Weeks|{{weeks}} workweek{{"s" if weeks != 1 else ""}}|inline"
{{f"""-f "Bonus|+{bonus}|inline" """ if bonus > 0 else ""}}
-f "Charisma (Persuasion)|{{persuasion_roll}}"
-f "Reward|{{f"{reward_roll} rolls on Magic Item Table {reward[2]} (`!mitable {reward[2]} {reward_roll.total}`)" if reward else "None"}}"
-footer "!buy | kbsletten#5710"
-color <color> -thumb <image>
