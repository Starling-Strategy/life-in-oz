# Reference annotations

These files support experiments with **community-life** and **leadership-network**:

- `members.json`: reference identities, roles and homes. These are authoring facts, not a claim that every field has documentary evidence.
- `experience-leads.json`: 156 agent-reviewed experience summaries, with 326 exact evidence anchors across 48 source documents, plus 10 editorial case notes.

For leadership-network:

- `leadership-network-members.json`: reference identities for the 300-member roster.
- `leadership-network-experience-leads.json`: 1,224 model-proposed, mechanically anchored experience summaries with 1,683 exact evidence anchors across 523 documents, plus case notes for the planted correction, disagreement and identity cases.
- `leadership-network-queries.json`: 62 target questions written before the documents, with supporting sources for each expected member.

They do not cover the five book-adventures supplements. They are not exhaustive, independently human-validated ground truth. Mechanical validation checks references and quoted substrings; it cannot certify that every summary is entailed by its quotations. See the [two release corrections](release-corrections.md) for a preserved ambiguity and a removed stale caveat.

For a blind run, exclude this directory, world/, generation/, source JSON and membership metadata from the tested assistant's context and search index. Provide only the selected source text. Use annotations afterwards to inspect misses, unsupported claims, attribution, duplicate retellings and plans mistaken for completed actions.

A correct answer outside this reference set is possible. Do not turn simple match rate into a claim of overall accuracy. There is no packaged scoring engine or established train/test split in this release.
