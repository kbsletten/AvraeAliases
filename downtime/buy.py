embed
<drac2>
args = argparse(&ARGS&)
char = character()

weeks = max(1, int(args.last("weeks", 0)))
cost = floor(max(100, int(args.last("cost", 0)))/100)
bonus = min(weeks - 1 + cost - 1, 10)

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
] if r[0] <= persuasion_roll.total]

reward = rewards[len(rewards) - 1] if rewards else None
reward_roll = vroll(reward[1]) if reward else None

complications = [
  "The item is a fake, planted by an enemy.",
  "The item is stolen by the party’s enemies.",
  "The item is cursed by a god.",
  "The item’s original owner will kill to reclaim it; the party’s enemies spread news of its sale.",
  "The item is at the center of a dark prophecy.",
  "The seller is murdered before the sale.",
  "The seller is a devil looking to make a bargain.",
  "The item is the key to freeing an evil entity.",
  "A third party bids on the item, doubling its price.",
  "The item is an enslaved, intelligent entity.",
  "The item is tied to a cult.",
  "The party’s enemies spread rumors that the item is an artifact of evil."
]

complications_roll = vroll("1d100")
complication = f"""||{complications[vroll(f"1d{len(complications)}").total - 1]}||""" if complications_roll.total <= 10 else "None"

</drac2>
-title "Downtime Activity: Buying a Magic Item"
-f "Cost|{{cost*100}}gp|inline"
-f "Weeks|{{weeks}} workweek{{"s" if weeks != 1 else ""}}|inline"
{{f"""-f "Bonus|+{bonus}|inline" """ if bonus > 0 else ""}}
-f "Charisma (Persuasion)|{{persuasion_roll}}"
-f "Reward|{{f"{reward_roll} rolls on Magic Item Table {reward[2]} (`!mitable {reward[2]} {reward_roll.total}`)" if reward else "None"}}"
-f "Complication|{{complications_roll}}
{{complication}}"
-footer "!buy | kbsletten#5710"
-color <color> -thumb <image>
