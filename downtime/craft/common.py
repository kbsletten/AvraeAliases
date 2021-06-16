embed
<drac2>
argv = &ARGS&
consumable = "potion" in argv

cost = 25 if consumable else 50
weeks = 1

complications = [
  "Rumors swirl that what you’re working on is unstable and a threat to the community.",
  "Your tools are stolen, forcing you to buy new ones.",
  "A local wizard shows keen interest in your work and insists on observing you.",
  "A powerful noble offers a hefty price for your work and is not interested in hearing no for an answer.",
  "A dwarf clan accuses you of stealing its secret lore to fuel your work.",
  "A competitor spreads rumors that your work is shoddy and prone to failure."
]

complication = ""
for i in range(0, floor(weeks/5)):
  complications_roll = vroll("1d100")
  complication += f"""-f "Complication|{complications_roll}
||{complications[vroll(f"1d{len(complications)}").total - 1]}||" """ if complications_roll.total <= 10 else f"""-f "Complication|{complications_roll}
None" """
</drac2>
-title "Crafting an Item: Common Magic Item"
-f "Cost|{{cost}}gp|inline"
-f "Weeks|{{weeks}} workweek{{"s" if weeks != 1 else ""}}|inline"
{{complication}}
-footer "!craft common | kbsletten#5710"
-color <color> -thumb <image>
