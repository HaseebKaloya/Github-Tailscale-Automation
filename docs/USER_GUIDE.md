# User Guide

Welcome to the official user guide for the **Github & Tailscale Automation** application. This guide provides a detailed walkthrough of every feature to help you get the most out of the tool.

---

## Table of Contents

1.  [**🚀 Getting Started**](#1--getting-started)
    *   [Installation](#installation)
    *   [Running the Application](#running-the-application)
2.  [**⚙️ Initial Configuration**](#2--initial-configuration)
3.  [**💻 The Dashboard**](#3--the-dashboard)
4.  [**📦 GitHub Automation**](#4--github-automation)
    *   [Repositories Tab](#repositories-tab)
    *   [Secrets Tab](#secrets-tab)
    *   [Files Tab](#files-tab)
    *   [Actions Tab](#actions-tab)
5.  [**🛡️ Tailscale Integration**](#5--tailscale-integration)
6.  [**❓ Getting Help**](#6--getting-help)

---

## 1. 🚀 Getting Started

### Installation

You have two options for installation:

*   **From Source (Recommended for Developers)**:
    1.  Clone the repository: `git clone https://github.com/haseebkaloya/Github-Tailscale-Automation.git`
    2.  Navigate into the directory: `cd Github-Tailscale-Automation`
    3.  Install dependencies: `pip install -r requirements.txt`

*   **From a Release (Recommended for End-Users)**:
    1.  Go to the [Releases Page](https://github.com/haseebkaloya/Github-Tailscale-Automation/releases).
    2.  Download the latest `.exe` file.

### Running the Application

*   **From Source**: Run `python main.py` in your terminal.
*   **From Executable**: Double-click the downloaded `.exe` file. No installation is needed.

---

## 2. ⚙️ Initial Configuration

On first launch, you must configure your API tokens. Navigate to the **Accounts** tab.

![Configuration](screenshots/4.png)
*A view of the Accounts tab for credential management.*

1.  **GitHub Token**: Paste your GitHub Personal Access Token. It must have `repo` and `workflow` scopes.
2.  **Tailscale Key**: Paste your Tailscale API Key.
3.  Click **Save Credentials**. Your tokens will be encrypted and stored locally.

---

## 3. 💻 The Dashboard

The **Monitor** tab serves as your main dashboard, providing real-time system diagnostics.

![Dashboard](screenshots/1.png)
*The main dashboard showing real-time system diagnostics.*

This screen checks:
*   **Network Status**: Verifies connectivity to GitHub and Tailscale APIs.
*   **Dependencies**: Confirms all required libraries are installed.
*   **Permissions**: Ensures the application can write to necessary log and configuration files.

---

## 4. 📦 GitHub Automation

### Repositories Tab

This is the hub for bulk repository management.

![Repository Manager](screenshots/2.png)
*The interface for bulk repository creation.*

1.  **Define Names**: Enter repository names manually, or use the **Auto-Generate** feature to create numbered repositories with a prefix.
2.  **Set Options**: Choose visibility (public/private) and enable features like Issues, Wiki, and Projects.
3.  **Execute**: Click **Create Repositories**. A progress dialog will show the status of each operation.

### Secrets Tab

Securely upload secrets to your repositories. Secrets are encrypted before being sent to GitHub.

1.  Enter the **Secret Name** (e.g., `API_KEY`).
2.  Enter the **Secret Value**.
3.  Select the repositories that should receive this secret.
4.  Click **Add Secret to Repositories**.

### Files Tab

Upload standard files (like `LICENSE` or `.gitignore`) to multiple repositories at once.

1.  Select a standard file from the dropdown (e.g., `MIT License`).
2.  Alternatively, click **Browse** to select a custom file from your local machine.
3.  Choose the repositories to upload the file to.
4.  Click **Upload File**.

### Actions Tab

Manually trigger GitHub Actions workflows.

1.  Select one or more repositories.
2.  Choose the workflow you wish to run from the dropdown menu.
3.  Click **Trigger Workflow**.

---

## 5. 🛡️ Tailscale Integration

Generate Tailscale authentication keys directly from the application.

![Tailscale Integration](screenshots/3.png)
*The interface for generating Tailscale auth keys.*

1.  Navigate to the **Secrets** tab and then the **Tailscale** sub-tab.
2.  Choose the **Key Type**:
    *   **Reusable**: For servers or long-lived devices.
    *   **Ephemeral**: For CI/CD runners or temporary containers. The device is removed from your tailnet when it goes offline.
3.  (Optional) Add **ACL Tags** to apply to the device (e.g., `tag:server`).
4.  Click **Generate Key**. The key will be displayed once and copied to your clipboard. **Store it immediately**, as it will not be shown again.

---

## 6. ❓ Getting Help

If you encounter any issues:

*   First, check the **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** guide for common solutions.
*   If the issue persists, please [open an issue](https://github.com/haseebkaloya/Github-Tailscale-Automation/issues) on our GitHub repository.
