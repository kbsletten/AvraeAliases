embed
<drac2>
PHB_ARCH = ["Hunter", "Beast Master"]
XGTE_ARCH = ["Gloom Stalker", "Horizon Walker", "Monster Slayer"]
TCOE_ARCH = ["Fey Wanderer", "Swarm Keeper"]

char = character()
name = char.name if char else name
ranger_level = char.levels.get("Ranger") if char else 0
ranger_subclass = load_json(char.cvars["subclass"])["RangerLevel"] if char and "subclass" in char.cvars else ""

title = "[name] is a Ranger".replace("[name]", name)
if ranger_level < 1:
  title = title.replace("is a", "is not a")

fields = f"""-f "Ranger Level|{ranger_level}|inline" """

if ranger_level >= 3 and ranger_subclass in (PHB_ARCH + XGTE_ARCH + TCOE_ARCH):
  fields += f"""-f "Ranger Archetype|{ranger_subclass}|inline" """

if ranger_level >= 3:
  fields += f"""-f "Primeval Awareness `!prim [-l LEVEL]`|You can use your action and expend one ranger spell slot to focus your awareness on the region around you. For 1 minute per level of the spell slot you expend, you can sense whether the following types of creatures are present within 1 mile of you (or within up to 6 miles if you are in your favored terrain): aberrations, celestials, dragons, elementals, fey, fiends, and undead. This feature doesn’t reveal the creatures’ location or number." """

</drac2>
-title "{{title}}"
{{fields}}
-footer "Ranger | PHB 89"
-color <color> -thumb <image>