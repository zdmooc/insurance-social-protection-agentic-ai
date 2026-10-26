# Insurance & Social Protection — Agentic AI

**Référentiel métier et architecture de solutions IA pour l'assurance, la santé, la prévoyance et la retraite.**

Statut : **V0.1 — CADRAGE / DESIGN** (26 octobre 2026). Ce dépôt vient d'être initialisé. Aucun POC propre à ce dépôt, déploiement cloud ou intégration à un SI assureur réel n'est revendiqué.

## Objectifs

- Traduire les processus d'assurance et de protection sociale en cas d'usage IA évaluables.
- Concevoir des architectures fonctionnelles, applicatives et solutions pour RAG, assistants et agents.
- Comparer IA **on-premise**, **API managée** et **hybride**, avec arbitrages techniques, économiques et réglementaires.
- Démontrer **un dossier de prestation santé synthétique** de bout en bout : document, recherche contractuelle, règles déterministes, décision contrôlée.
- Préparer les livrables attendus d'un architecte SI : cartographie, cible, trajectoire, ADR, NFR, dossier d'arbitrage et preuves.

## Navigation

| Volet | Document | Résultat attendu |
| --- | --- | --- |
| 1 — Métier | [Architecture métier](01-business-architecture/README.md) | Capacités, acteurs, objets, processus, décisions |
| 2 — Cas d'usage | [Agents et scénarios](02-agentic-ai-use-cases/README.md) | Backlog de cas métier, scénario et critères d'acceptation |
| 3 — Solution | [Architecture cible](03-solution-architecture/README.md) | Composants, flux, responsabilités, intégration SI |
| Décisions | [ADR-001 : placement des LLM](decisions/ADR-001-llm-placement.md) | Comparaison on-prem / cloud / hybride |
| Preuves | [Réutilisation des dépôts existants](REUSE.md) | Source de vérité et limites de chaque réutilisation |
| Exécution | [Roadmap](ROADMAP.md) | Itérations et états de preuve |
| Mission | [Couverture de l'offre](MISSION-ALIGNMENT.md) | Exigences d'un poste d'architecte IA et livrables associés |

## Périmètre métier

Santé complémentaire (adhésion, garanties, devis, prestations et remboursements), prévoyance (incapacité, invalidité, décès), retraite et retraite complémentaire (carrière, droits, réclamations), assurance collective (affiliations, DSN), relation adhérent.

**Aucune affirmation sur l'architecture interne de Malakoff Humanis, AG2R, AXA ou d'un autre client.** Les cas et données du portfolio sont fictifs.

## Principes d'architecture

1. **Métier d'abord :** mesurer le résultat métier, pas seulement la qualité d'un texte généré.
2. **Séparation des responsabilités :** le LLM lit/résume/propose ; le moteur de règles et le SI métier font autorité pour droits, calculs, décisions et transactions.
3. **Least agency :** un workflow classique avant de créer plusieurs agents autonomes.
4. **Intégration par contrats :** API/versionnement, événements métier, isolation de la GED/CRM/SI gestion.
5. **RAG gouverné :** documents autorisés, provenance, citations, qualité et abstention.
6. **Données synthétiques uniquement dans ce dépôt public** ; pas de données personnelles ou de santé réelles, ni de secrets.
7. **Evidence-first :** DESIGNED ≠ IMPLEMENTED ≠ CI_TESTED ≠ RUNTIME_PROVEN ≠ PRODUCTION.
8. **Réutilisation avant duplication :** conserver les composants techniques dans leurs dépôts d'origine, ne créer ici que des adaptateurs et cas métier spécifiques.

## Architecture en une ligne

Canal adhérent/gestionnaire → API métier → workflow → extraction documentaire et RAG → agent d'assistance gouverné → APIs de contrats/garanties/prestations + moteur de règles → revue humaine si nécessaire → SI de gestion.

Le choix du fournisseur LLM relève d'un **AI Gateway / model router** et d'une politique de données. Voir l'[ADR-001](decisions/ADR-001-llm-placement.md).

## Priorité immédiate

**UC-SANTE-01 : instruction assistée d'une demande de prestation santé** avec données 100 % synthétiques, décisions déterministes, citations de garanties et validation humaine sur cas incertains. Aucun ordre de paiement réel.
