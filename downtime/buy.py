embed
<drac2>
MINOR = {
  "common": "65b00601-deb4-4051-a561-4a40285cd133",
  "uncommon": "dafcda4c-667a-4439-97be-36bd36240074",
  "rare": "9a1aa943-7d3f-41df-84d8-2055549c6c29",
  "very": "6a388878-1efa-4a0d-8e74-d71f1e79d2c9",
  "legendary": "63426df2-941c-4405-9390-acebed0e9140"
}
MAJOR = {
  "uncommon": "fe1be3aa-c941-41b9-bb1c-a809c6d92efe",
  "rare": "88b76793-df1c-4942-8c36-ee23177d7cc2",
  "very": "7ec88982-7735-4e24-9011-470efbc62527",
  "legendary": "cf2f122b-cdb7-4b42-ae49-ddf6559fb5e1"
}

argv = &ARGS&
args = argparse(argv)
char = character()

rarity = argv[0] if argv else None
weeks = max(1, int(args.last("weeks", 0)))
cost = floor(max(100, int(args.last("cost", 0)))/100)
bonus = min(weeks - 1 + cost - 1, 10)
dc = 30 if rarity == "legendary" else 25 if rarity == "very" else 20 if rarity == "rare" else 15 if rarity == "uncommon" else 10 if rarity == "common" else None

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

result = None
if dc:
  result = persuasion_roll.total >= dc

capped = min(dc or 100, persuasion_roll.total)
rewards = ""
if capped >= 30:
  minor_list = get_gvar(MINOR["legendary"]).split("\n")
  major_list = get_gvar(MAJOR["legendary"]).split("\n")
  reward_roll = vroll(f"1d{len(major_list)}")
  cost_roll = vroll("2d6*25000")
  rewards += f"""-f "Major Item|**Roll**: {reward_roll}
**Item**: {major_list[reward_roll.total - 1]}
**Price**: {cost_roll}" """
  minor_roll = vroll("1d2")
  rewards += f"""-f "Minor Items|{minor_roll}" """
  for x in range(0, minor_roll.total):
    reward_roll = vroll(f"1d{len(minor_list)}")
    cost_roll = vroll("2d6*12500")
    rewards += f"""-f "Minor Item {x + 1}|**Roll**: {reward_roll}
**Item**: {minor_list[reward_roll.total - 1]}
**Price**: {cost_roll}" """
elif capped >= 25:
  minor_list = get_gvar(MINOR["very"]).split("\n")
  major_list = get_gvar(MAJOR["very"]).split("\n")
  reward_roll = vroll(f"1d{len(major_list)}")
  cost_roll = vroll("(1d4+1)*10000")
  rewards += f"""-f "Major Item|**Roll**: {reward_roll}
**Item**: {major_list[reward_roll.total - 1]}
**Price**: {cost_roll}" """
  minor_roll = vroll("1d4")
  rewards += f"""-f "Minor Items|{minor_roll}" """
  for x in range(0, minor_roll.total):
    reward_roll = vroll(f"1d{len(minor_list)}")
    cost_roll = vroll("(1d4+1)*5000")
    rewards += f"""-f "Minor Item {x + 1}|**Roll**: {reward_roll}
**Item**: {minor_list[reward_roll.total - 1]}
**Price**: {cost_roll}" """
elif capped >= 20:
  minor_list = get_gvar(MINOR["rare"]).split("\n")
  major_list = get_gvar(MAJOR["rare"]).split("\n")
  reward_roll = vroll(f"1d{len(major_list)}")
  cost_roll = vroll("2d10*1000")
  rewards += f"""-f "Major Item|**Roll**: {reward_roll}
**Item**: {major_list[reward_roll.total - 1]}
**Price**: {cost_roll}" """
  minor_roll = vroll("1d4")
  rewards += f"""-f "Minor Items|{minor_roll}" """
  for x in range(0, minor_roll.total):
    reward_roll = vroll(f"1d{len(minor_list)}")
    cost_roll = vroll("2d10*500")
    rewards += f"""-f "Minor Item {x + 1}|**Roll**: {reward_roll}
**Item**: {minor_list[reward_roll.total - 1]}
**Price**: {cost_roll}" """
elif capped >= 15:
  minor_list = get_gvar(MINOR["uncommon"]).split("\n")
  major_list = get_gvar(MAJOR["uncommon"]).split("\n")
  reward_roll = vroll(f"1d{len(major_list)}")
  cost_roll = vroll("1d6*100")
  rewards += f"""-f "Major Item|**Roll**: {reward_roll}
**Item**: {major_list[reward_roll.total - 1]}
**Price**: {cost_roll}" """
  minor_roll = vroll("1d4")
  rewards += f"""-f "Minor Items|{minor_roll}" """
  for x in range(0, minor_roll.total):
    reward_roll = vroll(f"1d{len(minor_list)}")
    cost_roll = vroll("1d6*50")
    rewards += f"""-f "Minor Item {x + 1}|**Roll**: {reward_roll}
**Item**: {minor_list[reward_roll.total - 1]}
**Price**: {cost_roll}" """
elif capped >= 10:
  minor_roll = vroll("1d6")
  rewards += f"""-f "Minor Items|{minor_roll}" """
  minor_list = get_gvar(MINOR["common"]).split("\n")
  for x in range(0, minor_roll.total):
    reward_roll = vroll(f"1d{len(minor_list)}")
    cost_roll = vroll("(1d6 + 1)*5")
    rewards += f"""-f "Minor Item {x + 1}|**Roll**: {reward_roll}
**Item**: {minor_list[reward_roll.total - 1]}
**Price**: {cost_roll}" """

</drac2>
-title "Downtime Activity: Buying a Magic Item"
-f "Cost|{{cost*100}}gp|inline"
-f "Weeks|{{weeks}} workweek{{"s" if weeks != 1 else ""}}|inline"
{{f"""-f "Bonus|+{bonus}|inline" """ if bonus > 0 else ""}}
-f "Charisma (Persuasion)|{{persuasion_roll}}{{"; Success!" if result is True else "; Failure" if result is False else ""}}"
{{rewards}}
-footer "!buy | kbsletten#5710"
-color <color> -thumb <image>
