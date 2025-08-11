import sys
import json
from dotenv import load_dotenv
from .graph.graph import build_graph
from langfuse.langchain import CallbackHandler 

def main():
    load_dotenv()
    if len(sys.argv) < 2:
        print("Usage: python -m src.app <job_url>")
        sys.exit(1)

    url = sys.argv[1]
    
    #langfuse handler
    langfuse_handler = CallbackHandler()
        
    app = build_graph()
    
    result = app.invoke(
        {"url": url},
        config={
            "callbacks": [langfuse_handler],
            "run_name": "job-scrape",
            "tags": ["job-scraper", "mvp"],              # put tags here
            "metadata": {"url": url, "release": "v0.1"}  # put release in metadata
        },
    )
    

    if "job" in result:
        print(json.dumps(result["job"], indent=2, ensure_ascii=False))
    else:
        print(json.dumps({"error": result.get("error", "Unknown error")}, indent=2))

if __name__ == "__main__":
    main()
