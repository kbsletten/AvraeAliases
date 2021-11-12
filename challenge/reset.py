embed
<drac2>
argv = &ARGS&
args = argparse(argv)

init = combat()

config = load_json(init.get_metadata("skillChallenge")) if init and init.get_metadata("skillChallenge") else { "dc": 13, "goalSuccess": 6, "goalFailure": 3, "success": 0, "failure": 0, "log": [] }
dc = int(args.last("dc", config["dc"]))
success = int(args.last("success", config["goalSuccess"]))
failure = int(args.last("failure", config["goalFailure"]))
config = { "dc": dc, "goalSuccess": success, "goalFailure": failure, "success": 0, "failure": 0, "log": [] }

if init:
  init.set_metadata("skillChallenge", dump_json(config))
</drac2>
-title "Resetting Skill Challenge!"
-f "DC|{{config["dc"]}}|inline"
-f "Successes|{{config["success"]}}/{{config["goalSuccess"] or "None"}}|inline"
-f "Failures|{{config["failure"]}}/{{config["goalFailure"] or "None"}}|inline"
-footer "!challenge reset | kbsletten#5710"
-color <color>
