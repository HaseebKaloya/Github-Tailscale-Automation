# Troubleshooting Guide

This document lists common issues encountered when using **Github&Tailscale-Automation** and their solutions.

## Common Issues

### 1. "Authentication Failed" or "Bad Credentials"
**Symptoms**:
*   Red error banner when testing connection.
*   Logs show `401 Unauthorized`.

**Solution**:
*   **GitHub**: Ensure your Personal Access Token has not expired. Regenerate it with `repo` and `workflow` scopes.
*   **Tailscale**: Ensure your API Key is valid. Check if the key has expired in the Tailscale Admin Console.
*   **Action**: Go to **Accounts** tab and re-enter your credentials.

### 2. "Repository Creation Failed"
**Symptoms**:
*   Progress bar stops or turns red.
*   Error message: `name already exists on this account`.

**Solution**:
*   Repository names must be unique within your account.
*   Check if you have reached the rate limit (secondary API limit). Wait a few minutes and try again.
*   Check `logs/app_YYYYMMDD.log` for specific error details.

### 3. "Network Unreachable"
**Symptoms**:
*   Diagnostics show "Internet connection: FAILED".

**Solution**:
*   Check your internet connection.
*   If you are behind a corporate proxy, set the `HTTP_PROXY` and `HTTPS_PROXY` environment variables before running the application.

### 4. "Permission Denied" (Windows)
**Symptoms**:
*   App fails to start or crash immediately.
*   Diagnostics show "Write access: DENIED".

**Solution**:
*   Ensure you are not running the app from a protected folder (like `C:\Program Files`) without Admin privileges.
*   Move the application folder to your Desktop or Documents folder.
*   Right-click `main.py` or the executable and select **Run as Administrator**.

### 5. Application UI looks broken or too small
**Symptoms**:
*   Text is overlapping or buttons are tiny.

**Solution**:
*   This is often a High-DPI scaling issue.
*   The application attempts to auto-scale, but you can force it by changing Windows Display Settings to 100% scaling.
*   Or, set environment variable `QT_AUTO_SCREEN_SCALE_FACTOR=1`.

---

## Using Recovery Mode

If a bulk operation (like creating 50 repositories) crashes halfway:

1.  Do **not** delete the `recovery/` folder.
2.  Restart the application.
3.  Check the logs. The application is designed to save the state of failed operations.
4.  (Advanced) You can manually inspect `recovery/session_*.json` to see which repositories were created successfully and which failed.

## Logs

Logs are your best friend for troubleshooting.
*   **Location**: `logs/` directory in the application folder.
*   **Format**: `app_YYYYMMDD.log`.
*   **Level**: Search for `ERROR` or `CRITICAL` tags in the log file.

---

## Getting Support

If you cannot resolve the issue:
1.  Run the diagnostics check (`python main.py --check`).
2.  Copy the output.
3.  Open an issue on GitHub with the diagnostics output and the relevant section of the log file.
