# Integration Contract: POS Client → Apollo Gateway (Cart Lookup)
**Module:** 400 — Architecture (Wide Path)  
**Kata:** K 4.W.4 (Kata 4.4)  
**Status:** Approved for Engineering Implementation  

---

## 1. Metadata & Ownership
- **Consumer:** POS Client (In-store store associate mobile terminal)
- **Provider:** Apollo GraphQL Gateway (`/graphql`)
- **Owner:** Core Commerce Architecture Team
- **Last Reviewed:** 2026-09-26

## 2. Protocol & Connection
- **API Style:** GraphQL over HTTPS (POST)
- **Endpoint:** `https://api.meridian.retail/graphql`
- **Authentication:** Bearer Token (`Authorization: Bearer <store-associate-JWT>`) scoped with `pos:cart:read`.
- **Rate Limiting:** 200 requests/minute per POS terminal.

## 3. Request Payload Shape (GraphQL Query)
```graphql
query GetCustomerCartByQR($$qrCodeToken: String!, $$storeId: ID!) {
  customerCartByQR(qrCodeToken: $$qrCodeToken, storeId: $$storeId) {
    customerId
    customerName
    loyaltyTier
    activeCart {
      cartId
      items {
        sku
        quantity
        unitPrice
        stockStatus
      }
      subtotal
    }
  }
}