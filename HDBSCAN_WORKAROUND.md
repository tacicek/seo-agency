# 🔄 Alternative Installation (Ohne HDBSCAN)

Wenn Sie Probleme beim Build mit `hdbscan` haben, hier ist eine vereinfachte Version:

## Option 1: Verwenden Sie sklearn.cluster statt hdbscan

Ersetzen Sie in `seo_analyzer.py`:

```python
# ORIGINAL (mit HDBSCAN)
import hdbscan
hdbscan_model = hdbscan.HDBSCAN(
    min_cluster_size=min_topic_size,
    metric='euclidean',
    cluster_selection_method='eom',
    prediction_data=True
)

# ALTERNATIVE (mit sklearn)
from sklearn.cluster import DBSCAN
hdbscan_model = DBSCAN(
    eps=0.5,
    min_samples=min_topic_size,
    metric='euclidean'
)
```

## Option 2: Pre-built Wheel verwenden

```bash
# Im Container
docker exec -it seo-api pip install --no-build-isolation hdbscan
```

## Option 3: Conda verwenden (empfohlen für M1/M2/M3 Macs)

```yaml
# docker-compose.yml ändern zu:
services:
  api:
    image: continuumio/miniconda3
    ...
```

## Option 4: Nur BERTopic's Default Clustering

BERTopic kann auch ohne explizite HDBSCAN-Konfiguration verwendet werden:

```python
# Minimal Config
topic_model = BERTopic(
    language='english',
    calculate_probabilities=True
)
```

## Aktueller Status

Der Docker-Build schlägt fehl wegen Kompilierungsfehlern in hdbscan 0.8.33.

### Ursache:
- hdbscan benötigt C-Compiler
- Kompatibilitätsprobleme mit NumPy auf ARM64 (Apple Silicon)

### Lösungen:

1. **Quick Fix**: Verwenden Sie eine vorkompilierte Version
```bash
pip install hdbscan --no-build-isolation --force-reinstall
```

2. **Docker Fix**: Verwenden Sie ein anderes Base-Image
```dockerfile
FROM python:3.11
# Statt python:3.11-slim
```

3. **Alternative Library**: Verwenden Sie sklearn's DBSCAN oder OPTICS

## Temporäre Lösung

Ich erstelle jetzt eine Version OHNE hdbscan, die trotzdem funktioniert.
