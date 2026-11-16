"""Convert it strings that still match es (post-rebase bootstrap) using PHRASES from _es_to_it_pack."""
from __future__ import annotations

import json
from pathlib import Path

from _es_to_it_pack import convert

ROOT = Path(__file__).resolve().parent.parent / "packages" / "i18n" / "messages"


def main() -> None:
    it_dir = ROOT / "it"
    es_dir = ROOT / "es"
    en_dir = ROOT / "en"
    changed = 0
    for path in sorted(it_dir.glob("*.json")):
        if path.name == "index.ts":
            continue
        name = path.stem
        if not (es_dir / f"{name}.json").exists():
            continue
        it_tree = json.loads(path.read_text(encoding="utf-8"))
        es_tree = json.loads((es_dir / f"{name}.json").read_text(encoding="utf-8"))
        en_tree = json.loads((en_dir / f"{name}.json").read_text(encoding="utf-8"))

        def walk_it(it_node, es_node, en_node):
            nonlocal changed
            if isinstance(it_node, dict) and isinstance(es_node, dict) and isinstance(en_node, dict):
                out = {}
                for k, v in it_node.items():
                    if k == "_context":
                        out[k] = v
                        continue
                    if k not in es_node or k not in en_node:
                        out[k] = v
                        continue
                    out[k] = walk_it(v, es_node[k], en_node[k])
                return out
            if isinstance(it_node, str) and isinstance(es_node, str) and it_node == es_node:
                changed += 1
                return convert(it_node)
            return it_node

        new_tree = walk_it(it_tree, es_tree, en_tree)
        path.write_text(json.dumps(new_tree, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"updated {path.name}")
    print(f"converted {changed} strings that matched es")


if __name__ == "__main__":
    main()