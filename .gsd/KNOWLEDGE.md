# Knowledge Base

Recurring gotchas, non-obvious rules, and useful patterns discovered during execution.

## K001: BSD sed frontmatter word count is broken

**Context:** Task/slice plans specify `sed '1,/^---$/d' | sed '1,/^---$/d' | wc -w` to count body words after stripping YAML frontmatter.

**Problem:** On macOS BSD sed, `sed '1,/^---$/d'` matches `---` on line 1 and deletes only line 1 (the range `1,/pattern/` is satisfied immediately since line 1 matches). The second `sed` then deletes through the closing `---`, leaving the body. But if the frontmatter has multi-line values (like `description: >-`), the second sed's range `1,/^---$/` extends through ANY `---` in the body, potentially deleting everything.

**Fix:** Use `awk` instead:
```bash
awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' SKILL.md | wc -w
```

This correctly counts `---` delimiters and emits only content after the second one.

**Discovered:** T01/S01/M002
