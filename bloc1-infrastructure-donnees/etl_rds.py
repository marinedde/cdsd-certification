"""
ETL Kayak — Rechargement du Data Warehouse RDS MySQL depuis le Data Lake S3.

Ce script relit les 3 CSV nettoyés stockés dans S3 (raw/) et les charge dans
une instance RDS MySQL fraîchement recréée, puis vérifie le chargement.

Lancement :
    python etl_rds.py

Avant de lancer, renseigne au minimum l'endpoint de ta nouvelle instance RDS
ci-dessous (RDS_HOST), ou via la variable d'environnement RDS_HOST.

Les identifiants sensibles sont lus depuis les variables d'environnement :
    export RDS_PASSWORD="ton_mot_de_passe_rds"
    export AWS_ACCESS_KEY_ID="..."
    export AWS_SECRET_ACCESS_KEY="..."
"""

import io
import os
import sys

import boto3
import pandas as pd
from sqlalchemy import create_engine, text

# ---------------------------------------------------------------------------
# CONFIGURATION — colle ton nouvel endpoint RDS ici (ou via $RDS_HOST)
# ---------------------------------------------------------------------------
RDS_HOST = os.environ.get(
    "RDS_HOST",
    "kayak-db.c9eaa6c44d7i.eu-west-3.rds.amazonaws.com",
)
RDS_PORT = int(os.environ.get("RDS_PORT", 3306))
RDS_USER = os.environ.get("RDS_USER", "admin")
RDS_DB = os.environ.get("RDS_DB", "kayak")
RDS_PASSWORD = os.environ.get("RDS_PASSWORD")

BUCKET_NAME = os.environ.get("BUCKET_NAME", "kayak-project-marine")
AWS_REGION = os.environ.get("AWS_REGION", "eu-west-3")

# Fichiers source dans S3 (clé = raw/<fichier>) -> table de destination
SOURCES = {
    "cities_gps.csv": "cities",
    "weather_score.csv": "weather",
    "hotels_clean.csv": "hotels",
}


def check_config():
    problems = []
    if "XXXXXXXX" in RDS_HOST:
        problems.append(
            "RDS_HOST n'a pas été renseigné. Colle ton nouvel endpoint RDS dans "
            "etl_rds.py (variable RDS_HOST) ou fais : export RDS_HOST=..."
        )
    if not RDS_PASSWORD:
        problems.append("RDS_PASSWORD manquant. Fais : export RDS_PASSWORD='...'")
    if problems:
        print("Configuration incomplète :\n")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)

    # Les identifiants AWS sont résolus automatiquement par boto3 :
    # variables d'environnement OU fichier ~/.aws/credentials (aws configure).
    has_env_keys = os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get(
        "AWS_SECRET_ACCESS_KEY"
    )
    if not has_env_keys:
        print(
            "Info : pas de clés AWS dans l'environnement, "
            "boto3 utilisera ~/.aws/credentials (aws configure) si disponible.\n"
        )


def read_csv_from_s3(s3_client, filename):
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=f"raw/{filename}")
    content = response["Body"].read().decode("utf-8")
    return pd.read_csv(io.StringIO(content))


def transform(name, df):
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    if name == "weather":
        for col in ["avg_temp", "avg_temp_max", "total_rain", "avg_humidity", "weather_score"]:
            if col in df.columns:
                df[col] = df[col].round(2)
    if name == "hotels":
        for col in ["latitude", "longitude"]:
            if col in df.columns:
                df[col] = df[col].round(6)
    return df


def main():
    check_config()

    print(f"Connexion S3 (région {AWS_REGION}, bucket {BUCKET_NAME})...")
    s3 = boto3.client(
        "s3",
        region_name=AWS_REGION,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    # --- EXTRACT ---
    print("\nLecture des données depuis S3...")
    frames = {}
    for filename, table in SOURCES.items():
        df = read_csv_from_s3(s3, filename)
        frames[table] = df
        print(f"  {filename:<20} -> {len(df)} lignes")

    # --- TRANSFORM ---
    print("\nTransformation...")
    for table, df in frames.items():
        frames[table] = transform(table, df)

    # --- LOAD ---
    print(f"\nConnexion à RDS ({RDS_HOST})...")
    base_engine = create_engine(
        f"mysql+pymysql://{RDS_USER}:{RDS_PASSWORD}@{RDS_HOST}:{RDS_PORT}/"
    )
    with base_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {RDS_DB}"))
        print(f"  Base '{RDS_DB}' prête")

    engine = create_engine(
        f"mysql+pymysql://{RDS_USER}:{RDS_PASSWORD}@{RDS_HOST}:{RDS_PORT}/{RDS_DB}"
    )
    for table, df in frames.items():
        df.to_sql(table, engine, if_exists="replace", index=False)
        print(f"  Table '{table}' chargée ({len(df)} lignes)")

    # --- VÉRIFICATION (étape 4) ---
    print("\nVérification du chargement :")
    with engine.connect() as conn:
        for table in SOURCES.values():
            count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            print(f"  SELECT COUNT(*) FROM {table:<8} = {count}")

    print("\nETL terminé avec succès. Tu peux faire ton screenshot.")


if __name__ == "__main__":
    main()
