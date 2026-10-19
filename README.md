# fgsaverecall40270840

The one stateful part of QUBCloud-FraudGuard. It saves a batch of transactions and returns an ID, and recalls a saved batch by ID. It runs on Google Cloud, because the private cloud used for the rest of the system has no persistent storage.

Part of [QUBCloud-FraudGuard](https://github.com/QUBFraudGuard).

## Design

- **Object store:** each batch is saved as a JSON file named by its ID in a Cloud Storage bucket. The access pattern is write once, recall by exact key, so an object store fits without paying for querying that would never be used.
- **Serverless:** a Flask app in a Docker container on Cloud Run.
- **Keeps the core stateless:** only the frontend talks to this service. The screening services never touch it.

## Limitations

- No searching or filtering of saved batches.
- IDs are the first 8 characters of a UUID, so collisions are possible at large scale.
- The endpoints have no authentication. Traffic is encrypted (HTTPS), but anyone with the URL can call it, so this would need fixing before production.

## Run it

```bash
git clone https://github.com/QUBFraudGuard/fgsaverecall40270840.git
cd fgsaverecall40270840
pip install -r requirements.txt
python app.py
```
