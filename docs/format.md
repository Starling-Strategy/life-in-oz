# File formats

All text is UTF-8. JSON is ordinary JSON, not a database export. Source documents use stable IDs and retain their original format labels. Version 1.0.0 used eight labels. Leadership-network adds `newsletter_feature`, `intake_email`, `panel_transcript`, `post_event_debrief`, `nomination_letter`, `meeting_minutes`, `press_release`, `survey_response`, `radio_interview`, `speaker_bio`, `grant_report` and `membership_intake_form`; it also uses `news_article`, `email_thread`, `social_thread`, `webinar` and `manager_conversation`.

## Manifest and collections

`manifest.json` lists every document with `id`, `title`, `theme`, `format`, `collection_id`, `text_file`, `canonical_blocks_file`, `member_ids`, `words`, `text_sha256` and `content_sha256`. Paths are relative to the repository root.

Each file in `collections/` names its `document_ids`, totals, continuity boundary and annotation scope. Sources stay in one flat directory so existing IDs remain stable. Use the collection lists instead of inferring a scenario from a filename.

`words` counts `str.split()` tokens in block prose, not titles, banners or speaker labels. It is a consistent package size measure, not a linguistic word tokenizer.

## Source text and blocks

`.txt` is the readable document, including a fiction banner and labels. `.json` contains `id`, `title`, `format`, `fictional`, `notice`, `members`, `blocks` and `content_sha256`.

Each block has `id`, `speaker_id` and `text`. `speaker_id` is a preserved attribution label, which may be a roster ID, a display name, `manager`, `narrator` or, in leadership-network, a lowercase role label for an unnamed person (`neighbor`, `clinic manager`). Do not treat every label as a person ID. `members` identifies roster participants but is not an assertion that every speaker is a roster member.

The hashes use SHA-256:

- `text_sha256`: exact UTF-8 bytes of the `.txt` file.
- `content_sha256`: UTF-8 bytes of Python `json.dumps(blocks, ensure_ascii=False)` with its default separators, without a terminal newline. Preserve block array order, object key order and text. This convention is specific, not a generic canonical-JSON standard.

Changing whitespace or wording can change a hash. Preserve source bytes for comparisons or explicitly publish a new edition.

## Reference evidence

Each experience has a `person_id`, `episode_key`, `summary`, `review_method` and `evidence` array. Each evidence entry has `source_id`, `block_id`, `quote`, `context`, `start` and `end`.

Offsets count Unicode code points within the **individual canonical block text**, not the full text file. They are zero-based and end-exclusive: Python `text[start:end]` must equal `quote`, and `context` must equal the whole block text. JavaScript UTF-16 string offsets can differ for some Unicode characters; use code-point-aware indexing.

An exact anchor proves where a quotation occurs. It does not prove that the surrounding summary is justified or that the invented event happened in the real world.

In `member_coverage`, `source_documents` counts distinct documents cited by that person's reference experiences, not every document in which the person appears.

## Target questions

`evaluation/leadership-network-queries.json` lists `queries`, each with `id`, `query`, `kind` (`vocabulary-gap`, `exact-term`, `skill/sector/place`, `speaker/convening` or `negative-no-answer`), `expected_member_ids` and `support`. For each expected member, `support` gives the planted `episode_keys`, the `source_ids` that carry them and whether a `reference_lead` exists. Offers and plans can be supporting sources without a reference lead. Negative questions have no expected members.

## Roster and recipes

`world/people.json` (community-life) and `world/leadership-network-people.json` (leadership-network, which adds `organization`, `district`, `circles`, an optional `nickname`, and top-level `circles` and `districts`) store the community premise and `members`, including each person's `id`, name, role, home, background, voice, inspiration, relationships and experience domains. Background and relationship fields guide fiction writing; they are not independent evidence for document extraction.

Generation recipes contain document briefs and authoring seeds. Reference identities live separately in `evaluation/members.json`. Keep both out of blind document tests.
