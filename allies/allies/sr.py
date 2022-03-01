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
    old_hp = comb.hp
    comb.set_hp(comb.max_hp)
    fields += f"""-f "{comb.name}|{comb.hp_str()} (+{comb.hp - old_hp})" """

</drac2>
-title "Allies take a short rest!"
{{fields}}
