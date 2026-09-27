# CI/CD Workflow & Supply-Chain Audit: `cart-api`

## 1. The AI-Generated First Draft (The Pipeline)
*This is the typical first-draft GitHub Actions workflow an AI generates. It builds and deploys the code, but it fails almost every modern supply-chain security standard.*

```yaml
name: Build and Deploy cart-api

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Tests
        run: npm run test

      - name: Build and Push Docker Image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: myregistry/cart-api:latest
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Deploy to Kubernetes
        uses: azure/k8s-set-context@v3
        with:
          kubeconfig: ${{ secrets.KUBE_CONFIG }}
      - run: kubectl apply -f deployment.yaml
```

---

## 2. Fresh-Session Supply-Chain Audit
*I pasted the above workflow into a fresh AI session and asked it to audit the pipeline against the six critical supply-chain controls. Here are the results:*

| Supply-Chain Control | Status | Why it matters | One-line fix |
| :--- | :--- | :--- | :--- |
| **Pinned Action Versions** | ❌ Missing | Using tags like `@v4` is dangerous because the author can overwrite that tag with malicious code. | Pin to an immutable commit SHA (e.g., `uses: actions/checkout@1d96c772d19495a3b5c517cd2bc0cb401ea0529f`). |
| **OIDC Short-Lived Credentials** | ❌ Missing | The pipeline uses long-lived passwords (`secrets.DOCKER_PASSWORD`). If stolen, they grant permanent access. | Remove the secrets and configure cloud OIDC trust to issue temporary, 1-hour tokens. |
| **Image Signing / Provenance** | ❌ Missing | There is no proof that the image deployed to production is the exact one built by this pipeline. | Add the `sigstore/cosign-installer` action and sign the image digest before deploying. |
| **Dependency & Image Scanning** | ❌ Missing | The pipeline runs unit tests, but it pushes the image without checking for known CVEs (vulnerabilities). | Add the `aquasecurity/trivy-action` step to scan the image and fail the build on `CRITICAL` CVEs. |
| **Least-Privilege Token** | ❌ Missing | There is no `permissions:` block, meaning the GitHub token defaults to broad read/write access across the repo. | Add `permissions: contents: read` at the top of the job to restrict what the pipeline can touch. |
| **Rollback Gate** | ❌ Missing | It runs `kubectl apply` and assumes success. If the new container crashes, the pipeline won't roll it back. | Add `kubectl rollout status` and a failure catch to trigger `kubectl rollout undo deployment/cart-api`. |