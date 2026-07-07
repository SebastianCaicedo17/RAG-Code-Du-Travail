"""À lancer une seule fois pour construire la base vectorielle persistante.
Remplace la liste `chunks` par tes vrais extraits du Code du travail."""

from src.vector_store import VectorStore

chunks = [
    {
        "text": "Le contrat de travail à durée indéterminée (CDI) est la forme normale et générale de la relation de travail.",
        "source": "art_L1221-2",
    },
    {
        "text": "La durée légale du travail effectif des salariés à temps complet est fixée à 35 heures par semaine.",
        "source": "art_L3121-27",
    },
    {
        "text": "Le salarié a droit à un congé de deux jours et demi ouvrables par mois de travail effectif chez le même employeur.",
        "source": "art_L3141-3",
    },
    {
        "text": "La période d'essai permet à l'employeur d'évaluer les compétences du salarié et au salarié d'apprécier si les fonctions lui conviennent.",
        "source": "art_L1221-20",
    },
    {
        "text": "Tout salarié victime d'un licenciement sans cause réelle et sérieuse a droit à une indemnité.",
        "source": "art_L1235-3",
    },
]

VectorStore(chunks, persist_directory="chroma_db")
print(f"Base créée avec {len(chunks)} chunks dans ./chroma_db")
