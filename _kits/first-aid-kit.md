---
title: First Aid Kit
order: 1
status: Released
version: ""
tagline: Potions, bandages and cures in one satchel, so they stop eating your action bars.
icon: ""
curseforge: https://www.curseforge.com/wow/addons/first-aid-kit
command: /fak
blocks:
  - type: features
    heading: What's in the kit
    items:
      - title: A ring of supplies
        text: Click the kit to fan out its slots and click again to tuck them away. Mana (or Thistle Tea or Rage Potion), healing potion and bandage sit above; tourniquet, anti-venom and poultice sit below.
      - title: Two slots for anything
        text: The left and right slots take any consumable you like, such as food, elixirs or Free Action Potions. Drag an item onto one to assign it.
      - title: Picks the right version
        text: Each slot uses the version of an item you chose, and moves to the next one when it runs out.
      - title: Cure alerts
        text: When a poison, disease or bleed you can cure lands on you, its slot glows, and pops out of the kit if it's closed. Poison alerts work in combat; the rest wait until combat ends.
      - title: First Aid button
        text: A button under the kit opens your First Aid profession window for crafting.
  - type: text
    heading: Setting it up
    body: |-
      Right-click a slot to choose what goes in it, or shift-right-click to keep that slot showing while the kit is closed. You can resize the kit and set a keybind for every slot, plus a Cure key, in **Esc > Options > AddOns** or with `/fak`. `/fak help` lists the other commands.

      By default the kit opens when a fight starts and closes afterward. Tourniquets and poultices grey out in combat; anti-venom stays usable.
---
