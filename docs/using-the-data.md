# Using the data

## Read or download

Open a document from [the catalog](../CATALOG.md), or download a ZIP from [releases](https://github.com/Starling-Strategy/life-in-oz/releases/latest). You do not need a GitHub account to read a public release.

The full release includes reference annotations and authoring materials. The collection-specific text ZIPs include only that collection's documents, a short instruction file and rights notices. Choose a text ZIP when you want to test what a tool can discover without seeing the reference answers.

## Choose a scenario

Start with community-life for ordinary businesses, community services and conversations. Use leadership-network for a larger set with 300 members, many document forms and target questions. Use book-adventures for short, recognizable fantasy scenes. Shared names across collections are not one shared biography.

To list the selected text files from a local copy:

```sh
python3 scripts/select.py community-life
python3 scripts/select.py book-adventures
python3 scripts/select.py leadership-network
```

The paths are relative to the repository root. The selector does not copy files, create a database or contact a service.

## Try a small task

Give an assistant only `sources/oz-09-style-phone-notes.txt` and ask:

> Summarize what each person reports doing. Separate completed work, secondhand information and possible future plans. Quote the passage supporting each point. If the source does not settle something, say so.

Then read the source yourself. Did the answer assign the right action to the right person? Did it turn a possibility into a fact? These checks matter more than whether the response sounds polished.

For a search experiment, index the selected `.txt` files and ask a question about a subject in them. Require the system to show its supporting passage. Do not include reference files in the search index.

## Evaluate without giving away answers

Withhold `world/`, `generation/`, `evaluation/`, source JSON, and manifest membership metadata from the tested system. The evaluator can use the annotations after the run. Public release means a model may already have seen the material; do not claim a guaranteed unseen benchmark.

For leadership-network, index its `.txt` files and ask the questions in `evaluation/leadership-network-queries.json`, then compare the returned members and passages with each question's `support`. Negative questions should return nobody.

The annotations cover community-life and leadership-network, not book-adventures, and are not exhaustive. Check unsupported claims and correct extractions outside the reference set, rather than scoring every difference as an error. A reference summary can itself need correction.

## Extend the material

Reuse the existing documents or create a new collection. The prompts are available for adaptation, but no paid generation runner is included. Use clearly fictional inputs and preserve a separate scenario boundary when changing roles, physical rules or time periods.

An advocacy database, for example, would need newly authored organizations, issues, positions and activities, plus documents supporting those records. Those tables do not exist in this release. Do not reinterpret incidental mentions as a complete campaign dataset.

## Check a local copy

Run these commands from the repository root with Python 3.9 or later:

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Neither command needs an account, network access or third-party Python packages. They check structural integrity and exact references, not semantic accuracy or readiness for use with real people's information.
