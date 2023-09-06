multiline
<drac2>
using(
    util="6665acd4-2763-4e51-9e44-f328bfb78a09"
)

search = "&*&".lower()

FOOTER = """-footer "!homebrew install | kbsletten#5710" """

commands = ""

char = character()

server_homebrew, user_homebrew, character_homebrew = util.load_homebrew(char)

installed = character_homebrew.keys()

options = {}
for source in [server_homebrew, user_homebrew]:
  for package in source:
    for package_name, package_details in package.items():
      if search in package_name.lower() and package_name not in installed:
        options[package_name] = package_details

if not len(options):
  commands += f"""!embed -title "Homebrew Not Found" -desc "Unable to find package matching: &*&" {FOOTER}
"""
elif len(options) > 1:
  matching = "\n".join([
    f"{package_name} {util.homebrew_summary(package_details)}"
    for package_name, package_details in options.items()
  ])
  commands += f"""!embed -title "Multiple Homebrew Found" -desc "Found multiple packages matching: &*&
{matching}" {FOOTER}
"""
else:
  option_name, option_details = list(options.items())[0]
  commands += f"""!embed -title "Installing Homebrew" -desc "Installing: {option_name} {util.homebrew_summary(option_details)}" {FOOTER}
"""
  character_homebrew |= options
  if char:
    char.set_cvar("homebrew", dump_json(character_homebrew))
  for cc_name, cc_details in option_details["ccs"].items() if "ccs" in option_details else []:
    cc_name = cc_name.replace('"', '\\"')
    cc_details = " ".join([
      "-" + option_name + " \"" + str(option_value).replace('"', '\\"') + "\""
      for option_name, option_value in cc_details.items()
    ])
    commands += f"""!customcounter create "{cc_name}" {cc_details}
"""
  for action_name, action_details in option_details["actions"].items() if "actions" in option_details else []:
    commands += f"""!action import {dump_json(action_details)}
"""

</drac2>
{{commands}}
