# AssurAI — POC assurance & protection sociale

**POC exécutable :** instruction assistée d'une prestation santé fictive. **Python/FastAPI + moteur de règles Java 21 + SQLite + recherche de clauses contrôlée.** Ollama facultatif pour reformuler une décision ; **le LLM ne calcule rien et ne valide aucun paiement**.

## Démarrer sur portable (WSL2/Docker)

```bash
git clone https://github.com/zdmooc/insurance-social-protection-agentic-ai.git
cd insurance-social-protection-agentic-ai
docker compose up --build -d
curl http://localhost:8000/health
curl -s -X POST http://localhost:8000/v1/claims -H 'Content-Type: application/json' -d @data/example-claim.json
```

**Résultat attendu :** `status=READY_FOR_REVIEW`, `eligible_cents=4000`, citation `CG-ESS-2026-01-A`, `payment_executed=false`.

Après envoi du dossier :
```bash
curl http://localhost:8000/v1/claims/CLM-100/explanation
curl -s -X POST http://localhost:8000/v1/claims/CLM-100/review -H 'Content-Type: application/json' -d '{"reviewer":"GestionnaireTest","decision":"APPROVE","reason":"Dossier fictif contrôlé"}'
curl http://localhost:8000/v1/claims/CLM-100
```

Documentation interactive : http://localhost:8000/docs. Arrêt : `docker compose down` (les dossiers SQLite persistent dans le volume Docker).

## Tests (Python + Java disponibles en local)

```bash
python -m pip install -r requirements.txt pytest
PYTHONPATH=. pytest -q  # les tests compilent et démarrent automatiquement Java
```

## Comprendre en 3 fichiers

- [Métier assurance](01-business-architecture/README.md)
- [Cas d'usage et scénarios](02-agentic-ai-use-cases/README.md)
- [Architecture locale et cloud](03-solution-architecture/README.md)

## Fonctionnement

`POST /v1/claims` → validation contrat et bénéficiaire → recherche de garantie avec source → extraction stricte du document texte fictif → calcul **Java** → `READY_FOR_REVIEW` → décision explicite du gestionnaire → lecture du dossier.

Cas d'erreur : document absent, incohérence, faible confiance, contrat expiré, prestation non couverte, doublon et replay idempotent. La consultation optionnelle d'Ollama : `GET /v1/claims/CLM-100/explanation?use_ollama=true` (requiert Ollama local et `qwen2.5:3b`). Sans modèle, la réponse reste fonctionnelle.

**Limites claires :** données entièrement inventées ; extraction de texte structuré (pas d'OCR sur PDF), récupération de clauses filtrée (pas d'index vectoriel), workflow contrôlé (pas d'autonomie multi-agents), revue simulée sans IAM, SQLite mono-instance, aucun SI assureur réel, aucune transaction bancaire, aucun cloud externe. Ce POC n'est pas un système de liquidation ou de paiement de production.
