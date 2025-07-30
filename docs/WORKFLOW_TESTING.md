# Workflow Testing Example

## Testing the CI Pipeline

To test the GitHub Actions workflows, you can:

### 1. Test via Pull Request (Recommended)
Create a simple change and push to test the CI pipeline:

```bash
# Create a test branch
git checkout -b test-ci-pipeline

# Make a small change (add a comment to any Python file)
echo "# CI pipeline test" >> packages/cluefin-openapi/src/cluefin_openapi/__init__.py

# Commit and push
git add .
git commit -m "test: trigger CI pipeline"
git push origin test-ci-pipeline

# Create a pull request via GitHub UI or CLI
gh pr create --title "Test CI Pipeline" --body "Testing the new GitHub Actions CI pipeline"
```

### 2. Test via Manual Trigger
```bash
# Using GitHub CLI
gh workflow run ci.yml

# Using GitHub UI
# Go to Actions tab > CI Pipeline > Run workflow button
```

### 3. Test Release Pipeline
```bash
# Create a release
gh release create v0.1.0-test --title "Test Release" --notes "Testing release pipeline"

# Or manually trigger
gh workflow run release.yml -f version="0.1.0-test" -f environment="staging"
```

## Expected Results

### CI Pipeline Success Indicators:
- ✅ Linting passes (ruff check)
- ✅ Tests run on Python 3.10, 3.11, 3.12
- ✅ Package builds successfully
- ✅ Security scans pass
- ✅ Coverage report generated

### Workflow Logs Location:
- GitHub repo > Actions tab > Workflow run > Job details

### Status Badge:
The CI status badge in README.md will show the current status:
- 🟢 Passing: All checks successful
- 🔴 Failing: One or more checks failed
- 🟡 Running: Pipeline currently executing

## Troubleshooting First Run

Common issues on first workflow execution:

1. **Missing Secrets**: Some jobs may skip due to missing API keys
   - This is expected - add secrets as needed per docs/ENVIRONMENT_VARIABLES.md

2. **Test Dependencies**: May need to install missing packages
   - Run: `pip install python-dotenv requests-mock`

3. **Integration Tests**: Will be skipped unless `ENABLE_INTEGRATION_TESTS=true`
   - Set environment variables as documented

## Monitoring

- Check workflow runs: `gh run list`
- View specific run: `gh run view <run-id>`
- View logs: `gh run view <run-id> --log`

This completes the GitHub Actions setup for the Cluefin project! 🎉