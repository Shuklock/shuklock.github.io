# Shardlock Idle art

Every sprite is a PNG strip in this folder: frames side by side, all the same size, transparent background, drawn facing right. The game flips enemies to face left. `ART` in index.html says how many frames a strip has and how fast it plays; a `mob_*.png` with no entry is treated as 2 frames at 4 fps.

One pixel size for the whole scene (2–5 screen pixels per sprite pixel, from the stage height), so size things relative to each other in the source:

- Warlock: 20×29. Pets: 12–18 px wide, 10–22 tall. Regular enemies: 16–28 tall. Zone bosses: 36–48 tall (the game also scales elites ×1.5).
- Feet on the bottom row. Horizontal centre is the sprite centre.
- Two idle frames is enough for anything that stands still; hits and deaths are done by the engine (flash, squash, fade).

Names the engine looks for:

- `warlock.png`, `warlock_channel.png`
- `pet_imp.png`, `pet_vw.png`, `pet_succ.png`, `pet_felh.png`, `pet_inf.png`, `pet_doom.png`
- `mob_<slug>.png` where slug is the enemy name lower-cased with non-letters as `_`: `mob_kobold_miner.png`, `mob_edwin_vancleef.png`, `mob_ragnaros.png`

Palette (16 colours, plus transparent). Fel green is the only bright colour; keep it for flames, eyes and glow.

| key | hex | use |
|---|---|---|
| K | #0b0912 | outline |
| N | #1a1433 | darkest navy |
| P | #2d2459 | navy |
| V | #4a3a8a | violet |
| L | #7b5fd6 | lilac highlight |
| G | #2fff6a | fel green |
| g | #1b8a3c | fel dark |
| Y | #c9ff8a | fel bright |
| R | #7a2e1e | robe shadow |
| r | #a8472a | robe |
| o | #d9733a | orange / imp |
| B | #e8d9b0 | bone |
| S | #8a8fa8 | steel |
| s | #555a70 | steel dark |
| E | #ff4d4d | red eye |
| b | #4878ff | blue |

`mk.py` (repo root `tools/`) draws the first set from text grids using these keys. Edit a grid, run it, and the PNGs are regenerated. Replace any PNG with hand-drawn art at any time; the engine only cares about the strip layout.

## Backdrops

One painted scene per place, `art/bg_<key>.png` (jpg also works). The engine shows it from the top of the stage down to the horizon, scaled to cover the width with the bottom edge on the horizon line, and draws its own floor plane under it. So the bottom of the picture should be plain ground with nothing important in the lowest 15%.

Keys: durotar, tirisfal, westfall, barrens, duskwood, stranglethorn, tanaris, searing_gorge, blackrock, winterspring, molten_core, karazhan, dg_dm, dg_sfk, dg_gnom, dg_sm, dg_zf, dg_brd, dg_ubrs.

Which one shows: a zone's first two targets use its first place, the last two and the elite use the second. Size 1024×480 or wider is plenty; the engine pixel-scales it.
