# Environment Variables Setup Guide

This document provides a comprehensive guide for setting up and managing environment variables for the Cluefin project's GitHub Actions workflows.

## Overview

The Cluefin project uses GitHub Actions for continuous integration, testing, and deployment. Environment variables are used to configure the workflows securely and flexibly across different environments.

## Types of Environment Variables

### 1. Repository Secrets
Secrets are encrypted environment variables that store sensitive information like API keys, tokens, and credentials.

### 2. Environment Variables
Environment-specific variables that can be configured per environment (development, staging, production).

### 3. Workflow Variables
Variables that are directly defined in the workflow files for configuration.

## Required Environment Variables and Secrets

### Repository Secrets (Settings > Secrets and variables > Actions > Secrets)

#### API Keys and Credentials
- `KIWOOM_API_KEY`: API key for Kiwoom financial data service
- `KIWOOM_SECRET_KEY`: Secret key for Kiwoom financial data service  
- `KRX_API_KEY`: API key for Korea Exchange (KRX) data service

#### Deployment and Publishing
- `PYPI_TOKEN`: Token for publishing packages to PyPI
- `TEST_PYPI_TOKEN`: Token for publishing packages to Test PyPI
- `DEPLOY_HOST`: Hostname for deployment server
- `DEPLOY_USER`: Username for deployment server
- `DEPLOY_SSH_KEY`: SSH private key for deployment server access
- `DATABASE_URL`: Database connection string for production
- `REDIS_URL`: Redis connection string for caching

#### Integration and Notifications
- `CODECOV_TOKEN`: Token for uploading coverage reports to Codecov
- `SLACK_WEBHOOK`: Webhook URL for Slack notifications
- `DISCORD_WEBHOOK`: Webhook URL for Discord notifications
- `TEAMS_WEBHOOK`: Webhook URL for Microsoft Teams notifications
- `DEPENDENCY_UPDATE_TOKEN`: GitHub token with repo permissions for automated dependency updates

### Environment Variables (Settings > Secrets and variables > Actions > Variables)

#### Testing Configuration
- `TEST_ENVIRONMENT`: Environment name for testing (development/staging/production)
- `LOG_LEVEL`: Logging level (DEBUG/INFO/WARNING/ERROR)
- `ENABLE_INTEGRATION_TESTS`: Whether to run integration tests (true/false)

#### Deployment Configuration  
- `ENABLE_DEPLOYMENT`: Whether to enable deployment steps (true/false)

## Setting Up Environment Variables

### Step 1: Access Repository Settings
1. Navigate to your GitHub repository
2. Click on "Settings" tab
3. In the left sidebar, click "Secrets and variables" > "Actions"

### Step 2: Add Repository Secrets
1. Click on the "Secrets" tab
2. Click "New repository secret"
3. Enter the secret name (e.g., `KIWOOM_API_KEY`)
4. Enter the secret value
5. Click "Add secret"

Repeat for all required secrets listed above.

### Step 3: Add Environment Variables
1. Click on the "Variables" tab
2. Click "New repository variable"
3. Enter the variable name (e.g., `TEST_ENVIRONMENT`)
4. Enter the variable value (e.g., `development`)
5. Click "Add variable"

Repeat for all required variables listed above.

### Step 4: Configure Environment-Specific Variables
For more advanced setups, you can create environment-specific variable sets:

1. Go to "Settings" > "Environments"
2. Click "New environment"
3. Enter environment name (e.g., "development", "staging", "production")
4. Add environment-specific secrets and variables
5. Configure protection rules if needed

## Environment Configuration Examples

### Development Environment
```yaml
Variables:
  TEST_ENVIRONMENT: development
  LOG_LEVEL: DEBUG
  ENABLE_INTEGRATION_TESTS: false

Secrets:
  KIWOOM_API_KEY: dev_api_key_here
  KRX_API_KEY: dev_krx_key_here
```

### Staging Environment
```yaml
Variables:
  TEST_ENVIRONMENT: staging
  LOG_LEVEL: INFO
  ENABLE_INTEGRATION_TESTS: true
  ENABLE_DEPLOYMENT: true

Secrets:
  KIWOOM_API_KEY: staging_api_key_here
  KRX_API_KEY: staging_krx_key_here
  TEST_PYPI_TOKEN: test_pypi_token_here
  DEPLOY_HOST: staging.example.com
```

### Production Environment
```yaml
Variables:
  TEST_ENVIRONMENT: production
  LOG_LEVEL: WARNING
  ENABLE_INTEGRATION_TESTS: true
  ENABLE_DEPLOYMENT: true

Secrets:
  KIWOOM_API_KEY: prod_api_key_here
  KRX_API_KEY: prod_krx_key_here
  PYPI_TOKEN: pypi_token_here
  DEPLOY_HOST: production.example.com
  DATABASE_URL: postgresql://prod_db_url
  REDIS_URL: redis://prod_redis_url
```

## Workflow Configuration

### Environment Usage in Workflows
The workflows are configured to use these environment variables in different contexts:

#### CI Pipeline (`ci.yml`)
- Uses development environment by default
- API keys for running integration tests
- Codecov token for coverage reporting
- Notification webhooks for status updates

#### Release Pipeline (`release.yml`)  
- Uses production environment for releases
- PyPI tokens for package publishing
- Deployment credentials for application deployment
- Notification webhooks for release status

#### Dependency Update (`dependency-update.yml`)
- Uses development environment
- GitHub token for creating pull requests
- Notification webhooks for update status

### Security Best Practices

1. **Use Secrets for Sensitive Data**: Always use GitHub secrets for API keys, tokens, passwords, and other sensitive information.

2. **Environment Separation**: Use different API keys and credentials for different environments.

3. **Least Privilege**: Only grant the minimum necessary permissions for each token or key.

4. **Regular Rotation**: Regularly rotate API keys and tokens.

5. **Monitor Usage**: Monitor the usage of your API keys and tokens for unusual activity.

6. **Environment Protection**: Use GitHub environment protection rules for production environments.

## Troubleshooting

### Common Issues

#### Secret Not Available
If a secret is not available in a workflow:
1. Check the secret name spelling in both the workflow file and GitHub settings
2. Ensure the secret is added to the correct repository
3. Check if the workflow is running in the correct environment context

#### Integration Tests Failing
If integration tests fail due to API access:
1. Verify API keys are correctly set in secrets
2. Check if API keys have necessary permissions
3. Ensure the API service is accessible from GitHub Actions runners

#### Deployment Issues
If deployment fails:
1. Verify deployment secrets (SSH keys, hostnames, etc.)
2. Check network connectivity to deployment targets
3. Ensure deployment credentials have necessary permissions

### Getting Help

1. Check GitHub Actions logs for specific error messages
2. Verify environment variable and secret configurations
3. Test API credentials independently
4. Review GitHub Actions documentation for troubleshooting

## Maintenance

### Regular Tasks
1. **Review and rotate secrets** quarterly
2. **Update API keys** when they expire
3. **Monitor workflow execution** for failures
4. **Update documentation** when adding new variables

### Security Audits
1. **Review access permissions** regularly
2. **Check for unused secrets** and remove them
3. **Validate environment configurations** match current requirements
4. **Monitor for security vulnerabilities** in dependencies

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [GitHub Environments Documentation](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
- [Security Hardening for GitHub Actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)