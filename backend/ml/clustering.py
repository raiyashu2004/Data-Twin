"""
ML – Behaviour Clustering
=========================
Uses K-Means to group daily entries into behavioural clusters such as
"Productive", "Average", and "Low-Performance / Burnout Risk".
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

FEATURE_COLS = ["screen_time_hours", "study_hours", "sleep_hours", "exercise_minutes"]
N_CLUSTERS = 3
CLUSTER_LABELS = {0: "Low Performance", 1: "Average", 2: "Productive"}


def cluster(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assign a behavioural cluster to each row in *df*.

    Returns the original DataFrame with an additional ``cluster`` column and a
    human-readable ``cluster_label`` column.
    """
    if df.empty or len(df) < N_CLUSTERS:
        df["cluster"] = -1
        df["cluster_label"] = "Insufficient data"
        return df

    features = df[FEATURE_COLS].fillna(0)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    km = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init="auto")
    km.fit(scaled)
    labels = km.labels_

    # Rank clusters by mean study hours so label assignment is deterministic
    centres = pd.DataFrame(km.cluster_centers_, columns=FEATURE_COLS)
    rank = centres["study_hours"].argsort().values  # ascending
    remap = {old: new for new, old in enumerate(rank)}
    df = df.copy()
    df["cluster"] = [remap[lbl] for lbl in labels]
    df["cluster_label"] = df["cluster"].map(CLUSTER_LABELS)
    return df
