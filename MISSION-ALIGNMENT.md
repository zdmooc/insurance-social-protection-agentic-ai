# Couverture d'une mission d'Architecte Solutions IA générative et agentique

**Cas de mission :** architecture SI fonctionnelle/applicative/solution, trajectoire, intégration des agents/LLM au SI et accompagnement du cadrage à la production. L'annonce utilisée pour le cadrage ne démontre pas le client final, la plateforme cloud ni l'hébergement du modèle.

| Attente de mission | Production dans ce dépôt | État |
| --- | --- | --- |
| Architecture fonctionnelle | Capacités santé/prévoyance/retraite, états et décisions | DESIGN |
| Architecture applicative | Frontières workflow / API / GED / RAG / règles | DESIGN |
| Architecture solution | HLD hybride et modèles d'hébergement | DESIGN |
| Trajectoire | I0–I5, preuves et risques | DESIGN |
| Socle agentique | Reprise de l'architecture mère + projet de POC métier | REFERENCES |
| Contrats d'interface | Endpoints fictifs de prestation et garanties | DRAFT |
| Choix techniques | ADR-001 local vs managé vs hybride | PROPOSED |
| Arbitrage | Critères coût, qualité, résilience, conformité et réversibilité | DRAFT |
| Industrialisation | Validation sur OpenShift/Azure/AWS si justifiée | NOT PROVEN |

## Démonstration ciblée

Cas **prestations santé** : facture synthétique → lecture structurée → consultation contrat fictif → recherche des garanties → règles déterministes → révision humaine → décision et audit. Démontrer une distinction nette entre aide du LLM et autorité du SI.

## Limites explicites

- Aucune preuve d'activité réelle pour Malakoff Humanis, AG2R, AXA ou un assureur précis.
- Ne pas présenter une plateforme technique externe déjà testée comme une prestation santé industrialisée.
- Le choix AWS Bedrock / Azure AI / OpenShift AI sera adapté après découverte de l'environnement client.
- Le dépôt n'atteste aucune conformité réglementaire, aucun calcul de remboursement réel, ni traitement autorisé de données de santé.
