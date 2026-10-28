# Shardlock Idle art

The sprites are Gemini (and now Midjourney) pixel art. Gemini paints each one on a flat magenta background, working from WoW screenshots and the Felheart warlock reference. `tools/grid.py` then snaps the render to its pixel grid. Black outlines stay on. Anything with no Gemini version yet gets a placeholder from `tools/mk.py`.

| sprite | source | ART entry |
|---|---|---|
| `warlock.png` | Gemini | `frames:1, scale:.36` |
| `pet_imp.png` | Gemini | `frames:1, scale:.27` |
| `pet_vw.png` | Gemini | `frames:1, scale:.38` |
| `pet_succ.png` | Gemini | `frames:1, scale:.32` |
| `pet_felh.png` | Midjourney | `frames:1, scale:.42` |
| `pet_inf.png`, `pet_doom.png` | mk.py placeholder | `frames:2, fps:2, scale:1.2–1.3` |
| `mob_scorpid.png` | mk.py placeholder | none (mob default) |

## How the engine reads a sprite

- Each file is a PNG strip: frames side by side, all the same size, on a transparent background.
- Sprites face right. Enemies are flipped to face left; the warlock and pets are drawn as they are.
- `ART` in index.html gives each sprite's `frames`, `fps` and `scale`. A `mob_*.png` with no entry counts as 2 frames at 4 fps with scale 1.
- On-screen size is (sprite height × `scale`) × the scene pixel size (2–5, from the stage height). For example, the warlock is 151 px × .36 ≈ 54 units tall. Choose `scale` to place a new sprite against that: imp ≈ 36, voidwalker ≈ 52, succubus ≈ 44.
- Put the feet on the bottom row and centre the figure horizontally.
- The Shadow Bolt and Drain Soul beams start from fixed points on the warlock sprite: the hand at (−14, 90) and the staff tip at (47, 129), in sprite pixels from the feet centre. A new warlock render has to move these numbers in `drawScene` too.
- Hits, deaths and bobbing are done by the engine. A still is enough.

Names the engine looks for:

- `warlock.png`, plus an optional `warlock_channel.png`. The channel sprite needs the same size and anchors as `warlock.png` and its own ART entry, so leave it out until a Gemini channel pose exists.
- `pet_imp.png`, `pet_vw.png`, `pet_succ.png`, `pet_felh.png`, `pet_inf.png`, `pet_doom.png`
- `mob_<slug>.png`, where the slug is the enemy name lower-cased with non-letters turned into `_`. Examples: `mob_kobold_miner.png`, `mob_edwin_vancleef.png`, `mob_ragnaros.png`. A missing one draws the built-in silhouette for that mob family.

## Adding or replacing a sprite

1. In Gemini, make a full-body pixel-art still on solid magenta (#ff00ff) with no ground shadow, facing right. If it comes out facing left, use `--flip` in step 2.
2. Run `python3 tools/grid.py render.jpg pet_felh --preview`. This writes `drain-soul/art/pet_felh.png` and a 6× look in `tools/preview/` (not committed). If the grid is detected wrong, pass `--cell N`. For a render with no clean grid, `tools/clean.py render.jpg pet_felh --height 48` makes a quantized version instead.
3. Set the sprite's `ART` entry to `{frames:1,fps:1,scale:S}`, using the height guide above.
4. If you replaced `warlock.png` or `bg_durotar.jpg`, run `python3 tools/inline.py` so the base64 copies in index.html match. `--check` only reports.

## Placeholders (`tools/mk.py`)

`mk.py` draws 2-frame sprites from text grids for anything still waiting on Gemini art. It never writes the Gemini sprites. By default it also skips any PNG that already exists, so a Gemini file you drop in stays put.

- `python3 tools/mk.py` writes only the placeholders that are missing.
- `python3 tools/mk.py pet_inf --force` redraws one.
- `--preview` writes a contact sheet to `tools/preview/`.

Once a placeholder has a Gemini version, delete its grid from mk.py.

## Backdrops

One painted scene per place, `art/bg_<key>.png` (jpg also works). The engine shows it from the top of the stage down to the horizon, scaled to cover the width with the bottom edge on the horizon line, and draws its own floor plane under it. So the bottom of the picture should be plain ground with nothing important in the lowest 15%.

Keys: durotar, tirisfal, westfall, barrens, duskwood, stranglethorn, tanaris, searing_gorge, blackrock, winterspring, molten_core, karazhan, dg_dm, dg_sfk, dg_gnom, dg_sm, dg_zf, dg_brd, dg_ubrs.

Which one shows: a zone's first two targets use its first place, the last two and the elite use the second. Size 1024×480 or wider is plenty; the engine pixel-scales it.
