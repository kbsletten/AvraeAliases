embed
<drac2>
argv = &ARGS&
args = argparse(argv)
char = character()

level = argv[1] if argv else None

lower_class = level in ["low", "lower", "lower-class"]
middle_class = level in ["mid", "middle", "middle-class"]
upper_class = level in ["up", "upper", "upper-class"]

cost = 10 if lower_class else 50 if middle_class else 250 if upper_class else None

base_adv = args.adv(boolwise=True)

persuasion_roll = vroll(
  "+".join(
    [(char.skills.persuasion.d20(base_adv=base_adv) if char else
      "2d20kh1" if base_adv is True else
      "2d20kl1" if base_adv is False else
      "1d20")] +
    args.get("b")
)

rewards = [r for r in [
  (6, "Character has made no new contacts."),
  (11, "Character has made an allied contact."),
  (16, "Character has made two allied contacts."),
  (21, "Character has made three allied contacts."),
] if r[0] <= persuasion_roll.total]

reward = rewards[len(rewards) - 1][1] if rewards else "Character has made a hostile contact."

</drac2>
-title "Downtime Activity: Carousing"
-f "Class|{{"Lower-Class" if lower_class else "Middle-Class" if middle_class else "Upper-Class" if upper-class else "None"}}"
-f "Cost|{{f"{cost}gp" if cost else "None"}}"
-f "Charisma (Persuasion)|{{persuasion_roll}}"
-f "Reward|{{reward}}"
-footer "!carouse | kbsletten#5710"
-color <color> -thumb <image>
