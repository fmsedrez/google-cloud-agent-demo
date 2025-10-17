#!/usr/bin/env python3
"""Script to setup environment variables for the project."""

import os
import sys
from pathlib import Path


def main():
    """Setup environment variables from .env.example.example template."""
    env_example = Path.cwd() / ".env.example"
    env_file = Path.cwd() / ".env"

    if not env_example.exists():
        print(f"Error: {env_example} not found")
        print("Please create a .env.example file with the required environment variables")
        sys.exit(1)
    # Read existing env vars
    existing_vars = {}
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    existing_vars[key] = value
    # Read env.example to get required keys
    required_keys = []
    comments = {}
    with open(env_example, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                # Store comment for next key
                last_comment = line[1:].strip()
            elif "=" in line:
                key, example_value = line.split("=", 1)
                required_keys.append(key)
                if 'last_comment' in locals():
                    comments[key] = last_comment
                    del last_comment
    # Prompt for missing or empty values
    if "--export" not in sys.argv:
        print("Setting up environment variables...\n")
    for key in required_keys:
        if key not in existing_vars or not existing_vars[key]:
            if key in comments:
                print(f"# {comments[key]}")
            value = input(f"{key}: ").strip()
            existing_vars[key] = value
        else:
            if "--export" not in sys.argv:
                print(f"{key}: (already set)")
    # Write to .env
    with open(env_file, "w") as f:
        for key in required_keys:
            f.write(f"{key}={existing_vars[key]}\n")
    if "--export" not in sys.argv:
        print(f"\n✓ Environment variables written to {env_file}", file=sys.stderr)
    if "--export" in sys.argv:
        # Output export commands to stdout for eval
        for key in required_keys:
            print(f"export {key}={existing_vars[key]}")
    else:
        print("\nTo export to your shell, run:", file=sys.stderr)
        print("  eval $(uv run setenv --export)", file=sys.stderr)
        print("\n✓ Setup complete!", file=sys.stderr)


if __name__ == "__main__":
    main()
