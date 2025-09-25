# Git Branching Cheat Sheet

A quick reference for safely experimenting with code without breaking your main project.

## Core Branching Commands

### Creating and Switching Branches
```bash
# Create and switch to new branch (older syntax)
git checkout -b branch-name

# Create and switch to new branch (newer syntax)
git switch -c branch-name

# Switch to existing branch
git checkout branch-name
git switch branch-name
```

### Viewing Branches
```bash
# List all local branches (* shows current branch)
git branch

# List all branches (local and remote)
git branch -a

# Show current branch
git branch --show-current
```

## Safe Experimentation Workflow

### 1. Before Starting Experiments
```bash
# Check status and commit any changes
git status
git add .
git commit -m "Save current working state"

# Create backup of working code
git checkout -b working-backup
git checkout main
```

### 2. Create Experiment Branch
```bash
# Create branch for testing new features
git checkout -b experiment-feature-name
```

### 3. After Experimenting

**If experiments worked:**
```bash
# Switch back to main
git checkout main

# Merge successful changes
git merge experiment-feature-name

# Delete experiment branch (optional)
git branch -d experiment-feature-name
```

**If experiments failed:**
```bash
# Simply switch back to main - your original code is untouched!
git checkout main

# Delete failed experiment branch
git branch -D experiment-feature-name  # Force delete
```

## Useful Branch Management

### Merging
```bash
# Merge branch into current branch
git merge branch-name

# Merge with commit message
git merge branch-name -m "Merge feature: description"
```

### Cleaning Up
```bash
# Delete merged branch
git branch -d branch-name

# Force delete branch (even if not merged)
git branch -D branch-name

# Delete remote branch
git push origin --delete branch-name
```

### Remote Branches
```bash
# Push branch to GitHub
git push origin branch-name

# Set upstream for future pushes
git push -u origin branch-name

# Pull latest changes
git pull origin branch-name
```

## Emergency Commands

### Undo Changes (Before Commit)
```bash
# Discard all changes in working directory
git checkout .

# Discard changes to specific file
git checkout filename.py
```

### Undo Last Commit (Keep Changes)
```bash
git reset --soft HEAD~1
```

### See What Changed
```bash
# Show differences
git diff

# Show commit history
git log --oneline
```

## Quick Reference Workflow

1. **Start experimenting:** `git checkout -b experiment-name`
2. **Make changes and test**
3. **If good:** `git checkout main` → `git merge experiment-name`
4. **If bad:** `git checkout main` (changes automatically discarded)
5. **Clean up:** `git branch -d experiment-name`

## Pro Tips

- Always commit working code before creating experiment branches
- Use descriptive branch names: `fix-login-bug`, `add-database-feature`
- Create a `working-backup` branch before major experiments
- Use `git status` frequently to see what's changed
- Experiment branches are cheap - create as many as you need!

---
*Remember: Your main branch stays safe no matter what you do in experiment branches!*