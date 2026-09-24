# Reference annotations

These files support experiments with **community-life only**:

- `members.json`: reference identities, roles and homes. These are authoring facts, not a claim that every field has documentary evidence.
- `experience-leads.json`: 156 agent-reviewed experience summaries, with 326 exact evidence anchors across 48 source documents, plus 10 editorial case notes.

They do not cover the five book-adventures supplements. They are not exhaustive, independently human-validated ground truth. Mechanical validation checks references and quoted substrings; it cannot certify that every summary is entailed by its quotations. See the [two release corrections](release-corrections.md) for a preserved ambiguity and a removed stale caveat.

For a blind run, exclude this directory, world/, generation/, source JSON and membership metadata from the tested assistant's context and search index. Provide only the selected source text. Use annotations afterwards to inspect misses, unsupported claims, attribution, duplicate retellings and plans mistaken for completed actions.

A correct answer outside this reference set is possible. Do not turn simple match rate into a claim of overall accuracy. There is no packaged scoring engine or established train/test split in this release.
