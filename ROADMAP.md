# Roadmap — mission-ready assurance et protection sociale

Baseline : **26 octobre 2026 — DESIGN**, aucun POC propre à ce dépôt encore exécuté.

| Itération | Livrable | Critère de fin | État |
| --- | --- | --- | --- |
| I0 | Cartographie métier, cas d'usage, HLD, choix d'hébergement, matrice de réutilisation | README + 3 volets + ADR + preuves référencées | DOCUMENTED |
| I1 | Corpus santé synthétique et contrats métier simulés | 10+ dossiers couvrant nominal, incomplet, doublon, garantie expirée, contradiction | TODO |
| I2 | Extraction + RAG cité + adaptateur moteur de règles | Tests : sources identifiables, abstention, calcul déterministe et versionné | TODO |
| I3 | Agent/workflow + HITL + traces + API dossier | Traçabilité bout en bout, contrôle des actions, idempotence, revue | TODO |
| I4 | Comparatif Ollama local vs fournisseur cloud autorisé | Même dataset, métriques qualité/coût/latence/risques ; aucune donnée réelle | TODO |
| I5 | Dossier d'architecture et démonstration entretien | HLD/LLD, ADR, NFR, tests, arbitrages et preuves reproductibles | TODO |

## Ordre de réalisation

**I1 → I2 → I3** d'abord. Les composants déjà prouvés en trading sont référencés et non recopiés. Le travail nouveau porte sur le métier assurance, la frontière de décision, la qualité documentaire et la démonstration.

Le fournisseur externe est **optionnel pour atteindre le premier POC** et ne doit pas entraîner de dépenses ni envoyer de données sensibles sans décision explicite.

## Définition d'un POC réellement démontré

1. Commande reproductible et versions fixées.
2. Jeu de données fictif dans le dépôt, aucune donnée personnelle réelle.
3. Tests automatisés sur scénarios positifs, négatifs et ambigus.
4. Résultat vérifiable : citations, décision de règles, revue humaine.
5. Evidence horodatée (commit, sortie tests, environnement, limitations).
6. Aucun claim de production, de conformité certifiée ou de déploiement chez un assureur.
