# LStack in Codex

Read once per task. These mappings replace Cursor-specific instructions in the bundled skills and their references. Keep the playbook steps. `<pstack>` is this plugin's root, two directories above this file.

## Tools

| Upstream name | Codex operation |
| --- | --- |
| `Read`, `Grep`, `Glob`, `Bash`, file edits | Available file and shell tools. Search with `rg`; edit with the patch tool. |
| `AskQuestion` | Available user-input tool, or a question in the conversation. |
| Todolist, `TodoWrite` | Available plan tool, or a short tracked list when absent. |
| `/name`, the **name** skill | Read `<pstack>/skills/<name>/SKILL.md`. User invocation is `$pstack:name`. |
| `Task`, `generalPurpose` | Available native agent spawn tool. Use only its actual schema. |
| `poteto-agent`, `comment-sicko` | Pass the corresponding `<pstack>/agents/<name>.md` instructions and absolute skill paths to a native agent. Do not assume a custom agent type is registered. |
| `run_in_background`, `resume`, `file_attachments` | Native agents run asynchronously. Use native wait/message/resume operations when supported; put file paths in the brief. |
| `readonly: true` | Give a read-only brief. This does not create a separate sandbox. |
| `environment: "cloud"`, `cloud_base_branch` | A separate local worktree at the specified base. Create it before spawning and give its absolute path to the agent. |

Repository instructions govern delegation. Without authorization or agent tools, carry out the same investigation, implementation, and review steps sequentially yourself and report that independent review did not run. Do not bypass this fallback through a second Codex CLI or an external model API. Parallel writers need separate worktrees or disjoint file ownership.

## Models

Replace all upstream role defaults, model pools, budget ladders, and model-family fallback rules with these settings. Do not read or write `pstack-models.mdc` in Codex.

| Role | Model | Reasoning effort |
| --- | --- | --- |
| Ordinary exploration, implementation, synthesis, prose | `gpt-6.1-sol` | `medium` |
| Architecture, independent review, difficult debugging | `gpt-6.1-sol` | `high` |
| One specific judgment explicitly requested from Astra | `gpt-6-astra` | `low` |

Astra is never an automatic fallback, panel member, or cross-judge. An authorized Astra consultation receives only the question and necessary code/evidence, defaults to one call, and does not delegate or retry automatically. Sol handles follow-up implementation.

Use actual spawn model/effort settings or a configured custom agent. Do not encode reasoning effort in the model name or claim that prose changes the running model. When changing a child's model, use a fresh context if required by the spawn tool and supply a self-contained brief. If the requested settings are unavailable, inherit the parent, report the actual fallback, and do not probe other expensive models. The main chat retains its launch settings; the plugin cannot change them.

For `arena`, `architect`, and `interrogate`, keep the requested perspectives using Sol at the role's effort. This is independent same-model review, not multi-model review. Arena's different-family judge is skipped unless the user explicitly requests Astra. A sequential pass is not an independent review.

## Paths and capabilities

Use the installed `<pstack>` paths instead of searching `~/.cursor/plugins/`. Codex plugin metadata is `<pstack>/.codex-plugin/plugin.json`. Project skill paths are `.agents/skills/`; project instructions are `AGENTS.md`. Do not write Cursor or Claude configuration from Codex.

For history, use a supported session-history tool scoped to the current project, or user-supplied transcripts. Do not guess Cursor transcript paths in Codex.

For built-in PR actions, use the available forge connector or CLI. Existing Bugbot comments can be read as ordinary PR reviews. Cursor cloud control, automations, and Cursor-specific script commands are unavailable. Skip an optional step with a reason; if required evidence depends on it, report the missing capability rather than claiming completion. A long-running request does not create a background monitor by itself.

`deslop`, `control-cli`, and `control-ui` are bundled in `<pstack>/skills/`. Read those local skills when a playbook references them, including references naming `cursor-team-kit`. They are instructions, not installed runtimes; use available terminal/browser tools or the project's existing harness. Report a missing capability when it prevents verification. Cursor's built-in `create-skill` maps to the available `skill-creator` skill.

## setup-pstack

In Codex, report the current model/effort when observable and explain the role settings above, then stop. Do not follow the Cursor setup steps or install hooks. To start a chat with the baseline settings, the user can run:

```bash
codex --model gpt-6.1-sol -c 'model_reasoning_effort="medium"'
```
