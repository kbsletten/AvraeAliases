embed
<drac2>
argv = &ARGS&
args = argparse(argv)
allies = load_json(get_svar("allies", "[]"))

init = combat()

targets = [init.get_combatant(t) for t in allies + (args.get("t") if init else [])]
target_ids = [comb.id for comb in targets if comb]

fields = ""

for comb in init.combatants if init else []:
  if comb.id in target_ids or comb.controller != ctx.author.id and comb.monster_name:
    remaining_casts = [comb.spellbook.remaining_casts_of(spell, 9) for spell in comb.spellbook.spells]
    slots = "\n".join([slot for slot in remaining_casts if slot != "No spell slots." and not slot.startswith("`")])
    fields += f"""-f "{comb.name}|{comb.hp_str()}
{slots}" """

</drac2>
-title "Calling all Allies!"
{{fields}}
