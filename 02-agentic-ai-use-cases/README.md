# Cas d'usage IA

| Priorité | Cas | Apport IA |
|---|---|---|
| 1 | Prestations santé | Lecture facture, RAG garanties, dossier préparé |
| 2 | Conseiller adhérent | Recherche de garanties et réponses sourcées |
| 3 | Prévoyance | Extraction de pièces et dossier incomplet |
| 4 | Retraite | Recherche de périodes et explication des droits |
| 5 | Assurance collective / DSN | Contrôle et qualification d'anomalies |
| 6 | Réclamations | Classification et brouillon de réponse |

## POC n° 1 — Prestation santé (à implémenter)

**Entrée :** facture fictive, contrat fictif, clauses de garantie et barème simulé.

**Traitement :**
```text
Facture → extraction JSON → API contrat/garanties
        → RAG (clauses citées) → règles de calcul
        → revue humaine si nécessaire → décision simulée + audit
```

**Sortie :** dossier qualifié, calcul traçable, motifs, sources utilisées, statut de validation. Aucun paiement réel.

**Tests obligatoires :**
1. Dossier nominal et garantie valide.
2. Facture manquante ou champs illisibles.
3. Contrat expiré ou bénéficiaire non couvert.
4. Doublon d'une demande.
5. Clause introuvable ou contradictoire : abstention/escalade.
6. Instruction malveillante dans un document : aucun appel d'outil non autorisé.
7. Montant calculé par le moteur de règles, jamais inventé par le LLM.
8. Même dossier rejoué : pas de double décision.

**Livrables à produire :** corpus synthétique, services/API simulées, tests automatisés, démonstration reproductible.
