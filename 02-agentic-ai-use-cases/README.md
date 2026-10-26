# 02 — Cas d'usage IA générative et agentique

Statut : **BACKLOG / DESIGN**. Aucun POC métier ci-dessous n'est considéré exécuté.

## Catalogue priorisé

| ID | Use case | Patrons | Priorité |
| --- | --- | --- | --- |
| UC-SANTE-01 | Instruction assistée d'une prestation santé | IDP/OCR, RAG, workflow, rules engine, HITL | P1 |
| UC-RELATION-02 | Assistant conseiller : contrats et garanties | RAG gouverné, citations, API CRM | P1 |
| UC-PREVOYANCE-03 | Constitution et pré-analyse d'un dossier prévoyance | Extraction, workflow, escalade | P2 |
| UC-RETRAITE-04 | Recherche des périodes de carrière et explication de droits | RAG, API carrière, validation métier | P2 |
| UC-COLLECTIF-05 | Assistance au traitement d'anomalies d'affiliation/DSN | Contrôles de cohérence, outils, file de travail | P3 |
| UC-RECLAM-06 | Préparation de réponses aux réclamations | Classification, RAG, rédaction contrôlée | P3 |

## UC-SANTE-01 — Vertical slice cible

### Chaîne prévue

```text
Demande synthétique + facture fictive
    -> API / dossiers
    -> Workflow d'instruction (orchestrateur explicite)
    -> Extraction structurée et validation de schéma
    -> API contrat + garanties (mock)
    -> RAG garanties versionnées (avec citations)
    -> Calcul via règles déterministes (mock / adaptateur)
    -> Contrôle des écarts et seuils métier
    -> Approbation humaine si nécessaire
    -> Enregistrement d'une décision fictive
    -> Réponse explicative traçable
```

### Découpage agentique

Commencer avec **workflow déterministe + un assistant RAG/outils** ; n'introduire un second agent spécialisé (pièces, contrats, analyse d'anomalie) que lorsque les évaluations montrent un bénéfice mesurable. LangGraph est une option de mise en œuvre déjà présente dans le portfolio.

### Contrats minimaux envisagés

- `POST /v1/prestations/dossiers` — ouvrir dossier synthétique.
- `GET /v1/contrats/{contratId}/garanties?date=...` — lire garanties fictives.
- `POST /v1/documents/extractions` — produire un JSON validé (provenance et score).
- `POST /v1/prestations/{dossierId}/evaluations` — calcul métier déterministe.
- `POST /v1/prestations/{dossierId}/revues` — revue humaine simulée.
- `GET /v1/prestations/{dossierId}/audit` — preuve des décisions et versions.

Ces chemins sont des **propositions d'API**, non des interfaces réelles d'assureurs.

### Tests d'acceptation indispensables

1. La réponse cite les clauses de garanties utilisées ou s'abstient.
2. Une pièce manquante n'aboutit pas à une décision automatique.
3. Un contrat expiré ou un bénéficiaire non couvert déclenche un contrôle déterministe.
4. Le LLM ne peut modifier un calcul ou initier un paiement.
5. Une instruction cachée dans un document ne déclenche aucune action non autorisée.
6. Le même dossier rejoué ne crée pas de décision ou paiement en doublon (idempotence).
7. Journal d'audit = références, versions de modèles/prompts/règles, décision, identité de l'acteur.
8. Les profils privés/cloud sont testables par le même contrat, sans envoyer de données classifiées vers un fournisseur non autorisé.

## Exigences de preuve

**DESIGNED** = schéma et contrat ; **IMPLEMENTED** = code réel ; **CI_TESTED** = tests reproductibles ; **RUNTIME_PROVEN** = traces d'exécution conservées. La démonstration d'un POC local ne signifie ni certification, ni conformité ni production.
