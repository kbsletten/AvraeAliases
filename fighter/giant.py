embed
<drac2>
argv = &ARGS&
ignore = "-i" in argv
cc = "Giant's Might"

char = character()
name = char.name if char else name
proficiency_bonus = char.stats.prof_bonus if char else 2
fighter_level = char.levels.get("Fighter") if char else 0
subclass_json = load_json(char.cvars["subclass"]) if char and "subclass" in char.cvars else None
fighter_subclass = subclass_json["FighterLevel"] if subclass_json and "FighterLevel" in subclass_json else ""

char_has_cc = char.cc_exists(cc) if char else False
char_cc = char.get_cc(cc) if char_has_cc else 0

title = f"{name} uses Giant's Might!"
fields = ""

if (fighter_level < 3 or fighter_subclass != "Rune Knight") and not ignore:
  title = title.replace("uses", "cannot use")
  fields += """-f "Invalid Alias|This character does not have the necessary class levels to use this alias. A third level Rune Knight Fighter gains this ability. If you have not run `!level`, do that and try again." """
  fields += f"""-f "Fighter Level|{fighter_level or 'None'}|inline" """
  fields += f"""-f "Fighter Subclass|{fighter_subclass or 'None'}|inline" """
elif not char_has_cc and not ignore:
  title = title.replace("uses", "cannot use")
  fields += f"""-f "Getting Started|Set up your CC with !level or by running `!cc crate \\"Giant's Might\\" -min 0 -max {proficiency_bonus} -type bubble -reset long -desc \\"You have learned how to imbue yourself with the might of giants. As a bonus action, you magically gain the following benefits, which last for 1 minute:

- If you are smaller than Large, you become Large, along with anything you are wearing. If you lack the room to become Large, your size doesn’t change.
- You have advantage on Strength checks and Strength saving throws.
- Once on each of your turns, one of your attacks with a weapon or an unarmed strike can deal an extra 1d6 damage to a target on a hit.

You can use this feature a number of times equal to your proficiency bonus, and you regain all expended uses of it when you finish a long rest.\\"`" """
elif char_cc < 1 and not ignore:
  title = title.replace("uses", "tries to use")
  fields += f"""-f "No Uses Remaining|You can use this feature a number of times equal to your proficiency bonus, and you regain all expended uses of it when you finish a long rest." """
  fields += f"""-f "{cc}|{char.cc_str(cc)}" """
else:
  init = combat()
  me = init.me if init else None
  fields += f"""-f "Effect|You have learned how to imbue yourself with the might of giants. As a bonus action, you magically gain the following benefits, which last for 1 minute:

- If you are smaller than Large, you become Large, along with anything you are wearing. If you lack the room to become Large, your size doesn’t change.
- You have advantage on Strength checks and Strength saving throws.
- Once on each of your turns, one of your attacks with a weapon or an unarmed strike can deal an extra 1d6 damage to a target on a hit.

You can use this feature a number of times equal to your proficiency bonus, and you regain all expended uses of it when you finish a long rest." """
  if not ignore:
    char.mod_cc(cc, -1)
    fields += f"""-f "{cc}|{char.cc_str(cc)} (-1)" """
  if me:
    me.add_effect("Giant's Might", "", duration=10)

</drac2>
-title "{{title}}"
{{fields}}
-footer "Rune Knight | TCoE"
-color <color> -thumb <image>