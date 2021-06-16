embed
<drac2>
argv = &ARGS&
args = argparse(argv)
char = character()

level = argv[0] if argv else None

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
)

rewards = [r for r in [
  (6, "Character has made no new contacts."),
  (11, "Character has made an allied contact."),
  (16, "Character has made two allied contacts."),
  (21, "Character has made three allied contacts."),
] if r[0] <= persuasion_roll.total]

reward = rewards[len(rewards) - 1][1] if rewards else "Character has made a hostile contact."

pickpocket_roll = vroll("1d10*5")

complications = [
  f"A pickpocket lifts {pickpocket_roll} from you.",
  "A bar brawl leaves you with a scar.",
  "You have fuzzy memories of doing something very, very illegal, but can’t remember exactly what.",
  "You are banned from a tavern after some obnoxious behavior.",
  "After a few drinks, you swore in the town square to pursue a dangerous quest.",
  "Surprise! You’re married.",
  "Streaking naked through the streets seemed like a great idea at the time.",
  "Everyone is calling you by some weird, embarrassing nickname, like Puddle Drinker or Bench Slayer, and no one will say why."
] if lower_class else [
  "You accidentally insulted a guild master, and only a public apology will let you do business with the guild again.",
  "You swore to complete some quest on behalf of a temple or a guild.",
  "A social gaffe has made you the talk of the town.",
  "A particularly obnoxious person has taken an intense romantic interest in you.",
  "You have made a foe out of a local spellcaster.",
  "You have been recruited to help run a local festival, play, or similar event.",
  "You made a drunken toast that scandalized the locals.",
  "You spent an additional 100 gp trying to impress people."
] if middle_class else [
  "A pushy noble family wants to marry off one of their scions to you.",
  "You tripped and fell during a dance, and people can’t stop talking about it.",
  "You have agreed to take on a noble’s debts.",
  "You have been challenged to a joust by a knight.",
  "You have made a foe out of a local noble.",
  "A boring noble insists you visit each day and listen to long, tedious theories of magic.",
  "You have become the target of a variety of embarrassing rumors.",
  "You spent an additional 500 gp trying to impress people."
] if upper_class else []

complications_roll = vroll("1d100")
complication = f"""||{complications[vroll(f"1d{len(complications)}").total - 1]}||""" if complications_roll.total <= 10 else "None"

</drac2>
-title "Downtime Activity: Carousing"
-f "Class|{{"Lower-Class" if lower_class else "Middle-Class" if middle_class else "Upper-Class" if upper_class else "None"}}"
-f "Cost|{{f"{cost}gp" if cost else "None"}}"
-f "Charisma (Persuasion)|{{persuasion_roll}}"
-f "Reward|{{reward}}"
-f "Complication|{{complications_roll}}
{{complication}}"
-footer "!carouse | kbsletten#5710"
-color <color> -thumb <image>
