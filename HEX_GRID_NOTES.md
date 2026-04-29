# Hex-Grid Variant Notes

The current `ca_multiverse.html` / `Sq_Multomaton.html` version is the square-grid
baseline. The planned hex-grid fork should keep square-grid Life-style rules as
much as possible while changing how cells are displayed and how rotated universes
choose their lattice basis.

## Working Intuition

On a square grid, many rotated universes can still land on neighborhoods whose
virtual cell dimensions read as square. On a hexagonal lattice, a perfectly square
virtual cell is probably not possible at most angles, so the radius search should
optimize two goals:

1. Keep each universe's neighbor radius as close as possible to the others.
2. Keep the projected virtual cell dimensions as close to square as possible.

That means the hex variant probably needs a score-based search rather than the
current first-collision-free-radius search.

## Likely Implementation Split

- Preserve `Sq_Multomaton.html` as the square-grid reference.
- Add a hex version after the geometry helpers are isolated enough to compare.
- Separate logical cell coordinates from display coordinates.
- Keep Life-like rule counting over generated neighbor offsets.
- Let the renderer map logical coordinates to a hex lattice.
- Change seed projection to use the selected universe's best two basis vectors.

## Open Geometry Questions

- Whether the logical backing array stays rectangular with odd/even row hex
  projection, or moves to axial/cube coordinates internally.
- Whether wrap modes should remain square/rectangular, become axial torus-like,
  or become selectable.
- How to score "as square as possible" for each universe: edge-length ratio,
  angle closeness to 90 degrees, area consistency, or a weighted combination.
