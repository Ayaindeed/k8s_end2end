# Airflow on Kubernetes - Production Deployment

This repository contains the complete configuration and DAGs for deploying Apache Airflow on Kubernetes using Helm.

## 📁 Repository Structure

```
├── dags/                      # Airflow DAG files
│   ├── hello.py              # Simple hello world DAG
│   └── fetch_and_preview.py  # Data fetching and preview DAG
├── k8s/                       # Kubernetes configuration files
│   ├── dashboard-adminuser.yaml
│   ├── dashboard-clusterrole.yaml
│   ├── dashboard-secret.yaml
│   └── values.yaml           # Helm values for Airflow deployment
```

## 🚀 Quick Start

### Prerequisites
- Docker Desktop with Kubernetes enabled
- kubectl installed and configured
- Helm 3.x installed

### Deployment Steps

1. **Add Airflow Helm repository**
   ```bash
   helm repo add apache-airflow https://airflow.apache.org
   helm repo update
   ```

2. **Deploy Kubernetes Dashboard** (optional)
   ```bash
   kubectl apply -f k8s/dashboard-adminuser.yaml
   kubectl apply -f k8s/dashboard-clusterrole.yaml
   kubectl apply -f k8s/dashboard-secret.yaml
   ```

3. **Run PostgreSQL container**
   ```bash
   docker run -d --name postgres-airflow \
     -e POSTGRES_USER=airflow \
     -e POSTGRES_PASSWORD=airflow \
     -e POSTGRES_DB=airflow \
     -p 5432:5432 \
     postgres:15-alpine
   ```

4. **Deploy Airflow**
   ```bash
   helm upgrade --install airflow apache-airflow/airflow \
     --namespace airflow \
     --create-namespace \
     -f k8s/values.yaml
   ```

5. **Access Airflow UI**
   ```bash
   kubectl port-forward svc/airflow-api-server 8080:8080 --namespace airflow
   ```
   Visit: http://localhost:8080

## 📝 DAG Development

All DAGs are stored in the `/dags` folder and synchronized automatically via GitSync when configured in `values.yaml`.

## 🔧 Configuration

Edit `k8s/values.yaml` to customize:
- Executor type (CeleryExecutor/KubernetesExecutor)
- Database connection settings
- GitSync repository configuration
- Resource limits and scaling

## 📚 Documentation

For detailed setup instructions and architecture overview, see the accompanying article.

## 🔐 Security Notes

- Never commit secrets to this repository
- Use Kubernetes Secrets for sensitive data
- Rotate Fernet keys regularly
- Enable RBAC for production deployments
