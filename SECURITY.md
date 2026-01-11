# 🛡️ Security Policy

We take the security of our application and its users seriously. This document outlines our security practices and provides guidance on how to report vulnerabilities.

## Supported Versions

We are committed to providing security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| `1.x`   | :white_check_mark: |
| `< 1.0` | :x:                |

When a new major version is released, we will continue to support the previous major version with critical security patches for a period of 3 months.

---

## Application Security

### Credential Storage
Your API tokens for GitHub and Tailscale are sensitive credentials. Here is how we handle them:

*   **Local Encryption**: All credentials are encrypted using your operating system's native encryption capabilities and stored in the `configs/config.json` file on your local machine.
*   **No Cloud Storage**: Your credentials are **never** uploaded to or stored on any cloud server. They are only used to communicate directly with the GitHub and Tailscale APIs from your machine.
*   **Git Exclusion**: The `configs/` directory is explicitly excluded from version control via `.gitignore` to prevent accidental exposure.

### API Communication
All communication with the GitHub and Tailscale APIs is performed over HTTPS, ensuring that data transmitted between the application and the services is encrypted in transit.

### Dependency Management
We use a `requirements.txt` file to manage our dependencies. We strive to keep our dependencies up to date to incorporate the latest features and security patches.

---

## User Best Practices

To enhance the security of your own workflow, we recommend the following:

*   **Use Fine-Grained Tokens**: When creating a GitHub Personal Access Token, grant it only the minimum required scopes (`repo`, `workflow`).
*   **Use Ephemeral Keys**: For short-lived environments like CI/CD runners, prefer to generate **ephemeral** Tailscale keys.
*   **Secure Your Machine**: Since credentials are stored locally, ensure your machine is protected with a strong password and full-disk encryption if possible.

---

## Reporting a Vulnerability

If you discover a security vulnerability, we would appreciate your help in disclosing it to us responsibly. Please follow these steps:

1.  **Do not create a public GitHub issue.**
2.  Email the project maintainer directly at **haseebkaloya@gmail.com** with the subject line "Security Vulnerability Report".
3.  Provide a detailed description of the vulnerability, including:
    *   Steps to reproduce it.
    *   The version of the application you are using.
    *   Any relevant screenshots or logs.

We are committed to addressing all security reports in a timely manner. We will acknowledge your email within 48 hours and work with you to understand and resolve the issue.

Thank you for helping to keep our community and project safe.
