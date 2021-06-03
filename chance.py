embed
<drac2>
args = argparse(&ARGS&)
dc = int(args.last("dc", 10))
bonus = int(args.last("b", 0))
target = dc - bonus - 1
probability = (20 - target) * 5 if target > 0 and target < 21 else 100 if target < 1 else 0
has_adv = "adv" in args and "dis" not in args
has_dis = "dis" in args and "adv" not in args
percentage = floor(probability + ((100 - probability) * probability)/100 if has_adv else probability*probability/100 if has_dis else probability)
</drac2>
-title "What are the chances?"
-f "Meta|**DC:** {{dc}}
**Bonus:** {{"+" if bonus >= 0 else ""}}{{bonus}}
**Modifier:** {{"advantage" if has_adv else "disadvantage" if has_dis else "none"}}"
-f "Probability of Success|{{percentage}}%{{f" ({probability}% unmodified)" if has_adv or has_dis else ""}}"
-footer "!chance"
-color <color>
