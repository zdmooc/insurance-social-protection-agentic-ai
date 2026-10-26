# IA agentique — Assurance & protection sociale

**Objectif :** concevoir et démontrer une solution IA intégrée au SI d'un assureur ou d'un groupe de protection sociale.

## Commencer ici

1. [Métier](01-business-architecture/README.md) — santé, prévoyance, retraite, contrats, prestations.
2. [Cas d'usage](02-agentic-ai-use-cases/README.md) — scénario de remboursement santé et tests.
3. [Architecture](03-solution-architecture/README.md) — API, agents, règles métier, LLM local ou cloud.

## Premier POC : instruction d'une prestation santé

Facture fictive → extraction → consultation des garanties → RAG documentaire → calcul par moteur de règles → validation → décision tracée.

**À construire dans l'ordre :**
- [x] Modèle métier et architecture cible.
- [ ] 10 dossiers de test entièrement fictifs + contrats et garanties.
- [ ] API métier simulées + règles de remboursement déterministes.
- [ ] RAG + workflow agentique + approbation du gestionnaire.
- [ ] Tests de bout en bout : exactitude, citations, erreurs, coûts et traçabilité.

Ne pas recopier les plateformes IA déjà présentes dans les autres dépôts. Ce dépôt contient le **métier, les adaptateurs spécifiques et les preuves du POC assurance**. Aucun POC d'assurance n'est encore exécuté.
