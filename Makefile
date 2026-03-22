.PHONY: validate audit manifest check

# Spec + convention validation
validate:
	@echo "=== Spec validation (agentskills) ==="
	@failed=0; \
	for skill_dir in skills/*/; do \
		if ! agentskills validate "$$skill_dir"; then \
			failed=1; \
		fi; \
	done; \
	if [ "$$failed" -ne 0 ]; then echo "FAIL: spec validation"; exit 1; fi
	@echo ""
	@echo "=== Convention validation ==="
	bash scripts/validate.sh

# Security audit on all skills
audit:
	@echo "=== Security audit ==="
	python3 scripts/skill_security_auditor.py skills/

# Manifest drift + schema check
manifest:
	@echo "=== Manifest validation ==="
	@python3 -c " \
import json, os, sys; \
m = json.load(open('manifest.json')); \
errors = []; \
[errors.append(f'Missing required key: {k}') for k in ['name','version','skills','profiles'] if k not in m]; \
skill_names = set(); \
skill_dirs = {d for d in os.listdir('skills') if os.path.isfile(os.path.join('skills', d, 'SKILL.md'))}; \
[skill_names.add(s.get('name','')) or errors.extend( \
    [f'Skill {s.get(\"name\",\"?\")} missing field: {f}' for f in ['name','path','safetyTier'] if f not in s] + \
    ([f'Skill {s.get(\"name\")}: invalid safetyTier'] if s.get('safetyTier') not in ('read-only','read-write') else []) \
) for s in m.get('skills', [])]; \
missing = skill_dirs - skill_names; \
stale = skill_names - skill_dirs; \
errors += [f'Skills on disk but not in manifest: {missing}'] if missing else []; \
errors += [f'Skills in manifest but not on disk: {stale}'] if stale else []; \
[errors.extend([f'Profile {p} references unknown skill: {s}' for s in (pr.get('skills',[]) if pr.get('skills') != '*' else []) if s not in skill_names]) for p, pr in m.get('profiles',{}).items()]; \
[print(f'ERROR: {e}', file=sys.stderr) for e in errors] if errors else print(f'manifest.json: valid ({len(skill_names)} skills, {len(m[\"profiles\"])} profiles)'); \
sys.exit(1 if errors else 0) \
"

# Run everything
check: validate manifest
	@echo ""
	@echo "=== All checks passed ==="
