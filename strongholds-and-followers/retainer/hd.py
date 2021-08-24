embed
<drac2>
argv = &ARGS&
args = argparse(argv)

dice = int(argv[0]) if argv and not argv[0].startswith("-") else None

char = character()

ret_name = get("_retainerName")
ret_class = get("_retainerClass")
ret_level = int(get("_retainerLevel", 0))
ret_image = get("_retainerImage")

if not char.cc_exists("Retainer HD"):
  char.create_cc("Retainer HD", minVal=0, maxVal=ret_level, dispType='bubble', reset='long', reset_by=min(1, int(floor(ret_level/2))), desc="""A retainer can spend one or more Hit Dice at the end of a short rest, up to the retainer’s maximum number of Hit Dice, which is equal to the retainer’s level. For each Hit Die spent in this way, the retainer regains one Health Level. At the end of a long rest, a retainer regains spent Hit Dice, up to a number of dice equal to half of the retainer's total number of them (minimum of one die).""")
  char.set_cc("Retainer HD", ret_level)

fields = ""

title = f"{char.name} doesn't have a retainer!"
if ret_name and ret_class and ret_level:
  if dice and dice <= char.get_cc("Retainer HD"):
    title = f"{ret_name} uses Hit Dice!"
    char.mod_cc("Retainer HD", -dice)
    fields += f"""-f "Retainer HD|{char.cc_str("Retainer HD")} (-{dice})" """
    char.mod_cc("Retainer HP", dice)
    fields += f"""-f "Retainer HP|{char.cc_str("Retainer HP")} (+{dice})" """
  else:
    title = f"{ret_name}'s Hit Dice!"
    fields += f"""-f "Retainer HD|{char.cc_str("Retainer HD")}" """

</drac2>
-title "{{title}}"
{{fields}}
-footer "!retainer hd | kbsletten#5710"
-color <color> -thumb {{get("_retainerImage")}}
