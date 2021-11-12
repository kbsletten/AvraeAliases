embed
<drac2>
init = combat()
config = load_json(init.get_metadata("skillChallenge")) if init and init.get_metadata("skillChallenge") else { "dc": 13, "goalSuccess": 6, "goalFailure": 3, "success": 0, "failure": 0, "log": [] }
</drac2>
-title "Skill Challenge"
-f "DC|{{config["dc"]}}|inline"
-f "Successes|{{config["success"]}}/{{config["goalSuccess"] or "None"}}|inline"
-f "Failures|{{config["failure"]}}/{{config["goalFailure"] or "None"}}|inline"
{{"\n".join(f"""-f "{log["name"]}|{log["roll"]}; {log["result"]}" """ for log in config["log"])}}
-footer "!challenge | kbsletten#5710"
-color <color>
