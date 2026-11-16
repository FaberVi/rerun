"""FR->IT pack pass for selected namespaces (ICU-safe), with slow batching."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from deep_translator import GoogleTranslator

ROOT = Path(__file__).resolve().parent.parent / "packages" / "i18n" / "messages"
SOURCE = "fr"
TARGET = "it"
NAMESPACES = ("dialogs", "templates", "chat", "errors")
CONTEXT_KEY = "_context"
BATCH = 25
PAUSE_S = 1.2

DASH_RE = re.compile(r"[—–]")
GLOSSARY_FIXES = (
    (re.compile(r"\bvostro\b", re.I), "tuo"),
    (re.compile(r"\bvostra\b", re.I), "tua"),
    (re.compile(r"\bvostri\b", re.I), "tuoi"),
    (re.compile(r"\bvostre\b", re.I), "tue"),
    (re.compile(r"\bvoi\b", re.I), "tu"),
    (re.compile(r"\bcollegh[ioae]\b", re.I), "coworker"),
    (re.compile(r"\bspazi[oi]\s+di\s+lavoro\b", re.I), "workspace"),
    (re.compile(r"\bcompagno\s+di\s+lavoro\b", re.I), "coworker"),
    (re.compile(r"\bcompagni\s+di\s+lavoro\b", re.I), "coworker"),
    (re.compile(r"\bcompetenze\b", re.I), "skill"),
    (re.compile(r"\bcompetenza\b", re.I), "skill"),
)


def tokenize_message(msg: str) -> tuple[str, list[str]]:
    tokens: list[str] = []
    out: list[str] = []
    i = 0
    while i < len(msg):
        if msg[i] == "<":
            end = msg.find(">", i)
            if end == -1:
                out.append(msg[i])
                i += 1
                continue
            chunk = msg[i : end + 1]
            tokens.append(chunk)
            out.append(f"\x00T{len(tokens) - 1}\x00")
            i = end + 1
            continue
        if msg[i] == "{":
            depth = 0
            j = i
            while j < len(msg):
                if msg[j] == "{":
                    depth += 1
                elif msg[j] == "}":
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
                j += 1
            chunk = msg[i:j]
            tokens.append(chunk)
            out.append(f"\x00T{len(tokens) - 1}\x00")
            i = j
            continue
        out.append(msg[i])
        i += 1
    return "".join(out), tokens


def detokenize(text: str, tokens: list[str]) -> str:
    for idx, tok in enumerate(tokens):
        text = text.replace(f"\x00T{idx}\x00", tok)
    return text


def postprocess(text: str) -> str:
    text = DASH_RE.sub(", ", text)
    text = re.sub(r",\s*,", ",", text)
    for pattern, repl in GLOSSARY_FIXES:
        text = pattern.sub(repl, text)
    return text


def flatten(tree: dict, prefix: str = "") -> dict[str, str]:
    out: dict[str, str] = {}
    for key, value in tree.items():
        if key == CONTEXT_KEY:
            continue
        dotted = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            out.update(flatten(value, dotted))
        else:
            out[dotted] = str(value)
    return out


def unflatten_like(source: dict, flat: dict[str, str], prefix: str = "") -> dict:
    out: dict = {}
    for key, value in source.items():
        if key == CONTEXT_KEY:
            continue
        dotted = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            child = unflatten_like(value, flat, dotted)
            if child:
                out[key] = child
        elif dotted in flat:
            out[key] = flat[dotted]
    return out


def translate_batch(translator: GoogleTranslator, texts: list[str], retries: int = 4) -> list[str]:
    protected_list: list[tuple[str, list[str]]] = []
    for text in texts:
        protected_list.append(tokenize_message(text))

    payload = [p for p, _ in protected_list]
    for attempt in range(retries):
        try:
            translated = translator.translate_batch(payload)
            break
        except Exception as exc:
            if attempt + 1 == retries:
                raise exc
            time.sleep(PAUSE_S * (attempt + 2))
    else:
        translated = payload

    out: list[str] = []
    for (_, tokens), tr in zip(protected_list, translated):
        out.append(postprocess(detokenize(tr or "", tokens)))
    return out


def main() -> None:
    translator = GoogleTranslator(source="fr", target="it")
    (ROOT / TARGET).mkdir(parents=True, exist_ok=True)

    for ns in NAMESPACES:
        fr_tree = json.loads((ROOT / SOURCE / f"{ns}.json").read_text(encoding="utf-8"))
        en_tree = json.loads((ROOT / "en" / f"{ns}.json").read_text(encoding="utf-8"))
        fr_flat = flatten(fr_tree)
        keys = list(fr_flat.keys())
        it_flat: dict[str, str] = {}

        for start in range(0, len(keys), BATCH):
            chunk_keys = keys[start : start + BATCH]
            chunk_texts = [fr_flat[k] for k in chunk_keys]
            print(f"{ns}: {start}/{len(keys)}", flush=True)
            try:
                chunk_tr = translate_batch(translator, chunk_texts)
            except Exception as exc:
                print(f"  batch failed at {start}: {exc}", flush=True)
                chunk_tr = chunk_texts
            for key, val in zip(chunk_keys, chunk_tr):
                it_flat[key] = val
            time.sleep(PAUSE_S)

        out_tree = unflatten_like(en_tree, it_flat)
        out_path = ROOT / TARGET / f"{ns}.json"
        out_path.write_text(
            json.dumps(out_tree, indent=4, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {out_path}", flush=True)


if __name__ == "__main__":
    main()