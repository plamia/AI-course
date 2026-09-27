# Cloud Stack & Ownership Map: `cart-api`

## Component List & Ownership Tags
Here is the path a single request takes, from the user to the backend and back, along with who owns what:

1. **User / Client Request** 
2. **Load Balancer `[ops]`** - Distributes incoming customer traffic across available containers so no single server gets overwhelmed.
3. **Kubernetes Cluster (cart-api container) `[mine/Product]`** - The actual application code and business logic that we wrote and govern. (Note: The underlying cluster infrastructure is `[ops]`, but the app's behavior is ours).
4. **Postgres Database `[ops]`** - Persistent storage where saved carts and checkout data live.
5. **Redis Cache `[ops]`** - Fast, temporary storage for active user sessions to keep the app snappy.
6. **EPAM DIAL Gateway `[ops]`** - The governed front door for our AI calls. It handles cost attribution, rate limits, and audit trails.
7. **Language Model `[ops]`** - The actual LLM that processes the "summarise my cart" prompt.
8. **Observability Stack (Metrics/Logs/Traces) `[ops]`** - The monitoring tools (like Grafana/Datadog) watching every piece of this infrastructure to catch failures before the customer does.

---

## Architecture Flowchart

```mermaid
graph TD
    User([User Request]) --> LB[Load Balancer <br/> tag: ops]
    LB --> App[cart-api Container <br/> tag: mine/Product]
    
    App --> DB[(Postgres Database <br/> tag: ops)]
    App --> Cache[(Redis Cache <br/> tag: ops)]
    App --> Gateway[EPAM DIAL Gateway <br/> tag: ops]
    
    Gateway --> LLM((Language Model <br/> tag: ops))
    
    Obs[Observability Stack <br/> tag: ops] -. watches .-> LB
    Obs -. watches .-> App
    Obs -. watches .-> DB
    Obs -. watches .-> Cache
    Obs -. watches .-> Gateway