embed
<drac2>
argv = &ARGS&
args = argparse(argv)
GVARS = load_json(get_gvar("c1ee7d0f-750d-4f92-8d87-70fa22c07a81"))
CLASSES = [load_json(get_gvar(gvar)) for gvar in GVARS]

char = character()
ret_name = get("_retainerName")
ret_class = get("_retainerClass")

init = combat()
ret_comb = init.get_combatant(ret_name) if init and ret_name else None
ret_name = "An unknown creature" if "-h" in argv else ret_comb.name if ret_comb else ret_name

cl_info = [c for c in CLASSES if c["name"] == ret_class]
cl_info = cl_info[0] if cl_info else None

is_proficient = "pro" in argv or (cl_info and "con" in cl_info["saves"])
ret_bonus = 3 + (3 if is_proficient else 0)

title = f"{char.name} doesn't have a retainer!"
if ret_name:
  title = f"{ret_name} makes a Constitution save!"
fields = ""
desc = ""

bonus = [str(ret_bonus)] + args.get("b") + ([effect.effect["sb"] for effect in ret_comb.effects if "sb" in effect.effect] if ret_comb else [])
has_adv = "adv" in argv
has_dis = "dis" in argv
adv = 1 if has_adv and not has_dis else -1 if has_dis and not has_adv else 0
adv = 2 if adv == 1 and "ea" in argv else adv
save = {
  -1: "2d20kl1",
  0: "1d20",
  1: "2d20kh1",
  2: "3d20kh1"
}[adv]
check_roll = vroll("+".join([save] + bonus))

dc = int(args.last("dc")) if args.last("dc") else None

if dc:
  desc = f"""**DC {dc}**
"""
desc += f"{check_roll}"

harm = 0
if dc and check_roll.total < dc:
  harm = int(args.last("d", 1))

if harm:
  char.mod_cc("Retainer HP", -harm)
</drac2>
-title "{{args.last("title").replace("[name]", ret_name).replace("[sname]", "Constitution") if args.last("title") else title}}"
{{f"""-phrase "{args.last("phrase")}" """ if args.last("phrase") else ""}}
{{f"""-desc "{desc}" """ if desc else ""}}
{{fields}}
-footer "{{f"""{ret_name} {char.cc_str("Retainer HP")} (-{harm})""" if level and char and char.cc_exists("Retainer HP") else "!retainer damage | kbsletten#5710"}}"
-color <color> -thumb {{get("_retainerImage") if "-h" not in argv else ""}}
