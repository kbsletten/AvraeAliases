{{argv=&ARGS&}}{{op=argv[0] if argv else ""}}{{"multiline" if op == "run" else "echo"}}
{{cmds=get("dmCommands", "!br\n!br\n!br")}}
{{cmds="\n".join([cmds, " ".join('"' + arg.replace('"', '\\"') + '"' if " " in arg else arg for arg in argv[1:])]).replace("\n\n", "\n") if op == "add" else cmds}}
{{cmds="" if op == "clear" else cmds}}
{{_=set_uvar("dmCommands", cmds)}}
{{cmds if "run" else cmds.replace('"', '\\"') or "(no output)"}}