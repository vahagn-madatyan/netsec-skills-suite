#!/usr/bin/env bash
# validate.sh — Custom convention validator for network-security-skills-suite.
# Enforces requirements beyond what `agentskills validate` checks:
#   1. metadata.safety exists and is 'read-only' or 'read-write'
#   2. All required body sections present as H2 headers
#   3. references/ directory exists alongside SKILL.md
#
# Usage: bash scripts/validate.sh [skills_dir]
# Default skills_dir: skills/
# Exit code: 0 if all checks pass, 1 if any fail.

set -euo pipefail

SKILLS_DIR="${1:-skills}"
ERRORS=0
SKILLS_CHECKED=0

# Required H2 sections in SKILL.md body (after frontmatter)
REQUIRED_SECTIONS=(
  "When to Use"
  "Prerequisites"
  "Procedure"
  "Threshold Tables"
  "Decision Trees"
  "Report Template"
  "Troubleshooting"
)

# Valid values for metadata.safety
VALID_SAFETY_VALUES=("read-only" "read-write")

log_error() {
  echo "  ERROR: $1" >&2
  ERRORS=$((ERRORS + 1))
}

log_ok() {
  echo "  OK: $1"
}

# Extract YAML frontmatter (between --- markers) from a SKILL.md file.
extract_frontmatter() {
  local file="$1"
  sed -n '/^---$/,/^---$/p' "$file" | sed '1d;$d'
}

# Extract metadata.safety value from frontmatter.
# Handles both inline (metadata: {safety: value}) and block YAML styles.
get_safety_value() {
  local frontmatter="$1"
  # Try block style: metadata:\n  safety: value
  local safety
  safety=$(echo "$frontmatter" | awk '
    /^metadata:/ { in_meta=1; next }
    in_meta && /^  safety:/ { gsub(/^  safety:[[:space:]]*/, ""); gsub(/[[:space:]]*$/, ""); print; exit }
    in_meta && /^[^ ]/ { exit }
  ')
  echo "$safety"
}

# Check if a value is in the valid safety values list.
is_valid_safety() {
  local value="$1"
  for valid in "${VALID_SAFETY_VALUES[@]}"; do
    if [[ "$value" == "$valid" ]]; then
      return 0
    fi
  done
  return 1
}

# Main validation loop
if [[ ! -d "$SKILLS_DIR" ]]; then
  echo "FAIL: Skills directory '$SKILLS_DIR' does not exist." >&2
  exit 1
fi

skill_dirs=()
while IFS= read -r -d '' skill_file; do
  skill_dirs+=("$(dirname "$skill_file")")
done < <(find "$SKILLS_DIR" -name "SKILL.md" -print0 2>/dev/null)

if [[ ${#skill_dirs[@]} -eq 0 ]]; then
  echo "FAIL: No SKILL.md files found in '$SKILLS_DIR'." >&2
  exit 1
fi

for skill_dir in "${skill_dirs[@]}"; do
  skill_file="$skill_dir/SKILL.md"
  skill_name=$(basename "$skill_dir")
  SKILLS_CHECKED=$((SKILLS_CHECKED + 1))

  echo ""
  echo "Checking: $skill_name ($skill_file)"
  echo "---"

  # --- Check 1: metadata.safety exists and has a valid value ---
  frontmatter=$(extract_frontmatter "$skill_file")

  if [[ -z "$frontmatter" ]]; then
    log_error "No YAML frontmatter found (missing --- delimiters)"
  else
    safety_value=$(get_safety_value "$frontmatter")

    if [[ -z "$safety_value" ]]; then
      log_error "metadata.safety is missing from frontmatter"
    elif is_valid_safety "$safety_value"; then
      log_ok "metadata.safety: $safety_value"
    else
      log_error "metadata.safety has invalid value '$safety_value' (expected: read-only or read-write)"
    fi
  fi

  # --- Check 2: All required body sections present as H2 headers ---
  # Extract body content (after second --- marker)
  body=$(awk 'BEGIN{c=0} /^---$/{c++; if(c==2){found=1; next}} found{print}' "$skill_file")

  for section in "${REQUIRED_SECTIONS[@]}"; do
    if echo "$body" | grep -q "^## ${section}"; then
      log_ok "Section found: ## $section"
    else
      log_error "Missing required section: ## $section"
    fi
  done

  # --- Check 3: references/ directory exists ---
  if [[ -d "$skill_dir/references" ]]; then
    ref_count=$(find "$skill_dir/references" -type f | wc -l | tr -d ' ')
    log_ok "references/ directory exists ($ref_count files)"
  else
    log_error "references/ directory missing (expected at: $skill_dir/references/)"
  fi
done

echo ""
echo "================================"
echo "Skills checked: $SKILLS_CHECKED"
if [[ $ERRORS -eq 0 ]]; then
  echo "Result: PASS (0 errors)"
  exit 0
else
  echo "Result: FAIL ($ERRORS errors)"
  exit 1
fi
