embed
<drac2>
argv = &ARGS&
args = argparse(argv)

char = character()
init = combat()

target = init.get_combatant(args.last("t")) if init and args.last("t") else init.me if init and init.me else init.current if init and init.current else None
target = init.me if init and init.me else init.current if init and init.current else None

name = target.name if target else char.name if char else name

modifier = None
if "adv" in argv:
  modifier = 1
if "dis" in argv:
  modifier = -1 if modifier is None else 0

d20 = (target or char).skills.stealth.d20(base_adv=({-1: False, 0: None, 1: True})[modifier or 0]) if target or char else ({ -1: "2d20kl1", 0: "1d20", 1: "2d20kh1" })[modifier or 0]
b = [effect.effect["cb"] for effect in target.effects if "cb" in effect.effect] if target else []

stealth_roll = vroll("+".join([d20] + b + args.get("b")))

if target:
  target.add_effect(f"Hidden ({stealth_roll.total})", "", 2)

</drac2>
-title "{{name}} tries to Hide!"
-f "Dexterity (Stealth)|{{stealth_roll}}"
-footer "!hide | kbsletten#5710"
-color <color> {{"-thumb <image>" if not target or init.me and init.me.id == target.id else ""}}
