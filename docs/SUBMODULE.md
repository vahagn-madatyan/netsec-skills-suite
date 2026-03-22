# Using netsec-skills-suite as a Git Submodule

This guide covers how to consume `netsec-skills-suite` as a git submodule
in your own projects (NemoNet, OpenClaw forks, custom agent platforms).

## Add as Submodule

```bash
git submodule add https://github.com/vahagn-madatyan/netsec-skills-suite.git skills/netsec-skills-suite
git commit -m "feat: add netsec-skills-suite as submodule"
```

## Initialize After Clone

```bash
git clone --recurse-submodules https://github.com/your-org/your-project.git
# Or if already cloned:
git submodule update --init
```

## Update to Latest

```bash
cd skills/netsec-skills-suite && git pull origin main && cd ../..
git add skills/netsec-skills-suite
git commit -m "chore: bump netsec-skills-suite to latest"
```

## Pin to a Specific Version

```bash
cd skills/netsec-skills-suite && git checkout v1.0.0 && cd ../..
git add skills/netsec-skills-suite
git commit -m "chore: pin netsec-skills-suite to v1.0.0"
```

## OpenClaw extraDirs (Zero-Symlink)

Configure OpenClaw to discover skills directly from the submodule path
without symlinking. Add to your `openclaw.json`:

```json5
{
  skills: {
    load: {
      extraDirs: ["./skills/netsec-skills-suite/skills"],
      watch: true
    }
  }
}
```

## CI: Shallow Clone for Speed

```bash
git submodule update --init --depth 1
```

## Docker: Copy Skills into Container

```dockerfile
COPY skills/netsec-skills-suite/skills/ /sandbox/skills/
```
