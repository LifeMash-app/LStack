# LifeMash pstack model configuration

# Role values use model@effort. auto and inherit-parent follow the session.
# Panel entries each run one delegate, subject to repository authorization.
# Astra requires an explicit user request under the Codex adapter's limit.
# budget: small (medium)
default effort: medium
feature, refactoring: gpt-6.2-sol@medium
bug-fix: gpt-6.2-sol@medium
perf-issue: gpt-6.2-sol@medium
hillclimb: gpt-6.2-sol@medium
judgment and prose: gpt-6.2-sol@medium
arena runners: gpt-6.2-sol@high, gpt-6.2-sol@high
arena cross-judge pool: inherit-parent
swarm workers: gpt-6.2-sol@medium
interrogate reviewers: gpt-6.2-sol@high, gpt-6.2-sol@high
