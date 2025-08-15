import sys
import json
from dotenv import load_dotenv
from .graph.graph import build_graph
from langfuse.langchain import CallbackHandler 

def _parse_args():
    import argparse
    import os
    parser = argparse.ArgumentParser(description="Job scraping agent (URL → JSON structured)")
    parser.add_argument("url", help="Job posting URL to scrape")
    parser.add_argument(
        "--langfuse",
        action="store_true",
        default=str(os.getenv("LANGFUSE_ENABLED", "")).lower() in ("1", "true", "yes", "on"),
        help=(
            "Enable Langfuse tracing for this run, or set LANGFUSE_ENABLED=1 in the environment"
        ),
    )
    return parser.parse_args()


def main():
    load_dotenv() 
    
    args = _parse_args()
        
    app = build_graph()
    
    config = {
        "run_name": "job-scrape",
        "tags": ["job-scraper", "mvp"],
        "metadata": {"url": args.url, "release": "v0.1"},
    }

    if args.langfuse:
        from langfuse.langchain import CallbackHandler
        handler = CallbackHandler()
        config["callbacks"] = [handler]

    result = app.invoke({"url": args.url}, config=config)

    if "job" in result:
        print(json.dumps(result["job"], indent=2, ensure_ascii=False))
    else:
        print(json.dumps({"error": result.get("error", "Unknown error")}, indent=2))

    if args.langfuse:
        try:
            from langfuse import get_client
            get_client().flush()
        except Exception:
            pass
if __name__ == "__main__":
    main()
