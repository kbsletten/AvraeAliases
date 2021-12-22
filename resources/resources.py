embed
<drac2>
char = character()
char_resources = load_json(char.cvars["resources"] if "resources" in char.cvars else "[]")

fields = ""

for resource in char_resources:
  res_name = resource["name"]
  res_value = resource["value"]
  res_tags = f""" ({", ".join(resource["tags"])})""" if resource["tags"] else ""
  fields += f"""-f "{res_name}|{res_value}{res_tags}|inline" """

</drac2>
-title "{{char.name}} checks their resources!"
{{fields}}
-footer "!resources | kbsletten#5710"
-color <color> -thumb <image>
