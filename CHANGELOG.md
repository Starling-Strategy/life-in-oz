# Releases

## 1.1.0

Adds the Emerald City Leadership Network collection. The 53 version 1.0.0 documents, their hashes and their annotations are unchanged.

- New `leadership-network` collection: 523 fictional documents (233,110 words) in 17 format labels. About 78% involve more than one member.
- New 300-member roster with twelve circles and five districts, in `world/leadership-network-people.json`. Nine members keep the facts shown in StoryBank's Emerald City playground. Planted identity cases cover a shared surname, a nickname and a non-member namesake.
- 62 target questions, written before the documents, in `evaluation/leadership-network-queries.json`. Each expected member has a supporting source. Eight questions are designed to have no answer.
- 1,224 model-proposed, mechanically anchored reference experiences with 1,683 exact evidence anchors. Every member has three to five.
- Generation notes, author prompt and document briefs in `generation/`.
- After an independent review: four lead summaries or evidence sets corrected, the query answer sets completed with 78 checked additions (one out-of-scope answer removed), anonymization artifacts and an ambiguous first name fixed, and generic closing morals trimmed in 37 documents.
- `validate.py` now checks every roster, duplicate full names, format labels and the target-question file. `select.py` lists any collection, and the tests cover the new files.

## 1.0.0

First standalone release of Life in Oz under CC0.

- Preserves all 53 fictional documents as readable text and canonical JSON blocks.
- Separates 48 modern community documents from five book-inspired adventure supplements.
- Includes the 50-member modern roster, generation prompts and 156 reference experiences with 326 exact evidence anchors.
- Removes application-specific dependencies and fixture flags.
- Adds an indexed catalog, dataset limitations, rights notice, standard-library validation and a plain-language article.
- Recomputes word totals consistently: 26,300 words in source prose, excluding labels and headings.

This is a data release, not a hosted tool, scored benchmark or civic advocacy database.
