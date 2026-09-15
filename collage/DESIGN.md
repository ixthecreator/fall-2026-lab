# VIE — interactive study

A photo-based interactive reproduction of Tony Oursler’s **VIE (2014)**, following the artist reference supplied by the student. The initial composition uses the original artwork photograph, rather than a newly authored portrait or reconstructed video installation. The 22 visible ring nodes are individually traced into SVG, with 39 explicitly mapped connections in `network.json`. Every node supports pointer dragging and keyboard movement. Moving a feature also moves its nearby attached landmarks. Escape restores all nodes and all four image excerpts. Connections are drawn from the live node positions, with the eye windows masking the portions behind them. The positions are traced from a photograph; occluded connections are an interpretation, not access to the original artwork’s technical drawing.

There is no visible navigation, text, or interface framing. SVG preserves the reference proportions on desktop and mobile. Alt descriptions and keyboard instructions remain accessible to screen readers.

## Artwork and image credit

- **Artist and copyright:** Tony Oursler. This work is not represented as the student’s original artwork.
- **Title/date:** VIE, 2014.
- **Original medium:** Wood, mounted photo print, monitors and media player.
- **Courtesy/source:** [Lisson Gallery artwork page](https://www.lissongallery.com/artists/tony-oursler/artworks/vie?image_id=8831).
- **Photograph:** [Gallery-hosted reference image](https://lisson-art.s3.amazonaws.com/uploads/attachment/image/body/8831/OURS140007_1__1_.jpg). The gallery page does not identify a separate photographer.
- **Context:** [template/variant/friend/stranger, Lisson Gallery, 2015](https://www.lissongallery.com/exhibitions/tony-oursler--5).
- **Web adaptation:** Developed with OpenAI Codex. The original gallery photograph remains the main source. A clean plate generated with the built-in OpenAI image-generation tool removes the baked-in diagram. It is blended into narrow SVG masks around the original lines and rings, while the remainder of the photo stays original. SVG supplies the reconstructed diagram and interactive excerpts. No replacement video is used. The original monitor footage is not available here.

The previous three-page design is preserved at commit `21e27be`, and the stripped-back original collage at `c90d4af`.

## Course submission

This one-screen reference study does not meet the original three-page collage assignment. It reproduces another artist’s work and currently contains no student-created photography. It should not be submitted as an original student artwork.

## Clean-plate asset

- File: `assets/vie-clean-plate.png`. AI-edited from the credited gallery photograph using the built-in imagegen tool.
- Full edit prompt: `assets/vie-clean-plate-prompt.txt`.
- Only original line and ring regions use the repaired image; the generated full frame is not used as a replacement photograph.
