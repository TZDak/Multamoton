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

## First Draft

`Hex_Multomaton.html` keeps the rectangular backing array but interprets each
cell address as an axial hex coordinate for display and neighborhood geometry.
Each universe chooses two axial basis vectors by scoring:

- closeness to the requested orientation,
- closeness to a 90 degree rendered angle,
- closeness of rendered x/y basis lengths,
- closeness to the current radius shell.

The Life neighborhood is still square-rule-like: each universe uses eight
offsets derived from the two basis vectors: plus/minus both axes and the four
corner sums/differences.

## Grid Element Selection

The first draft now exposes a `Grid element` rendering control in
`Hex_Multomaton.html`:

- `hexagon`: cells are drawn as hexagonal elements on the axial point lattice.
- `triangle`: cells are drawn as alternating triangular elements on the same
  underlying point lattice.
- `square`: cells are drawn as square markers on the same underlying point
  lattice. This is a visual comparison mode, not the original square-grid app.
- `circle centers`: a neutral reference view that emphasizes the cell centers
  rather than a tiling shape. It is not a separate grid; it is the same
  underlying lattice with the cells rendered as disks.

This is currently a rendering comparison, not a change to the Life rules. The
universe-local x/y axes and eight-neighbor square-rule neighborhoods are still
chosen from the same axial lattice vectors.

## Future Rule-Neighborhood Families

Possible future rule-level neighborhood families should be added one at a time
and tested separately:

- Square Moore neighborhood.
- Square Von Neumann neighborhood.
- Triangular Von Neumann-style neighborhood.
- Hexagonal Moore-like neighborhood.
- Hexagonal nearest-neighbor neighborhood.
- Extended-radius versions of the above.

These should be treated as rule geometry choices, distinct from the visual
`Grid element` rendering control.
