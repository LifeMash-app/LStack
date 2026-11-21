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

For a model-selecting skill, read `pstack-models.md` under `CODEX_HOME` (default `~/.codex`). Apply the skill's current role names and use the defaults below for roles without a setting. The [LStack model template](codex/pstack-models.md) is available for a first-time setup.

| Role | Model | Reasoning effort |
| --- | --- | --- |
| Ordinary exploration, implementation, synthesis, prose | `gpt-6.1-sol` | `medium` |
| Architecture, independent review, difficult debugging | `gpt-6.1-sol` | `high` |
| One specific judgment explicitly requested from Astra | `gpt-6-astra` | `low` |

Astra is never an automatic fallback, panel member, or cross-judge. An authorized Astra consultation receives only the question and necessary code/evidence, defaults to one call, and does not delegate or retry automatically. Sol handles follow-up implementation.

For `model@effort`, pass the model and effort separately using the active spawn tool's schema. For `auto` or `inherit-parent`, inherit the parent model and effort. For a bare model, use the sheet's `default effort` when set and supported. Otherwise inherit the session effort when the host supports it. Do not encode reasoning effort in the model name or claim that prose changes the running model. When changing a child's model, use a fresh context if required by the spawn tool and supply a self-contained brief. If the requested settings are unavailable, inherit the parent, report the actual fallback, and do not probe other expensive models. The main chat retains its launch settings; the plugin cannot change them.

For `arena` and `interrogate`, use the configured reviewers or Sol at the default review effort. Repeated Sol reviewers cover independent perspectives with the same model. When Arena requires a different model family and none is available under the user's settings, report that the cross-judge check did not run.

## Paths and capabilities

Use the installed `<pstack>` paths instead of searching `~/.cursor/plugins/`. Codex plugin metadata is `<pstack>/.codex-plugin/plugin.json`. Project skill paths are `.agents/skills/`; project instructions are `AGENTS.md`. Do not write Cursor or Claude configuration from Codex.

For history, use a supported session-history tool scoped to the current project, or user-supplied transcripts. Use the current conversation or an available handoff digest when permitted by the skill. For worktree cleanup, check recent Codex activity using an available history tool. If you cannot verify it, report that before treating the worktree as safe to remove.

For built-in PR actions, use the available forge connector or CLI. Existing Bugbot comments can be read as ordinary PR reviews. Cursor cloud control, automations, and Cursor-specific script commands are unavailable. Skip an optional step with a reason; if required evidence depends on it, report the missing capability rather than claiming completion. A long-running request does not create a background monitor by itself.

`deslop`, `control-cli`, and `control-ui` are bundled in `<pstack>/skills/`. Read those local skills when a playbook references them, including references naming `cursor-team-kit`. They are instructions, not installed runtimes; use available terminal/browser tools or the project's existing harness. Report a missing capability when it prevents verification. Cursor's built-in `create-skill` maps to the available `skill-creator` skill.

## setup-pstack

In Codex, use the user's `pstack-models.md` for role settings. Show the current choices, or the LStack defaults when the file is absent. Offer the models and effort levels supported by the current host. Write only the choices the user confirms and retain existing settings for the other roles. These settings apply to delegates. The main conversation uses its own model and effort.

## Conversation mode

Trusted local Codex hooks recognize `poteto 모드 켜줘`, `poteto 모드 꺼줘`, and `poteto 모드 상태` on the first line of a prompt. English equivalents are `poteto mode on`, `poteto mode off`, and `poteto mode status`. A task may follow on later lines. A control-only message acknowledges the state without starting a playbook.

The hook keeps an enabled marker per conversation under `PLUGIN_DATA` and provides a short skill reference each turn and after compaction. A resumed conversation keeps its state; a new conversation, fork, or clear starts off. Ordinary `$pstack:poteto-mode <task>` remains a one-turn invocation. Hook context reporting ON is evidence of persistence; without it, do not claim the mode is saved. The mode does not change model settings or permissions.

Plugin hooks require native trust through `/hooks`. Local plugin hooks do not run with cloud orchestration. When unavailable, use explicit per-request invocation and report that persistence is unavailable.
