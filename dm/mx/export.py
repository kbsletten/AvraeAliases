embed
<drac2>
using (
  util='f90efd6e-d7ce-44e0-b0c9-0b3438a14271'
)
init = combat()
command = "!map "

for each in init.combatants if init else []:
  settings = util.get_settings(each)
  location = settings["Location"] if "Location" in settings else ""
  size = settings["Size"][0] if "Size" in settings else ""
  color = settings["Color"].partition(" ")[0] if "Color" in settings else ""
  command += f"""-t "{each.name}|{location}|{size}|{color}" """

map_options, comb = util.get_map_options(init)
if "Size" in map_options:
  command += f"""-size {map_options["Size"]} """
if "Background" in map_options:
  command += f"""-bg {map_options["Background"]} """
if "Options" in map_options:
  command += f"""-options {map_options["Options"]} """

command = command.replace("\"", "\\\"")
</drac2>
-title "Export Map Settings"
-desc "`{{command}}`"
-footer "!mx export | kbsletten#5710"
