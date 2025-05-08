                    #--------------------------------------#
                    # IMPLEMENTATION DES TETS UNITAIRES    #
                    #--------------------------------------#

import os
import pytest
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv(override=True)

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION")
CSV_PATH = os.getenv("CSV_PATH", "data/healthcare_dataset.csv")

@pytest.fixture(scope="module")
# Migration
def migrate_data():
   
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    df = pd.read_csv(CSV_PATH)
    print(f"Nombre de lignes dans le CSV : {len(df)}")

    collection.delete_many({})
    collection.insert_many(df.to_dict(orient="records"))

    yield collection, df

    client.close()   # Fermeture de la connexion à la fin du test

# Intégrité : Vérifie l'intégrité des données après la migration.
def test_integrity(migrate_data):
    
    collection, df_csv = migrate_data

    # 1. Nombre de lignes
    docs = list(collection.find({}, {"_id": 0}))
    df_mongo = pd.DataFrame(docs)
    assert len(df_csv) == len(df_mongo), f"Incohérence lignes : CSV={len(df_csv)}, Mongo={len(df_mongo)}"

    # 2. Colonnes
    assert set(df_csv.columns) == set(df_mongo.columns), f"Colonnes différentes : {set(df_csv.columns) ^ set(df_mongo.columns)}"

    # 3. Types de données (simples)
    for col in df_csv.columns:
        assert df_csv[col].dtype == df_mongo[col].dtype, f"Type incompatible pour '{col}': CSV={df_csv[col].dtype}, Mongo={df_mongo[col].dtype}"

    # 4. Valeurs manquantes
    na_csv = df_csv.isnull().sum().to_dict()
    na_mongo = df_mongo.isnull().sum().to_dict()
    assert na_csv == na_mongo, f"Différence valeurs manquantes :\nCSV : {na_csv}\nMongo : {na_mongo}"

    # 5. Doublons
    dup_csv = df_csv.duplicated().sum()
    dup_mongo = df_mongo.duplicated().sum()
    assert dup_csv == dup_mongo, f"Différence doublons : CSV={dup_csv}, Mongo={dup_mongo}"

    print("Tous les tests d'intégrité sont passés.")
