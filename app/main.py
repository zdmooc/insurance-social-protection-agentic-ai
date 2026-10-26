"""Synthetic health-claims assistant: retrieval + deterministic Java rules + human review."""
from __future__ import annotations

from datetime import date, datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Literal
import json
import os
import re
import sqlite3

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
CATALOG = json.loads((ROOT / "data" / "catalog.json").read_text(encoding="utf-8"))
CLAUSES = json.loads((ROOT / "data" / "clauses.json").read_text(encoding="utf-8"))


class Claim(BaseModel):
    claim_id: str = Field(pattern=r"^[A-Za-z0-9_-]{3,40}$")
    invoice_ref: str = Field(pattern=r"^[A-Za-z0-9_-]{3,40}$")
    contract_id: str = Field(pattern=r"^[A-Za-z0-9_-]{3,40}$")
    beneficiary_id: str = Field(pattern=r"^[A-Za-z0-9_-]{3,40}$")
    care_date: date
    act_code: Literal["CONSULTATION", "OPTIQUE", "DENTAIRE", "HOSPITALISATION"]
    amount_cents: int = Field(gt=0, le=1_000_000)
    document_text: str = Field(default="", max_length=3000)
    extraction_confidence: float = Field(default=1.0, ge=0, le=1)


class Review(BaseModel):
    reviewer: str = Field(min_length=2, max_length=60)
    decision: Literal["APPROVE", "REJECT"]
    reason: str = Field(min_length=3, max_length=500)


def extract_fields(document: str) -> dict[str, str]:
    """Strict extraction of synthetic key=value invoices; never execute document instructions."""
    found: dict[str, str] = {}
    for line in document.splitlines():
        match = re.fullmatch(r"\s*(invoice_ref|amount_cents|act_code|care_date)\s*=\s*([A-Za-z0-9_-]+)\s*", line)
        if match:
            if match.group(1) in found and found[match.group(1)] != match.group(2):
                found[match.group(1)] = "CONFLICT"
            else:
                found[match.group(1)] = match.group(2)
    return found


def retrieve_clause(plan: str, act: str) -> dict | None:
    """Plan/act-scoped documentary retrieval with an explicit source ID."""
    return next((c for c in CLAUSES if c["plan"] == plan and c["act"] == act), None)


def evaluate(claim: Claim, rules_url: str) -> dict:
    audit: list[str] = ["request_schema_validated"]
    contract = next((c for c in CATALOG["contracts"] if c["contract_id"] == claim.contract_id), None)
    if not contract:
        return result("INELIGIBLE", "UNKNOWN_CONTRACT", claim, audit)
    if contract["beneficiary_id"] != claim.beneficiary_id:
        return result("INELIGIBLE", "BENEFICIARY_MISMATCH", claim, audit)
    if not (date.fromisoformat(contract["start_date"]) <= claim.care_date <= date.fromisoformat(contract["end_date"])):
        return result("INELIGIBLE", "OUTSIDE_COVERAGE_DATES", claim, audit)
    audit.append("contract_coverage_checked")
    clause = retrieve_clause(contract["plan"], claim.act_code)
    if clause is None:
        return result("INELIGIBLE", "ACT_NOT_COVERED", claim, audit)
    audit.append("clause_retrieved:" + clause["source_id"])
    citations = [{"source_id": clause["source_id"], "text": clause["text"]}]

    if not claim.document_text.strip():
        return result("NEEDS_REVIEW", "DOCUMENT_MISSING", claim, audit, citations)
    if claim.extraction_confidence < 0.85:
        return result("NEEDS_REVIEW", "LOW_EXTRACTION_CONFIDENCE", claim, audit, citations)
    extracted = extract_fields(claim.document_text)
    expected = {"invoice_ref": claim.invoice_ref, "amount_cents": str(claim.amount_cents),
                "act_code": claim.act_code, "care_date": claim.care_date.isoformat()}
    if not all(extracted.get(k) == v for k, v in expected.items()):
        return result("NEEDS_REVIEW", "DOCUMENT_MISMATCH", claim, audit, citations)
    audit.append("synthetic_invoice_fields_matched")

    try:
        response = httpx.get(rules_url.rstrip("/") + "/quote", params={
            "amount_cents": claim.amount_cents, "rate_percent": clause["rate_percent"],
            "cap_cents": clause["cap_cents"]}, timeout=3)
        response.raise_for_status()
        eligible = response.json()["eligible_cents"]
        if type(eligible) is not int or not 0 <= eligible <= claim.amount_cents:
            raise ValueError("Invalid rules-service amount")
    except (httpx.HTTPError, ValueError, KeyError, TypeError) as exc:
        raise HTTPException(status_code=503, detail="Java rules service unavailable or invalid") from exc
    audit.append("java_deterministic_rule_calculated")
    return result("READY_FOR_REVIEW", "RULES_QUOTE_COMPUTED", claim, audit, citations, eligible)


def result(status: str, reason: str, claim: Claim, audit: list[str],
           citations: list[dict] | None = None, eligible_cents: int | None = None) -> dict:
    return {"claim_id": claim.claim_id, "status": status, "reason": reason,
            "eligible_cents": eligible_cents, "citations": citations or [], "audit": audit,
            "payment_executed": False}


def connect(path: str) -> sqlite3.Connection:
    con = sqlite3.connect(path, timeout=5)
    con.row_factory = sqlite3.Row
    return con


def create_app(db_path: str | None = None, rules_url: str | None = None) -> FastAPI:
    db_path = db_path or os.getenv("DB_PATH", "/tmp/assurai.db")
    rules_url = rules_url or os.getenv("RULES_URL", "http://localhost:8090")
    with connect(db_path) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS claims (
            claim_id TEXT PRIMARY KEY, invoice_ref TEXT UNIQUE NOT NULL,
            fingerprint TEXT NOT NULL, request_json TEXT NOT NULL,
            result_json TEXT NOT NULL, review_json TEXT)""")
    app = FastAPI(title="AssurAI - Synthetic Health Benefits", version="1.0")

    def lookup(claim_id: str) -> dict:
        with connect(db_path) as con:
            row = con.execute("SELECT * FROM claims WHERE claim_id = ?", (claim_id,)).fetchone()
        if row is None:
            raise HTTPException(404, "Unknown claim")
        output = json.loads(row["result_json"])
        if row["review_json"]:
            recorded_review = json.loads(row["review_json"])
            output["review"] = recorded_review
            output["status"] = ("APPROVED_SIMULATED" if recorded_review["decision"] == "APPROVE"
                                else "REJECTED_BY_REVIEWER")
        return output

    @app.get("/health")
    def health():
        return {"status": "ok", "rules_url": rules_url}

    @app.post("/v1/claims")
    def submit(claim: Claim):
        serialized = claim.model_dump_json()
        fingerprint = sha256(serialized.encode()).hexdigest()
        # Transactional mutex ensures idempotent replays and invoice uniqueness.
        with connect(db_path) as con:
            con.execute("BEGIN IMMEDIATE")
            existing = con.execute("SELECT fingerprint, result_json, review_json FROM claims WHERE claim_id = ?",
                                   (claim.claim_id,)).fetchone()
            if existing:
                if existing["fingerprint"] != fingerprint:
                    raise HTTPException(409, "Claim ID reused with different data")
                saved = json.loads(existing["result_json"])
                if existing["review_json"]:
                    saved["review"] = json.loads(existing["review_json"])
                return saved
            dupe = con.execute("SELECT claim_id FROM claims WHERE invoice_ref = ?", (claim.invoice_ref,)).fetchone()
            if dupe:
                raise HTTPException(409, "Invoice already attached to another claim")
            output = evaluate(claim, rules_url)
            con.execute("INSERT INTO claims VALUES (?, ?, ?, ?, ?, NULL)",
                        (claim.claim_id, claim.invoice_ref, fingerprint, serialized, json.dumps(output)))
            return output

    @app.get("/v1/claims/{claim_id}")
    def get_claim(claim_id: str):
        return lookup(claim_id)

    @app.post("/v1/claims/{claim_id}/review")
    def review_claim(claim_id: str, request: Review):
        with connect(db_path) as con:
            con.execute("BEGIN IMMEDIATE")
            row = con.execute("SELECT * FROM claims WHERE claim_id = ?", (claim_id,)).fetchone()
            if row is None:
                raise HTTPException(404, "Unknown claim")
            stored = json.loads(row["result_json"])
            if stored["status"] == "INELIGIBLE" and request.decision == "APPROVE":
                raise HTTPException(409, "Cannot override contract ineligibility")
            if row["review_json"]:
                raise HTTPException(409, "Decision already reviewed")
            review = {"reviewer": request.reviewer, "decision": request.decision,
                      "reason": request.reason, "recorded_at": datetime.now(timezone.utc).isoformat(),
                      "simulation_only": True}
            con.execute("UPDATE claims SET review_json = ? WHERE claim_id = ?",
                        (json.dumps(review), claim_id))
            stored["review"] = review
            stored["status"] = "APPROVED_SIMULATED" if request.decision == "APPROVE" else "REJECTED_BY_REVIEWER"
            # Immutable original evaluation + review overlay; no payment endpoint exists.
            return stored

    @app.get("/v1/claims/{claim_id}/explanation")
    def explanation(claim_id: str, use_ollama: bool = False):
        claim = lookup(claim_id)
        if not claim["citations"]:
            return {"source": "deterministic", "text": "Aucune clause applicable citée ; revue nécessaire."}
        clause = claim["citations"][0]
        default = f"Selon {clause['source_id']} : {clause['text']} État : {claim['status']}. Montant proposé : {claim['eligible_cents']} centimes."
        if not use_ollama:
            return {"source": "deterministic", "text": default, "citations": claim["citations"]}
        try:
            # Only vetted clause and computed result sent to LLM, never untrusted document text.
            ollama = os.getenv("OLLAMA_URL", "http://localhost:11434").rstrip("/")
            prompt = ("Résume brièvement en français ce résultat FICTIF. Aucun conseil médical, aucune nouvelle décision. "
                      "Ne modifie jamais le montant ni les citations.\n" + default)
            r = httpx.post(ollama + "/api/generate", json={"model": os.getenv("OLLAMA_MODEL", "qwen2.5:3b"),
                           "prompt": prompt, "stream": False}, timeout=25)
            r.raise_for_status()
            answer = r.json()["response"]
            return {"source": "ollama", "text": answer, "citations": claim["citations"],
                    "authoritative_amount_cents": claim["eligible_cents"]}
        except (httpx.HTTPError, KeyError, ValueError):
            return {"source": "deterministic_fallback", "text": default, "citations": claim["citations"]}

    return app


app = create_app()
