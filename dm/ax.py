embed
<drac2>
using(
  util=''
)
argv = &ARGS&
args = argparse(argv)

flavor = util.flavor(args)

hit_expr = "+".join([{ -1: "2d20kl1", 0: "1d20", 1: "2d20kh1" }[args.adv()]] + args.get("b"))
dam_expr = "+".join(args.get("d")) or "0"

fields = ""

init = combat()
targets = [(init.get_combatant(name), args) for name, args in [target_expr.partition("|") for target_expr in args.get("t")] if init.get_combatant(name)]

if not targets:
  hit_roll = vroll(hit_expr)
  is_crit = hit_roll.result.crit == 1
  is_miss = hit_roll.result.crit == 2
  dam_roll = None if is_miss else vroll(dam_expr, multiply=2 if is_crit else 1)
  meta = {
    "To Hit": hit_roll,
    "Damage": dam_roll
  }
  mfields = "\n".join(f"**{name}**: {value}" for name, value in meta.items() if value)
  fields += f"""-f "Meta|{mfields}
{"**Miss!**" if is_miss else ""}" """

if args.last("desc"):
  fields += f"""-f "Effect|{args.last("desc")}" """

</drac2>
-title "{{flavor["title"]}}"
{{fields}}
-footer "!ax | kbsletten#5710"