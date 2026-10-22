# Life in Oz

Fictional people and everyday documents for building and testing tools, without using private community records.

Life in Oz turns a familiar imaginary setting into practice material: local news, emails, meeting transcripts, social posts and call notes. Use it to try a search tool, teach an assistant to cite its sources, or explore how scattered documents could become useful records. No particular application, AI provider or database is required.

A project of [Starling Strategy](https://starlingstrategy.com). Released under [CC0](LICENSE): reuse, change and share our contributions, including commercially, without asking permission or giving credit. Credit is welcome, not required. See [rights and attribution](NOTICE.md) for the original book and other rights.

## Start with a document

You do not need to install anything to read these:

- [A newspaper answers residents' tenancy questions](sources/oz-01-civic-news.txt).
- [Neighbors discuss whether a booking board needs an app](sources/oz-05-invention-email.txt).
- [A baker and a mechanic work through a practical problem](sources/oz-06-maker-conversation.txt).
- [A manager records what was said, what is secondhand and what is still a plan](sources/oz-09-style-phone-notes.txt).
- [A freight owner tells a safety forum why she asked for a bridge to close](sources/ln-523-panel-transcript.txt).
- [A volunteer lead and a tinsmith disagree about how many lanterns arrived](sources/ln-351-email-thread.txt).

[Download the release](https://github.com/Starling-Strategy/life-in-oz/releases/latest) or browse [the document catalog](CATALOG.md). For the reason behind the project, read [Why we're practicing with the people of Oz](docs/why-oz.md).

## What's included in v1.1.0

| Material | Community life and book adventures | Leadership network | Total |
| --- | ---: | ---: | ---: |
| Fictional roster members | 50 | 300 | 350 |
| Source documents, each in plain text and JSON | 53 | 523 | 576 |
| Words in source prose, excluding headings and labels | 26,300 | 234,872 | 261,172 |
| Reference experience summaries | 156 | 1,223 | 1,379 |
| Exact passage references supporting those summaries | 326 | 1,680 | 2,006 |
| Target demonstration questions | | 62 | 62 |

The fictional community manager Rowan Bell and incidental speakers are not roster members. These counts describe the supplied files, not the number of people an application must extract or the number of facts it must find.

### Choose a collection

**[Community life](collections/community-life.json): 48 documents.** Modern human adaptations of Oz characters and original residents run small businesses, maintain public services and help their neighbors. The fictional network is the Munchkin Association Alumni. The roster and reference annotations belong to this collection.

**[Book adventures](collections/book-adventures.json): 5 short documents.** Familiar travel and rescue scenes are recast as notes and correspondence. These retain fantasy elements, including a woodman who needs oil. They are a separate scenario, not extensions of the modern people's biographies. They have no supplied reference experience annotations.

**[Emerald City Leadership Network](collections/leadership-network.json): 523 documents.** A larger modern scenario with its own 300-member roster: drivers, growers, clerks, founders, mechanics and mediators in twelve circles across the Emerald City and the four countries. The documents are call notes, news items, newsletters, email threads, intake emails, webinars and panels, debriefs, nomination letters, community-board threads, minutes, press releases, survey responses, radio interviews, speaker bios, grant reports and membership forms. Most involve several members. They include completed work, ordinary work, setbacks, unfinished plans, hearsay, a disagreement between accounts and later corrections. Reference annotations and [62 target questions](evaluation/leadership-network-queries.json) belong to this collection.

The collections reuse some names as cast correspondences. In particular, many leadership-network names also appear in community-life with different roles, and the IDs differ (`ln001`, not `m007`). Do not combine their facts as one consistent history. The underlying text is preserved rather than quietly rewritten to hide the difference.

## Ways to use it

- Ask a search tool to find the passage that supports an answer.
- Compare how assistants summarize the same conversation.
- Extract people and actions without turning plans or hearsay into completed facts.
- Prototype a contact directory or document browser.
- Try document-to-record workflows before introducing authorized real material.

This release supplies documents, a roster and reference annotations. It does **not** include a civic advocacy database, a trained AI model, a hosted service or a scored benchmark. Further collections could add structured organizations, campaigns and activity records, but those are not part of this release.

## Find your way around

| Path | Purpose |
| --- | --- |
| `sources/` | Preserved fictional documents: `.txt` to read, `.json` for exact passage references |
| `collections/` | Explicit document lists for the three separate scenarios |
| `world/people.json` | Community-life authoring roster: names, roles, background and acquaintances |
| `world/leadership-network-people.json` | Leadership-network roster, circles and districts |
| `evaluation/` | Reference identities, experience summaries, evidence and target questions; keep out of blind tests |
| `generation/` | Writing briefs, prompts and style examples; no credentials or paid runner |
| `manifest.json` | Machine-readable catalog, word counts, collection membership and hashes |
| `provenance/` | Preserved source hashes and the edition boundary |
| `docs/` | Method, limitations, format and a nontechnical explanation |
| `scripts/` | Standard-library Python validation and document selection |

For a blind test, provide **only the selected `.txt` documents**. The roster, source JSON, manifest memberships, generation briefs and evaluation files contain information that would give away answers. [Using the data](docs/using-the-data.md) explains the distinction.

## Check the package

Python 3.9 or later; no packages, network connection, account or API key needed:

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/select.py community-life
python3 scripts/select.py leadership-network
```

The first command checks document pairs, hashes, references, rosters, format labels, target questions, collection boundaries and totals. The `select.py` commands list only the text paths for one collection; they do not load any data into a service.

## Be clear about what this is

Every document is invented, including all quoted speech. Transcript-shaped files are not transcripts of real recordings. The material is inspired by the book, not a factual account of its plot or a set of verified quotations from it.

The collection was made with AI assistance and agent editorial review. Reference answers can still miss something or overstate a passage. Passing a test here does not prove that a tool is secure, unbiased or ready for sensitive real-world use. Read the [dataset notes and limitations](docs/dataset-notes.md) before relying on it.
