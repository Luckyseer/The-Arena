# - Alpha v2.1

 - Added a Health bar to enemies.
 - Added a Day/Night cycle. Events can happen/change depending on the time on the in-game clock.
 + Fixed a few minor bugs.
 * Changed font for damage taken and dealt as well as for critical strikes.
 * Adjusted the size of the font on certain UI elements.
 
# - Alpha v2.2
 + Added the option to select choices during dialogue.
 + Added a Gold icon next to the player's gold count in the inn.
 + Added a menu to select who you want to talk to when using the 'Talk' option.
 + Added an indicator to show whether you have talked to people before or if their dialogue has been updated.
 + At night the music will stop playing and be replaced with night time ambiance.

# - Alpha v2.3
 + Added an Event manager to make cutscenes and stuff more manageable.
 + Added a cutscene for the first floor boss.
 * Fixed a bug with loading games after a defeat.

# - Alpha v2.4
 + Added a fading out effect for scene transitions.
 + Added a small 'animation' for textboxes.
 + Uses json files to store enemy and item data now.
 + Changed the damage formula
 + Added the shop! and weapons! and items!(ok no consumables yet working on that later.)
 
 NOTE: currently as soon as you buy the item, you will equip it,I'll change it later on so that you can equip your desired equipment
       through the status screen.	
 + Added multiple weapons, armour and accessories which can be bought in the shop.
 * Minor bug fixes.
 * Changed the stats for some of the monsters(Still not final).
 * The 'Fading in' effect should work properly now.
 * Changed formatting to be more PEP-8 compliant(getting there).
# - Alpha v3.0
 + Added the town. (Not implemented)
 + Updated Battle system!
 + Cleaned up a lot of old code.
 + Added descriptions to items in the shop.
 + Added an indicator when there are more items than shown in the shop.
 + Made the player and monster move while attacking just to make it look a bit more lively.
 + Added skills and the fuctionality to easily make more with 'sequences'!
 + Added new warrior skills.
 + Added new status effect "defend" which increases defence.
 + Added status icons to player HUD to indicate the effect.
 + Completely rewrote damage calculation function.
 + Adjusted heights of larger monsters.
 + Now enemies can use skills the same way players can. 
 + You can test the new battle system by typing  in "test" while in the main menu.
# - Alpha v3.1 
 + Added consumables to shops.
 + You can now use consumables in battle.
 + Added new accessories and item effects.
 + You can only buy one of each weapon, armour or accessory now.
 + Added the amount of the consumable in player's inventory in the shop.
 + You can now change your equipment on the status screen.
 + You no longer automatically equip the item after purchase.
# - Alpha v4.0
 + Updated the textbox system. (Some of the old dialogue is broken as a result haven't gotten round to fixing it.)
 + Changed the intro, added some more plot.
 + You no longer gain stats when leveling up. Instead you get stat points that you can spend on your stats as you like. You can spend the points via the status menu.
 + You get a message when you level up after a battle.
 + Fixed an issue when starting a new game after death
 + Fixed issues with the old textbox events, should be working perfectly now.
 + Added mage skills
 + Added debuffs
 + Added Cutscene after defeating first boss
 + Fixed issue of song not updating after victory
# - Alpha v4.1
 + Added a popup message when trying to do things that  you can't do(Not enough gold, no stat points, etc.) 
 + Added elements and weaknesses to enemies
 + Added stat changes to equip screen
 + Added a few monsters to floor 2
 + Added item descriptions to the shop
 + Updated first floor boss moves
# - Alpha v4.2
 + Added a splash screen on startup
 + Added new 'talk' dialogue to floor 2 arena.
# Known issues:
 - Update current song after victory
# TODO:
 - Finish the town.
 - ~~Items in battle.~~ Done
 - ~~Changing equipment in status screen.~~ Done