# Maintaining LStack

LStack forks `cursor/plugins` pstack. When updating this fork, fetch `upstream/main` and compare pstack changes against the revisions in `pstack/docs/harness/upstream.json`. Import relevant changes and update that record. Changes to unrelated plugins do not require an import.

Import upstream pstack changes after they land on `upstream/main`. LStack maintains its own Codex adapter and packaging.

Preserve the role settings in the user's `pstack-models.md`, explicit-request-only Astra use, Korean writing guidance, conversation mode hooks, and bundled `deslop`, `control-cli`, and `control-ui`. Keep the Codex native manifest so hooks remain usable. Generated Claude files must be regenerated rather than edited directly.

Run the Codex packaging checks, generated-tree checks, hook tests, and relevant pstack script tests after changes. These instructions do not authorize delegation.
