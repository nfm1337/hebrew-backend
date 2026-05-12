import json
import sys
from collections import defaultdict
from pathlib import Path


def _resolve_reports_dir(arg: str | None) -> Path:
    if arg:
        return Path(arg)
    base = Path(__file__).parent / "reports"
    runs = sorted(d for d in base.iterdir() if d.is_dir())
    if not runs:
        raise FileNotFoundError(f"No runs found in {base}")
    return runs[-1]


def aggregate(reports_dir: Path | None = None) -> None:
    run_dir = _resolve_reports_dir(str(reports_dir) if reports_dir else None)
    print(f"Run: {run_dir.name}\n")
    reports = [json.loads(f.read_text()) for f in run_dir.glob("*.json")]

    by_model: dict[str, dict[str, int]] = defaultdict(
        lambda: {"total": 0, "level_pass": 0, "topic_pass": 0, "grammar_pass": 0, "all_pass": 0}
    )

    for r in reports:
        m = r["model"]
        by_model[m]["total"] += 1

        level_ok = r["judgements"]["level"]["matches_expected"]
        topic_ok = r["judgements"]["topic"]["on_topic"]
        grammar_ok = (
            r["judgements"]["grammar"]["is_grammatical"]
            or r["judgements"]["grammar"]["severity"] != "major"
        )

        by_model[m]["level_pass"] += int(level_ok)
        by_model[m]["topic_pass"] += int(topic_ok)
        by_model[m]["grammar_pass"] += int(grammar_ok)
        by_model[m]["all_pass"] += int(level_ok and topic_ok and grammar_ok)

    print(f"{'Model':<40} {'Level':<10} {'Topic':<10} {'Grammar':<10} {'All':<10}")
    for model, stats in by_model.items():
        t = stats["total"]
        print(
            f"{model:<40} "
            f"{stats['level_pass']}/{t} ({stats['level_pass'] / t:.0%})  "
            f"{stats['topic_pass']}/{t} ({stats['topic_pass'] / t:.0%})  "
            f"{stats['grammar_pass']}/{t} ({stats['grammar_pass'] / t:.0%})  "
            f"{stats['all_pass']}/{t} ({stats['all_pass'] / t:.0%})"
        )


if __name__ == "__main__":
    aggregate(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
