# LifeMash pstack model configuration

# Role values use model@effort. auto and inherit-parent follow the session.
# Panel entries each run one delegate, subject to repository authorization.
# Astra requires an explicit user request under the Codex adapter's limit.
# budget: small (medium)
default effort: medium
feature, refactoring: gpt-6.1-sol@medium
bug-fix: gpt-6.1-sol@medium
perf-issue: gpt-6.1-sol@medium
hillclimb: gpt-6.1-sol@medium
judgment and prose: gpt-6.1-sol@medium
hardest tasks: gpt-6.1-sol@high
how explorer: gpt-6.1-sol@medium
how explainer: gpt-6.1-sol@medium
why investigators: gpt-6.1-sol@medium
why synthesizer: gpt-6.1-sol@medium
reflect tooling: gpt-6.1-sol@medium
reflect judgment, divergent, synthesizer: gpt-6.1-sol@high
arena runners: gpt-6.1-sol@high, gpt-6.1-sol@high
arena cross-judge pool: inherit-parent
swarm workers: gpt-6.1-sol@medium
architect runners: gpt-6.1-sol@high, gpt-6.1-sol@high
interrogate reviewers: gpt-6.1-sol@high, gpt-6.1-sol@high
