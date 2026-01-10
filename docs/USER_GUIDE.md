# User Guide

Welcome to the comprehensive user manual for **Github&Tailscale-Automation**. This guide will walk you through every feature of the application, from initial setup to advanced automation workflows.

## Table of Contents
1.  [Getting Started](#getting-started)
2.  [Interface Overview](#interface-overview)
3.  [Managing Accounts](#managing-accounts)
4.  [Bulk Repository Creation](#bulk-repository-creation)
5.  [Managing Secrets](#managing-secrets)
6.  [Tailscale Automation](#tailscale-automation)
7.  [System Diagnostics](#system-diagnostics)

---

## Getting Started

### Prerequisites
Before launching the application, ensure you have:
*   **GitHub Personal Access Token**: Create one at [GitHub Settings > Tokens](https://github.com/settings/tokens).
    *   **Required Scopes**: `repo`, `workflow`, `admin:org` (if using organizations).
*   **Tailscale API Key**: Create one at [Tailscale Admin > Settings > Keys](https://login.tailscale.com/admin/settings/keys).

### First Launch
1.  Run the application using `python main.py` or the executable.
2.  The application will perform a self-check on startup.
3.  You will be greeted by the **Dashboard**.

---

## Interface Overview

The application uses a modern, sidebar-based navigation system:

*   **Sidebar (Left)**: Quick access to all major modules (Accounts, Repositories, Secrets, Tailscale, etc.).
*   **Main Content (Right)**: The active workspace for the selected module.
*   **Status Bar (Bottom)**: Displays real-time status updates and progress.

---

## Managing Accounts

Navigate to the **Accounts** tab to configure your credentials.

1.  **GitHub Token**: Paste your Personal Access Token (starts with `ghp_`).
2.  **Tailscale Key**: Paste your API Key (starts with `tskey-`).
3.  **Tailnet**: Enter your Tailscale organization name (e.g., `example.com` or `user@gmail.com`).
4.  Click **Save Credentials**.
    *   *Note: Credentials are encrypted and stored locally in `configs/config.json`.*

---

## Bulk Repository Creation

This is the core feature for initializing multiple projects simultaneously.

### Step 1: Naming Strategy
Navigate to the **Repositories** tab.
*   **Auto-Generate**: Select a prefix (e.g., `microservice-`, `app-`) and a starting number.
    *   *Example*: `microservice-01`, `microservice-02`...
*   **Custom List**: Manually type a list of names, one per line.
*   **Import File**: Load a `.txt` file containing repository names.

### Step 2: Configuration
*   **Visibility**: Choose `Public` or `Private`.
*   **Features**: Check boxes to enable **Issues**, **Wiki**, or **Projects**.
*   **Auto-Init**: Check this to automatically create a `README.md`.

### Step 3: Execution
Click **Create Repositories**. A progress dialog will show the status of each creation.

---

## Managing Secrets

Securely inject API keys and secrets into your repositories without handling them manually.

### Shared Secrets
These are secrets that apply to **all** repositories you are working on.
1.  Create a text file with `KEY=VALUE` pairs.
    ```env
    AWS_ACCESS_KEY=AKIA...
    DATABASE_URL=postgres://...
    ```
2.  In the **Secrets** tab, browse and select this file.

### Repository-Specific Secrets
1.  Click **Add Secret**.
2.  Enter the Secret Name (e.g., `DEPLOY_KEY`).
3.  Enter the Value.
4.  Select the specific repository it applies to.

---

## Tailscale Automation

Generate authentication keys for your devices instantly.

1.  Navigate to the **Tailscale** tab.
2.  **Key Type**:
    *   **Reusable**: Can be used to authenticate multiple machines (good for server fleets).
    *   **Ephemeral**: Device is removed from network when it goes offline (good for containers/CI).
3.  **Tags**: Enter ACL tags (e.g., `tag:prod`, `tag:web`).
4.  Click **Generate Key**.
5.  Copy the key immediately; it will not be shown again.

---

## System Diagnostics

If you encounter issues, go to the **Monitor** or **About** tab to run diagnostics.

*   **Network Check**: Verifies connectivity to GitHub and Tailscale APIs.
*   **Permission Check**: Ensures the app can write to logs and config files.
*   **Dependency Check**: Verifies all Python libraries are installed correctly.

---

*For technical details, please refer to the [Developer Guide](DEVELOPER_GUIDE.md).*
