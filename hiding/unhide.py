embed
<drac2>
argv = &ARGS&
args = argparse(argv)

init = combat()

target = None
if init:
  target = init.get_combatant(args.last("t")) if args.last("t") else init.me or init.current

name = target.name if target else name

if target:
  for effect in target.effects:
    if not effect.name.startswith("Hidden ("):
      continue
    target.remove_effect(effect.name)

</drac2>
-title "{{name}} is Revealed!"
-footer "!unhide | kbsletten#5710"
-color <color> {{"-thumb <image>" if not target or init and init.me and init.me.id == target.id else ""}}
