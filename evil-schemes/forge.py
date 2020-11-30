embed
<drac2>
args = argparse(&ARGS&)

light = 'light' in args
heavy = not light and 'heavy' in args
finesse = 'finesse' in args
versatile = 'versatile' in args
two_handed = not light and not versatile and '2h' in args
reach = 'reach' in args

default_die = 8
modifier = "max(strengthMod, dexterityMod)" if finesse else "strengthMod" if char else 0
proficiency = char.stats.prof_bonus if char else 2

if light:
  default_die -= 2
if reach:
  default_die -= 2
if two_handed:
  default_die += 2
if heavy:
  default_die += 2

name = args.last('name', 'Custom Weapon')

bonus = args.last('b', modifier+proficiency)

number = int(args.last('n', 1))
die = int(args.last('die', default_die))
damage_type = args.last('type', 'bludgeoning')
damage = args.last('d', f"{number}d{die}+{modifier}[{damage_type}]")
two_handed_damage = args.last('d2', f"{number}d{die+2}+{modifier}[{damage_type}]")

scripts = "\n".join([
  f"""`!attack add \\"{name}\\" -b \\"{bonus}\\" -d \\"{damage}\\"`""",
  f"""`!attack add \\"2-Handed {name}\\" -b \\"{bonus}\\" -d \\"{two_handed_damage}\\"`""" if versatile else "",
])
plural = "s" if versatile else ""
reach_str = args.last("reach", "10 ft." if reach else "5 ft.")
avg_damage = number*die//2+modifier
damage_str = f"{number}d{die}+{modifier}"
versatile_str = f" or {number*(die+2)//2+modifier} ({number}d{die+2}+{modifier}) {damage_type} damage if used with two hands" if versatile else ""
</drac2>
-title "Forge a Weapon"
-f "Script{{plural}}|{{scripts}}"
-f "Effect|***Melee Weapon Attack:*** +{{bonus}} to hit, reach {{reach_str}}, one target. *Hit:* {{avg_damage}} ({{damage_str}}) {{damage_type}} damage{{versatile_str}}."
-footer "Forge"
-color <color>