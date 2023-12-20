# Testing template based job execution

### Setting-up celery
```bash
celery -A celery_worker worker --loglevel=info
```

### Setting-up FastAPI server