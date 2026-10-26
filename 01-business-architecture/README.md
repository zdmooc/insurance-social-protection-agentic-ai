# 01 — Architecture métier assurance et protection sociale

Statut : **DESIGNED / V0.1**, modèles métier de référence fictifs à valider pour chaque organisme.

## Cartographie des capacités

| Domaine | Capacités clés | Acteurs | Objets métier | Opportunité IA |
| --- | --- | --- | --- | --- |
| Santé complémentaire | Affiliations, garanties, devis, prestations, tiers payant, réclamations | Adhérent, gestionnaire, conseiller | Contrat, bénéficiaire, garantie, facture, décompte, prestation | Lecture pièces, RAG contractuel, complétude dossier |
| Prévoyance | Déclaration, constitution de dossier, analyse de pièces, instruction, suivi | Assuré, employeur, gestionnaire | Arrêt, incapacité, invalidité, garantie, justificatif | Classification, extraction et synthèse d'instruction |
| Retraite | Carrières, droits, liquidation, paiement, réclamations | Affilié, gestionnaire, employeur | Carrière, période, cotisation, point, droit, pension | Explication traçable et recherche d'anomalies |
| Assurance collective | Affiliations, cotisations, événements de population | Entreprise, salarié, gestionnaire | Contrat collectif, affiliation, DSN, cotisation | Contrôle de cohérence, pré-tri d'anomalies |
| Relation adhérent | Demandes, réponses, réclamations, escalades | Adhérent, conseiller, gestionnaire | Interaction, demande, preuve, réponse | Assistant documentaire et rédaction contrôlée |

## UC-SANTE-01 — Instruction assistée d'un remboursement

### But

Réduire le temps de qualification d'un dossier **fictif**, en donnant au gestionnaire des éléments vérifiables pour statuer.

### Processus métier cible

1. **Réception** : demande et justificatif synthétiques.
2. **Contrôle de complétude** : pièces attendues, dossier identifié, doublons potentiels.
3. **Extraction** : date, acte, montant, bénéficiaire, références du document.
4. **Contexte contrat** : récupérer garanties applicables et période de couverture via API simulée.
5. **Recherche documentaire** : RAG sur une version datée des garanties, avec références des passages.
6. **Calcul** : moteur de règles déterministe sur paramètres contractuels fictifs ; la réponse LLM ne fournit pas le montant faisant autorité.
7. **Contrôle** : détection des cas hors cadre, incohérences, incertitudes et escalade vers un gestionnaire.
8. **Traçabilité** : décision finale dans le SI de gestion simulé avec références de pièces, versions de règles et acteur valideur.
9. **Notification** : brouillon de message au bénéficiaire, soumis à validation si nécessaire.

### États métier minimaux

`RECUE` → `A_COMPLETER` ou `COMPLETE` → `EN_ANALYSE` → `A_VALIDER` → `VALIDEE` ou `REJETEE` → `NOTIFIEE`.

Les transitions, responsabilités et règles exactes sont propres à chaque organisme ; ne pas les confondre avec un processus réglementaire réel.

### Événements métier de référence (fictifs)

`PrestationDemandee`, `PieceExtraite`, `DossierIncomplet`, `GarantiesIdentifiees`, `CalculEffectue`, `RevueHumaineRequise`, `DecisionValidee`, `AdherentNotifie`.

Chaque événement inclut identifiant de corrélation, horodatage, schéma versionné et référence opaque du dossier ; jamais de pièce médicale en clair sur un bus d'événements.

## Décisions et frontières d'autorité

| Décision | Autorité |
| --- | --- |
| Quelle pièce est présente ? | Extraction assistée + validation selon niveau de confiance |
| Quelle garantie s'applique ? | Contrat/SI de gestion, explication RAG en soutien |
| Quel montant rembourser ? | Moteur de règles métier versionné + SI de prestations |
| Faut-il rejeter ou payer ? | Processus décisionnel autorisé / validation humaine selon règles |
| Que communiquer à l'adhérent ? | Modèle de réponse, contrôles de conformité, gestionnaire si nécessaire |

## Indicateurs à mesurer dans un POC

Taux de dossiers complets à l'entrée, taux d'extraction correcte par champ, exactitude des citations de garantie, taux d'abstention correct, taux d'escalade utile, temps gestionnaire par dossier, taux de faux positifs sur anomalies.

**Données d'essai :** personnages, contrats, barèmes, factures et pièces 100 % synthétiques ; aucune donnée de santé personnelle réelle.
