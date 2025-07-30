# GitHub Actions Workflows Quick Start

This guide provides a quick overview of the GitHub Actions workflows set up for the Cluefin project.

## Available Workflows

### 1. CI Pipeline (`ci.yml`)
**Triggers:** Push to main/develop, Pull Requests, Manual dispatch

**What it does:**
- Lints code with ruff
- Runs tests on Python 3.10, 3.11, 3.12
- Generates coverage reports
- Builds the package
- Performs security scans
- Sends notifications on completion

**Manual execution:**
```bash
# Via GitHub UI: Actions tab > CI Pipeline > Run workflow
# Or via GitHub CLI:
gh workflow run ci.yml
```

### 2. Release Pipeline (`release.yml`)
**Triggers:** New GitHub release, Manual dispatch

**What it does:**
- Validates the release with full test suite
- Builds and publishes package to PyPI
- Deploys application (if enabled)
- Sends release notifications

**Manual execution:**
```bash
# Via GitHub UI: Actions tab > Release Pipeline > Run workflow
# Or via GitHub CLI:
gh workflow run release.yml -f version="1.0.0" -f environment="staging"
```

### 3. Dependency Update (`dependency-update.yml`)
**Triggers:** Weekly schedule (Mondays 9 AM UTC), Manual dispatch

**What it does:**
- Updates all dependencies to latest compatible versions
- Runs tests with updated dependencies
- Creates a pull request if updates are successful
- Sends notifications about updates

**Manual execution:**
```bash
# Via GitHub UI: Actions tab > Dependency Update > Run workflow
# Or via GitHub CLI:
gh workflow run dependency-update.yml -f update_type="minor"
```

## Quick Setup Checklist

### Before Running Workflows

1. **Set up required secrets** (see [ENVIRONMENT_VARIABLES.md](ENVIRONMENT_VARIABLES.md)):
   - [ ] `KIWOOM_API_KEY` - For financial data access
   - [ ] `KRX_API_KEY` - For Korea Exchange data
   - [ ] `CODECOV_TOKEN` - For coverage reporting

2. **Set up optional secrets for full functionality**:
   - [ ] `PYPI_TOKEN` - For package publishing
   - [ ] `SLACK_WEBHOOK` - For notifications
   - [ ] `DEPLOY_HOST` / `DEPLOY_SSH_KEY` - For deployment

3. **Configure environment variables**:
   - [ ] `TEST_ENVIRONMENT` = "development"
   - [ ] `LOG_LEVEL` = "INFO"
   - [ ] `ENABLE_INTEGRATION_TESTS` = "false" (initially)

### Testing the Setup

1. **Trigger CI Pipeline:**
   - Make a small change and push to a branch
   - Create a pull request
   - Watch the CI pipeline run

2. **Check workflow status:**
   ```bash
   # List workflow runs
   gh run list
   
   # View specific run
   gh run view <run-id>
   
   # View logs
   gh run view <run-id> --log
   ```

### Common First-Run Issues

1. **Missing dependencies:** Install python-dotenv and requests-mock if tests fail
2. **API key errors:** Set dummy values for development environment initially
3. **Permission errors:** Ensure GitHub token has appropriate permissions

### Environment-Specific Setup

#### Development Environment
- Set `ENABLE_INTEGRATION_TESTS=false`
- Use development/test API keys
- Enable debug logging

#### Production Environment  
- Set `ENABLE_INTEGRATION_TESTS=true`
- Use production API keys
- Enable deployment if needed

## Monitoring and Maintenance

### Workflow Status
- Check workflow status badges in README
- Monitor GitHub Actions tab for failures
- Set up notification webhooks for alerts

### Regular Tasks
- Review dependency update PRs weekly
- Rotate secrets quarterly
- Update workflow configurations as needed

### Troubleshooting
- Check workflow logs for error details
- Verify environment variable configurations
- Test API credentials independently
- Review GitHub Actions documentation

## Additional Resources

- [Environment Variables Setup Guide](ENVIRONMENT_VARIABLES.md)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)