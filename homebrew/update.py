multiline
<drac2>
using(
    util="6665acd4-2763-4e51-9e44-f328bfb78a09"
)

FOOTER = """-footer "!homebrew update | kbsletten#5710" """

commands = ""

char = character()

server_homebrew, user_homebrew, character_homebrew = util.load_homebrew(char)

installed = character_homebrew.keys()

options = {}
for source in [server_homebrew, user_homebrew]:
  for package in source:
    for package_name, package_details in package.items():
      if package_name in installed:
        options[package_name] = package_details

if not installed:
  commands += f"""!embed -title "No Homebrew Installed" -desc "Install new homebrew with `!homebrew install PACKAGE` first." {FOOTER}
"""
else:
  updates = "\n".join([f"{option_name} {util.homebrew_summary(option_details)}" for option_name, option_details in options.items()])
  commands += f"""!embed -title "Updating Homebrew" -desc "Updating: {updates}" {FOOTER}
"""

for option_name, option_details in options.items():
  character_homebrew |= options
  if char:
    char.set_cvar("homebrew", dump_json(character_homebrew))
  for cc_name, cc_details in option_details["ccs"].items() if "ccs" in option_details else []:
    cc_name = cc_name.replace('"', '\\"')
    cc_details = " ".join([
      "-" + option_name + " \"" + str(option_value).replace('"', '\\"') + "\""
      for option_name, option_value in cc_details.items()
    ])
    commands += f"""!customcounter delete "{cc_name}"
"""
    commands += f"""!customcounter create "{cc_name}" {cc_details}
"""
  for action_name, action_details in option_details["actions"].items() if "actions" in option_details else []:
    action_name = action_name.replace('"', '\\"')
    commands += f"""!action delete "{action_name}"
"""
    commands += f"""!action import {dump_json(action_details)}
"""

</drac2>
{{commands}}
