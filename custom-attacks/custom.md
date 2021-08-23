Create a custom attack.

-b <bonus> - to hit bonus (uses variables like `strengthMod` and `proficiencyBonus`)
-cc <counter> - a custom counter to decrement by `ccnum` when the attack is used
-ccerr <warn/error> - change the error behavior of the `cc` (default `warn`)
-ccnum <number> - the amount to decrement the `cc` by
ccovf - allow the `cc` to overflow (or underflow) its max and min values
-d <damage> - damage (uses variables like `strengthMod` and `proficiencyBonus`)
-dc <save DC> - difficulty class of the save
-effect <"[name]|[effects]"> - applies the specified effect on a hit or failed save
half - deal half damage on save
-mod <modifier> - the modifier to use for attack and damage rolls (uses variables like `strengthMod+1`)
-name <name> - the name of the attack
nopro - don't add the proficiency bonus (used with the `mod` option)
proper - the attack is a proper noun
-save <str/dex/con/int/wis/cha> - the ability to make the save with (shortened like `str`)
-verb <verb> - the verb to use with the attack


**Add a weapon attack**
`!custom -name "Longsword+1" -mod "strengthMod+1" -d "1d8[slashing]"`

**Add a finesse attack**
`!custom -name "Rapier+2" -mod "max(strengthMod, dexterityMod)+2" -d "1d8[piercing]"`

**Add a save on hit**
`!custom -name "Walloping Maul" -mod "strengthMod" -d "2d6" -save str -dc 10 -effect "Prone"`

**Add a CC usage**
`!custom -name "Breath Weapon" -cc "Breath Weapon" -d "{5 if level > 15 else 4 if level > 10 else 3 if level > 6 else 2}d6[fire]" -save dex -dc "8+constitutionMod+proficiencyBonus" half`