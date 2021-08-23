attack import
<drac2>
argv = &ARGS&
args = argparse(argv)

name = args.last("name", "Mysterious Weapon")

ABILITIES = ["str", "dex", "con", "int", "wis", "cha"]

mod = args.last("mod")
pro = "+proficiencyBonus" if "nopro" not in argv else ""

to_hit = "+".join(args.get("b") + ([mod + pro] if mod else []))
damage = "+".join(args.get("d") + ([f"{{{mod}}}"] if mod else []))

save_ability = args.last("save") if args.last("save") in ABILITIES else None
save_dc = args.last("dc") if args.last("dc") else "8+spell+proficiencyBonus" if save_ability else None

effect = args.last("effect").split("|") if args.last("effect") else None

ccs = [(args.last(f"cc{i}"), args.last(f"ccnum{i}", "1"), f"ccovf{i}" in argv, args.last(f"ccerr{i}", "warn")) for i in [""] + [str(x) for x in range(1, 11)]]
resource = args.last("resource")

json = []

effect_json = []
if effect:
  effect_name = effect[0]
  effect_argv = effect[1] if len(effect) > 1 else ""
  effect_args = argparse(effect_argv)
  effect_duration = effect_args.last("duration", "-1")
  effect_end = "end" in effect_args
  effect_desc = effect_args.last("desc")
  
  effect_json = [
    {
      "type": "ieffect",
      "name": effect_name,
      "duration": effect_duration,
      "effects": effect_argv,
      "end": effect_end,
      "desc": effect_desc
    }
  ]

check_json = []
resource_json = []
if resource:
  check_json = [
    {
      "type": "counter",
      "counter": resource,
      "amount": "0",
      "errorBehaviour": None
    }
  ]
  resource_json = [
    {
      "type": "condition",
      "condition": "lastCounterRemaining > 1",
      "onTrue":
      [
        {
          "type": "roll",
          "dice": "1d{lastCounterRemaining*2}",
          "name": "Resource"
        }
      ],
      "onFalse": [],
      "errorBehaviour": "false"
    },
    {
      "type": "condition",
      "condition": "lastRoll < 2",
      "onTrue":
      [
        {
          "type": "counter",
          "counter": resource,
          "amount": "1",
          "errorBehaviour": "warn"
        },
      ],
      "onFalse": [],
      "errorBehaviour": "true"
    },
  ]
cc_json = [{ "type": "counter", "counter": cc, "amount": ccnum, "allowOverflow": ccovf, "errorBehaviour": ccerr } for cc, ccnum, ccovf, ccerr in ccs if cc]
use_json = resource_json or cc_json

damage_json = [{ "type": "damage", "damage": damage }] if damage else []
desc_json = [{ "type": "text", "text": args.last("desc") }] if args.last("desc") else []
if to_hit:
  if effect_json and save_ability:
    effect_json = [
      {
        "type": "save",
        "stat": save_ability,
        "fail": effect_json,
        "success": [],
        "dc": save_dc
      }
    ]
  json = check_json + [
    {
      "type": "target",
      "target": "each",
      "effects": use_json + [
        {
          "type": "attack",
          "hit": damage_json + effect_json,
          "miss": [],
          "attackBonus": to_hit
        }
      ]
    }
  ]
elif save_ability and damage:
  json = check_json + use_json + [
    {
      "type": "roll",
      "dice": damage,
      "name": "Damage"
    },
    {
      "type": "target",
      "target": "all",
      "effects": [
        {
          "type": "save",
          "stat": save_ability,
          "fail": [{ "type": "damage", "damage": "{Damage}" }] + effect_json,
          "success": [{ "type": "damage", "damage": "({Damage})/2" }] if "half" in argv else [],
          "dc": save_dc
        }
      ]
    }
  ]
elif save_ability:
  json = use_json + [
    {
      "type": "target",
      "target": "all",
      "effects": [
        {
          "type": "save",
          "stat": save_ability,
          "fail": effect_json,
          "success": [],
          "dc": save_dc
        }
      ]
    }
  ]

json = dump_json({
  "name": name,
  "automation": json + desc_json,
  "_v": 2,
  "proper": "proper" in argv,
  "verb": args.last("verb")
})
</drac2>
{{json}}