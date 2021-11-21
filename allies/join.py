multiline {{C=character()}}{{A=load_json(C.cvars["ally"] if "ally" in C.cvars else "{}")}}{{N=A["name"] if "name" in A else f"""{C.name}'s {A["type"]} ally"""}}{{I=combat()}}{{M=I.me}}{{G=(M.group if M else None) or ctx.author.display_name}}
{{f"""!i join -group "{G}" %*% """ if not M else f"""!i opt "{M.name}" -group "{G}" """ if M.group != G else ""}}
!init madd "{{A["type"]}}" -h False -name "{{N}}" -group "{{G}}" %*%
