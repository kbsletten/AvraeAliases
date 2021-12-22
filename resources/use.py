embed
<drac2>
argv = &ARGS&

char = character()
char_resources = load_json(char.cvars["resources"] if "resources" in char.cvars else "[]")

fields = ""

if argv:
  fields += f"""-f "Tags|{", ".join(argv)}" """

for resource in char_resources:
  res_name = resource["name"]
  res_value = resource["value"]
  res_tags = resource["tags"]
  res_skip = False
  for tag in argv:
    if tag not in res_tags:
      res_skip = True
      break
  if res_skip:
    continue
  res_roll = vroll(f"d{res_value}") if res_value else vroll("0")
  if res_roll.total == 1:
    res_value = res_value - 2 if res_value > 4 else 0 if res_value <= 1 else 1
  res_used = f""" (was {resource["value"]})""" if resource["value"] != res_value else ""
  fields += f"""-f "{res_name}|{res_roll}
{res_value}{res_used}|inline" """
  resource["value"] = res_value

char.set_cvar("resources", dump_json(char_resources))

</drac2>
-title "{{char.name}} uses resources!"
{{fields}}
-footer "!resources use | kbsletten#5710"
-color <color> -thumb <image>
