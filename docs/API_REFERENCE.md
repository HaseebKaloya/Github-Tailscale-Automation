# API Reference

Technical documentation for the internal API wrappers.

## GitHubAPI

**Module**: `api.github_api`

The `GitHubAPI` class wraps the `PyGithub` library to provide simplified methods for automation.

### Initialization
```python
api = GitHubAPI(token="ghp_...", username="octocat")
```

### Methods

#### `create_repository`
Creates a new repository.

```python
def create_repository(
    name: str,
    description: str = "",
    private: bool = True,
    auto_init: bool = True,
    has_issues: bool = True,
    has_wiki: bool = False,
    has_projects: bool = False
) -> Tuple[bool, Any]
```
*   **Returns**: `(True, RepositoryObject)` on success, or `(False, ErrorMessage)` on failure.

#### `upload_file`
Uploads or updates a file in a repository.

```python
def upload_file(
    repo_name: str,
    file_path: str,
    content: str,
    commit_message: str = "Automated upload"
) -> bool
```

#### `create_secret`
Encrypts and uploads a secret using PyNaCl.

```python
def create_secret(
    repo_name: str,
    secret_name: str,
    secret_value: str
) -> bool
```

---

## TailscaleAPI

**Module**: `api.tailscale_api`

The `TailscaleAPI` class handles direct HTTP communication with the Tailscale Control Plane.

### Initialization
```python
ts_api = TailscaleAPI(api_key="tskey-...", tailnet="example.com")
```

### Methods

#### `generate_auth_key`
Generates a new authentication key.

```python
def generate_auth_key(
    expiry_days: int = 90,
    reusable: bool = True,
    ephemeral: bool = False,
    preauthorized: bool = True,
    tags: Optional[List[str]] = None
) -> Tuple[bool, str]
```
*   **Returns**: `(True, "tskey-auth-...")` on success, or `(False, ErrorMessage)` on failure.
