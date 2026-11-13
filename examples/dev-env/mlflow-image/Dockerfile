# The MLflow tracking server, built by CI from Artifactory and pushed to the dev
# Docker repository. Cloud Run pulls it through the Artifact Registry mirror.
ARG BASE_IMAGE
FROM ${BASE_IMAGE}

ARG INDEX_URL
ARG MLFLOW_VERSION

RUN --mount=type=secret,id=netrc,target=/root/.netrc \
    pip install --no-cache-dir --index-url "${INDEX_URL}" \
      "mlflow==${MLFLOW_VERSION}" psycopg2-binary google-cloud-storage

# Backend and artifact locations come from the environment (Terraform). The
# server proxies artifacts, so clients never touch the bucket directly.
EXPOSE 8080
CMD exec mlflow server --host 0.0.0.0 --port 8080 \
      --backend-store-uri "${MLFLOW_BACKEND_STORE_URI}" \
      --artifacts-destination "${MLFLOW_ARTIFACTS_DESTINATION}" \
      --serve-artifacts
