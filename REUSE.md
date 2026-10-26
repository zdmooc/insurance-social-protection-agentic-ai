# Source de vérité — Réutilisation sans duplication

Statut : **INVENTAIRE V0.1**, état lu au 26 octobre 2026 ; revalider avant toute affirmation en entretien.

| Brique | Dépôt propriétaire à référencer | Ce qui est réutilisé | État |
| --- | --- | --- | --- |
| Architecture IA agentique | [maya-ai-agentic-architecture-reference](https://github.com/zdmooc/maya-ai-agentic-architecture-reference) | Architecture cible, comité, IAM, MCP/A2A, Build vs Buy | DESIGN |
| Moteur de démonstration | [TradeOps-GenAI-Integration](https://github.com/zdmooc/TradeOps-GenAI-Integration) | LangGraph, RAG, MCP, AI Gateway, LiteLLM, observabilité | CODE + certaines preuves CRC |
| Infrastructure privée/cloud | [enterprise-ai-infrastructure-reference-architecture](https://github.com/zdmooc/enterprise-ai-infrastructure-reference-architecture) | GPU, SLM/LLM, on-prem/cloud/hybride, coûts, carbone | DOCUMENTAIRE |
| Patterns IA | [enterprise-architecture-patterns-handbook](https://github.com/zdmooc/enterprise-architecture-patterns-handbook) | RAG, AI Gateway, Model Router, HITL, Model Serving | PÉDAGOGIQUE |
| Décision métier | [mayabank-ibm-odm-ai-decision-architecture](https://github.com/zdmooc/mayabank-ibm-odm-ai-decision-architecture) | Frontière règles/LLM, décision déterministe | À qualifier avant réemploi du runtime |
| Azure | [mayabank-azure-cloud-ai-platform](https://github.com/zdmooc/mayabank-azure-cloud-ai-platform) | Landing zone, identité, réseau, patterns Azure AI | DESIGN, cloud live non prouvé |
| Données retraite | [retirement-social-protection-data-platform-reference-architecture](https://github.com/zdmooc/retirement-social-protection-data-platform-reference-architecture) | Concepts carrière/provenance, données synthétiques | Laboratoire CI, pas SI réel |

## Règle de propriété

Ce dépôt est **propriétaire des objets métier assurance/protection sociale, des scénarios, des mappings vers l'architecture SI, des contrats de démonstration, jeux de données synthétiques et preuves propres au POC assurance**.

Les plateformes génériques (IA Gateway, IAM, outils MCP, CI/CD, OpenShift, patterns) restent dans leurs dépôts maîtres. Consommer ces briques via API, module versionné ou contrat documenté ; ne pas recopier le code par défaut.

## Discipline de preuve

- **SOURCE / DESIGN** : référence ou intention.
- **CODE / CI** : implémentation ou test observé (périmètre exact à citer).
- **CRC_RUNTIME_PROVEN** : démonstration locale datée, non transposable à la production par simple affirmation.
- **CLOUD_RUNTIME_PROVEN** : exige logs/exécution réel chez le fournisseur ciblé (non revendiqué ici).
- **ASSURANCE_USE_CASE_PROVEN** : exige tests sur corpus synthétique + moteur de règles + citations + audit (non revendiqué ici).
