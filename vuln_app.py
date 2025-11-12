"""
vuln_app.py

Examples of insecure Python patterns for demonstration and code scanning.
Do NOT use these patterns in production. These are intentionally vulnerable
to show what tools like Bandit/CodeQL might flag.
"""
import subprocess
import hashlib


def run_untrusted_code(code_str):
    """Dangerous: directly evaluates an input string as Python code.

    Example vulnerability flagged by static analyzers (use of eval/exec).
    """
    # Vulnerable: arbitrary code execution
    return eval(code_str)


def run_shell_command(cmd):
    """Dangerous: runs a shell command with shell=True and string input.

    Example vulnerability: command injection via uncontrolled input.
    """
    # Vulnerable: uses shell=True with an interpolated command string
    subprocess.run(cmd, shell=True)


def use_insecure_hash(value: str) -> str:
    """Uses MD5 (insecure for cryptographic purposes)."""
    return hashlib.md5(value.encode()).hexdigest()


if __name__ == "__main__":
    # Simple demo (do NOT run with untrusted input)
    print("MD5 of 'password':", use_insecure_hash("password"))
    # Dangerous examples commented out to avoid accidental execution
    # run_untrusted_code("__import__('os').system('echo hi')")
    # run_shell_command("ls -la")



# Not used demo Azure credentials (do not use in real environments)
DEMO_AZURE_CLIENT_ID = "b78186dd-32ca-4dcb-8aba-c65f47cd0104"
DEMO_AZURE_CLIENT_SECRET = "JAj8Q~uILxPmXZ5iMaOsFbJ.62Mtv_RzOOsepdbZ"

# FAKE demo GitHub token (pattern only)
DEMO_GITHUB_TOKEN = "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"


def print_demo_secrets():
    """Prints truncated demo secrets to avoid leaking full strings in logs.

    Purpose: keep references so linters don't treat them as unused, and
    provide a simple runtime demonstration that these are present.
    """
    secrets = {
        "DEMO_AWS_ACCESS_KEY_ID": DEMO_AWS_ACCESS_KEY_ID,
        "DEMO_AWS_SECRET_ACCESS_KEY": DEMO_AWS_SECRET_ACCESS_KEY,
        "DEMO_GITHUB_TOKEN": DEMO_GITHUB_TOKEN,
    }
    for k, v in secrets.items():
        print(f"{k}: {v[:10]}... (demo)")
