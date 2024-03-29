Manage custom attacks and abilities for players and monsters.

**Result Syntax**
These can be used on any of `hit`, `miss`, `crit`, `save`, `fail` or `fail5`
`damage <damage dice>` - deals damage to the creature
`effect <effect name>` - adds an effect

**Attack Syntax**
`attack <to hit>` - adds an attack with a to-hit bonus
`hit` - specifies what to do when the attack hits
`miss` - specifies what to do if the attack misses (e.g. Acid Arrow)
`crit` - specifies what to do if the attack is a critical hit

 **Save Syntax**
`save <ability> <dc>` - forces the targeted creature to make a save, if you use `attack` and `save` together, only creatures who are hit will save
`fail5` - specifies what to do if the target fails by 5 or more
`fail` - specifies what to do if the target fails
`pass` - specifies what to do if the target passes
 - `half` - deals half the damage the creature would have taken

**Examples**
Wolf Bite - `!custom_attack test attack 4 hit damage 2d4+2[piercing] save str 11 fail effect Prone -t TARGET`

Dragonborn Breath - `!custom_attack test save dex 11 fail damage 2d6[fire] pass half -t TARGET`

Quasit Claw - `!custom_attack test attack 4 hit damage 1d4+3[piercing] save con 10 fail damage 2d4[poison] effect Poisoned -t TARGET`
