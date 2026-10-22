# How the leadership-network collection was made

Working notes for the Emerald City Leadership Network collection added in 1.1.0. They record the order of work, the models and the checks, so someone can repeat the approach. They are not a byte-for-byte reproduction recipe: raw model responses, the runner and the API key are not published.

## Order of work

1. **Roster.** `world/leadership-network-people.json` has 300 adult members. Fifty-four names come from StoryBank's fictional Emerald City cast. Nine of them keep the facts the StoryBank playground already shows (Dorothy Gale, Martin Woodward, Clara Micefield, Leona Bracken, Ruth Fenwick, Samuel Strawbridge, Oscar Diggs, Glinda Southwell, Jellia Jamb). The other 246 were generated from Oz-echo name pools with a fixed random seed (20261022), rejecting duplicate full names. Roles, organizations, homes, circles and acquaintance links are deterministic. A model drafted the background, voice and experience-domain text for generated members.
2. **Queries first.** The 62 questions in `evaluation/leadership-network-queries.json` were written before any document. Each expected member received a planted episode, and 34 fixed documents were briefed to carry the convening, correction, disagreement and identity cases.
3. **Episode seeds.** A model proposed further episodes for every member, with mostly completed work, some plans and some secondhand reports. Each member has five or more seeds, one of which is usually a plan.
4. **Document briefs.** A deterministic planner placed the fixed documents first. About 29% of the remaining documents carry one member with two items. The rest group two to six members who share a circle, with one episode each, rotating through 17 format labels.
5. **Pilot.** A 30-member tranche (44 documents) went through generation, checks, audit, assembly and validation before the main run. The pilot led to tighter rules on invented names, brands, real-world languages and narrated voice notes, and to background notes for shared facts. It also produced the decision to hand-adapt the documents behind the StoryBank playground stories.
6. **Generation.** Each brief went to the author model with [the author prompt](leadership-network-author-prompt.md).
7. **Editorial pass.** Scripted checks looked for missing or extra cast members, invented names (bigrams, honorifics and an unknown-capitalized-word scan), banned phrases, brands, contact details, negative-query topics and invalid speaker labels. Failing documents were regenerated up to two times. A model lint listed any remaining personal names, brands and real-world places. A minimal-edit repair fixed them and was rejected if it changed more than 7% of a document. The agent then read a sample and the fixed documents and made hand edits. Eight documents that back StoryBank playground stories were adapted by hand from the playground's own fictional sources so their facts match exactly.
8. **Annotation.** The coverage audit prompt (`coverage-audit-prompt.md`, unchanged from 1.0.0) ran on every document with only its identity list. Every proposed quote was located mechanically in its block. Leads were kept only for completed or reported episodes, matched to the member's briefed episode in that document, and merged across documents that retell the same episode. Plans produce no lead. Correction, disagreement and identity cases received hand-written summaries.

## Models

The bake-off brief asked for free OpenRouter models. On this account, every listed free model was excluded by the zero-data-retention privacy setting, except `xingchen-agi/xing4.0-29b-a4b:free`. That model needed about seven minutes per document behind upstream rate limits and failed two of five bake-off documents. The account setting was not changed. Paid models were compared on the same five briefs:

| Model | Bake-off result |
| --- | --- |
| `xingchen-agi/xing4.0-29b-a4b:free` | 3 of 5 returned; usable prose, wrong form for call notes; too slow |
| `deepseek/deepseek-v3.2` | 5 of 5 valid JSON; closest to the briefs; terse; one invented first name |
| `qwen/qwen3-235b-a22b-2507` | 5 of 5 valid JSON; livelier; added more unbriefed facts, dates and figures |

`deepseek/deepseek-v3.2` was chosen for seeds, drafting, lint and repair (temperature 0.85 to 0.9 for writing, 0 for lint and repair). On the pilot audit it found 107 of 112 intended completed episodes and misread none of 12 plans as completed, compared with 93 of 112 and 2 of 12 for Qwen. It was therefore also used for the audit (temperature 0.1). Author and auditor are the same model, so the audit is not independent corroboration.

## Limits

The planner grouped people by circle, not by a shared history, so most multi-member documents are roundups, panels or minutes rather than one joint event. Seeded episodes are small and practical by design. Summaries are model-written. Agent review covered the fixed documents and a sample, not every lead.
