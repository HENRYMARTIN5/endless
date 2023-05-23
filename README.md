# Endless

A simple modding tool for Dead Cells that allows modification and/or replacement of the game's files.

## Features

- [x] Unpacking and repacking `res.pak` - the container for all the
       game's assets.
- [x] Packaging "bare-minimum" mod packages based on modifications to
       `res.pak`.
- [x] Starting either vanilla or modded Dead Cells with specific mods.
- [ ] More efficient handling of modded launches - binary patching?
- [ ] Game version compatibility checks
- [ ] Mod compatability checks
- [ ] CastleDB diffing/treating different CDB lines as different
       changes and not having every mod be incompatible if it even
       touches CDB

## Installation

1. Clone the repo.
2. `pip install -r requirements.txt`
3. `python endless.py`
4. Follow instructions in-app to setup.

## Making and Packaging Mods

1. First, unpack your game files - select the option in the main menu.
2. Make your changes to the game files - see the below section for things that you can change and add.
3. Package the mod by selecting the option in the menu.
4. Profit?

## Overview of Modding

Things that can be done with modding as of now:

- Custom biomes
- Custom rooms and generation
- Modification of existing mobs (AI scripting not available)
- Modification of existing items (Stats, bonuses, spawn rate, etc.)

For more, see the official Dead Cells modding documentation (which this repo heavily depends on, but still differs from slightly) in `<Your Dead Cells Install>/ModTools/ModsDoc.pdf`.

## License

MIT License. See `LICENSE` for more information.

### Licensing Exemptions

- Motion Twin (and the Dead Cells team) is hereby permitted to use this software and the associated documentation in any way they see fit, without any restrictions.
