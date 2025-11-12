"""
secure_app.py

Secure versions of patterns in `vuln_app.py` demonstrating safer alternatives.
"""
import subprocess
import hashlib
import shlex


def safe_eval(expr: str):
    """Safer limited evaluation — using literal_eval to avoid arbitrary code execution."""
    from ast import literal_eval

    try:
        return literal_eval(expr)
    except Exception:
        raise ValueError("Expression not allowed")


def run_shell_command_safe(args):
    """Run a command safely by passing a list of args and avoiding shell=True."""
    if isinstance(args, str):
        args = shlex.split(args)
    subprocess.run(args, shell=False)


def use_secure_hash(value: str) -> str:
    """Use SHA-256 for hashing (not for password storage, but stronger than MD5)."""
    return hashlib.sha256(value.encode()).hexdigest()


if __name__ == "__main__":
    print("SHA256 of 'password':", use_secure_hash("password"))
