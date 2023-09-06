# !gvar edit 6665acd4-2763-4e51-9e44-f328bfb78a09

def load_homebrew(char = None):
  # {server,user}_homebrew: gvar_id[]
  server_homebrew = load_json(get_svar("homebrew") or "[]")
  user_homebrew = load_json(get_uvar("homebrew") or "[]")
  # character_homebrew: {
  #     [package_name]: { ...package }
  # }
  character_homebrew = load_json((char.cvars["homebrew"] if char and "homebrew" in char.cvars else None) or "{}")

  # global_homebrew: {
  #    [gvar_id]: {
  #        [package_name]: {
  #            ccs: {
  #                [cc_name]: { ...cc }
  #            },
  #            actions: {
  #                [action_name]: { ...action }
  #            }
  #        }
  #    }
  # }
  global_homebrew = {}
  for homebrew in server_homebrew + user_homebrew + character_homebrew.keys():
      if homebrew in global_homebrew:
          continue
      global_homebrew[homebrew] = load_json(get_gvar(homebrew) or "{}")
  
  # (server_homebrew, user_homebrew, character_homebrew)
  available_homebrew = [
    [global_homebrew[gvar_id] for gvar_id in source]
    for source in [server_homebrew, user_homebrew]
  ]
  return tuple(available_homebrew + [character_homebrew])

def homebrew_summary(homebrew):
  cc_count = len(homebrew["ccs"]) if "ccs" in homebrew else 0
  action_count = len(homebrew["actions"]) if "actions" in homebrew else 0

  details = [
    x
    for x in [
      f"""{cc_count} consumable{"" if cc_count == 1 else "s"}""" if cc_count else None,
      f"""{action_count} action{"" if action_count == 1 else "s"}""" if action_count else None
    ]
    if x
  ]

  if not details:
    return ""
  
  return f"""({", ".join(details)})"""