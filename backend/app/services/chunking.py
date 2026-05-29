from pathlib import Path
import json
import os

from dotenv import load_dotenv
from llama_index.core import Document, VectorStoreIndex
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY manjka v .env datoteki.")

json_path = Path(r"C:\Users\jakak\Desktop\Diplomska\backend\scraper\test6.json")

with open(json_path, "r", encoding="utf-8") as f:
    items=json.load(f)

documents = [
    Document(
        text=item.get("html", ""),
        metadata={
            "url": item.get("url"),
            "depth": item.get("depth"),
        },
    )
    for item in items
    if item.get("html")
]

embed_model = OpenAIEmbedding()

splitter = SemanticSplitterNodeParser(
    buffer_size=1,
    breakpoint_percentile_threshold=95,
    embed_model=embed_model,
)

nodes = splitter.get_nodes_from_documents(documents)

print(f"Število strani iz JSON: {len(items)}")
print(f"Število dokumentov: {len(documents)}")
print(f"Število node-ov: {len(nodes)}")

for i, node in enumerate(nodes[:5], start=1):
    print("=" * 80)
    print(f"NODE {i}")
    print("URL:", node.metadata.get("url"))
    print("DEPTH:", node.metadata.get("depth"))
    print(node.get_content()[:1000])