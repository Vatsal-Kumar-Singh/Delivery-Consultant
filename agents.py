"""Agent definitions with a graceful fallback when `crewai` is not available.

This file exposes `create_crew()` which returns an object with a `.run(prompt)`
method. If `crewai` is installed and usable we use its `Agent` and `Crew`.
Otherwise we provide lightweight local replacements so the app can run
without external CrewAI dependencies.
"""

from dataclasses import dataclass
import logging
logger = logging.getLogger(__name__)

try:
    # Prefer real crewai objects when available
    from crewai import Agent, Crew  # type: ignore
    CREWAI_AVAILABLE = True
except Exception:
    CREWAI_AVAILABLE = False

if not CREWAI_AVAILABLE:
    # Lightweight local Agent and Crew implementations
    @dataclass
    class Agent:
        name: str
        role: str = ""
        goal: str = ""
        backstory: str = ""

    class Crew:
        def __init__(self, agents):
            self.agents = agents

        def run(self, prompt: str) -> str:
            """Return simple heuristic recommendations based on the prompt.

            This is intentionally simple — it's a fallback so the UI behaves
            reasonably when `crewai` isn't installed or configured.
            """
            logger.debug("Fallback Crew.run called with prompt: %s", prompt)

            # Basic heuristic: return 3 concise actions tailored to logistics
            return (
                "1) Re-route to avoid high-traffic corridors when possible.\n"
                "2) Assign a faster vehicle or driver to high-priority shipments.\n"
                "3) Increase buffer time and proactively notify customers about adjusted ETAs."
            )

# --- Agent Definitions ---
DataLoaderAgent = Agent(
    name="DataLoaderAgent",
    role="Data Loader and Cleaner",
    goal="Load and preprocess all logistics datasets into a clean DataFrame.",
    backstory="Expert in handling and merging multiple datasets for logistics analysis."
)

PerformanceAnalystAgent = Agent(
    name="PerformanceAnalystAgent",
    role="Delivery Performance Analyst",
    goal="Analyze delays, compute KPIs, and highlight underperforming routes.",
    backstory="Specialist in supply chain performance optimization."
)

RouteOptimizerAgent = Agent(
    name="RouteOptimizerAgent",
    role="Route Optimization Strategist",
    goal="Identify the most efficient routes using distance, weather, and cost data.",
    backstory="Uses analytical skills to optimize route efficiency and reduce cost."
)

FleetAdvisorAgent = Agent(
    name="FleetAdvisorAgent",
    role="Fleet Efficiency Advisor",
    goal="Recommend optimal vehicles based on efficiency and CO₂ impact.",
    backstory="Fleet expert optimizing resource allocation and sustainability."
)

InsightReporterAgent = Agent(
    name="InsightReporterAgent",
    role="Insight Summarizer",
    goal="Generate human-readable insights and summaries for management.",
    backstory="Transforms analytics into clear business recommendations."
)

PredictiveAdvisorAgent = Agent(
    name="PredictiveAdvisorAgent",
    role="Predictive Risk and Action Advisor",
    goal="Interpret delay predictions and suggest proactive corrective actions.",
    backstory="AI logistics consultant trained in predicting and mitigating risks."
)


def create_crew():
    """Return a Crew instance.

    If `crewai` is available the Crew will be the real object. Otherwise the
    fallback Crew defined above will be returned so the rest of the app can
    call `.run(prompt)` transparently.
    """
    try:
        return Crew(
            agents=[
                DataLoaderAgent,
                PerformanceAnalystAgent,
                RouteOptimizerAgent,
                FleetAdvisorAgent,
                InsightReporterAgent,
                PredictiveAdvisorAgent,
            ]
        )
    except Exception:
        # In the unlikely case creating the real Crew fails, use our fallback
        logger.exception("Failed to create real Crew, using fallback implementation.")
        return Crew([
            DataLoaderAgent,
            PerformanceAnalystAgent,
            RouteOptimizerAgent,
            FleetAdvisorAgent,
            InsightReporterAgent,
            PredictiveAdvisorAgent,
        ])
