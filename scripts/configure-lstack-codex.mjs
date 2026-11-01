#!/usr/bin/env node

import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const skills = join(root, "pstack", "skills");
const check = process.argv.includes("--check");
const adapter = "In Codex, first read [the Codex adapter](../../docs/harness/codex.md) once per task. It replaces the Cursor tool and model instructions below.";
const policy = "policy:\n  allow_implicit_invocation: false\n";
const cursorNames = /\bTask\b|AskQuestion|todolist|todo list|generalPurpose|poteto-agent|comment-sicko|readonly:|run_in_background|cloud_base_branch|file_attachments|\b(?:claude|grok|gpt)-\d|claude-opus|inherit-parent|\.cursor|Cursor|the \*\*[^*]+\*\* skill/;
let errors = 0;
let count = 0;

for (const name of readdirSync(skills).sort()) {
  const path = join(skills, name, "SKILL.md");
  if (!existsSync(path)) continue;
  const source = readFileSync(path, "utf8");
  const needsAdapter = readdirSync(join(skills, name), { recursive: true })
    .filter((file) => file.endsWith(".md"))
    .some((file) => cursorNames.test(readFileSync(join(skills, name, file), "utf8")));
  const expected = !needsAdapter || source.includes(adapter) ? source : source.replace(/^(# .*)\n+/m, `$1\n\n${adapter}\n\n`);
  if (needsAdapter && !expected.includes(adapter)) throw new Error(`${path} has no heading`);
  const metadata = join(skills, name, "agents", "openai.yaml");
  const current = existsSync(metadata) ? readFileSync(metadata, "utf8") : "";
  if (current && current !== policy) throw new Error(`Inspect existing metadata before replacing ${metadata}`);
  for (const [file, actual, wanted] of [[path, source, expected], [metadata, current, policy]]) {
    if (actual === wanted) continue;
    if (check) {
      console.error(`Out of date: ${file}`);
      errors++;
    } else {
      mkdirSync(dirname(file), { recursive: true });
      writeFileSync(file, wanted);
    }
  }
  count++;
}

if (!existsSync(join(root, "pstack", "docs", "harness", "codex.md"))) throw new Error("Missing Codex adapter");
const marketplace = JSON.parse(readFileSync(join(root, ".agents", "plugins", "marketplace.json"), "utf8"));
const manifest = JSON.parse(readFileSync(join(root, "pstack", ".codex-plugin", "plugin.json"), "utf8"));
if (marketplace.plugins[0].name !== manifest.name || manifest.skills !== "./skills/") throw new Error("Codex plugin registration mismatch");
console.log(`${count} skills ${check ? "checked" : "configured"}; ${errors} errors`);
process.exitCode = errors ? 1 : 0;
