# Actor / PwC shared visualization — mobile test matrix

Source-level acceptance matrix for the shared visualization introduced 19 Aug 2026.

| Viewport class | Expected layout |
|---|---|
| >980px | Homepage actor grid retains desktop layout; replica shows 3 actor cards; quote/body uses 2 columns. |
| 761–980px | Homepage actor grid forced to 2 columns; replica actor cards use 2 columns with final card spanning row; quote/body remains readable. |
| <=760px | Homepage actor grid forced to 1 column; replica actor cards 1 column; quote/body 1 column; links wrap/stack. |
| <=390px | Reduced padding/border and quote size; replica width uses 0.5rem side gutters; long relationship labels wrap anywhere. |

No horizontal minimum width is introduced by the shared component. All grid children use min-width:0 or wrapping rules where needed.

This is a source-level responsive verification. It does not substitute for independent rendered-device/browser verification after GitHub Pages propagation.
