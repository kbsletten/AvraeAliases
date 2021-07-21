attack import
<drac2>
GVARS = load_json(get_gvar("c1ee7d0f-750d-4f92-8d87-70fa22c07a81"))
CLASSES = [load_json(get_gvar(gvar)) for gvar in GVARS]

char = character()
ret_class = get("_retainerClass")
ret_level = int(get("_retainerLevel", 0))

cl_info = [c for c in CLASSES if c["name"] == ret_class]
cl_info = cl_info[0] if cl_info else None

json = []

if cl_info:
  json += [cl_info["attack"]]
  for action in cl_info["actions"]:
    if ret_level < action["level"]:
      continue
    if action["cc"]:
      char.create_cc(action["cc"], minVal=0, maxVal=action["cc_max"], dispType='bubble', reset='long')
    json += [action["attack"]]
</drac2>
{{dump_json(json)}}