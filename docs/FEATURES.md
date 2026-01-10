# Features Documentation

This document provides a detailed overview of the features available in the Github & Tailscale Automation application.

---

## GitHub Automation

The application provides a comprehensive suite of tools to automate GitHub repository management.

### Bulk Repository Creation

*   **Functionality**: Create multiple GitHub repositories at once with a consistent set of configurations.
*   **How to Use**: Navigate to the **Repositories** tab, specify the number of repositories to create, and define a naming convention (e.g., prefix, auto-generated names). You can also set a default description and toggle visibility (public/private).

### Secret Management

*   **Functionality**: Securely encrypt and upload secrets (e.g., API keys, environment variables) to your GitHub repositories. Secrets are encrypted using PyNaCl before being sent to GitHub, ensuring they are never exposed.
*   **How to Use**: In the **Secrets** tab, you can define shared secrets that will be added to all created repositories. You can also specify repository-specific secrets.

### Workflow Triggers

*   **Functionality**: Manually trigger GitHub Actions workflows for your repositories directly from the application.
*   **How to Use**: Go to the **Actions** tab, select the repositories and the workflow you want to run, and click the trigger button.

### File Management

*   **Functionality**: Upload standard files like `.gitignore`, `LICENSE`, or `CONTRIBUTING.md` to multiple repositories at once.
*   **How to Use**: In the **Files** tab, you can select the files you want to upload, and they will be added to each new repository created.

---

## Tailscale Integration

The application integrates with the Tailscale API to automate secure network operations.

### Auth Key Generation

*   **Functionality**: Generate Tailscale authentication keys with different properties.
    *   **Reusable**: Keys that can be used multiple times to add devices to your network.
    *   **Ephemeral**: Keys for single-use devices that are automatically removed from your network after a period of inactivity.
    *   **Pre-authorized**: Keys that are pre-approved to join your network, bypassing the need for manual device approval.
*   **How to Use**: In the **Secrets** tab, enable Tailscale integration and select the type of key you want to generate.

### Tag Management

*   **Functionality**: Automatically apply Access Control List (ACL) tags to new devices added with a generated key. This is useful for enforcing network policies.
*   **How to Use**: When generating a Tailscale key, you can specify one or more tags to be associated with it.

### Expiry Control

*   **Functionality**: Set an expiration date for generated keys to enhance security.
*   **How to Use**: Define the key's lifespan (e.g., 1 hour, 7 days, 90 days) during the generation process.

---

## System & Diagnostics

The application includes built-in tools for monitoring and troubleshooting.

### Real-time Diagnostics

*   **Functionality**: Perform system health checks to verify network connectivity, API access, and dependency status.
*   **How to Use**: The main dashboard displays the real-time status of critical components. You can also run a full diagnostic check from the command line using `python main.py --check`.

### Robust Logging

*   **Functionality**: All actions are logged to a file for auditing and debugging purposes.
*   **How to Use**: Log files are stored in the `logs/` directory.

### Secure Configuration

*   **Functionality**: Your sensitive API tokens for GitHub and Tailscale are stored in an encrypted format on your local machine.
*   **How to Use**: Configure your tokens in the **Accounts** tab. The application handles the encryption and storage automatically.
