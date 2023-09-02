# RLCraftVillagers v1.01

This is a **Command Line Interface (CLI)** organization tool used for tracking Librarians and their Enchants in the
Minecraft modpack **RLCraft**.

## Game Mechanics

**Librarians** are a type of **villager**, which is a type of mob (NPC) in **Minecraft**. Villagers offer **trades**
that allow players to exchange items with them. The primary currency used is **Emeralds**. Different types of villagers
offer different possible trades, and within a type, each individual villager entity has some **randomization**. Prices
and sometimes specific items can vary greatly. RLCraft is based off of Minecraft version 1.12.2 and uses an older system
of villagers compared to the most recent Minecraft versions.

Librarians are guaranteed exactly 3 trades for an **Enchanted Book**. This is an item associated with a particular
**Enchantment** (or **Enchant** for short), a special modifier that can be applied to compatible items, that enhances
various aspects of them
(ranging anywhere from efficacy of the item, to longevity of it, to special added effects). Each Enchanted Book slot
offers a one-time-randomly-selected Enchantment, of a pool of around ~200 unique enchantments (RLCraft adds a plethora).
This Enchantment can be traded for "indefinitely" (some RNG). Including the different **Enchantment Levels** that
Enchantments can come with (which affect the efficacy of the Enchantment; possible levels depend on the specific type of
Enchant), this number jumps to 600+. The price of an Enchanted Book in Emeralds is a random value in the inclusive
overall range of **5-64** with sub-ranges based on the specific level (ie level 1 Enchants go for 5-19) (a normal book
is also required for the Enchant to be applied to)

Two of the same Enchant type & level can be combined to produce a single copy of the next level of the Enchant. For
example, Sharpness 3 + Sharpness 3 = Sharpness 4. In ordinary Minecraft, this becomes inefficient very quickly due to
how repeated uses of an **Anvil** (the tool used for applying Enchanted Books to items or combining them)
works. The mechanics behind that are beyond the scope of this description, but resources on Anvil Cost are widely
available. In short, anvils charge an XP cost to use, and the cost of applying an Enchant (or any item) increases based
on how many times that item has been through an anvil. Combining books, especially from a low level to a high level one,
involves many anvil uses. This can result in a single usage of the anvil with the item costing several times what it
would have if combinations were not necessary (also affecting any further applications of Enchants). At a certain cost,
the Enchantment will no longer be allowed to be applied. In RLCraft, this is not an issue, as you can run a combined
Enchanted Book through a Disenchantment Table to reset its anvil cost while preserving the level (also the limit based
on cost reached is removed).

For more resources on 1.12.2 villagers, I would recommend an archive of the old Minecraft Gamepedia
page: https://web.archive.org/web/20190106161728/https://minecraft.gamepedia.com/Trading

## Purpose

An effective strategy for collecting important Enchantments is collecting a vast number of Librarians. As there are so
many possible Enchants to get, you can easily wind up going through a ludicrous number of Librarians in an attempt to
find sources for the Enchants you are looking for.

The purpose of this tool is to help track Librarians and their Enchanted Books. Specifically, there are two aspects of
each Enchant type it focuses on: the **highest level** possessed of it, and the **best rate** available for it.

**Rate** refers to the proportional cost between Enchant level and Emeralds. This is significant because perhaps you
have Sharpness 5 available for 64 Emeralds, and Sharpness 3 available for 11 Emeralds. For a total cost of 44 Emeralds,
you could buy four Sharpness 3 enchants and combine them up to Sharpness 5, which may be more desirable (depending on
which is more scarce between XP and Emeralds).

## Commands

* Note: the game uses Roman numerals, however this program uses decimal numbers (1, 2, 3, etc.)
* A comma followed by a space is often used as a delimiter in parsing commands

### Quick Reference

|  Command  | Usage                                             | Example                                                       |
|:---------:|:--------------------------------------------------|:--------------------------------------------------------------|
|   list    | list                                              | list                                                          |
|   find    | find \<enchant_name>                              | find ash destroyer                                            |
|   check   | check \<cost> \<enchant_name>, ..                 | check 27 critical strike 2                                    |
| villagers | villagers                                         | villagers                                                     |
|    add    | add \<villager_name>, \<cost> \<enchant_name>, .. | add bob, 10 infinity, 36 supreme sharpness 5, 17 protection 3 |
|  rename   | rename <villager_name>, <new_villager_name>       | rename bob, jim                                               |
|  remove   | remove \<villager_name>                           | remove jim                                                    |  

### list

* Lists the highest level of each enchant type owned alongside its cost and villager in alphabetical order. If the best
  rate for that enchant type is not the highest-level trade, will also display information for the best rate trade.

### find \<enchant_name>

* Searches for an owned enchant of the given name and prints its information (highest level, cost, villager, and best
  rate if applicable)
* If an exact match is not found for the given name, will search for an enchant starting with the given string

### check \<cost> \<enchant_name>, ..

* Takes any number of comma-separated costs & enchant names. For each pair, checks against the current inventory to see
  if that enchant trade would be new or beat any of the current bests in terms of level and/or rate
* Each enchant is printed in two sections— the **best level** evaluation and **best rate** evaluation. For quick
  reference, there are three types of indicators printed (or, with a lack of a print) at the start of each:
    * (none) — Given trade does not beat any current values
    * ! — Given trade is a new best for the corresponding category
    * ~! — Given trade ties current best in its corresponding category but is more efficient (ie for best level it does
      not beat the level but it's a better rate for the same level)
* When comparing rates, a **scaled value** will also be given when applicable, displaying how many Emeralds the highest level available of that enchant would cost for each rate

### villagers

* Lists every villager and what bests it contributes (ie what enchants it has that are the best level for that enchant, the best rate for it, or both), starting with those that have none. Sorted in order of villager creation

### add \<villager_name>, \<cost> \<enchant_name>, ..

* Adds a villager with the corresponding data. Make sure that exactly all **three** enchants are provided
* Also runs a check for every enchant added with the same style as the check command as described above
* A notification will be given after updating the data if any villager(s) no longer contribute any best values

### rename <villager_name>, <new_villager_name>

* Renames the villager and updates the matching data accordingly

### remove <villager_name>

* Deletes the villager from the database and updates the data accordingly