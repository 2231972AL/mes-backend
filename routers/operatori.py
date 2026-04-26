from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Commessa, Fase, LogLavorazione, Utente
from auth import get_user_from_token_db
from datetime import datetime, timedelta

router = APIRouter(prefix="/operatori", tags=["Operatori"])


# ---------------------------------------------------------
# FASI ASSEGNATE ALL'OPERATORE
# ---------------------------------------------------------
@router.get("/{operatore_id}/fasi")
def fasi_operatore(
    operatore_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_user_from_token_db)
):
    commesse = db.query(Commessa).filter(Commessa.operatore_id == operatore_id).all()

    risultato = []
    for c in commesse:
        for f in c.fasi:
            if f.stato in ["da_fare", "in_corso"]:
                risultato.append({
                    "id": f.id,
                    "nome": f.nome,
                    "stato": f.stato,
                    "tempo_previsto": f.tempo_previsto,
                    "commessa_id": c.id,
                    "commessa_codice": c.codice
                })

    return risultato


# ---------------------------------------------------------
# PROFILO OPERATORE
# ---------------------------------------------------------
@router.get("/{operatore_id}/profilo")
def profilo_operatore(
    operatore_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_user_from_token_db)
):
    operatore = db.query(Utente).filter(Utente.id == operatore_id).first()
    if not operatore:
        return {"errore": "Operatore non trovato"}

    commesse = db.query(Commessa).filter(Commessa.operatore_id == operatore_id).all()

    # Fasi in corso
    fasi_in_corso = []
    for c in commesse:
        for f in c.fasi:
            if f.stato == "in_corso":
                fasi_in_corso.append({
                    "id": f.id,
                    "nome": f.nome,
                    "commessa_codice": c.codice
                })

    # Minuti lavorati oggi
    oggi = datetime.utcnow().date()
    minuti_oggi = (
        db.query(LogLavorazione)
        .filter(
            LogLavorazione.operatore_id == operatore_id,
            LogLavorazione.azione == "minuti_lavorati",
            LogLavorazione.timestamp >= oggi
        )
        .all()
    )

    totale_minuti = sum(l.minuti or 0 for l in minuti_oggi)

    return {
        "id": operatore.id,
        "username": operatore.username,
        "ruolo": operatore.ruolo,
        "commesse_assegnate": [
            {"id": c.id, "codice": c.codice, "stato": c.stato}
            for c in commesse
        ],
        "fasi_in_corso": fasi_in_corso,
        "minuti_lavorati_oggi": totale_minuti
    }


# ---------------------------------------------------------
# STORICO ATTIVITÀ OPERATORE
# ---------------------------------------------------------
@router.get("/{operatore_id}/storico")
def storico_operatore(
    operatore_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_user_from_token_db)
):
    logs = (
        db.query(LogLavorazione)
        .filter(LogLavorazione.operatore_id == operatore_id)
        .order_by(LogLavorazione.timestamp.desc())
        .limit(200)
        .all()
    )

    risultato = []
    for l in logs:
        risultato.append({
            "id": l.id,
            "azione": l.azione,
            "minuti": l.minuti,
            "timestamp": l.timestamp,
            "commessa_id": l.commessa_id,
            "fase_id": l.fase_id
        })

    return risultato


# ---------------------------------------------------------
# GRAFICO MINUTI (ULTIMI 7 GIORNI)
# ---------------------------------------------------------
@router.get("/{operatore_id}/grafico_minuti")
def grafico_minuti_operatore(
    operatore_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_user_from_token_db)
):
    oggi = datetime.utcnow().date()
    inizio = oggi - timedelta(days=6)

    logs = (
        db.query(LogLavorazione)
        .filter(
            LogLavorazione.operatore_id == operatore_id,
            LogLavorazione.azione == "minuti_lavorati",
            LogLavorazione.timestamp >= inizio
        )
        .all()
    )

    # aggregazione per giorno
    giorni = {str(oggi - timedelta(days=i)): 0 for i in range(7)}

    for l in logs:
        giorno = str(l.timestamp.date())
        if giorno in giorni:
            giorni[giorno] += l.minuti or 0

    labels = list(sorted(giorni.keys()))
    valori = [giorni[g] for g in labels]

    return {
        "labels": labels,
        "valori": valori
    }
@router.get("/{operatore_id}/grafico_mensile")
def grafico_mensile_operatore(
    operatore_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_user_from_token_db)
):
    oggi = datetime.utcnow().date()
    inizio_mese = oggi.replace(day=1)

    logs = (
        db.query(LogLavorazione)
        .filter(
            LogLavorazione.operatore_id == operatore_id,
            LogLavorazione.azione == "minuti_lavorati",
            LogLavorazione.timestamp >= inizio_mese
        )
        .all()
    )

    # giorni del mese corrente
    giorni = {}
    giorno_corrente = inizio_mese
    while giorno_corrente <= oggi:
        giorni[str(giorno_corrente)] = 0
        giorno_corrente += timedelta(days=1)

    # aggregazione
    for l in logs:
        giorno = str(l.timestamp.date())
        if giorno in giorni:
            giorni[giorno] += l.minuti or 0

    labels = list(sorted(giorni.keys()))
    valori = [giorni[g] for g in labels]

    return {
        "labels": labels,
        "valori": valori
    }
@router.get("/{operatore_id}/grafico_annuale")
def grafico_annuale_operatore(
    operatore_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_user_from_token_db)
):
    oggi = datetime.utcnow().date()
    inizio_anno = oggi.replace(month=1, day=1)

    logs = (
        db.query(LogLavorazione)
        .filter(
            LogLavorazione.operatore_id == operatore_id,
            LogLavorazione.azione == "minuti_lavorati",
            LogLavorazione.timestamp >= inizio_anno
        )
        .all()
    )

    # inizializza i 12 mesi
    mesi = {m: 0 for m in range(1, 13)}

    # aggregazione
    for l in logs:
        mese = l.timestamp.month
        mesi[mese] += l.minuti or 0

    labels = [
        "Gen", "Feb", "Mar", "Apr", "Mag", "Giu",
        "Lug", "Ago", "Set", "Ott", "Nov", "Dic"
    ]

    valori = [mesi[i] for i in range(1, 13)]

    return {
        "labels": labels,
        "valori": valori
    }
@router.get("/{operatore_id}/kpi")
def kpi_operatore(
    operatore_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_user_from_token_db)
):
    oggi = datetime.utcnow().date()

    # Minuti lavorati oggi
    logs_oggi = (
        db.query(LogLavorazione)
        .filter(
            LogLavorazione.operatore_id == operatore_id,
            LogLavorazione.azione == "minuti_lavorati",
            LogLavorazione.timestamp >= oggi
        )
        .all()
    )
    minuti_lavorati_oggi = sum(l.minuti or 0 for l in logs_oggi)

    # Commesse assegnate
    commesse = db.query(Commessa).filter(Commessa.operatore_id == operatore_id).all()

    totale_previsto = 0
    totale_lavorato = 0
    fasi_totali = 0
    fasi_complete = 0
    fasi_ritardo = 0

    for c in commesse:
        for f in c.fasi:
            fasi_totali += 1
            totale_previsto += f.tempo_previsto or 0

            # minuti lavorati su questa fase
            logs_fase = (
                db.query(LogLavorazione)
                .filter(
                    LogLavorazione.operatore_id == operatore_id,
                    LogLavorazione.fase_id == f.id,
                    LogLavorazione.azione == "minuti_lavorati"
                )
                .all()
            )
            minuti_fase = sum(l.minuti or 0 for l in logs_fase)
            totale_lavorato += minuti_fase

            if f.stato == "completata":
                fasi_complete += 1

            if f.stato != "completata" and f.tempo_previsto and minuti_fase > f.tempo_previsto:
                fasi_ritardo += 1

    efficienza = round((totale_lavorato / totale_previsto) * 100, 1) if totale_previsto > 0 else 0
    saturazione = round((minuti_lavorati_oggi / 480) * 100, 1)  # 8 ore

    completamento = round((fasi_complete / fasi_totali) * 100, 1) if fasi_totali > 0 else 0

    return {
        "minuti_lavorati_oggi": minuti_lavorati_oggi,
        "efficienza": efficienza,
        "saturazione": saturazione,
        "completamento_fasi": completamento,
        "fasi_ritardo": fasi_ritardo
    }
@router.get("/{operatore_id}/kpi_grafico")
def kpi_grafico_operatore(
    operatore_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_user_from_token_db)
):
    oggi = datetime.utcnow().date()
    inizio = oggi - timedelta(days=6)

    # logs ultimi 7 giorni
    logs = (
        db.query(LogLavorazione)
        .filter(
            LogLavorazione.operatore_id == operatore_id,
            LogLavorazione.azione == "minuti_lavorati",
            LogLavorazione.timestamp >= inizio
        )
        .all()
    )

    # fasi dell’operatore
    commesse = db.query(Commessa).filter(Commessa.operatore_id == operatore_id).all()

    # struttura dati
    giorni = {}
    for i in range(7):
        giorno = oggi - timedelta(days=i)
        giorni[str(giorno)] = {"minuti": 0, "previsto": 0}

    # minuti lavorati
    for l in logs:
        g = str(l.timestamp.date())
        if g in giorni:
            giorni[g]["minuti"] += l.minuti or 0

    # tempo previsto (per efficienza)
    for c in commesse:
        for f in c.fasi:
            if f.tempo_previsto:
                giorni[str(f.data_assegnazione.date())]["previsto"] += f.tempo_previsto

    # output
    labels = sorted(giorni.keys())
    minuti = [giorni[g]["minuti"] for g in labels]
    efficienza = [
        round((giorni[g]["minuti"] / giorni[g]["previsto"]) * 100, 1)
        if giorni[g]["previsto"] > 0 else 0
        for g in labels
    ]

    return {
        "labels": labels,
        "minuti": minuti,
        "efficienza": efficienza
    }
@router.get("/{operatore_id}/kpi_puntualita")
def kpi_puntualita_operatore(
    operatore_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_user_from_token_db)
):
    commesse = (
        db.query(Commessa)
        .filter(Commessa.operatore_id == operatore_id)
        .all()
    )

    completate = [c for c in commesse if c.stato == "completata"]

    if not completate:
        return {
            "puntualita_percentuale": 0,
            "in_ritardo": 0,
            "in_anticipo": 0,
            "ritardo_medio": 0,
            "anticipo_medio": 0
        }

    in_ritardo = 0
    in_anticipo = 0
    giorni_ritardo = []
    giorni_anticipo = []

    for c in completate:
        if not c.data_consegna or not c.data_scadenza:
            continue

        diff = (c.data_consegna.date() - c.data_scadenza.date()).days

        if diff > 0:
            in_ritardo += 1
            giorni_ritardo.append(diff)
        else:
            in_anticipo += 1
            giorni_anticipo.append(abs(diff))

    totale = len(completate)
    puntualita = round((in_anticipo / totale) * 100, 1)

    ritardo_medio = round(sum(giorni_ritardo) / len(giorni_ritardo), 1) if giorni_ritardo else 0
    anticipo_medio = round(sum(giorni_anticipo) / len(giorni_anticipo), 1) if giorni_anticipo else 0

    return {
        "puntualita_percentuale": puntualita,
        "in_ritardo": in_ritardo,
        "in_anticipo": in_anticipo,
        "ritardo_medio": ritardo_medio,
        "anticipo_medio": anticipo_medio
    }
@router.get("/{operatore_id}/kpi_qualita")
def kpi_qualita_operatore(
    operatore_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_user_from_token_db)
):
    # Log qualità dell’operatore
    logs = (
        db.query(LogLavorazione)
        .filter(LogLavorazione.operatore_id == operatore_id)
        .all()
    )

    totale = len(logs)
    if totale == 0:
        return {
            "percentuale_qualita": 100,
            "errori": 0,
            "rilavorazioni": 0,
            "dettaglio_errori": [],
            "dettaglio_rilavorazioni": []
        }

    errori = [l for l in logs if l.azione == "errore"]
    rilavorazioni = [l for l in logs if l.azione == "rilavorazione"]

    percentuale = round(((totale - len(errori) - len(rilavorazioni)) / totale) * 100, 1)

    return {
        "percentuale_qualita": percentuale,
        "errori": len(errori),
        "rilavorazioni": len(rilavorazioni),
        "dettaglio_errori": [
            {"fase": e.fase_id, "note": e.note, "data": e.timestamp}
            for e in errori
        ],
        "dettaglio_rilavorazioni": [
            {"fase": r.fase_id, "note": r.note, "data": r.timestamp}
            for r in rilavorazioni
        ]
    }
