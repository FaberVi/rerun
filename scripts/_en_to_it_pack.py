"""EN -> IT heuristic for i18n (ICU-safe). For manual review afterward."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "packages" / "i18n" / "messages"
FILES = ("dialogs", "templates", "chat", "errors")
CONTEXT = "_context"

PHRASES: list[tuple[str, str]] = [
    ("Something went wrong. Please try again.", "Qualcosa è andato storto. Riprova."),
    ("Something went wrong", "Qualcosa è andato storto"),
    ("Please try again", "Riprova"),
    ("Please try again.", "Riprova."),
    ("Try again in a few minutes.", "Riprova tra qualche minuto."),
    ("Try again in a minute.", "Riprova tra un minuto."),
    ("Try again in a moment.", "Riprova tra poco."),
    ("Try again tomorrow.", "Riprova domani."),
    ("Try again later.", "Riprova più tardi."),
    ("Try again.", "Riprova."),
    ("Try rephrasing.", "Prova a riformularlo."),
    ("Try the other channel, or use email or Google.", "Prova l'altro canale o usa email o Google."),
    ("Not authenticated", "Non autenticato"),
    ("Not authorized", "Non autorizzato"),
    ("You are not a member of this workspace", "Non sei membro di questo workspace"),
    ("This user is not a member of the workspace.", "Questo utente non è membro del workspace."),
    ("Coworker not found", "Coworker non trovato"),
    ("Coworker not reachable", "Coworker non raggiungibile"),
    ("Box not found", "Box non trovata"),
    ("Name is required", "Il nome è obbligatorio"),
    ("Keep the name under {max} characters", "Il nome deve avere meno di {max} caratteri"),
    ("Keep the name under {max} characters.", "Il nome deve avere meno di {max} caratteri."),
    ("Keep it under {max} characters", "Massimo {max} caratteri"),
    ("Keep it under {max} characters.", "Massimo {max} caratteri."),
    ("Unknown language.", "Lingua sconosciuta."),
    ("Please choose an image file.", "Scegli un file immagine."),
    ("No logo found at this address", "Nessun logo trovato a questo indirizzo"),
    ("Invitation not found", "Invito non trovato"),
    ("This invitation is no longer valid.", "Questo invito non è più valido."),
    ("This invitation has expired.", "Questo invito è scaduto."),
    ("This invitation is for another email. Sign in with the invited address.", "Questo invito è per un altro indirizzo email. Accedi con quello invitato."),
    ("This invitation is for {email}. Sign in with that email to accept it.", "Questo invito è per {email}. Accedi con quell'email per accettarlo."),
    ("This workspace has reached its seat limit.", "Questo workspace ha raggiunto il limite di posti."),
    ("This workspace has no seat left. Ask an admin to free one.", "Questo workspace non ha posti liberi. Chiedi a un admin di liberarne uno."),
    ("This workspace has no active plan.", "Questo workspace non ha un piano attivo."),
    ("This person is already a member of the workspace.", "Questa persona è già membro del workspace."),
    ("The workspace needs at least one admin", "Il workspace deve avere almeno un admin"),
    ("Only an admin can change the workspace settings", "Solo un admin può modificare le impostazioni del workspace"),
    ("Only an admin can manage API keys", "Solo un admin può gestire le chiavi API"),
    ("Only an admin or a manager of this Box can do this", "Solo un admin o chi gestisce questa Box può farlo"),
    ("Only an admin or a manager of this Box can change this", "Solo un admin o chi gestisce questa Box può modificarlo"),
    ("No machine is available right now", "Nessuna macchina disponibile in questo momento"),
    ("Only an admin of the workspace can do this", "Solo un admin del workspace può farlo"),
    ("Space not found", "Space non trovato"),
    ("Session not found", "Sessione non trovata"),
    ("Conversation not found", "Conversazione non trovata"),
    ("Account not found", "Account non trovato"),
    ("Template not found", "Template non trovato"),
    ("Template not found.", "Template non trovato."),
    ("Reserved for expert accounts", "Riservato agli account expert"),
    ("Could not ", "Non è stato possibile "),
    ("Failed to ", "Impossibile "),
    ("You cannot remove yourself from the workspace.", "Non puoi rimuovere te stesso dal workspace."),
    ("You must be signed in to accept an invitation.", "Devi essere connesso per accettare un invito."),
    ("You manage no Box in this workspace yet. Create one first.", "Non gestisci ancora nessuna Box in questo workspace. Creane una prima."),
    ("You no longer have access to this Box", "Non hai più accesso a questa Box"),
    ("You have reached the limit of {max} templates.", "Hai raggiunto il limite di {max} template."),
    ("Your workspace is paused. Bring it back first.", "Il tuo workspace è in pausa. Riattivalo prima."),
    ("Your workspace is being restored. It will be back in a minute or two.", "Il tuo workspace è in ripristino. Tornerà disponibile tra un minuto o due."),
    ("Your workspace already has a subscription. Manage it from Billing.", "Il tuo workspace ha già un abbonamento. Gestiscilo da Fatturazione."),
    ("Your trial ends on its own, there is nothing to cancel.", "La prova termina da sola: non c'è nulla da annullare."),
    ("Your subscription is not active.", "Il tuo abbonamento non è attivo."),
    ("Your subscription is already active.", "Il tuo abbonamento è già attivo."),
    ("Your subscription is already set to cancel.", "Il tuo abbonamento è già impostato per l'annullamento."),
    ("Your subscription is set to cancel. Resume it first.", "Il tuo abbonamento è impostato per l'annullamento. Riprendilo prima."),
    ("Start your free trial", "Inizia la prova gratuita"),
    ("Start your subscription", "Inizia l'abbonamento"),
    ("Subscribe first.", "Abbonati prima."),
    ("Subscribe to Rerun first", "Abbonati prima a Rerun"),
    ("Sign in to ", "Accedi per "),
    ("Sign in with ", "Accedi con "),
    ("Enter a valid email address", "Inserisci un indirizzo email valido"),
    ("Enter a valid email address.", "Inserisci un indirizzo email valido."),
    ("Enter a valid email", "Inserisci un'email valida"),
    ("Enter a valid mobile number.", "Inserisci un numero di cellulare valido."),
    ("Enter the address and the key of the server.", "Inserisci l'indirizzo e la chiave del server."),
    ("Enter the business name", "Inserisci la ragione sociale"),
    ("Enter the number", "Inserisci il numero"),
    ("Type {word} to confirm.", "Scrivi {word} per confermare."),
    ("Add a card first: the number is checked against its billing address.", "Aggiungi prima una carta: il numero viene verificato con l'indirizzo di fatturazione."),
    ("Add a payment method first.", "Aggiungi prima un metodo di pagamento."),
    ("No free coworker slot on your plan. Start Pro for unlimited coworkers, or delete a coworker to make room.", "Nessuno slot coworker libero nel tuo piano. Passa a Pro per coworker illimitati, oppure elimina un coworker per fare spazio."),
]

PHRASES.sort(key=lambda x: len(x[0]), reverse=True)
DASH = re.compile(r"[—–]")


def tokenize(msg: str) -> tuple[str, list[str]]:
    tokens: list[str] = []
    out: list[str] = []
    i = 0
    while i < len(msg):
        if msg[i] == "<":
            end = msg.find(">", i)
            chunk = msg[i : end + 1] if end != -1 else msg[i]
            if end == -1:
                i += 1
                continue
            tokens.append(chunk)
            out.append(f"\x00T{len(tokens)-1}\x00")
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
            out.append(f"\x00T{len(tokens)-1}\x00")
            i = j
            continue
        out.append(msg[i])
        i += 1
    return "".join(out), tokens


def detokenize(text: str, tokens: list[str]) -> str:
    for idx, tok in enumerate(tokens):
        text = text.replace(f"\x00T{idx}\x00", tok)
    return text


def convert(text: str) -> str:
    text = DASH.sub(", ", text)
    protected, tokens = tokenize(text)
    for a, b in PHRASES:
        protected = protected.replace(a, b)
    return detokenize(protected, tokens)


def walk(obj):
    if isinstance(obj, dict):
        return {k: walk(v) for k, v in obj.items() if k != CONTEXT}
    return convert(obj) if isinstance(obj, str) else obj


def main() -> None:
    for name in FILES:
        en = json.loads((ROOT / "en" / f"{name}.json").read_text(encoding="utf-8"))
        it = walk(en)
        (ROOT / "it" / f"{name}.json").write_text(json.dumps(it, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
        print(name)


if __name__ == "__main__":
    main()