{{C=character()}}{{A=load_json(C.cvars["ally"] if "ally" in C.cvars else "{}")}}{{N=A["name"] if "name" in A else f"""{C.name}'s {A["type"]} ally"""}}{{I=combat()}}{{M=I.get_combatant(N) if I else None}}{{f"""init offturncheck "{M.name}" """ if M else f"""monster_check  "{A["type"]}" """}} %1%
{{f"""-title "{N} makes a [cname] check!" """ if not M else ""}}
{{f"""-thumb "{A["image"]}" """ if "image" in A else ""}}
{{"&*&"[len("&1&"):]}}
