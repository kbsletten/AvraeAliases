embed
<drac2>
n = "name"
c = "count"
d = "die"
t = "type"
f = "finesse"
v = "versatile"
r = "ranged"
bl="bludgeoning"
pi="piercing"
sl="slashing"
weapons = {
  "ba": { n: "Battleaxe", d: 8, t: sl, v: 10 },
  "battleaxe": { n: "Battleaxe", d: 8, t: sl, v: 10 },
  "club": { n: "Club", d: 4, t: bl },
  "cl": { n: "Club", d: 4, t: bl },
  "dg": { n: "Dagger", d: 4, t: bl, f: True },
  "dagger": { n: "Dagger", d: 4, t: bl, f: True },
  "da": { n: "Dart", d: 4, t: pi, f: True },
  "dart": { n: "Dart", d: 4, t: pi, f: True },
  "fl": { n: "Flail", d: 8, t: bl },
  "flail": { n: "Flail", d: 8, t: bl },
  "gl": { n: "Glaive", d: 10, t: sl },
  "glaive": { n: "Glaive", d: 10, t: sl },
  "ga": { n: "Greataxe", d: 12, t: sl },
  "greataxe": { n: "Greataxe", d: 12, t: sl },
  "gc": { n: "Greatclub", d: 8, t: bl },
  "greatclub": { n: "Greatclub", d: 8, t: bl },
  "gs": { n: "Greatsword", c: 2, d: 6, t: sl },
  "greatsword": { n: "Greatsword", c: 2, d: 6, t: sl },
  "hl": { n: "Halberd", d: 10, t: sl },
  "halberd": { n: "Halberd", d: 10, t: sl },
  "handaxe": { n: "Handaxe", d: 6, t: sl },
  "ha": { n: "Handaxe", d: 6, t: sl },
  "jv": { n: "Javelin", d: 6, t: sl },
  "javelin": { n: "Javelin", d: 6, t: sl },
  "la": { n: "Lance", d: 12, t: pi },
  "lance": { n: "Lance", d: 12, t: pi },
  "lc": { n: "Light Crossbow", d: 8, t: pi, r: True },
  "light crossbow": { n: "Light Crossbow", d: 8, t: pi, r: True },
  "lh": { n: "Light Hammer", d: 4, t: bl },
  "light hammer": { n: "Light Hammer", d: 4, t: bl },
  "ls": { n: "Longsword", d: 8, t: sl, v: 10 },
  "longsword": { n: "Longsword", d: 8, t: sl, v: 10 },
  "mc": { n: "Mace", d: 6, t: bl },
  "mace": { n: "Mace", d: 6, t: bl },
  "maul": { n: "Maul", c: 2, d: 6, t: bl },
  "ml": { n: "Maul", c: 2, d: 6, t: bl },
  "morningstar": { n: "Morningstar", d: 8, t: pi },
  "ms": { n: "Morningstar", d: 8, t: pi },
  "pi": { n: "Pike", d: 10, t: pi },
  "pike": { n: "Pike", d: 10, t: pi },
  "qs": { n: "Quarterstaff", d: 6, t: bl, v: 8 },
  "quarterstaff": { n: "Quarterstaff", d: 6, t: bl, v: 8 },
  "rp": { n: "Rapier", d: 8, t: pi, f: True },
  "rapier": { n: "Rapier", d: 8, t: pi, f: True },
  "sc": { n: "Scimitar", d: 6, t: sl, f: True },
  "scimitar": { n: "Scimitar", d: 6, t: sl, f: True },
  "sb": { n: "Shortbow", d: 6, t: pi, r: True },
  "shortbow": { n: "Shortbow", d: 6, t: pi, r: True },
  "ss": { n: "Shortsword", d: 6, t: pi, f: True },
  "shortsword": { n: "Shortsword", d: 6, t: pi, f: True },
  "si": { n: "Sickle", d: 4, t: sl },
  "sickle": { n: "Sickle", d: 4, t: sl },
  "sl": { n: "Sling", d: 6, t: bl, r: True },
  "sling": { n: "Sling", d: 6, t: bl, r: True },
  "trident": { n: "Trident", d: 6, t: pi, v: 8 },
  "sp": { n: "Spear", d: 6, t: pi, v: 8 },
  "spear": { n: "Spear", d: 6, t: pi, v: 8 },
  "unarmed": { n: "Unarmed Strike", d: 1, t: bl },
  "un": { n: "Unarmed Strike", d: 1, t: bl },
  "wp": { n: "War Pick", d: 8, t: pi },
  "war pick": { n: "War Pick", d: 8, t: pi },
  "wh": { n: "Warhammer", d: 8, t: bl, v: 10 },
  "warhammer": { n: "Warhammer", d: 8, t: bl, v: 10 },
  "wp": { n: "Whip", d: 4, t: sl, f: True },
  "whip": { n: "Whip", d: 4, t: sl, f: True }
}

argv = &ARGS&
args = argparse(argv)
command = argv[0] if len(argv) > 0 else ""
is_debug = "debug" in argv

current_combat = combat()
current_combatant = current_combat.current if current_combat else None
combatant_name = args.last("name", current_combatant.name if current_combatant else "An Unknown Creature")

proficiency_bonus = current_combatant.stats.prof_bonus if current_combatant else 2
strength_modifier = current_combatant.stats.get_mod("strength") if current_combatant else 0
strength_attack = proficiency_bonus + strength_modifier
strength_dc = 8 + strength_attack
dexterity_modifier = current_combatant.stats.get_mod("dexterity") if current_combatant else 0
dexterity_attack = proficiency_bonus + dexterity_modifier
dexterity_dc = 8 + dexterity_attack

weapon = weapons[command] if command in weapons else None
weapon_name = "Unarmed Strike"
weapon_count = 1
weapon_die = 1
weapon_type = bl
weapon_finesse = "finesse" in argv
weapon_ranged = "ranged" in argv
two_handed = "2h" in argv
auto_miss = "miss" in argv
weapon_size = int(args.last("s", 1))
if weapon:
  weapon_name = weapon["name"] if "name" in weapon else weapon_name
  weapon_count = weapon["count"] if "count" in weapon else weapon_count
  if two_handed and "versatile" in weapon:
    weapon_die = weapon["versatile"]
  else:
    weapon_die = weapon["die"] if "die" in weapon else weapon_die
  weapon_type = weapon["type"] if "type" in weapon else weapon_type
  weapon_finesse = weapon["finesse"] if "finesse" in weapon else weapon_finesse
  weapon_ranged = weapon["ranged"] if "ranged" in weapon else weapon_ranged
weapon_attack = int(args.last("b", dexterity_attack if weapon_ranged else (max(strength_attack, dexterity_attack) if weapon_finesse else strength_attack)))
weapon_bonus = dexterity_modifier if weapon_ranged else (max(strength_modifier, dexterity_modifier) if weapon_finesse else strength_modifier)
weapon_dc = int(args.last("dc", dexterity_dc if weapon_ranged else (max(strength_dc, dexterity_dc) if weapon_finesse else strength_dc)))

if weapon_size > 1 and weapon_die > 1:
  weapon_count *= weapon_size
weapon_expr = (f"{weapon_count}d{weapon_die}" if weapon_die > 1 else str(weapon_count)) + (f"+{weapon_bonus}" if weapon_bonus != 0 else "")

debug = f"""-f "Debug|**Weapon**: {weapon_count}d{weapon_die}
**Strength**: {strength_modifier}, +{strength_attack}, DC {strength_dc}
**Dexterity**: {dexterity_modifier}, +{dexterity_attack}, DC {dexterity_dc}
"
"""

fields = ""
title = f"""{combatant_name} attacks with a {weapon_name}{" (Two-handed)" if two_handed else ""}"""
desc = ""
target_info = ""

if command == "help":
  title = "Custom Attack"
  desc = """Make a custom attack.
**Standard Equipment**
`!ca spear -t Hero`
**Versatile Weapons**
`!ca spear 2h -t Hero`
**Oversized Weapons**
`!ca spear -s 2 2h -t Hero`
"""
  fields = ""
else:
  for target_name in args.get("t"):
    attack_roll = vroll(f"1d20+{weapon_attack}")
    damage_expr = args.last("d", f"{weapon_expr}[{weapon_type}]")
    is_miss = auto_miss or "(**1**)" in attack_roll.dice
    is_crit = "crit" in argv or "(**20**)" in attack_roll.dice
    target = current_combat.get_combatant(target_name) if current_combat else None
    target_damage = f"**Damage**: {vroll(damage_expr)}"
    if target and attack_roll.total >= target.ac:
      target_damage = target.damage(damage_expr, crit=is_crit)["damage"]
    elif target:
      target_damage = "**Miss!**"
    fields += f"""
  -f "{target.name}|**To Hit**: {attack_roll if not auto_miss else "Automatic miss"}
{target_damage}"
"""
    target_info += f"{target.name} {target.hp_str()}\n" if target else ""
</drac2>
-title "{{title}}"
-desc  "{{desc}}"
{{fields}}
{{debug if is_debug else ""}}
{{f"""-footer "{target_info}" """ if target_info else """-footer "Equipment | PHB" """}}
-color <color>