embed
<drac2>
complications = [
  "The item is a fake, planted by an enemy.",
  "The item is stolen by the party’s enemies.",
  "The item is cursed by a god.",
  "The item’s original owner will kill to reclaim it; the party’s enemies spread news of its sale.",
  "The item is at the center of a dark prophecy.",
  "The seller is murdered before the sale.",
  "The seller is a devil looking to make a bargain.",
  "The item is the key to freeing an evil entity.",
  "A third party bids on the item, doubling its price.",
  "The item is an enslaved, intelligent entity.",
  "The item is tied to a cult.",
  "The party’s enemies spread rumors that the item is an artifact of evil."
]

complication = f"""||{complications[vroll(f"1d{len(complications)}").total - 1]}||"""
</drac2>
-title "Buying a Magic Item: Complication"
-f "Complication|{{complication}}"
-footer "!buy complication | kbsletten#5710"
-color <color> -thumb <image>
