embed
<drac2>
char = character()

ally_info = load_json(char.cvars["ally"] if "ally" in char.cvars else "{}")
ally_type = ally_info["type"] if "type" in ally_info else None
ally_name = ally_info["name"] if "name" in ally_info else ally_type
ally_image = ally_info["image"] if "image" in ally_info else None

title = ""
if ally_name:
  title = f"{char.name}'s ally {ally_name}!"
else:
  title = f"{char.name} doesn't have an ally!"
</drac2>
-title "{{title}}"
-f "Setup|`!ally set -type <creature type> -name <creature name> -image <image url>`"
-f "Join|`!ally join`"
-f "Ability Check|`!ally check <skill (e.g. athletics, wisdom)>`"
-f "Save|`!ally save <save (e.g. str, dex)>`"
-f "Attack|`!ally attack <attack (e.g. longsword, scare)>`"
-footer "!ally | kbsletten#5710"
-color <color> -thumb {{ally_image}}
