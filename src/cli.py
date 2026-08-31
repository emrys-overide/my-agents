#!/usr/bin/env python3
"""
Deloitte Autonomous AI Consultancy CLI
Run complete multi-agent engagements from brief to executive delivery.
"""

import argparse
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.framework.orchestrator_engine import EVDOrchestrationEngine


def main():
    parser = argparse.ArgumentParser(
        description="Deloitte Autonomous AI Consultancy Framework - Multi-Agent Engagement Runner"
    )
    parser.add_argument(
        "--brief",
        type=str,
        default="Enterprise GenAI Customer Care Agent with Hybrid RAG & Zero-Retention Security",
        help="Client business brief or problem statement."
    )
    parser.add_argument(
        "--export-json",
        type=str,
        default=None,
        help="Optional path to export the complete ExecutiveEngagementReport JSON."
    )

    args = parser.parse_args()

    engine = EVDOrchestrationEngine()
    report = engine.run_engagement(client_brief=args.brief)

    print("\n" + "="*80)
    print("                      DELOITTE EXECUTIVE ENGAGEMENT SUMMARY")
    print("="*80)
    print(report.managing_director_summary)
    print("\n[Audit Pillars Scorecard]")
    for pillar, score in report.audit_report.trustworthy_ai_pillars.model_dump().items():
        print(f"  • {pillar.replace('_', ' ').title():<32}: {score:>5.1f}%")
    print("="*80)

    if args.export_json:
        out_path = Path(args.export_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            f.write(report.model_dump_json(indent=2))
        print(f"\n✓ Complete engagement artifact exported to: {out_path.resolve()}")


if __name__ == "__main__":
    main()
