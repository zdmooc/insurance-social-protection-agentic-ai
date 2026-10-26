# ADR-001 — Placement des modèles IA : on-premise, SaaS/API ou hybride

- **Statut : PROPOSED**
- **Date : 2026-10-26**
- **Périmètre :** POC synthétique santé/prévoyance et architecture de référence, sans client réel identifié.

## Question

Faut-il exécuter les modèles dans une infrastructure propre, payer un fournisseur de modèles via API, ou combiner les deux ?

## Options examinées

| Option | Description | Limite principale |
| --- | --- | --- |
| A — local/privé | Ollama CPU pour développement ou KServe/vLLM sur GPU privé | Exploitation et dimensionnement |
| B — managé | AWS Bedrock, Azure AI ou service équivalent sous contrat | Coûts variables, traitement et localisation des données à valider |
| C — hybride | Même contrat d'inférence ; choix via AI Gateway selon politique et modèle | Gouvernance et complexité de routage |
| D — sans LLM | Règles, OCR classique et workflow | Limité pour recherche/résumé libres, mais souvent préférable sur les décisions |

## Décision provisoire

**C pour l'architecture cible**, et **A ou D pour la première démonstration sans coût externe**. Le cloud n'est introduit que lorsqu'un test d'intégration réel justifie sa valeur et dispose des autorisations nécessaires.

### Règles de placement

1. Ne jamais transmettre des données de santé ou d'identité réelles dans le portfolio.
2. Classifier données, finalité et sortie avant tout routage.
3. **Pas de fallback transfrontalier ou non autorisé** sur indisponibilité du fournisseur.
4. Le LLM ne tranche pas seul les droits contractuels ni les montants de prestation.
5. Comparer qualité, latence, coût total, opérations, résilience, réversibilité, consommation et exigences réglementaires.
6. Assumer qu'un fournisseur managé peut être facturé **au token, à la capacité ou au contrat** ; vérifier l'offre et les tarifs à date avant décision.

## Vérifications avant ACCEPTED

- Matrice de sensibilité des données et traitements.
- Localisation contractuelle, sous-traitants, rétention et politique de non-entraînement.
- Performances sur un jeu de tests synthétiques et versions de modèles comparables.
- Coûts de bout en bout (API, OCR, réseau, stockage, GPU, exploitation et retries).
- Test de panne, circuit breaker, contrôle des accès et traces de routage.
- Accord sécurité/conformité, juriste/DPO et comité d'architecture si applicable.

## Sources internes à réutiliser

- [Dossier de choix banque / assurance](https://github.com/zdmooc/enterprise-ai-infrastructure-reference-architecture/blob/main/studies/I13-architecture-decision-banking-insurance.md).
- [ADR placement hybride](https://github.com/zdmooc/enterprise-ai-infrastructure-reference-architecture/blob/main/adrs/ADR-0002-hybrid-placement.md).
- [Agentic Platform Build vs Buy](https://github.com/zdmooc/maya-ai-agentic-architecture-reference/blob/main/enterprise/AGENTIC-PLATFORM-BUILD-VS-BUY-2026.md).
