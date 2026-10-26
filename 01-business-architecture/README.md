# Métier — Assurance et protection sociale

| Domaine | Processus | Objets métier |
|---|---|---|
| Santé complémentaire | Affiliation, garanties, devis, remboursement, réclamation | Adhérent, bénéficiaire, contrat, facture, prestation |
| Prévoyance | Incapacité, invalidité, décès, instruction | Assuré, sinistre, garantie, justificatif |
| Retraite | Carrière, cotisations, droits, réclamation | Affilié, période, point, pension |
| Assurance collective | Affiliations salariés, cotisations, DSN | Entreprise, salarié, contrat collectif |
| Relation adhérent | Information, assistance, réclamation | Demande, interaction, dossier |

## Processus de référence : remboursement santé

1. L'adhérent transmet une facture.
2. Le gestionnaire ou le SI contrôle l'identité et la complétude du dossier.
3. L'IA extrait les champs et signale les incertitudes.
4. Une API du SI récupère le contrat, le bénéficiaire et les garanties.
5. Le RAG retrouve les clauses contractuelles applicables et les cite.
6. **Le moteur de règles** calcule le montant admissible ; le LLM ne décide pas du montant.
7. Les anomalies sont envoyées en revue humaine.
8. Le SI de gestion enregistre la décision et notifie l'adhérent.

**États du dossier :** reçu → incomplet ou à instruire → à valider → validé ou rejeté → notifié.

**Rôles :** adhérent (demande), gestionnaire (instruction/validation), SI de gestion (référentiel), moteur de règles (calcul), IA (assistance).

Exemple pédagogique : les règles réelles de remboursement et les rôles précis varient selon l'organisme.
