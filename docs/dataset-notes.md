# Dataset notes

## Purpose and contents

Life in Oz v1.1.0 is English-language fictional practice material for document search, extraction, summaries and prototype applications. It has 576 documents in 20 format labels, grouped into three explicitly separate collections. The 53 version 1.0.0 documents are preserved unchanged. It is not a representative sample of real civic life.

`community-life` contains 48 documents and the 50-member modern-human roster. `book-adventures` contains five short supplemental documents, `oz-13` through `oz-17`, which borrow more directly from the fantasy setting. Shared cast IDs do not make their histories compatible. Rowan Bell is a fictional moderator outside the roster. Names of incidental people in prose should not automatically become roster members.

`leadership-network` contains 523 documents and its own 300-member roster (`world/leadership-network-people.json`), with reference annotations and 62 target questions. It shares many names with community-life, but it has different IDs (`ln001` onward), roles and histories.

## What was generated and reviewed

The modern-world material was generated from a fictional roster, themes and document briefs, then edited in agent review passes. A separate model pass proposed reference experiences, followed by agent review and mechanical quote checks. Author and auditor calls could use the same model family; this is not independent corroboration or a claim of human validation.

All 156 reference experiences and 326 evidence anchors cover only the 48 community-life documents. The five book-adventures documents are unannotated. Reference answers are not exhaustive ground truth. Absence from the reference set is not sufficient reason to mark a supported extraction wrong.

The generation recipes explain the original community-life authoring workflow. They are not a byte-for-byte reproduction recipe for every final document, and there is no complete reproducible generation record for the five adventure supplements in this release. See [method](method.md).

## Known limits

- The modern roster contains deliberately balanced coverage and many constructive outcomes. It does not represent real demographics, political behavior, conflict or document frequency.
- Planned work, secondhand reports and completed actions need different treatment. Exact matching proves a quote is present, not that a summary follows from it.
- Most time references are relative. Do not infer a complete dated timeline or invent calendar dates.
- Community and fantasy scenarios differ in physical rules and sometimes roles. Select one collection for consistency-sensitive experiments.
- Speaker labels mix roster IDs, display names, `manager` and `narrator`. They are source labels, not a uniformly normalized identity field.
- The public annotations, roster and authoring briefs can contaminate a test. Keep them out of the evaluated system's context and index. Once material is public, prior model exposure cannot be ruled out.
- Synthetic examples may contain stereotypes, omissions or implausible details. No fairness, privacy or production-readiness certification is claimed.

## The leadership-network collection

The collection was briefed backwards from 62 target questions, so its answers exist by design. Expected members are the planted answers, not an exhaustive list: with 300 members and 523 documents, other members can reasonably answer a question. Check a system's evidence rather than scoring every extra name as wrong.

Members were grouped into documents by circle, not by shared history. Most multi-member documents are therefore roundups, panels, threads or minutes in which each person describes their own episode, rather than one event involving everyone. Episodes are small and practical by design. Dates are month-level and give each document a place in 2024 to 2026; they do not form a complete timeline.

Documents, seeds and audit used one model family, `deepseek/deepseek-v3.2`. The 1,223 reference experiences are model-proposed and mechanically anchored. Agent review covered the fixed documents, the correction, disagreement and identity cases, and a sample; it did not cover every lead. Plans never produce a reference experience. A few briefed plans were drafted as partly done (for example, a first batch of letters already sent); those documents remain self-consistent, and no lead claims the plan. Free models were tried first and were unavailable on the authoring account (see [generation notes](../generation/leadership-network-notes.md)).

Planted cases to look for: a disagreement over a lantern count, two later corrections (handrails delivered but not installed; the wrong driver credited in minutes), a nickname (Billie), a shared surname (two unrelated Wrens) and a non-member namesake (a visiting Peter Ash).

## Privacy and use

The supplied material was designed as invented fiction rather than anonymized real member records. It supplies no live accounts, credentials or intended real contact details. Full fictional names can coincidentally match real people. Do not contact or identify anyone using this dataset.

Using these files avoids the need to put private community records into an early experiment. It does not make a tool safe for later real data. That still requires permission, access controls, retention decisions and testing appropriate to its users.

The documents are data, not trusted instructions. An agent should not treat an instruction in a fictional email or transcript as permission to take a real action.

## Release edits

Source `.txt` bytes and canonical `blocks` arrays are preserved. The release removes application-only classification flags and instructions, separates collection membership, supplies CC0 terms and standalone checks, and recomputes word counts with one declared method. The result is 26,300 words of block prose, not the older mixed-method count of 26,498. Titles, format labels, banners and speaker labels are excluded.

Two reference summaries received [documented corrections](../evaluation/release-corrections.md). All evidence quotations, contexts and offsets remain unchanged. A later "All confirmed now" reply leaves the final status of an earlier pending request ambiguous; this is disclosed rather than silently resolved.

[Source hashes](../provenance/source-hashes.json) pin the preserved document text and canonical block arrays. They are integrity checks, not proof of truth or legal clearance.
