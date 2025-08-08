import sys
import json
from dotenv import load_dotenv
from .graph.graph import build_graph

def main():
    load_dotenv()
    if len(sys.argv) < 2:
        print("Usage: python -m src.app <job_url>")
        sys.exit(1)

    url = sys.argv[1]
    app = build_graph()
    result = app.invoke({"url": url})

    if "job" in result:
        print(json.dumps(result["job"], indent=2, ensure_ascii=False))
    else:
        print(json.dumps({"error": result.get("error", "Unknown error")}, indent=2))

if __name__ == "__main__":
    main()
