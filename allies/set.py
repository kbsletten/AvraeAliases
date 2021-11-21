embed
<drac2>
argv = &ARGS&
args = argparse(argv)

char = character()

ally_info = load_json(char.cvars["ally"] if "ally" in char.cvars else "{}")
ally_type = args.last("type", ally_info["type"] if "type" in ally_info else None)
ally_name = args.last("name", ally_info["name"] if "name" in ally_info else None)
ally_image = args.last("image", ally_info["image"] if "image" in ally_info else None)

ally_info["type"] = ally_type
ally_info["name"] = ally_name
ally_info["image"] = ally_image

char.set_cvar("ally", dump_json(ally_info))

title = ""
if ally_name:
  title = f"{char.name}'s ally {ally_name}!"
else:
  title = f"{char.name} doesn't have an ally!"
</drac2>
-title "{{title}}"
-f "Setup|`!ally set -type <creature type> -name <name> -image <image url>`"
-f "Ability Check|`!ally check <skill>`"
-f "Save|`!ally save <save>`"
-f "Attack|`!ally attack <attack>`"
-footer "!ally | kbsletten#5710"
-color <color> -thumb {{ally_image}}
