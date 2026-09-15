# Borrowed Face

A three-page collage inspired by Tony Oursler's _template/variant/friend/stranger_. Facial features are movable nodes: the viewer changes the portrait by moving the images, and connecting lines follow. Links between pages are separate from dragging.

## Composition

| Page                       | Grid                 | Arrangement                                                                             |
| -------------------------- | -------------------- | --------------------------------------------------------------------------------------- |
| Face — `index.html`        | 12 columns × 16 rows | A large cutout portrait, smaller witnesses, and seven features layered across the face. |
| Fragments — `nodes.html`   | 8 columns × 14 rows  | An almost-absent face with oversized eyes and mouths separated across a dark field.     |
| Stranger — `mismatch.html` | 10 columns × 15 rows | Two overlapping portraits share a set of incompatible features.                         |

Each page has ten photographic image elements: three portraits and seven distinct feature crops. Crops repeat source photographs deliberately, so eyes, nose, and mouth can be separated and recombined. All images have descriptive alt text and source links in the page footer. Text includes a title, a short poem, an instruction, a margin note, and an afterword. All content is in English.

The three HTML documents contain all content and navigation. CSS defines the page grids, cropping, typography, color, and mobile layouts. JavaScript handles pointer/keyboard movement, the connecting SVG lines, rearranging, and resetting. Without JavaScript the static collage and links remain available. There are no external runtime dependencies, camera access, or face recognition.

## Sources

- Reference: [Tony Oursler, template/variant/friend/stranger, Lisson Gallery, 2015](https://www.lissongallery.com/artists/tony-oursler/artworks/template-varient-friend-stranger?image_id=8835).
- Context: [Lisson Gallery exhibition description](https://www.lissongallery.com/exhibitions/tony-oursler--5).
- `herschel.jpg`: [Julia Margaret Cameron, Sir John Herschel, 1867](https://commons.wikimedia.org/wiki/File:Sir_John_Herschel,_by_Julia_Margaret_Cameron.jpg).
- `bernhardt.jpg`: [Nadar, Sarah Bernhardt, c. 1864](https://commons.wikimedia.org/wiki/File:Sarah_Bernhardt,_par_Nadar,_1864.jpg).
- `thompson.jpg`: [Dorothea Lange, Migrant Mother, 1936](https://commons.wikimedia.org/wiki/File:Lange-MigrantMother.jpg).

The photographs are public-domain sources as described on their Commons pages. Source files are hosted locally; cropping and tinting are applied in CSS. The original Oursler artwork photographs are references and are not reproduced as website assets. Node graphics, layout, copy, and implementation were developed with OpenAI Codex. No AI-generated photographs are used.

## Before course submission

Add photographs or other media made by the student to meet the requirement for a mixture of self-created and found media. The current photographs are all found media. Ten image elements per page are supplied, but they are crops of three original photographs; confirm with the instructor if ten separate source photographs are expected. Replace selected portraits/crops and update the source credits when personal media is ready.
