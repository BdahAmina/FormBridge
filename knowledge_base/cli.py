"""Command-line tools for the official knowledge base."""

from __future__ import annotations

import argparse
import json

from knowledge_base.config import KBConfig
from knowledge_base.service import KnowledgeBaseService


def main() -> None:
    parser = argparse.ArgumentParser(description="FormBridge official knowledge base")
    parser.add_argument("command", choices=["ingest", "ingest-one", "rebuild", "status", "search"])
    parser.add_argument("--authority", default="")
    parser.add_argument("--query", default="")
    args = parser.parse_args()
    service = KnowledgeBaseService(KBConfig.from_env())

    if args.command == "ingest":
        results = service.update_all()
        print(json.dumps([item.model_dump() for item in results], ensure_ascii=False, indent=2))
    elif args.command == "ingest-one":
        result = service.update_one(args.authority)
        print(result.model_dump_json(indent=2, ensure_ascii=False))
    elif args.command == "rebuild":
        result = service.rebuild(args.authority)
        print(result.model_dump_json(indent=2, ensure_ascii=False))
    elif args.command == "status":
        print(json.dumps(service.list_status(), ensure_ascii=False, indent=2))
    elif args.command == "search":
        hits = service.search(args.query)
        payload = [
            {
                "score": round(hit.score, 3),
                "authority": hit.chunk.metadata.authority,
                "url": hit.chunk.metadata.source_url,
                "text": hit.chunk.text[:240],
            }
            for hit in hits
        ]
        print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
