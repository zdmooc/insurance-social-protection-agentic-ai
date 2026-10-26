# 03 — Architecture de solutions IA hybride pour assurance et protection sociale

Statut : **TARGET DESIGN V0.1**. Architecture indépendante, non attribuée à une entreprise.

## Vue logique

```text
Adhérent / gestionnaire / CRM / GED
                  |
             API Gateway
                  |
          Dossier & Workflow
                  |
       IA access / orchestration
         |             |
   Extracteur/RAG    Tools approuvés (MCP optionnel)
         |             |
    Vector store   APIs Contrat/Garantie/Prestations
         |             |
         +------> Rules engine ------> Revue humaine
                  |
             Audit / SI gestion simulé

               AI Gateway
                   |
              Model Router
           /        |        \
     Local privé   AWS       Azure
    Ollama/vLLM   Bedrock    AI models
```

### Répartition des responsabilités

| Couche | Rôle | Options réutilisables |
| --- | --- | --- |
| Applications métier | Capturer et suivre les dossiers ; état de référence | API mock, workflow métier |
| Intégration | Accès gouverné aux garanties et aux prestations | API REST/OpenAPI, événements, IBM MQ/Kafka si justifié |
| Knowledge | Ingestion, versionnage, ACL, citations, suppression | RAG, Qdrant/pgvector selon ADR |
| IA agentique | Recherche, extraction, planification bornée, synthèse | LangGraph, tool calling, MCP si justifié |
| Décision | Règles déterministes, contraintes contractuelles, validation | IBM ODM / moteur factice, HITL |
| Accès modèles | Routage, identité, quotas, coût, observabilité | AI Gateway/LiteLLM + routeur |
| Inférence | Modèles locaux ou managés selon politique | Ollama, KServe/vLLM, AWS Bedrock, Azure AI |
| Opérations | Évaluation, traçage, sécurité, GitOps | OpenTelemetry, Prometheus, Grafana, OpenShift |

## Scénarios d'hébergement à comparer

| Scénario | Où s'exécute le LLM ? | Atouts | Questions de qualification |
| --- | --- | --- | --- |
| S1 Privé | Machine locale, datacenter privé, OpenShift AI avec KServe/vLLM | Contrôle des données et de l'inférence | GPU/CPU, VRAM, SLO, MCO, coût complet |
| S2 Managé | AWS Bedrock / Azure AI / autre API approuvée | Évolutivité et catalogue de modèles | Localisation, traitements, sous-traitance, latence, coût/tokens |
| S3 Hybride | Router privé + fournisseurs selon classification | Placement par besoin et réversibilité | Politique de routage testée, repli strict et audit |

Une plateforme **interne** n'implique pas que le modèle est **on-premise**. Un abonnement bureautique type ChatGPT n'est pas équivalent à un service API facturé à l'usage.

## État des preuves réutilisables

- [TradeOps G1 : modèle Ollama réel, single-consumer CRC](https://github.com/zdmooc/TradeOps-GenAI-Integration/blob/main/evidence/d090/20261007-g1-crc-runtime-proof.md) — preuve technique locale, **pas POC assurance**.
- [TradeOps G2 : identité, quota, budget, télémétrie](https://github.com/zdmooc/TradeOps-GenAI-Integration/blob/main/evidence/d090/20261007-g2-crc-runtime-proof.md) — preuve technique sur le même périmètre.
- [TradeOps OpenShift AI / KServe / vLLM](https://github.com/zdmooc/TradeOps-GenAI-Integration/blob/main/docs/19-openshift-ai-model-serving.md) — design ; GPU live non prouvé.
- [Comparaison Build vs Buy / hybride](https://github.com/zdmooc/maya-ai-agentic-architecture-reference/blob/main/enterprise/AGENTIC-PLATFORM-BUILD-VS-BUY-2026.md) — cadrage documenté ; plateformes cloud managées non démontrées en exécution ici.

## NFR à formaliser

Disponibilité, RTO/RPO, p95/p99, confidentialité et minimisation, politique multi-tenant et ACL, capacité, coût par dossier utile, qualité des citations, taux d'erreur et d'abstention, continuité sans LLM, journalisation des décisions, traçabilité des changements.

Aucune valeur cible NFR n'est inventée : faire valider les seuils par le métier et l'exploitant.
