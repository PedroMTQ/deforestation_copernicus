# Guide 
https://medium.com/@robmarkcole/a-brief-introduction-to-satellite-image-classification-with-neural-networks-3ce28be15683

Checks copernicus data for over the time deforestation.44158
Uses postgis to store data locally and retrieve it according to use bounding box and timestamp

Uses a model do detect deforestation over time


# Idea




---

## 🛰️ 1. **Data Ingestion**

* **Sources:**

  * Satellite imagery (raster, vector, metadata).
  * Sensor data (IoT telemetry, weather stations, GPS feeds, etc.).

* **Streaming pipeline:**

  * Both are pushed to **Kafka** topics.
  * Kafka → Spark Structured Streaming (or **delta-rs streaming sink**) → **Delta tables**.

📌 Example:

* `satellite_raw` Delta table: large raster data + metadata (time, location, orbit, bands).
* `sensor_raw` Delta table: time-series sensor readings with geospatial coordinates.

---

## 🗄️ 2. **Storage Layer**

* **Delta Lake (Data Lake):**

  * Stores raw + processed data with ACID guarantees.
  * Supports **time travel** (so you can version datasets and retrain ML models consistently).
  * Good for ML and analytics pipelines.

* **PostGIS (Relational DB for Geospatial Queries):**

  * Store **derived geospatial features** (vector data like polygons, bounding boxes, shapefiles, sensor coverage).
  * Allows spatial queries (e.g., `ST_Within`, `ST_Intersects`) for maps, dashboards, or ad-hoc analysis.
  * Acts as the **query-serving layer** for applications and visualization tools (QGIS, GeoServer, Mapbox).

👉 Typical division:

* **Heavy raw data (satellite imagery)** → Delta tables (cheap, scalable).
* **Indexing + spatial search** → PostGIS (fast query response).

---

## ⚙️ 3. **Processing Layer (Spark + dbt)**

* **Spark:**

  * Batch + streaming processing over Delta tables.
  * Can handle large-scale raster transformations, feature extraction, and sensor data aggregation.
  * With **Sedona (Apache Sedona)** or **GeoMesa**, Spark can process geospatial data at scale (spatial joins, distance calculations).

* **dbt:**

  * Used for **SQL transformations on tabular/metadata layers** (not image pixels).
  * Example:

    * Create staging tables (`stg_sensors` = cleaned sensor feeds).
    * Build derived metrics (`avg_temp_per_region`, `sensor_health`).
    * Enrich geospatial indexes (lat/lon → region mapping).
  * Output: **curated Delta tables** ready for ML or BI.

---

## 🤖 4. **ML Workflow (DVC + Spark ML/other frameworks)**

* **Feature engineering:**

  * Spark jobs combine satellite + sensor data into a **feature set**.
  * Example: NDVI index from satellite imagery + soil moisture sensors = crop health features.

* **Model training:**

  * DVC tracks:

    * Which version of the Delta tables (snapshot ID) was used.
    * Model code, hyperparameters, and output weights.
  * Spark MLlib (or PyTorch/TF via PySpark) trains models at scale.
  * Output models are stored in DVC remote storage (S3, GCS, etc.).

* **Deployment:**

  * Inference pipeline can use Spark Structured Streaming:

    * New satellite + sensor data → Delta table → real-time model scoring.

---

## 📊 5. **Consumption**

* **PostGIS**: Fast geospatial queries for web apps, dashboards, and GIS visualization.
* **Delta Lake**: Downstream analytics (BI, ML pipelines, time-series analysis).
* **ML models**: Used for predictions like:

  * Crop yield forecasts.
  * Disaster detection (floods, fires, deforestation).
  * Sensor anomaly detection.

---

## 🔗 Workflow Diagram (Conceptual)

```
[Sensors]       [Satellites]
    │                 │
    ▼                 ▼
     ───► Kafka ──────────► Spark Streaming
                              │
                       [Delta Lake: Raw Zone]
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
        dbt models (SQL)              PySpark + Sedona
    [Delta Lake: Curated Zone]   [Raster/vector processing]
                │                           │
                └─────────────┬─────────────┘
                              ▼
                   [Delta Lake: Features]
                              │
                      ML Training (DVC)
                              │
                              ▼
                     [Models + Predictions]
                              │
           ┌───────────┬──────────────┬───────────┐
           ▼           ▼              ▼           ▼
     [PostGIS]   [Dashboards]   [Delta for BI]   [API]
```

---

✅ **Tool roles in your system:**

Messaging:
* **Kafka** → ingestion buffer.
Satellite data ingestion and downstream modelling:
* **PostGIS** → spatial querying/indexing for apps.

Sensor data ingestion and downstream modelling:
* **Delta Lake** → scalable, versioned storage for raw + processed data.

Sensor data processing: (and downstream modelling?)
* **Spark** → large-scale processing + ML.

Donstream modelling:
* **dbt** → SQL-based curation of structured metadata.
* **DVC** → ML reproducibility (datasets + models).

---

Use rio-cogeo to convert satellite data into queriable COG (for proper selection of images)

Workflow:
Satellite data:
  1. Satellite data download request pusher sends a download request to kafka
  2. Satellite data request consumer downloads satellite data and:
      2.1 checks if the data is available in minio, if so the request is dropped
      2.2 if not, it sends the request to another kafka topic (downloader)
  3. A consumer reads for the downloader kafka topic and downloads satellite data and saves it in minio (partition by geohash lvl X and timestamp e.g., sentinel_hub/sentinel_hub_function/geohash/timestamp/bounding_box_<minx>_<miny>_<maxx>_<maxy>/image.<tiff/cog>) as COG (using rio-cogeo), publish a message with path to kafka
  3. Satellite data postgis consumer adds data to postgis

Sensor data:
1. Sensor data pusher sends sensor data to kafka
2. Sensor data consumer adds sensor data to delta table (raw) and pushes sensor data to spark
3. Spark workers process sensor data and add processed data to delta table (processed)


# Guides

Fine-tuning pixtral for sat data:
https://github.com/mistralai/cookbook/blob/main/mistral/fine_tune/pixtral_finetune_on_satellite_data.ipynb