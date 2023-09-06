embed
<drac2>
using(
    util='6665acd4-2763-4e51-9e44-f328bfb78a09'
)

fields = ""

char = character()

server_homebrew, user_homebrew, character_homebrew = util.load_homebrew(char)

if server_homebrew:
    packages = "\n".join(
        f"{package_name} {util.homebrew_summary(package_details)}"
        for package in server_homebrew
        for package_name, package_details in package.items()
    )
    fields += f"""-f "Server Homebrew|{packages}" """

if user_homebrew:
    packages = "\n".join(
        f"{package_name} {util.homebrew_summary(package_details)}"
        for package in user_homebrew
        for package_name, package_details in package.items()
    )
    fields += f"""-f "User Homebrew|{packages}" """

if character_homebrew:
    packages = "\n".join(
        f"{package_name} {util.homebrew_summary(package_details)}"
        for package_name, package_details in character_homebrew.items()
    )
    fields += f"""-f "Character Homebrew|{packages}" """

</drac2>
-title "Manage Homebrew"
{{fields}}
-footer "!homebrew | kbsletten#5710"
