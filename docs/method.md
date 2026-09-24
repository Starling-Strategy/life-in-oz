# How the collection was made

The starting point was [Baum's book on Project Gutenberg](https://www.gutenberg.org/ebooks/55). Its characters and motifs suggested a setting for new fiction. The modern documents were not extracted from the novel, and invented dialogue is never offered as a quotation from Baum.

## The community-life collection

1. Create a fictional roster. Give people names, ordinary roles, places and acquaintances, while keeping invented backgrounds separate from evidence of events.
2. Write briefs for documents people might encounter: an email exchange, a local report, a discussion, a manager's notes. Give each document a reason to exist.
3. Use an AI model to draft the documents. The retained generation notes identify `qwen-3.8-27b` through Cerebras, with author temperature `0.9`, audit temperature `0.1`, `top_p` `0.95`, reasoning disabled and no fixed seed. These are historical settings, not a current provider recommendation or a promise of reproducibility.
4. Review and edit the drafts with agents. Check who did what, whether speakers respond to each other, whether physical actions make sense and whether an unfinished plan has accidentally become an accomplishment.
5. Propose reference experiences from the actual documents, not from the desired background facts. Review those proposals and locate exact supporting passages.
6. Preserve source text and stable block identifiers. Keep reference annotations apart from the documents used for a blind test.

The retained recipes cover an initial 12-document tranche, 35 expansion documents and a one-document Oscar supplement. Coverage goals helped shape this fiction; they should not be mistaken for naturally occurring data. The 156 annotated experiences are a useful reference set, not an independent human-certified benchmark.

## The book-adventures collection

Five later short documents recast recognizable arrival, trail-clearing, ravine-crossing, rescue and river scenes in documentary forms. They retain fantasy details that do not fit the modern-human roster. This release preserves them in a separate collection rather than silently changing their prose or using them to revise modern biographies.

The complete generation history of those supplements is not included, and the community-life evaluation does not cover them.

## Repeat the approach, not the exact output

The [generation folder](../generation/README.md) contains adaptable briefs and prompts. It does not include provider credentials, raw responses or an automated paid runner. Model behavior changes, and creative generation without a fixed seed will not reproduce these files exactly. The released edition itself is the stable test input.

For another collection, start with a practical use: what tool would these documents help someone test? Write new fictional premises rather than disguising real records. A future civic advocacy collection could combine campaign tables and correspondence, but this release does not contain that database.
