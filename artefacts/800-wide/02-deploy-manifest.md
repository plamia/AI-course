# Deployment Manifest & Production Audit: `cart-api`

## 1. The AI-Generated First Draft (The Manifest)
*This is the typical first-draft YAML an AI generates. It "works", but it is dangerous to run in production.*

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cart-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cart-api
  template:
    metadata:
      labels:
        app: cart-api
    spec:
      containers:
      - name: cart-api
        image: myregistry/cart-api:latest
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          value: "postgres://user:pass@db:5432/cart"
        - name: DIAL_API_KEY
          value: "my-super-secret-key"
---
apiVersion: v1
kind: Service
metadata:
  name: cart-api-service
spec:
  selector:
    app: cart-api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

---

## 2. Fresh-Session Audit Results
*I pasted the above YAML into a fresh, context-free AI session and asked it to audit the manifest for production readiness. Here is what it caught:*

| Missing Control | Why it matters | One-line fix |
| :--- | :--- | :--- |
| **Resource Requests/Limits** | Without memory limits (~512Mi), a memory leak in this container could crash the entire underlying Kubernetes node, taking down other apps with it. | Add `resources: limits: memory: "512Mi"` and `requests: memory: "256Mi"` under the container spec. |
| **Liveness/Readiness Probes** | Kubernetes doesn't know when the app is actually ready to receive traffic. During a deploy, it will send customers to the new container before it finishes booting up, causing dropped requests. | Add `readinessProbe: httpGet: path: /healthz port: 8080` to the container spec. |
| **Secret Handling** | `DATABASE_URL` and `DIAL_API_KEY` are hardcoded in plaintext. Anyone who can read this file in GitHub can steal the database and AI gateway credentials. | Change `value` to `valueFrom: secretKeyRef: name: cart-secrets key: DIAL_API_KEY`. |
| **Rollback Strategy** | There is no `RollingUpdate` strategy defined. If a bad version is deployed, it might take down all 3 replicas at once instead of safely replacing them one by one. | Add `strategy: type: RollingUpdate rollingUpdate: maxUnavailable: 1` under the Deployment spec. |
| **Image Tagging** | Using the `:latest` tag means we don't actually know which version of the code is running, making rollbacks to a specific previous version impossible. | Change `image: myregistry/cart-api:latest` to a specific commit SHA like `image: myregistry/cart-api:v1.2.4`. |