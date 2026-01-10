"""
Application constants for Github&Tailscale-Automation
Author: Haseeb Kaloya
"""

# Application Information
APP_NAME = "Github&Tailscale-Automation"
APP_VERSION = "2.0.0 (Python Edition)"
AUTHOR_NAME = "Haseeb Kaloya"
AUTHOR_EMAIL = "haseebkaloya@gmail.com"
AUTHOR_CONTACT = "03451622556"

# Window Settings
WINDOW_TITLE = f"{APP_NAME} | Developed by 🔥{AUTHOR_NAME}🔥"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 750
WINDOW_MIN_WIDTH = 1000
WINDOW_MIN_HEIGHT = 750

# Colors (Hex)
COLOR_PRIMARY = "#0078D4"      # Windows Blue
COLOR_SUCCESS = "#00B050"      # Green
COLOR_ERROR = "#C00000"        # Red
COLOR_WARNING = "#FFC000"      # Orange
COLOR_BACKGROUND = "#F5F5F5"   # Light Gray
COLOR_TEXT = "#000000"         # Black
COLOR_TEXT_SECONDARY = "#666666"  # Gray

# Repository Settings
MIN_REPO_COUNT = 1
MAX_REPO_COUNT = 100
DEFAULT_REPO_COUNT = 10

# Naming Strategies
STRATEGY_AUTO_GENERATE = "AutoGenerate"
STRATEGY_CUSTOM = "Custom"
STRATEGY_SEQUENTIAL = "Sequential"
STRATEGY_IMPORT_FILE = "ImportFile"

NAMING_STRATEGIES = [
    STRATEGY_AUTO_GENERATE,
    STRATEGY_CUSTOM,
    STRATEGY_SEQUENTIAL,
    STRATEGY_IMPORT_FILE
]

# Professional auto-generate prefixes - organized by categories for maximum diversity
AUTO_GEN_PREFIXES = [
    # Tech/Dev Terms (24 items)
    "nexus", "vertex", "core", "edge", "flux", "quantum", "matrix", "prism", 
    "cipher", "node", "apex", "zenith", "pixel", "debug", "spark", "forge",
    "pulse", "byte", "scope", "drift", "mesh", "sync", "lens", "vault",
    
    # Business/Professional (16 items) 
    "atlas", "titan", "summit", "prime", "elite", "fusion", "beacon", "crown",
    "phoenix", "orbit", "stellar", "lunar", "solar", "cosmic", "nova", "azure",
    
    # Modern/Creative (16 items)
    "echo", "vibe", "flow", "wave", "bloom", "craft", "shift", "twist",
    "spark", "glow", "rush", "dash", "leap", "rise", "zoom", "flex",
    
    # Abstract/Elegant (14 items)
    "essence", "vision", "dream", "infinity", "harmony", "serenity", "clarity", "grace",
    "unity", "balance", "wisdom", "truth", "light", "hope"
]

# Category-based naming for even more professional results
NAMING_CATEGORIES = {
    "tech": ["nexus", "vertex", "core", "edge", "flux", "quantum", "matrix", "prism", 
             "cipher", "node", "apex", "zenith", "pixel", "debug", "spark", "forge"],
    "business": ["atlas", "titan", "summit", "prime", "elite", "fusion", "beacon", "crown",
                 "phoenix", "orbit", "stellar", "lunar", "solar", "cosmic", "nova", "azure"],
    "creative": ["echo", "vibe", "flow", "wave", "bloom", "craft", "shift", "twist",
                 "pulse", "glow", "rush", "dash", "leap", "rise", "zoom", "flex"],
    "elegant": ["essence", "vision", "dream", "infinity", "harmony", "serenity", "clarity", "grace",
                "unity", "balance", "wisdom", "truth", "light", "hope"]
}

# Tailscale Settings
TAILSCALE_KEY_EXPIRY_DAYS = 90
TAILSCALE_API_BASE_URL = "https://api.tailscale.com/api/v2"

# GitHub Settings
GITHUB_API_BASE_URL = "https://api.github.com"
GITHUB_DEFAULT_BRANCH = "main"

# File Paths
DEFAULT_WORKFLOW_TARGET = ".github/workflows/main.yml"
DEFAULT_PROJECT_TARGET = "ProjectFiles"

# Tab Names
TAB_ACCOUNTS = "Accounts"
TAB_FILES = "Files"
TAB_REPOSITORIES = "Repositories"
TAB_SECRETS = "Secrets"
TAB_ACTIONS = "Actions"
TAB_MONITOR = "Monitor"
TAB_ABOUT = "About"
TAB_DISCLAIMER = "Disclaimer"

# Progress Steps
PROGRESS_STEPS = [
    "Step 1: Validating files",
    "Step 2: Generating Tailscale keys",
    "Step 3: Creating repositories",
    "Step 4: Uploading files",
    "Step 5: Adding secrets",
    "Step 6: Starting workflows",
    "Step 7: Finalizing"
]

# Message Box Titles
TITLE_SUCCESS = "Success"
TITLE_ERROR = "Error"
TITLE_WARNING = "Warning"
TITLE_INFO = "Information"
TITLE_CONFIRM = "Confirm"

# File Filters
FILTER_WORKFLOW = "Workflow Files (*.yml *.yaml);;All Files (*.*)"
FILTER_TEXT = "Text Files (*.txt);;All Files (*.*)"
FILTER_JSON = "JSON Files (*.json);;All Files (*.*)"
FILTER_GITIGNORE = ".gitignore Files (.gitignore);;All Files (*.*)"

# Rate Limiting
API_RATE_LIMIT_DELAY = 0.5  # seconds between API calls
