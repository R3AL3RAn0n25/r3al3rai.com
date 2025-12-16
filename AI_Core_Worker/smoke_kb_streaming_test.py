import sys, os, json
sys.path.append(os.path.dirname(__file__))
from knowledge_api import search_wikipedia_streaming

print("Running streaming smoke test…", flush=True)
res = search_wikipedia_streaming("Albert Einstein", max_passages=1, max_chars=200)
print(json.dumps({"count": len(res), "first": res[0] if res else None}, ensure_ascii=False))
