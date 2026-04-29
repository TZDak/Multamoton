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

## Internal Grid Selection

Cells should render as circular markers regardless of the internal grid. A cell
may participate in multiple universe-local neighborhoods, so the visual cell
shape should not reveal a single grid shape or neighborhood orientation.

The `Internal grid` control in `Hex_Multomaton.html` selects the computational
lattice used for cell-center placement, distance scoring, universe basis search,
and picking. Implemented options:

- `hexagonal lattice`: axial hex coordinates rendered in hex projection.
- `triangular lattice`: alternating triangular-cell centers rendered from
  triangle centroids, with the same universe-local square Life basis search
  layered on top.
- `square lattice`: ordinary integer grid coordinates rendered in square
  projection, but still with circular cell markers.
- `rhombic lattice`: each point-top hex cell is divided radially into three
  rhombi. The x-address modulo three selects the top, lower-left, or lower-right
  rhombus inside the composite hexagon, and cell centers are placed at the
  centroids of those rhombi.

More exotic deltoidal or nonperiodic tilings remain future possibilities.

The original square-grid version remains preserved in `Sq_Multomaton.html`.

For the first draft, the `Grid radius` control creates a rectangular backing
range of `(2R + 1) x (2R + 1)` axial addresses. This is still an implementation
compromise rather than a true finite hexagonal disk, but it presents the size in
terms of radius instead of square-grid width and height.

Universe count, rotated geometry, and universe color influence are separate
controls:

- `Universes` controls the number of universe masks/lanes.
- `1 / saved` switches between one universe and the last non-one universe count.
- `Different rotated geometry per universe` controls whether universes get
  unique rotated/spaced basis geometry or share the same basis as a deliberate
  isolation/test mode.
- `Universe color differentiation` controls universe-tinted seed and birth color
  bias, so bit slicing can be tested while preserving multiverse geometry.

## Future Rule-Neighborhood Families

Possible future rule-level neighborhood families should be added one at a time
and tested separately:

- Square Moore neighborhood.
- Square Von Neumann neighborhood.
- Triangular Von Neumann-style neighborhood.
- Hexagonal Moore-like neighborhood.
- Hexagonal nearest-neighbor neighborhood.
- Extended-radius versions of the above.

These should be treated as rule geometry choices, distinct from the internal
grid/lattice choice.
