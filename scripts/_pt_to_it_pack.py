"""PT-BR -> IT for i18n packs (ICU-safe, tu, glossary)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "packages" / "i18n" / "messages"
FILES = ("dialogs", "templates", "chat", "errors")

PHRASES: list[tuple[str, str]] = [
    ("Não foi possível", "Non è stato possibile"),
    ("Não pudemos", "Non siamo riusciti a"),
    ("Algo deu errado", "Qualcosa è andato storto"),
    ("Tente de novo", "Riprova"),
    ("tente de novo", "riprova"),
    ("Tente novamente", "Riprova"),
    ("Esta alteração", "Questa modifica"),
    ("esta alteração", "questa modifica"),
    ("Seu workspace", "Il tuo workspace"),
    ("seu workspace", "il tuo workspace"),
    ("Este workspace", "Questo workspace"),
    ("este workspace", "questo workspace"),
    ("Esta conta", "Questo account"),
    ("esta conta", "questo account"),
    ("Esta caixa", "Questa Box"),
    ("Esta pessoa", "Questa pessoa"),
    ("esta pessoa", "questa pessoa"),
    ("Este coworker", "Questo coworker"),
    ("este coworker", "questo coworker"),
    ("Este modelo", "Questo template"),
    ("este modelo", "questo template"),
    ("Esta ação", "Questa azione"),
    ("esta ação", "questa ação",
    ),
    ("Você não pode", "Non puoi"),
    ("Você não é", "Non sei"),
    ("Você precisa", "Devi"),
    ("Você pode", "Puoi"),
    ("Você deve", "Devi"),
    ("Você já", "Hai già"),
    ("Você", "Tu"),
    ("você", "tu"),
    ("Só um admin", "Solo un admin"),
    ("Só uma", "Solo una"),
    ("O workspace", "Il workspace"),
    ("o workspace", "il workspace"),
    ("do workspace", "del workspace"),
    ("no workspace", "nel workspace"),
    ("ao workspace", "al workspace"),
    ("da conta", "dell'account"),
    ("a esta conta", "a questo account"),
    ("Gerenciar", "Gestisci"),
    ("gerenciar", "gestire"),
    ("Remover", "Rimuovi"),
    ("remover", "rimuovere"),
    ("Adicionar", "Aggiungi"),
    ("adicionar", "aggiungere"),
    ("Alterar", "Cambia"),
    ("alterar", "cambiare"),
    ("Conectar", "Connetti"),
    ("conectar", "connettere"),
    ("Desconectar", "Disconnetti"),
    ("desconectar", "disconnettere"),
    ("desconectado", "disconnesso"),
    ("Abra o Rerun", "Apri Rerun"),
    ("no navegador", "nel browser"),
    ("navegador", "browser"),
    ("e-mail", "email"),
    ("E-mail", "Email"),
    ("número de telefone", "numero di telefono"),
    ("Número de telefone", "Numero di telefono"),
    ("atualizado", "aggiornato"),
    ("Membros", "Membri"),
    ("membros", "membri"),
    ("Membro", "Membro"),
    ("membro", "membro"),
    ("cobrança", "fatturazione"),
    ("configurações", "impostazioni"),
    ("gerenciam", "gestiscono"),
    ("usam os coworkers", "usano i coworker"),
    ("os coworkers", "i coworker"),
    ("agora é", "è ora"),
    ("precisa de pelo menos", "deve avere almeno"),
    ("pelo menos", "almeno"),
    ("na hora", "subito"),
    ("de novo", "di nuovo"),
    ("qualquer momento", "in qualsiasi momento"),
    ("para de funcionar", "smette di funzionare"),
    ("assentos", "posti"),
    ("assento", "posto"),
    ("# assentos", "# posti"),
    ("# assento", "# posto"),
    ("convite", "invito"),
    ("Convite", "Invito"),
    ("Revogar", "Revoca"),
    ("revogar", "revoca"),
    ("Pendente", "In attesa"),
    ("pendente", "in attesa"),
    ("atribuir depois", "da assegnare dopo"),
    ("Usuário desconhecido", "Utente sconosciuto"),
    ("desconhecido", "sconosciuto"),
    ("conta", "account"),
    ("Conta", "Account"),
    ("método de login", "metodo di accesso"),
    ("conectado a", "collegato a"),
    ("é o único", "è l'unico"),
    ("Tornar admin", "Rendi admin"),
    ("Tornar membro", "Rendi membro"),
    ("modelos", "template"),
    ("Modelos", "Template"),
    ("modelo", "template"),
    ("Modelo", "Template"),
    ("mensagem", "messaggio"),
    ("Mensagem", "Messaggio"),
    ("mensagens", "messaggi"),
    ("conversa", "conversazione"),
    ("Conversa", "Conversazione"),
    ("arquivo", "file"),
    ("Arquivo", "File"),
    ("arquivos", "file"),
    ("anexos", "allegati"),
    ("Enviar", "Invia"),
    ("enviar", "invia"),
    ("Cancelar", "Annulla"),
    ("cancelar", "annulla"),
    ("Continuar", "Continua"),
    ("continuar", "continua"),
    ("Copiar", "Copia"),
    ("copiar", "copia"),
    ("Copiado", "Copiato"),
    ("copiado", "copiato"),
    ("Conectado", "Connesso"),
    ("conectado", "connesso"),
    ("Notificações", "Notifiche"),
    ("notificações", "notifiche"),
    ("Servidores", "Server"),
    ("servidor", "server"),
    ("Chave API", "Chiave API"),
    ("chaves API", "chiavi API"),
    ("chave API", "chiave API"),
    ("créditos da Rerun", "Credit Rerun"),
    ("Créditos da Rerun", "Credit Rerun"),
    ("créditos", "Credit"),
    ("Créditos", "Credit"),
    ("crédito", "credito"),
    ("assinatura", "abbonamento"),
    ("Assinatura", "Abbonamento"),
    ("teste gratuito", "prova gratuita"),
    ("teste", "prova"),
    ("Grátis", "Gratis"),
    ("grátis", "gratis"),
    ("obrigatório", "obbligatorio"),
    ("caracteres", "caratteri"),
    ("válido", "valido"),
    ("válida", "valida"),
    ("incorreto", "errato"),
    ("indisponível", "non disponibile"),
    ("tabela", "tabella"),
    ("linhas", "righe"),
    ("coluna", "colonna"),
    ("colunas", "colonne"),
    ("visualização", "vista"),
    ("Visualização", "Vista"),
    ("Pergunta", "Domanda"),
    ("pergunta", "domanda"),
    ("Resposta", "Risposta"),
    ("resposta", "risposta"),
    ("Erro", "Errore"),
    ("erro", "errore"),
    ("Saída", "Output"),
    ("Entrada", "Input"),
    ("Contexto", "Contesto"),
    ("Pensando", "Sto pensando"),
    ("Processando", "Elaborazione"),
    ("Escrevendo", "Scrittura"),
    ("Instalar", "Installa"),
    ("instalar", "installa"),
    ("Mostrar mais", "Mostra altro"),
    ("Mostrar menos", "Mostra meno"),
    ("Nenhum", "Nessun"),
    ("nenhum", "nessun"),
    ("Nenhuma", "Nessuna"),
    ("nenhuma", "nessuna"),
    ("Todos", "Tutti"),
    ("todas", "tutte"),
    ("primeiro", "prima"),
    ("Primeiro", "Prima"),
    ("depois", "dopo"),
    ("agora", "ora"),
    ("ainda", "ancora"),
    ("já", "già"),
    ("ainda precisa ser confirmada pelo seu endereço atual", "va ancora confermata dal tuo indirizzo attuale"),
    ("pode gerenciar os membri", "può gestire i membri"),
    ("está limitado a um posto", "è limitato a un posto"),
    ("está limitado a", "è limitato a"),
    ("limitado a", "limitato a"),
    ("# assento", "# posto"),
    ("# assentos", "# posti"),
    ("um posto", "un posto"),
    ("um admin", "un admin"),
    ("removido do", "rimosso dal"),
    ("A pessoa perde na hora o acesso a este workspace e a tudo o que há nele", "Perde subito l'accesso a questo workspace e a tutto ciò che contiene"),
    ("Você pode convidá-la de novo depois", "Puoi invitarla di nuovo dopo"),
    ("O link do convite para de funcionar", "Il link d'invito smette di funzionare"),
    ("Você pode enviar um novo a qualquer momento", "Puoi inviarne uno nuovo in qualsiasi momento"),
    ("Envie este link para", "Invia questo link a"),
    ("Ele funciona só para essa pessoa, uma vez", "Funziona solo per lei, una sola volta"),
    ("Copie o link do convite", "Copia il link d'invito"),
    ("Convidar por email", "Invita via email"),
    ("Convidar", "Invita"),
    ("Convite enviado para", "Invito inviato a"),
    ("colega@", "collega@"),
    ("per connettere o Google", "per connettere Google"),
    ("Não ", "Non "),
    (" não ", " non "),
]

PHRASES.sort(key=lambda x: len(x[0]), reverse=True)
DASH_RE = re.compile(r"[—–]")


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


def convert(text: str) -> str:
    text = DASH_RE.sub(", ", text)
    protected, tokens = tokenize_message(text)
    for src, dst in PHRASES:
        protected = protected.replace(src, dst)
    return detokenize(protected, tokens)


def walk(obj):
    if isinstance(obj, dict):
        return {k: walk(v) for k, v in obj.items() if k != "_context"}
    if isinstance(obj, str):
        return convert(obj)
    return obj


def main() -> None:
    for name in FILES:
        pt = json.loads((ROOT / "pt" / f"{name}.json").read_text(encoding="utf-8"))
        out = ROOT / "it" / f"{name}.json"
        out.write_text(json.dumps(walk(pt), indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {out}")


if __name__ == "__main__":
    main()