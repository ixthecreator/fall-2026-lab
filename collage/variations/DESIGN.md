# Six borrowed faces

Six original web collage compositions combining Tony Oursler's use of facial fragments, flat sculptural heads and projected-image windows with structures studied in real computer vision systems. Each artwork page contains a single collage. Titles, explanations, navigation and credits live in the separate selection page.

These are artistic adaptations, not reproductions of six Oursler works and not functioning recognition systems. No camera, face identification, neural model or identity database is used. The photographs are found archival material; layouts, silhouettes, color treatments and interaction are newly composed with Codex. No AI-generated photographs are used.

## Six layouts

| Version                    | Structural source                                   | Composition                                                                                                                    | What moving a fragment does                                                        |
| -------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| 01 / A face in five places | InsightFace / ArcFace five-point alignment template | Five photographic islands over a pale, incomplete face silhouette; two mouth fragments deliberately belong to different people | Carries its corresponding anchor; the sparse spatial guides stretch                |
| 02 / Borrowed contours     | dlib / iBUG 68-point layout                         | An irregular cobalt head contains gold contour lines, a silver eye, green eye and pink mouth                                   | Eye, nose, brow or mouth contour points follow their image window                  |
| 03 / No single person      | InsightFace 106-point markup                        | Ten tilted photo fragments form a discontinuous face on a dark field; point markers remain unconnected                         | Moves the region's points, breaking the apparent face without inventing mesh edges |
| 04 / A measured stranger   | MediaPipe 468-point canonical mesh                  | A red archival portrait becomes a large photographic head; dense gold topology crosses blue and green image windows            | Assigned feature vertices move; triangles stretch around the displaced patch       |
| 05 / The face looks back   | 468-point base + ten schematic iris points          | Oversized circular eyes dominate a violet face; a narrow nose and small mouth oppose their scale                               | Eye and iris points move with the enlarged eye imagery                             |
| 06 / The face comes apart  | CelebAMask-HQ semantic class scheme                 | Fourteen handmade photographic pieces separate skin, hair, ears, brows, eyes, nose, mouth/lips, neck and clothing              | Regions move independently; no landmark graph is imposed                           |

Version 06 interprets a selection of the 19 classes. It does **not** claim that the dataset divides every face into 19 face-only regions. Background counts as a class; accessories need not appear. The crop shapes are hand-drawn approximations, not segmentation predictions. A skin region may retain features from its original photograph: that mismatch is deliberate collage material.

## Relationship to Oursler's practice

The [artist's archive for template/variant/friend/stranger](https://tonyoursler.com/templatevariantfriendstranger-london) documents large photographic faces interrupted by eye/mouth screens and facial-recognition markings, alongside abstracted etched panels. These layouts take three strategies from that practice: treating an eye or mouth as a separate image surface, making a flat support feel like a face, and placing human photographic expression against machine-like measurement.

The new material is the recombination: three historical sitters occupy one constructed face, while different mathematical descriptions hold—or fail to hold—the image together. Rectangular windows, oversized organs, missing facial skin and separated regions produce six distinct arrangements. Dragging makes the tension visible by moving an image fragment and deforming its assigned structure. Static photographs and drawn scan lines evoke screen surfaces; they do not reproduce Oursler's video footage or animate a real person.

## Model-to-art translation

Coordinates come from the [previous system studies](../studies/#structures), including the source/approximation notes saved with their JSON. They are rescaled to each composition; these collages are not technical calibration charts.

- **5 points:** real ArcFace destination-template coordinates; the connecting lines are our compositional guides, not official model topology. Source: [InsightFace face_align.py](https://github.com/deepinsight/insightface/blob/master/python-package/insightface/utils/face_align.py).
- **68 points:** standard IDs and dlib drawing connections on the original schematic face created for the research page. Source: [dlib renderer](https://github.com/davisking/dlib/blob/master/dlib/image_processing/render_face_detections.h).
- **106 points:** approximate manual trace of the diagram linked from [InsightFace coordinate regression](https://github.com/deepinsight/insightface/tree/master/alignment/coordinate_reg). No edge network was invented.
- **468 points:** orthographic projection of Google's canonical model with the [official connections](https://github.com/google-ai-edge/mediapipe/blob/master/mediapipe/tasks/web/vision/face_landmarker/face_landmarks_connections.ts). [Canonical model](https://github.com/google-ai-edge/mediapipe/blob/master/mediapipe/modules/face_geometry/data/canonical_face_model.obj). MediaPipe-derived data: Apache-2.0; source license retained in the research folder.
- **478 study:** the official 468-point base plus ten constructed iris positions using documented iris IDs. The additional positions remain schematic, not an inferred or canonical face result.
- **Region masks:** handmade shapes inspired by the [CelebAMask-HQ class definitions](https://github.com/switchablenorms/CelebAMask-HQ/blob/master/face_parsing/README.md). The blue hair, silver skin and separated lips are artistic materials, not predicted labels.

## Photograph credits

Existing local assets are reused. Source-image cropping, clipping, tinting and scan-line texture are implemented in SVG; no destructive photo edits were made.

- `../assets/bernhardt.jpg`: Nadar, **Sarah Bernhardt**, c. 1864. [Wikimedia Commons source](https://commons.wikimedia.org/wiki/File:Sarah_Bernhardt,_par_Nadar,_1864.jpg).
- `../assets/herschel.jpg`: Julia Margaret Cameron, **Sir John Herschel**, 1867. [Wikimedia Commons source](https://commons.wikimedia.org/wiki/File:Sir_John_Herschel,_by_Julia_Margaret_Cameron.jpg).
- `../assets/thompson.jpg`: Dorothea Lange, **Migrant Mother**, 1936, depicting Florence Owens Thompson. [Wikimedia Commons source](https://commons.wikimedia.org/wiki/File:Lange-MigrantMother.jpg), [Library of Congress context](https://guides.loc.gov/migrant-mother).

These sources are identified as public domain on their source pages. The sitters are credited historical photographic subjects; combining them makes no claim about their real identities, expressions or relationships. No photograph of an Oursler artwork is embedded in these six new compositions.

## Interaction and exports

Each `.html` is a complete static SVG composition with shared CSS and a small JavaScript dragging handler. It displays without JavaScript. Pointer dragging and arrow keys move the focused fragment; Shift + arrow moves farther; Escape restores the arrangement. Points attached to that fragment travel with it and edge endpoints update. Touch dragging uses SVG coordinates, so resizing does not change movement scale.

`build.py` regenerates the six HTML pages, portable SVGs and manifest. Each exported SVG embeds the source photographs so it remains usable outside the site. `exports/six-faces.png` is a browser-rendered comparison board. The index gallery and research-page link are the only new navigation; the original collage remains unchanged.
