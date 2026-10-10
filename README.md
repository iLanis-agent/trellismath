# Trellis math

Trellis and espalier planning for the vines already in the ground. A static site with three calculators:

- **Slat grid** - trellis dimensions become slat counts, the real gap and lumber meters.
- **Twine grid** - the same grid becomes line counts and twine meters with knot allowance.
- **Espalier wire** - wall dimensions become wire rows, vine eyes and tensioned wire meters.

Live site: https://ilanis-agent.github.io/trellismath/

## Labeled norms

Labeled garden-build references, not rules:

- Slat grids read well at about 15 cm spacing; the real gap is the width divided between the slats.
- Twine grids use the same squares, with about 10% extra for knots and tie-offs.
- Espalier wires run about 40 cm apart up the wall, anchored about every 60 cm, with about 5% extra for tensioning.

## Layout

- `engine.js` - pure arithmetic and text rendering, shared by the page and the tests.
- `index.html` - landing page. `app.html` - the calculators.
- `oracle.py` - independent Python mirror of the engine's exact float operations.
- `expected.json` - 36 oracle-generated cases. `test.js` - runs every case against the engine plus render checks.

## Tests

```
python3 oracle.py   # regenerate expected.json
node test.js        # 108 checks, 0 failures
```
