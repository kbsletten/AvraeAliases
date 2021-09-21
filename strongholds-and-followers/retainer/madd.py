i madd
<drac2>
GVARS = load_json(get_gvar("c1ee7d0f-750d-4f92-8d87-70fa22c07a81"))
CLASSES = [load_json(get_gvar(gvar)) for gvar in GVARS]

char = character()
ret_name = get("_retainerName")
ret_class = get("_retainerClass")
ret_level = int(get("_retainerLevel", 0))

init = combat()
me = init.me if init else None

cl_info = [c for c in CLASSES if c["name"] == ret_class]
cl_info = cl_info[0] if cl_info else None

stats = cl_info["stats"] if cl_info else "Commoner"
initMod = 3 + (1 if cl_info and "dex" == cl_info["primary"] else 0)
hp = cl_info["hp"] * ret_level if cl_info else 10
ac = cl_info["ac"] if cl_info else 10
group = f"""-group "{me.group}" """ if me and me.group else ""
</drac2>
"{{stats}}" -h False -name "{{ret_name}}" {{group}} -hp {{hp}} -ac {{ac}} %*%
