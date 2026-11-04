# Maintaining LStack

LStack forks `cursor/plugins` pstack. When updating this fork, fetch `upstream/main` and compare pstack changes against the revisions in `pstack/docs/harness/upstream.json`. Import relevant changes and update that record. Changes to unrelated plugins do not require an import.

The Codex adapter and history helpers incorporate unmerged upstream PR #1143. Fetch its current head when updating those features, review the diff, and record the imported commit. Do not describe the PR as an official release before it merges.

Preserve the role settings in the user's `pstack-models.md`, explicit-request-only Astra use, Korean writing guidance, conversation mode hooks, and bundled `deslop`, `control-cli`, and `control-ui`. Keep the Codex native manifest so hooks remain usable. Generated Claude files must be regenerated rather than edited directly.

Use Node 24.22+ in the 24.x line or Node 26.10+ for compressed-history checks. Run Codex packaging checks, generated-tree checks, hook tests, the Codex history tests, and relevant pstack script tests after changes. These instructions do not authorize delegation.
