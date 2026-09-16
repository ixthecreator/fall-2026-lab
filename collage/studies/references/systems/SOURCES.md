# Computational structure drawings

These drawings compare landmark layouts and pixel-region labels. They are not outputs from a live model and do not perform identity verification. IDs are zero-based. Colors are our explanatory annotations.

| Export               | Geometry                                                                               | IDs / connections                                                                                          |
| -------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `alignment-5.svg`    | Exact five `arcface_dst` coordinates in a 112 × 112 crop, uniformly scaled for display | Official point order. Dashed guides are illustrative, not a model graph.                                   |
| `landmarks-68.svg`   | Original schematic coordinates                                                         | dlib/iBUG 68-point indices; connections from dlib rendering code                                           |
| `landmarks-106.svg`  | Approximate manual trace of the official-linked diagram                                | 106 markup indices. A point cloud, with no invented mesh edges. Crowded eye/mouth labels are approximated. |
| `mesh-468.svg`       | Official canonical OBJ: x/y front projection; depth retained in JSON                   | Official tessellation and contour connections                                                              |
| `mesh-478-study.svg` | Same 468 points plus ten constructed iris positions                                    | Official iris boundary IDs; orange iris positions are schematic, not canonical coordinates or predictions  |
| `parsing-19.svg`     | Original silhouette and region shapes                                                  | Official CelebAMask-HQ class IDs; diagram colors are not official palette values                           |

## Primary references

- Five-point alignment: [InsightFace face_align.py](https://github.com/deepinsight/insightface/blob/master/python-package/insightface/utils/face_align.py). Eye centres, nose, mouth corners. This is not dlib's separate five-point eye-corner layout.
- 68-point connectivity: [dlib render_face_detections.h](https://github.com/davisking/dlib/blob/master/dlib/image_processing/render_face_detections.h). Local reference retains its copyright and Boost license.
- 106-point definition: [InsightFace coordinate regression](https://github.com/deepinsight/insightface/tree/master/alignment/coordinate_reg). Its README links [2d106markup.jpg](https://github.com/nttstar/insightface-resources/blob/master/alignment/images/2d106markup.jpg), saved here as the tracing reference. The reference chart is credited to the InsightFace resources repository; the redraw is approximate.
- Canonical 468 model: [MediaPipe canonical_face_model.obj](https://github.com/google-ai-edge/mediapipe/blob/master/mediapipe/modules/face_geometry/data/canonical_face_model.obj).
- Mesh and iris edges: [MediaPipe face_landmarks_connections.ts](https://github.com/google-ai-edge/mediapipe/blob/master/mediapipe/tasks/web/vision/face_landmarker/face_landmarks_connections.ts). MediaPipe references and derived mesh geometry: © MediaPipe Authors, Apache-2.0; license retained here.
- 478-output context: [Google Face Landmarker](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker). The official static OBJ has 468 vertices, so this study does not pretend to have canonical iris geometry for the extra ten.
- Pixel classes: [CelebAMask-HQ face_parsing README](https://github.com/switchablenorms/CelebAMask-HQ/blob/master/face_parsing/README.md). There are 19 labels including background, clothing and accessories. Subject-relative left/right conventions are used in the schematic.

Downloaded / consulted: 2026-09-16. Local files pin the material used for the diagrams; upstream links may change. `build_systems.py` regenerates the SVGs and JSON from these references and documented schematic positions. No photographs, face-identification results or AI-generated images are used in the new drawings.
