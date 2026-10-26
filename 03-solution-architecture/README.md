# Architecture solution — IA locale, cloud ou hybride

## Vue d'ensemble

```text
Adhérent / gestionnaire
        |
API Dossiers + workflow
        |
        +---- Extraction et RAG ---- GED / clauses / base documentaire
        |
        +---- Agent LangGraph ---- Outils autorisés / APIs contrats et garanties
        |
        +---- Moteur de règles ---- SI prestations simulé
        |
   Validation humaine (si nécessaire)
        |
   Décision simulée + audit

IA / RAG / Agents → AI Gateway (LiteLLM) → Modèle local OU service cloud autorisé
```

## Comparaison d'hébergement

| Variante | Modèle | À vérifier |
|---|---|---|
| **Locale** | Ollama ; à plus grande échelle OpenShift AI/KServe/vLLM | Ressources CPU/GPU, performance, exploitation |
| **Cloud** | AWS Bedrock ou Azure AI via API | Région, confidentialité, coût, contrats |
| **Hybride** | AI Gateway choisissant le fournisseur selon le dossier | Routage par classification, repli autorisé, traçabilité |

**Orientation POC :** commencer en local, comparer le cloud ensuite sur le **même jeu de tests fictifs**. Aucun abonnement cloud n'est requis pour le premier POC.

## Frontières techniques

- L'IA propose et explique ; les **règles déterministes** et le **SI métier** font autorité.
- Les outils ne reçoivent que les autorisations nécessaires ; une opération sensible nécessite un contrôle.
- Chaque décision conserve : identifiant du dossier, sources, version des garanties, version des règles, modèle et validation.
- Comparer exactitude, abstention, latence, coût par dossier et taux de revue humaine.

## Réutilisation (sans copie de code)

- [TradeOps-GenAI-Integration](https://github.com/zdmooc/TradeOps-GenAI-Integration) : LangGraph, RAG, MCP, AI Gateway/LiteLLM, Ollama sur CRC (tests locaux existants).
- [maya-ai-agentic-architecture-reference](https://github.com/zdmooc/maya-ai-agentic-architecture-reference) : architecture des agents et arbitrages fournisseurs.
- [enterprise-ai-infrastructure-reference-architecture](https://github.com/zdmooc/enterprise-ai-infrastructure-reference-architecture) : comparatif on-prem/cloud/hybride, notamment pour l'assurance.
- [mayabank-ibm-odm-ai-decision-architecture](https://github.com/zdmooc/mayabank-ibm-odm-ai-decision-architecture) : séparation moteur de règles / IA.

Le fonctionnement du modèle Ollama a été démontré dans TradeOps. **Aucun parcours prestations santé ni déploiement Bedrock/Azure propre à ce dépôt n'est encore démontré.**
