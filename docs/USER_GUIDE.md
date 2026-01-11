# 📘 User Guide

Welcome to the comprehensive user manual for **Github & Tailscale Automation**. This guide will walk you through every feature of the application, from initial setup to advanced automation workflows.

## Table of Contents
1.  [Getting Started](#-getting-started)
2.  [Interface Overview](#-interface-overview)
3.  [Managing Accounts](#-managing-accounts)
4.  [Bulk Repository Creation](#-bulk-repository-creation)
5.  [Managing Secrets](#-managing-secrets)
6.  [Tailscale Automation](#-tailscale-automation)
7.  [System Diagnostics](#-system-diagnostics)

---

## 🚀 Getting Started

### Prerequisites
Before launching the application, ensure you have the following credentials ready:

*   **GitHub Personal Access Token**: Create one at [GitHub Settings > Tokens](https://github.com/settings/tokens).
    *   **Required Scopes**: `repo`, `workflow`, `admin:org` (if using organizations).
*   **Tailscale API Key**: Create one at [Tailscale Admin > Settings > Keys](https://login.tailscale.com/admin/settings/keys).

> **💡 Tip:** Store these keys in a secure password manager. The application will encrypt and store them locally, but it's always good practice to have a backup.

### First Launch
1.  Run the application using the provided `.exe` or by running `python main.py` from the source.
2.  On first launch, the application will perform a self-check to ensure all dependencies are met.
3.  You will be greeted by the **Dashboard**, which provides a real-time overview of your system's status.

---

## 🖥️ Interface Overview

The application is designed to be intuitive and easy to navigate:

*   **Sidebar (Left)**: Your command center. Quickly access all major modules like Accounts, Repositories, Secrets, and Tailscale.
*   **Main Content (Right)**: The active workspace where you'll perform all your tasks.
*   **Status Bar (Bottom)**: Keep an eye on this for real-time feedback, progress updates, and success messages.

---

## 🔑 Managing Accounts

This is the first and most important step. Navigate to the **Accounts** tab to configure your API credentials.

1.  **GitHub Token**: Paste your Personal Access Token (it should start with `ghp_`).
2.  **Tailscale Key**: Paste your API Key (it should start with `tskey-`).
3.  **Tailnet**: Enter your Tailscale organization name (e.g., `example.com` or your personal `user@gmail.com`).
4.  Click **Save Credentials**.

> **🔒 Security Note:** Your credentials are encrypted using your machine's unique key and stored locally in the `configs/config.json` file. They are never transmitted anywhere except directly to the respective APIs.

---

## 📦 Bulk Repository Creation

This is the core feature for initializing multiple projects simultaneously.

### Step 1: Define Your Naming Strategy
Navigate to the **Repositories** tab and choose your preferred method:
*   **Auto-Generate**: Ideal for creating a series of related repositories. Just set a prefix (e.g., `microservice-`) and a starting number.
    *   *Example Output*: `microservice-01`, `microservice-02`, ...
*   **Custom List**: Manually type or paste a list of repository names, with each name on a new line.
*   **Import from File**: Load a `.txt` file containing one repository name per line.

### Step 2: Configure Repository Settings
*   **Visibility**: Choose `Public` or `Private` for all repositories in the batch.
*   **Features**: Use the checkboxes to enable **Issues**, **Wiki**, or **Projects**.
*   **Auto-Init**: Check this to automatically initialize each repository with a `README.md` file.

### Step 3: Execute
Click **Create Repositories**. A progress dialog will appear, showing the real-time status of each API call.

---

## 🤫 Managing Secrets

Securely inject API keys, environment variables, and other secrets into your repositories in bulk.

### Shared Secrets
These are secrets that will be applied to **all** repositories created in a batch.
1.  Create a simple text file with `KEY=VALUE` pairs. Comments are ignored.
    ```env
    # API Keys
    AWS_ACCESS_KEY=AKIA...
    DATABASE_URL="postgres://user:pass@host:port/db"
    ```
2.  In the **Secrets** tab, click **Browse** and select this file.

### Repository-Specific Secrets
For secrets that only belong to a single repository:
1.  Click the **Add Secret** button.
2.  Enter the **Secret Name** (e.g., `DEPLOY_KEY`).
3.  Paste the **Value**.
4.  Select the target repository from the dropdown menu.

---

## 🌐 Tailscale Automation

Generate Tailscale authentication keys for your devices and servers instantly.

1.  Navigate to the **Tailscale** tab.
2.  Choose the **Key Type**:
    *   **Reusable**: Can be used to authenticate multiple machines. Best for server fleets or development environments.
    *   **Ephemeral**: The device is automatically removed from your network after it goes offline. Ideal for CI/CD runners or containerized services.
3.  **Add Tags**: Apply ACL tags to the key (e.g., `tag:prod`, `tag:web`) to enforce network policies from the moment a device connects.
4.  Click **Generate Key**.

> **⚠️ Important:** Copy the generated key immediately and store it in a safe place. For security reasons, it will not be shown again.

---

## 🩺 System Diagnostics

If you encounter issues, the **Monitor** tab provides tools to help you troubleshoot.

*   **Network Check**: Verifies connectivity to the GitHub and Tailscale APIs.
*   **Permission Check**: Ensures the application has the necessary permissions to write to its logs and configuration files.
*   **Dependency Check**: Verifies that all required Python libraries are installed and up to date.

---

*For more technical information, including API details and contribution guidelines, please refer to the [Developer Guide](DEVELOPER_GUIDE.md).*
