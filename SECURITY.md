version: 1.0.0
# Security Policy

This document outlines the security procedures and policies for the **Github & Tailscale Automation** application.

---

## Supported Versions

Security updates are applied to the latest version available in the `main` branch and the most recent official release.

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < 1.0.0 | :x:                |

---

## Data Handling and Storage

This application is designed with security as a priority. Here is how we handle your sensitive data:

*   **Local Storage**: Your GitHub and Tailscale API tokens are stored **only on your local machine** in the `configs/config.json` file.
*   **Encryption**: The API tokens within `config.json` are encrypted using your machine's unique hardware identifiers. This means the configuration file is not portable and will not work on another computer, providing a strong layer of security.
*   **No Cloud Storage**: Your credentials are **never** sent to or stored on any third-party servers or cloud services by this application.

---

## Reporting a Vulnerability

We take all security reports seriously. If you discover a security vulnerability within this project, please follow these steps:

1.  **Do not open a public GitHub issue.** Vulnerabilities should be disclosed privately.
2.  Email the project maintainer directly at **[haseebkaloya@gmail.com](mailto:haseebkaloya@gmail.com)** with the subject line "Security Vulnerability Report: Github & Tailscale Automation".
3.  Provide a detailed description of the vulnerability, including:
    *   The steps to reproduce it.
    *   The version of the application you are using.
    *   Any relevant screenshots or code snippets.

We will acknowledge your report within 48 hours and work with you to understand and resolve the issue. We appreciate your efforts in responsibly disclosing your findings and helping us keep the project safe.
