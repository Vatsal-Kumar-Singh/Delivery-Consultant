"""Helper to create a Crew instance for the application.

This module centralizes crew creation so `main.py` can call
`create_crew()` and get a usable object whether or not `crewai` is
installed.
"""
from typing import Any
import os


def create_crew() -> Any:
    """Return a Crew instance.

    Prefer the `agents.create_crew()` implementation (which itself handles
    a crewai fallback). If that import fails for any reason, return a
    minimal object that implements `.run(prompt)` so the UI remains
    functional.
    """
    # Allow forcing local fallback via env var to avoid trying to instantiate
    # remote LLM providers when API keys are not configured.
    force_local = os.environ.get("FORCE_LOCAL_CREW", "0") in ("1", "true", "True")
    if force_local:
        class _SimpleCrew:
            def run(self, prompt: str) -> str:
                return (
                    "1) Re-route to avoid congestion.\n"
                    "2) Prioritize urgent shipments and reassign resources.\n"
                    "3) Notify customers with updated ETAs."
                )
        return _SimpleCrew()

    try:
        from agents import create_crew as _create_crew  # local module
        # If the environment lacks common API keys, prefer the local fallback
        # to avoid noisy provider import/instantiation errors.
        if not (os.environ.get("OPENAI_API_KEY") or os.environ.get("CREWAI_API_KEY")):
            # No API keys present: use local fallback
            class _SimpleCrew:
                def run(self, prompt: str) -> str:
                    return (
                        "1) Re-route to avoid congestion.\n"
                        "2) Prioritize urgent shipments and reassign resources.\n"
                        "3) Notify customers with updated ETAs."
                    )
            return _SimpleCrew()

        return _create_crew()
    except Exception:
        class _SimpleCrew:
            def run(self, prompt: str) -> str:
                return (
                    "1) Re-route to avoid congestion.\n"
                    "2) Prioritize urgent shipments and reassign resources.\n"
                    "3) Notify customers with updated ETAs."
                )
        return _SimpleCrew()
