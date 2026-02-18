# FreightBox: The Global Freight Marketplace Platform

## Executive Vision

FreightBox is not just a freight management tool—it's a **platform ecosystem** that powers the global logistics industry. Think of it as:

- **Shopify for Freight**: White-label freight management that anyone can deploy
- **Uber for International Logistics**: Marketplace connecting shippers with service providers globally
- **Stripe for Trade Finance**: Integrated payments, LC, insurance baked into every transaction

---

## The Two-Product Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FREIGHTBOX MARKETPLACE (Central)                      │
│                       marketplace.freightbox.org                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │
│  │  Shipment   │ │   Vendor    │ │   Bidding   │ │   Trade     │        │
│  │  Exchange   │ │   Network   │ │   Engine    │ │   Finance   │        │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘        │
└────────────────────────────┬────────────────────────────────────────────┘
                             │ API Gateway + ABAC
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   FreightBox    │ │   FreightBox    │ │   FreightBox    │
│   Instance A    │ │   Instance B    │ │   Instance C    │
│  (Shipper Co.)  │ │  (FF Company)   │ │  (CHA Firm)     │
│                 │ │                 │ │                 │
│ *.freightbox.org│ │ *.freightbox.org│ │ *.freightbox.org│
│ or own domain   │ │ or own domain   │ │ or own domain   │
└─────────────────┘ └─────────────────┘ └─────────────────┘
     Tenant 1            Tenant 2            Tenant 3
```

---

## Product 1: FreightBox Core (The SaaS)

### What It Is
A complete freight management system that can be:
- **Cloud-hosted** at `{company}.freightbox.org`
- **Self-hosted** on customer's infrastructure
- **White-labeled** with custom branding

### Target Users
| User Type | Use Case |
|-----------|----------|
| Freight Forwarders | End-to-end shipment management, BL generation, carrier booking |
| Custom House Agents | Customs documentation, duty calculations, compliance |
| Shippers/Exporters | Shipment tracking, vendor management, rate comparison |
| NVOCCs | Slot management, HBL generation, consolidation |
| 3PLs/Warehouses | Inventory, fulfillment, last-mile integration |

### Core Modules
```
FreightBox Core
├── Shipment Management
│   ├── Booking & Quotation
│   ├── Multi-leg journey planning
│   ├── Container/AWB tracking
│   └── Status notifications
├── Document Management (DMS)
│   ├── BL/AWB generation with QR
│   ├── Commercial Invoice, Packing List
│   ├── Customs documents (BOE, S/B)
│   └── Blockchain verification
├── Finance & Rates
│   ├── Rate cards & tariffs
│   ├── Invoice generation
│   ├── P&L per shipment
│   └── Multi-currency
├── Compliance
│   ├── HS code validation
│   ├── Sanctions screening
│   ├── DG/Hazmat compliance
│   └── AEO/C-TPAT
└── Customer Portal
    ├── Self-service tracking
    ├── Document download
    └── Quote requests
```

### Pricing Model
| Tier | Price | Limits |
|------|-------|--------|
| **Free** | $0 | 50 shipments/month, 1 user, basic features |
| **Starter** | $99/mo | 500 shipments, 5 users, DMS, basic reports |
| **Professional** | $299/mo | Unlimited, 20 users, API access, custom branding |
| **Enterprise** | Custom | Self-hosted, SLA, dedicated support, SSO |

---

## Product 2: FreightBox Marketplace (The Exchange)

### What It Is
A **central exchange** where:
- Shippers post shipment requirements
- Verified vendors compete for business
- Contracts are awarded, executed, and settled
- Trust is built through ratings and reviews

### The Network Effect
```
More Shippers → More Requirements → More Vendors Join
       ↑                                    │
       └────── More Competition ◄───────────┘
                Better Rates
                Better Service
```

### Marketplace Participants

#### 1. Shippers (Demand Side)
- Exporters, importers, manufacturers, traders
- Post shipment requirements
- Receive and compare bids
- Award contracts
- Track execution
- Rate vendors

#### 2. Service Providers (Supply Side)
| Type | Services |
|------|----------|
| Freight Forwarders | International shipping, consolidation |
| Custom House Agents | Customs clearance, documentation |
| Transporters | First/last mile, trucking, rail |
| Shipping Lines | Container booking, vessel space |
| Airlines | Air cargo capacity |
| NVOCCs | Sea freight, LCL consolidation |
| Insurance | Marine, cargo, transit insurance |
| Banks | LC, trade finance, forex |
| Warehouses | Storage, fulfillment, cross-dock |
| Surveyors | Pre-shipment inspection, claims |

### How It Works

```
┌──────────────────────────────────────────────────────────────────┐
│                     SHIPMENT LIFECYCLE                            │
└──────────────────────────────────────────────────────────────────┘

1. REQUIREMENT POSTED
   Shipper: "I need to move 20 pallets of electronics
            from Mumbai to Rotterdam by Feb 15"
                         │
                         ▼
2. SMART MATCHING (ABAC)
   System filters vendors by:
   ├── Service area (India → Netherlands) ✓
   ├── Cargo type (Electronics) ✓
   ├── Certifications (AEO, GDP) ✓
   ├── Past performance (Rating > 4.0) ✓
   └── Capacity availability ✓
                         │
                         ▼
3. BIDDING PHASE (48-72 hours)
   ┌─────────────────────────────────────────────────┐
   │ Vendor A (FF)    │ $4,200 │ 18 days │ ★★★★☆   │
   │ Vendor B (NVOCC) │ $3,800 │ 22 days │ ★★★★★   │
   │ Vendor C (FF)    │ $4,500 │ 15 days │ ★★★☆☆   │
   └─────────────────────────────────────────────────┘
                         │
                         ▼
4. AWARD & CONTRACT
   Shipper selects Vendor B
   → Digital contract generated
   → Escrow payment initiated
   → KYC/compliance verified
                         │
                         ▼
5. EXECUTION
   ├── Pickup scheduled
   ├── Documents generated (BL, Invoice)
   ├── Customs cleared
   ├── In-transit tracking
   └── Delivery confirmed
                         │
                         ▼
6. SETTLEMENT
   ├── Delivery verified
   ├── Documents released
   ├── Payment released from escrow
   └── Both parties rate each other
```

---

## RBAC + ABAC Architecture

### RBAC (Role-Based Access Control)
**Within each organization/tenant**

```yaml
Organization: "ABC Freight Forwarders"
Roles:
  - Admin:
      permissions: [all]
  - Operations Manager:
      permissions: [shipments.*, documents.*, vendors.view]
  - Operations Executive:
      permissions: [shipments.view, shipments.update, documents.create]
  - Finance:
      permissions: [invoices.*, payments.*, reports.financial]
  - Customer Service:
      permissions: [shipments.view, tracking.*, portal.*]
  - Viewer:
      permissions: [*.view]
```

### ABAC (Attribute-Based Access Control)
**For marketplace visibility and matching**

```yaml
Vendor: "XYZ Logistics"
Attributes:
  vendor_type: [FREIGHT_FORWARDER, CUSTOM_HOUSE_AGENT]
  service_areas: [INDIA, UAE, EUROPE, USA]
  freight_modes: [SEA_FCL, SEA_LCL, AIR]
  certifications: [ISO_9001, AEO, IATA, FIATA]
  cargo_specializations: [ELECTRONICS, PHARMA, PERISHABLES]
  min_shipment_value: 5000
  max_shipment_value: 500000
  dg_capable: true
  reefer_capable: true
  credit_rating: A
  avg_rating: 4.5
  completed_jobs: 1247

Policy: "Vendor can see shipment if"
  - shipment.origin IN vendor.service_areas
  - shipment.destination IN vendor.service_areas
  - shipment.freight_mode IN vendor.freight_modes
  - shipment.cargo_type IN vendor.cargo_specializations
  - shipment.is_dg == false OR vendor.dg_capable == true
  - shipment.is_reefer == false OR vendor.reefer_capable == true
  - shipment.estimated_value BETWEEN vendor.min_shipment_value AND vendor.max_shipment_value
```

---

## Multi-Tenant Data Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CENTRAL DATABASE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐                     │
│  │   Organizations  │  │      Users       │                     │
│  │   (Tenants)      │  │  (Multi-tenant)  │                     │
│  └────────┬─────────┘  └────────┬─────────┘                     │
│           │                     │                                │
│  ┌────────▼─────────────────────▼────────┐                      │
│  │         Tenant-Scoped Data            │                      │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐  │                      │
│  │  │Shipments│ │Documents│ │Invoices │  │                      │
│  │  │ org_id  │ │ org_id  │ │ org_id  │  │                      │
│  │  └─────────┘ └─────────┘ └─────────┘  │                      │
│  └───────────────────────────────────────┘                      │
│                                                                  │
│  ┌───────────────────────────────────────┐                      │
│  │      Marketplace Data (Shared)        │                      │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐  │                      │
│  │  │ Vendors │ │Requiremt│ │  Bids   │  │                      │
│  │  │(public) │ │(public) │ │(private)│  │                      │
│  │  └─────────┘ └─────────┘ └─────────┘  │                      │
│  └───────────────────────────────────────┘                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Data Isolation Rules
```typescript
// Every query is tenant-scoped
const shipments = await prisma.shipment.findMany({
  where: {
    organizationId: currentUser.organizationId, // ALWAYS enforced
    ...filters
  }
});

// Marketplace queries use ABAC
const visibleRequirements = await prisma.shipmentRequirement.findMany({
  where: {
    status: 'OPEN',
    ...abacFilter(currentVendor) // Based on vendor attributes
  }
});
```

---

## Revenue Model

### 1. SaaS Subscriptions (FreightBox Core)
```
Monthly Recurring Revenue from subscriptions
├── Free tier → Lead generation
├── Paid tiers → Core revenue
└── Enterprise → High-value contracts
```

### 2. Marketplace Transaction Fees
```
Per successful contract:
├── Platform fee: 1-3% of contract value
├── Minimum fee: $10 per transaction
├── Premium placement: $50-200 per listing
└── Verified badge: $99/month
```

### 3. Value-Added Services
```
├── Trade Finance (Revenue share with banks)
├── Insurance (Commission from insurers)
├── Compliance screening ($5-20 per check)
├── Document generation (Premium templates)
└── API access (Usage-based pricing)
```

### 4. Data & Analytics
```
├── Market intelligence reports
├── Rate benchmarking
├── Vendor performance analytics
└── Trade lane insights
```

---

## Competitive Positioning

```
                    INTERNATIONAL SCOPE
                           ▲
                           │
        FreightNET         │         FreightBox
        (Legacy, Complex)  │         (Modern, Open)
                           │              ★
    ◄──────────────────────┼──────────────────────►
    CLOSED NETWORK         │         OPEN MARKETPLACE
                           │
        Flexport           │         Porter/Blackbuck
        (Premium, US-centric)        (Local trucking)
                           │
                           ▼
                    DOMESTIC ONLY
```

### Why FreightBox Wins
| Factor | Legacy Systems | FreightBox |
|--------|---------------|------------|
| Deployment | 6-12 months | 1 day (SaaS) or 1 week (self-hosted) |
| Cost | $100K+ setup | Free to start |
| Integration | Closed APIs | Open GraphQL + REST |
| Marketplace | None | Built-in global exchange |
| Finance | External | Integrated LC, Insurance |
| Mobile | Desktop only | Mobile-first PWA |

---

## Technology Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND                                  │
│  Next.js 14 │ React │ TailwindCSS │ React Query │ PWA           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY                                 │
│  GraphQL (Mercurius) │ REST │ WebSocket │ Rate Limiting         │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│   Core API    │   │  Marketplace  │   │   Document    │
│   (Fastify)   │   │     API       │   │   Service     │
└───────────────┘   └───────────────┘   └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                                 │
│  PostgreSQL │ Prisma ORM │ Redis │ S3/MinIO │ Elasticsearch     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     INTEGRATIONS                                 │
│  Shipping Lines │ Airlines │ Banks │ Insurance │ Customs        │
│  (via ANKR APIBox)                                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Rollout Phases

### Phase 1: Foundation (Current)
- [x] FreightBox Core SaaS
- [x] Shipment management
- [x] Document generation
- [x] Customer portal
- [x] Marketplace MVP (vendors, requirements, bids)

### Phase 2: Marketplace Scale (Next)
- [ ] ABAC-based shipment visibility
- [ ] Smart matching algorithm
- [ ] Bid scoring and ranking
- [ ] Contract generation
- [ ] Escrow payments
- [ ] Rating and review system

### Phase 3: Financial Services
- [ ] Trade finance integration (ICICI, HDFC)
- [ ] Insurance integration (TATA AIG, ICICI Lombard)
- [ ] Forex services
- [ ] Letter of Credit workflow

### Phase 4: Network Effects
- [ ] Mobile app (React Native)
- [ ] WhatsApp/Voice bot (SUNOKAHOBOLO)
- [ ] API marketplace
- [ ] White-label reseller program
- [ ] Franchise model for regional coverage

### Phase 5: Intelligence Layer
- [ ] AI-powered rate prediction
- [ ] Demand forecasting
- [ ] Route optimization
- [ ] Risk scoring
- [ ] Automated compliance

---

## Success Metrics

### Platform Health
```
├── Active Organizations: Target 1,000 in Year 1
├── Monthly Transactions: Target 10,000 shipments
├── Marketplace GMV: Target $50M in Year 1
├── Vendor Network: Target 500 verified vendors
└── Geographic Coverage: India, UAE, EU, USA, SEA
```

### Unit Economics
```
├── Customer Acquisition Cost (CAC): <$200
├── Lifetime Value (LTV): >$5,000
├── LTV/CAC Ratio: >25x
├── Gross Margin: >70%
└── Net Revenue Retention: >120%
```

---

## The Vision

> **"Every freight transaction in the world should flow through FreightBox"**

We're not building a feature—we're building **infrastructure**. Just as:
- Stripe became the payment layer for the internet
- Shopify became the commerce layer for retail
- Twilio became the communication layer for apps

**FreightBox will become the logistics layer for global trade.**

---

## Next Steps

1. **Separate Marketplace UI**: Create `marketplace.freightbox.org` as standalone
2. **Implement ABAC Engine**: Build attribute-based filtering for shipment visibility
3. **Contract & Escrow**: Digital contracts with payment escrow
4. **Bank/Insurance APIs**: Integrate with financial services
5. **Mobile App**: React Native app for on-the-go access
6. **Voice Interface**: Hindi/regional language support via SUNOKAHOBOLO

---

*Document Version: 1.0*
*Created: January 2025*
*Author: Claude (AI Architecture Assistant)*
*For: ANKR Labs / FreightBox Team*
