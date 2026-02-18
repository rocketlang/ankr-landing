# FreightBox Marketplace - Complete Project Documentation

> **Document Version**: 2.0
> **Last Updated**: January 9, 2025
> **Status**: Active Development
> **Download**: Save this file as `FREIGHTBOX_MARKETPLACE.md`

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Product Vision](#2-product-vision)
3. [What Has Been Built](#3-what-has-been-built)
4. [Technical Architecture](#4-technical-architecture)
5. [Database Schema](#5-database-schema)
6. [API Reference](#6-api-reference)
7. [Frontend Pages](#7-frontend-pages)
8. [RBAC & ABAC Design](#8-rbac--abac-design)
9. [User Journeys](#9-user-journeys)
10. [Deployment Guide](#10-deployment-guide)
11. [Roadmap & Todo List](#11-roadmap--todo-list)
12. [Business Model](#12-business-model)
13. [Appendix](#13-appendix)

---

## 1. Executive Summary

### What is FreightBox Marketplace?

FreightBox Marketplace is a **global freight exchange platform** that connects:
- **Shippers** (exporters, importers, manufacturers) who need logistics services
- **Service Providers** (freight forwarders, CHAs, transporters, insurers, banks) who provide those services

Think of it as **"Uber for International Freight"** combined with **"Shopify for Logistics"**.

### The Two-Product Strategy

| Product | Purpose | Deployment |
|---------|---------|------------|
| **FreightBox Core** | Freight management SaaS | `{company}.freightbox.org` or self-hosted |
| **FreightBox Marketplace** | Central exchange for shipments & bids | `marketplace.freightbox.org` |

### Key Metrics (Targets)

| Metric | Year 1 Target |
|--------|---------------|
| Active Organizations | 1,000 |
| Monthly Shipments | 10,000 |
| Marketplace GMV | $50M |
| Verified Vendors | 500 |
| Geographic Coverage | India, UAE, EU, USA, SEA |

---

## 2. Product Vision

### The Problem

International freight is fragmented:
- Shippers struggle to find reliable vendors
- Vendors struggle to find consistent business
- No transparency in pricing
- Manual processes, paper documents
- No unified platform for FCL, LCL, Air, Road, Rail

### The Solution

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FREIGHTBOX MARKETPLACE                            │
│                                                                      │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐              │
│  │   SHIPPERS  │───▶│   BIDDING   │◀───│   VENDORS   │              │
│  │  Post Jobs  │    │   ENGINE    │    │  Submit Bids│              │
│  └─────────────┘    └──────┬──────┘    └─────────────┘              │
│                            │                                         │
│                     ┌──────▼──────┐                                  │
│                     │  CONTRACTS  │                                  │
│                     │   ESCROW    │                                  │
│                     │  TRACKING   │                                  │
│                     └─────────────┘                                  │
└─────────────────────────────────────────────────────────────────────┘
```

### Competitive Landscape

| Competitor | Focus | FreightBox Advantage |
|------------|-------|---------------------|
| Flexport | Premium, US-centric | Global, affordable, open platform |
| Freightos | Rate comparison | Full execution, not just quotes |
| Porter/Blackbuck | Local trucking | International, multimodal |
| Cogoport | Indian market | White-label, self-hosted option |
| Legacy TMS | Enterprise only | Free tier, modern UX |

---

## 3. What Has Been Built

### 3.1 Backend (GraphQL API)

**Location**: `/apps/freightbox/backend/`

#### New Prisma Models Added

```prisma
// Vendor Management
model Vendor {
  id                  String           @id @default(cuid())
  vendorCode          String           @unique  // VND-001
  companyName         String
  tradeName           String?
  vendorType          VendorType[]     // Multiple types allowed
  status              VendorStatus     @default(PENDING_VERIFICATION)

  // Contact
  email               String           @unique
  phone               String
  website             String?

  // Address
  address             String?
  city                String
  state               String
  country             String
  pincode             String?

  // Business Details
  yearEstablished     Int?
  employeeCount       String?
  annualTurnover      String?

  // Compliance
  gstNumber           String?
  panNumber           String?
  iecCode             String?
  chaLicenseNumber    String?
  ffLicenseNumber     String?
  iataCode            String?

  // Banking
  bankName            String?
  bankAccountNumber   String?
  bankIfscCode        String?

  // Capabilities
  serviceAreas        String[]         // Countries/regions served
  freightModes        String[]         // SEA_FCL, AIR, ROAD, etc.
  specializations     String[]         // PHARMA, DG, REEFER, etc.
  certifications      String[]         // ISO, AEO, etc.

  // Memberships
  isIATAMember        Boolean          @default(false)
  isFIATAMember       Boolean          @default(false)
  isWCAMember         Boolean          @default(false)

  // Performance
  rating              Float            @default(0)
  totalReviews        Int              @default(0)
  completedJobs       Int              @default(0)

  // Relations
  bids                Bid[]
  contracts           MarketplaceContract[]
  reviewsReceived     VendorReview[]
  rateCards           VendorRateCard[]
  users               VendorUser[]

  createdAt           DateTime         @default(now())
  updatedAt           DateTime         @updatedAt
}

// Shipment Requirements (Job Postings)
model ShipmentRequirement {
  id                   String            @id @default(cuid())
  requirementNumber    String            @unique  // REQ-2025-001
  title                String
  status               RequirementStatus @default(DRAFT)

  // Cargo Details
  cargoType            String
  cargoDescription     String
  hsCode               String?
  packageType          String
  numberOfPackages     Int
  totalWeight          Float
  totalVolume          Float?
  weightUnit           String            @default("KG")
  volumeUnit           String            @default("CBM")

  // Special Cargo
  isDangerous          Boolean           @default(false)
  dgClass              String?
  unNumber             String?
  isReefer             Boolean           @default(false)
  temperatureMin       Float?
  temperatureMax       Float?
  isOversized          Boolean           @default(false)

  // Route
  originPort           String
  originCountry        String
  originAddress        String?
  destinationPort      String
  destinationCountry   String
  destinationAddress   String?

  // Transport
  freightMode          String[]          // Can be multiple
  incoterm             String

  // Timeline
  pickupDateFrom       DateTime
  pickupDateTo         DateTime
  deliveryDeadline     DateTime?

  // Budget
  budgetMin            Float?
  budgetMax            Float?
  currency             String            @default("USD")

  // Services Needed
  servicesRequired     String[]
  documentsRequired    String[]
  specialInstructions  String?

  // Insurance
  insuranceRequired    Boolean           @default(false)
  insuranceValue       Float?

  // Bidding
  bidDeadline          DateTime?
  totalBids            Int               @default(0)

  // Relations
  organizationId       String
  organization         Organization      @relation(...)
  bids                 Bid[]
  contracts            MarketplaceContract[]

  createdAt            DateTime          @default(now())
  updatedAt            DateTime          @updatedAt
}

// Bids from Vendors
model Bid {
  id                String       @id @default(cuid())
  bidNumber         String       @unique  // BID-2025-001
  status            BidStatus    @default(PENDING)

  // Pricing
  quotedAmount      Float
  currency          String       @default("USD")
  freightCharges    Float?
  customsCharges    Float?
  transportCharges  Float?
  insuranceCharges  Float?
  otherCharges      Float?

  // Timeline
  transitDays       Int
  validUntil        DateTime

  // Details
  proposedRoute     String?
  remarks           String?
  termsConditions   String?

  // Scoring
  totalScore        Float?       @default(0)

  // Relations
  requirementId     String
  requirement       ShipmentRequirement @relation(...)
  vendorId          String
  vendor            Vendor              @relation(...)
  contract          MarketplaceContract?

  submittedAt       DateTime     @default(now())
  updatedAt         DateTime     @updatedAt
}

// Contracts
model MarketplaceContract {
  id               String         @id @default(cuid())
  contractNumber   String         @unique  // CTR-2025-001
  status           ContractStatus @default(DRAFT)

  // Value
  contractValue    Float
  currency         String         @default("USD")

  // Timeline
  startDate        DateTime
  endDate          DateTime

  // Payment
  paymentTerms     String?
  paidAmount       Float          @default(0)
  pendingAmount    Float          @default(0)

  // Relations
  requirementId    String
  requirement      ShipmentRequirement @relation(...)
  vendorId         String
  vendor           Vendor              @relation(...)
  bidId            String         @unique
  bid              Bid                 @relation(...)
  payments         ContractPayment[]

  createdAt        DateTime       @default(now())
  updatedAt        DateTime       @updatedAt
}

// Vendor Reviews
model VendorReview {
  id              String   @id @default(cuid())
  rating          Int      // 1-5
  review          String?
  shipmentType    String?

  // Response
  vendorResponse  String?
  respondedAt     DateTime?

  // Relations
  vendorId        String
  vendor          Vendor   @relation("ReviewsReceived", ...)
  reviewerId      String
  reviewer        Organization @relation(...)
  contractId      String?

  createdAt       DateTime @default(now())
}
```

#### New Enums

```prisma
enum VendorType {
  FREIGHT_FORWARDER
  CUSTOM_HOUSE_AGENT
  TRANSPORTER
  INSURANCE_PROVIDER
  BANK_TRADE_FINANCE
  WAREHOUSE_OPERATOR
  PACKAGING_PROVIDER
  SURVEYOR
  FUMIGATION_SERVICE
  CONTAINER_YARD
  SHIPPING_LINE
  AIRLINE
  NVOCC
}

enum VendorStatus {
  PENDING_VERIFICATION
  UNDER_REVIEW
  VERIFIED
  SUSPENDED
  REJECTED
}

enum RequirementStatus {
  DRAFT
  OPEN
  BIDDING
  AWARDED
  IN_PROGRESS
  COMPLETED
  CANCELLED
  EXPIRED
}

enum BidStatus {
  PENDING
  UNDER_REVIEW
  SHORTLISTED
  ACCEPTED
  REJECTED
  WITHDRAWN
  EXPIRED
}

enum ContractStatus {
  DRAFT
  PENDING_SIGNATURE
  ACTIVE
  IN_PROGRESS
  COMPLETED
  CANCELLED
  DISPUTED
}
```

#### GraphQL Queries Added

```graphql
type Query {
  # Vendors
  vendor(id: ID!): Vendor
  vendorByCode(code: String!): Vendor
  vendors(status: VendorStatus): [Vendor!]!
  searchVendors(filters: VendorSearchInput): [Vendor!]!
  vendorStats: VendorStats!

  # Requirements
  shipmentRequirement(id: ID!): ShipmentRequirement
  shipmentRequirements(status: RequirementStatus): [ShipmentRequirement!]!
  openRequirements(filters: RequirementFilters): [ShipmentRequirement!]!
  myRequirements: [ShipmentRequirement!]!

  # Bids
  bid(id: ID!): Bid
  bidsForRequirement(requirementId: ID!): [Bid!]!
  myBids: [Bid!]!
  rankedBids(requirementId: ID!): [Bid!]!

  # Contracts
  marketplaceContract(id: ID!): MarketplaceContract
  vendorContracts(vendorId: ID!): [MarketplaceContract!]!
  shipperContracts: [MarketplaceContract!]!

  # Reviews
  vendorReviews(vendorId: ID!): [VendorReview!]!

  # Stats
  marketplaceStats: MarketplaceStats!
}
```

#### GraphQL Mutations Added

```graphql
type Mutation {
  # Vendor Registration
  registerVendor(input: RegisterVendorInput!): Vendor!
  updateVendor(id: ID!, input: UpdateVendorInput!): Vendor!
  verifyVendor(id: ID!, notes: String): Vendor!
  suspendVendor(id: ID!, reason: String!): Vendor!

  # Rate Cards
  createRateCard(input: CreateRateCardInput!): VendorRateCard!
  updateRateCard(id: ID!, input: UpdateRateCardInput!): VendorRateCard!
  deleteRateCard(id: ID!): Boolean!

  # Requirements
  createShipmentRequirement(input: CreateRequirementInput!): ShipmentRequirement!
  updateShipmentRequirement(id: ID!, input: UpdateRequirementInput!): ShipmentRequirement!
  publishRequirement(id: ID!): ShipmentRequirement!
  closeRequirement(id: ID!): ShipmentRequirement!
  cancelRequirement(id: ID!, reason: String): ShipmentRequirement!

  # Bids
  submitBid(input: SubmitBidInput!): Bid!
  updateBid(id: ID!, input: UpdateBidInput!): Bid!
  withdrawBid(id: ID!): Bid!
  shortlistBid(id: ID!): Bid!
  acceptBid(id: ID!): Bid!
  rejectBid(id: ID!, reason: String): Bid!

  # Contracts
  updateContractStatus(id: ID!, status: ContractStatus!): MarketplaceContract!
  completeContract(id: ID!): MarketplaceContract!
  raiseDispute(id: ID!, reason: String!): MarketplaceContract!

  # Reviews
  submitReview(input: SubmitReviewInput!): VendorReview!
  respondToReview(id: ID!, response: String!): VendorReview!
}
```

### 3.2 Frontend Pages

**Location**: `/apps/freightbox/frontend/src/app/dashboard/marketplace/`

```
marketplace/
├── page.tsx                      # Marketplace dashboard
├── vendors/
│   ├── page.tsx                  # Browse vendors
│   ├── register/
│   │   └── page.tsx              # 4-step vendor registration
│   └── [id]/
│       └── page.tsx              # Vendor profile detail
├── requirements/
│   ├── page.tsx                  # List requirements
│   ├── new/
│   │   └── page.tsx              # 5-step requirement form
│   └── [id]/
│       ├── page.tsx              # Requirement detail + bid management
│       └── bid/
│           └── page.tsx          # Submit bid form
├── bids/
│   └── page.tsx                  # Manage bids (vendor & shipper views)
└── contracts/
    └── page.tsx                  # Contract management
```

### 3.3 Navigation Added

Added to `DashboardLayout.tsx`:

```typescript
{
  title: 'Marketplace',
  items: [
    {
      id: 'marketplace',
      label: 'Marketplace',
      href: '/dashboard/marketplace',
      icon: Store,
      children: [
        { id: 'mp-overview', label: 'Overview', href: '/dashboard/marketplace' },
        { id: 'mp-vendors', label: 'Vendors', href: '/dashboard/marketplace/vendors' },
        { id: 'mp-requirements', label: 'Requirements', href: '/dashboard/marketplace/requirements' },
        { id: 'mp-bids', label: 'Bids', href: '/dashboard/marketplace/bids' },
        { id: 'mp-contracts', label: 'Contracts', href: '/dashboard/marketplace/contracts' },
      ]
    },
    {
      id: 'vendor-register',
      label: 'Register Vendor',
      href: '/dashboard/marketplace/vendors/register'
    },
  ],
}
```

---

## 4. Technical Architecture

### 4.1 System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                           CLIENTS                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │   Web    │  │  Mobile  │  │   API    │  │  Voice   │            │
│  │  (Next)  │  │  (RN)    │  │ Clients  │  │  (Bani)  │            │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │
└───────┼─────────────┼─────────────┼─────────────┼───────────────────┘
        │             │             │             │
        └─────────────┴──────┬──────┴─────────────┘
                             │
                    ┌────────▼────────┐
                    │   API Gateway   │
                    │  (Next.js API)  │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼───────┐   ┌───────▼───────┐   ┌───────▼───────┐
│   FreightBox  │   │   Auth/IAM    │   │   Document    │
│   Backend     │   │   Service     │   │   Service     │
│  (Fastify)    │   │  (Keycloak)   │   │   (PDF/QR)    │
└───────┬───────┘   └───────────────┘   └───────────────┘
        │
┌───────▼───────────────────────────────────────────────┐
│                    DATA LAYER                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │PostgreSQL│ │  Redis  │  │  MinIO  │  │  Elastic │  │
│  │ (Prisma)│  │ (Cache) │  │(Storage)│  │ (Search) │  │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  │
└───────────────────────────────────────────────────────┘
```

### 4.2 Multi-Tenant Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    TENANT ISOLATION                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Organization A          Organization B          Organization C  │
│  ┌─────────────┐        ┌─────────────┐        ┌─────────────┐  │
│  │ Shipments   │        │ Shipments   │        │ Shipments   │  │
│  │ Documents   │        │ Documents   │        │ Documents   │  │
│  │ Invoices    │        │ Invoices    │        │ Invoices    │  │
│  │ (org_id=A)  │        │ (org_id=B)  │        │ (org_id=C)  │  │
│  └─────────────┘        └─────────────┘        └─────────────┘  │
│                                                                  │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ MARKETPLACE (SHARED) ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Vendors (public)  │  Requirements (public)  │  Bids    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 14, React, TailwindCSS, React Query |
| API | GraphQL (Mercurius), Fastify |
| Database | PostgreSQL, Prisma ORM |
| Cache | Redis |
| Storage | MinIO (S3-compatible) |
| Search | Elasticsearch |
| Auth | Keycloak (planned) |
| PDF | @react-pdf/renderer |
| Blockchain | Custom DocChain |

---

## 5. Database Schema

### 5.1 Entity Relationship Diagram

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│ Organization │───────│    User      │───────│    Role      │
│   (Tenant)   │ 1:N   │              │ N:M   │   (RBAC)     │
└──────┬───────┘       └──────────────┘       └──────────────┘
       │ 1:N
       │
┌──────▼───────┐       ┌──────────────┐
│   Vendor     │◄──────│  VendorUser  │
│  (Profile)   │ 1:N   │              │
└──────┬───────┘       └──────────────┘
       │
       │ 1:N                    1:N ┌──────────────┐
       │         ┌──────────────────│ShipmentReq.  │
       │         │                  │ (Job Post)   │
       │         │                  └──────┬───────┘
       │         │                         │ 1:N
┌──────▼───────┐ │                  ┌──────▼───────┐
│     Bid      │◄┘                  │     Bid      │
│              │                    │              │
└──────┬───────┘                    └──────────────┘
       │ 1:1
       │
┌──────▼───────┐       ┌──────────────┐
│  Contract    │───────│   Payment    │
│              │ 1:N   │              │
└──────┬───────┘       └──────────────┘
       │
       │ 1:N
┌──────▼───────┐
│   Review     │
│              │
└──────────────┘
```

### 5.2 Key Indexes

```sql
-- Vendor search
CREATE INDEX idx_vendor_status ON "Vendor"(status);
CREATE INDEX idx_vendor_country ON "Vendor"(country);
CREATE INDEX idx_vendor_rating ON "Vendor"(rating DESC);

-- Requirement search
CREATE INDEX idx_requirement_status ON "ShipmentRequirement"(status);
CREATE INDEX idx_requirement_origin ON "ShipmentRequirement"("originCountry");
CREATE INDEX idx_requirement_dest ON "ShipmentRequirement"("destinationCountry");
CREATE INDEX idx_requirement_deadline ON "ShipmentRequirement"("bidDeadline");

-- Bid search
CREATE INDEX idx_bid_status ON "Bid"(status);
CREATE INDEX idx_bid_requirement ON "Bid"("requirementId");
CREATE INDEX idx_bid_vendor ON "Bid"("vendorId");
```

---

## 6. API Reference

### 6.1 Vendor Registration

```graphql
mutation RegisterVendor($input: RegisterVendorInput!) {
  registerVendor(input: $input) {
    id
    vendorCode
    status
  }
}

# Input
{
  "input": {
    "companyName": "ABC Logistics Pvt Ltd",
    "tradeName": "ABC Freight",
    "vendorType": ["FREIGHT_FORWARDER", "CUSTOM_HOUSE_AGENT"],
    "email": "contact@abclogistics.com",
    "phone": "+91-9876543210",
    "city": "Mumbai",
    "state": "Maharashtra",
    "country": "India",
    "gstNumber": "27AABCU9603R1ZM",
    "panNumber": "AABCU9603R",
    "iecCode": "0300012345",
    "serviceAreas": ["INDIA", "UAE", "EUROPE"],
    "freightModes": ["SEA_FCL", "SEA_LCL", "AIR"],
    "specializations": ["PHARMACEUTICALS", "ELECTRONICS"],
    "isIATAMember": true,
    "isFIATAMember": true
  }
}
```

### 6.2 Post Shipment Requirement

```graphql
mutation CreateRequirement($input: CreateRequirementInput!) {
  createShipmentRequirement(input: $input) {
    id
    requirementNumber
    status
  }
}

# Input
{
  "input": {
    "title": "20 Pallets Electronics - Mumbai to Rotterdam",
    "cargoType": "Electronics",
    "cargoDescription": "Consumer electronics, properly packed",
    "hsCode": "8471.30",
    "packageType": "Pallets",
    "numberOfPackages": 20,
    "totalWeight": 4500,
    "weightUnit": "KG",
    "totalVolume": 35,
    "volumeUnit": "CBM",
    "originPort": "JNPT/Nhava Sheva",
    "originCountry": "India",
    "destinationPort": "Rotterdam",
    "destinationCountry": "Netherlands",
    "freightMode": ["SEA_FCL"],
    "incoterm": "FOB - Free On Board",
    "pickupDateFrom": "2025-02-01",
    "pickupDateTo": "2025-02-05",
    "deliveryDeadline": "2025-02-28",
    "budgetMin": 3000,
    "budgetMax": 5000,
    "currency": "USD",
    "servicesRequired": ["FREIGHT_FORWARDING", "CUSTOMS_CLEARANCE"],
    "bidDeadline": "2025-01-20T18:00:00Z",
    "publishImmediately": true
  }
}
```

### 6.3 Submit Bid

```graphql
mutation SubmitBid($input: SubmitBidInput!) {
  submitBid(input: $input) {
    id
    bidNumber
    quotedAmount
    status
  }
}

# Input
{
  "input": {
    "requirementId": "clxyz123...",
    "quotedAmount": 3850,
    "currency": "USD",
    "freightCharges": 3200,
    "customsCharges": 350,
    "transportCharges": 200,
    "otherCharges": 100,
    "transitDays": 21,
    "validUntil": "2025-01-25",
    "proposedRoute": "JNPT - Colombo - Rotterdam via MSC",
    "remarks": "Weekly sailing, direct service available",
    "termsConditions": "50% advance, 50% on BL release"
  }
}
```

### 6.4 Accept Bid & Create Contract

```graphql
mutation AcceptBid($bidId: ID!) {
  acceptBid(id: $bidId) {
    id
    status
    contract {
      id
      contractNumber
      contractValue
      status
    }
  }
}
```

---

## 7. Frontend Pages

### 7.1 Page Specifications

| Page | Route | Purpose |
|------|-------|---------|
| Marketplace Home | `/dashboard/marketplace` | Overview, stats, quick actions |
| Vendor List | `/dashboard/marketplace/vendors` | Browse & search vendors |
| Vendor Registration | `/dashboard/marketplace/vendors/register` | 4-step registration form |
| Vendor Profile | `/dashboard/marketplace/vendors/[id]` | Vendor details, reviews |
| Requirements List | `/dashboard/marketplace/requirements` | List shipment requirements |
| New Requirement | `/dashboard/marketplace/requirements/new` | 5-step job posting form |
| Requirement Detail | `/dashboard/marketplace/requirements/[id]` | View requirement + manage bids |
| Submit Bid | `/dashboard/marketplace/requirements/[id]/bid` | Bid submission form |
| My Bids | `/dashboard/marketplace/bids` | View submitted/received bids |
| Contracts | `/dashboard/marketplace/contracts` | Contract management |

### 7.2 Page Features

#### Marketplace Dashboard
- Stats cards (Open Requirements, Total Bids, Active Contracts, Contract Value)
- Quick actions for Shippers and Vendors
- Service category grid with vendor counts
- "How it Works" section

#### Vendor Registration (4 Steps)
1. **Company Info**: Name, type, contact, address
2. **Compliance**: GSTIN, PAN, IEC, CHA License, Banking
3. **Capabilities**: Freight modes, specializations, certifications, service areas
4. **Review**: Summary and submit

#### Post Requirement (5 Steps)
1. **Cargo Details**: Type, weight, volume, DG/Reefer flags
2. **Route & Mode**: Origin, destination, transport modes, incoterm
3. **Timeline & Budget**: Pickup window, delivery deadline, budget range
4. **Services Required**: Checklist of needed services, documents
5. **Review & Submit**: Summary, save draft or publish

#### Bid Management
- Sort by: Price, Transit Time, Score, Rating
- Shortlist/Accept/Reject actions
- Vendor details inline
- Charges breakdown view

---

## 8. RBAC & ABAC Design

### 8.1 RBAC (Within Organization)

```yaml
Roles:
  ADMIN:
    description: Full access to organization
    permissions:
      - "*"

  OPERATIONS_MANAGER:
    description: Manage shipments and vendors
    permissions:
      - shipments.*
      - documents.*
      - vendors.view
      - marketplace.requirements.*
      - marketplace.bids.*

  OPERATIONS_EXECUTIVE:
    description: Day-to-day operations
    permissions:
      - shipments.view
      - shipments.update
      - documents.create
      - documents.view
      - marketplace.requirements.view

  FINANCE:
    description: Financial operations
    permissions:
      - invoices.*
      - payments.*
      - reports.financial
      - contracts.view

  CUSTOMER_SERVICE:
    description: Customer-facing operations
    permissions:
      - shipments.view
      - tracking.*
      - portal.*

  VENDOR_ADMIN:
    description: Vendor organization admin
    permissions:
      - vendor.profile.*
      - marketplace.bids.*
      - contracts.*

  VIEWER:
    description: Read-only access
    permissions:
      - "*.view"
```

### 8.2 ABAC (Marketplace Visibility)

```typescript
// ABAC Policy Engine
interface VendorAttributes {
  vendorType: VendorType[];
  serviceAreas: string[];      // Countries/regions
  freightModes: string[];      // SEA_FCL, AIR, etc.
  specializations: string[];   // PHARMA, DG, REEFER
  dgCapable: boolean;
  reeferCapable: boolean;
  minShipmentValue: number;
  maxShipmentValue: number;
  rating: number;
  isVerified: boolean;
}

interface RequirementAttributes {
  originCountry: string;
  destinationCountry: string;
  freightMode: string[];
  cargoType: string;
  isDangerous: boolean;
  isReefer: boolean;
  estimatedValue: number;
  requiredCertifications: string[];
}

function canVendorSeeRequirement(
  vendor: VendorAttributes,
  requirement: RequirementAttributes
): boolean {
  // Must be verified
  if (!vendor.isVerified) return false;

  // Origin must be in vendor's service areas
  if (!vendor.serviceAreas.includes(requirement.originCountry)) return false;

  // Destination must be in vendor's service areas
  if (!vendor.serviceAreas.includes(requirement.destinationCountry)) return false;

  // At least one freight mode must match
  const modeMatch = requirement.freightMode.some(m =>
    vendor.freightModes.includes(m)
  );
  if (!modeMatch) return false;

  // DG capability check
  if (requirement.isDangerous && !vendor.dgCapable) return false;

  // Reefer capability check
  if (requirement.isReefer && !vendor.reeferCapable) return false;

  // Value range check (if specified)
  if (vendor.minShipmentValue && requirement.estimatedValue < vendor.minShipmentValue) {
    return false;
  }
  if (vendor.maxShipmentValue && requirement.estimatedValue > vendor.maxShipmentValue) {
    return false;
  }

  return true;
}
```

---

## 9. User Journeys

### 9.1 Shipper Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                      SHIPPER JOURNEY                             │
└─────────────────────────────────────────────────────────────────┘

1. ONBOARDING
   ├── Sign up on FreightBox
   ├── Create organization profile
   └── Verify email/phone

2. POST REQUIREMENT
   ├── Navigate to Marketplace → Post Requirement
   ├── Fill cargo details (type, weight, dimensions)
   ├── Specify route (origin, destination, mode)
   ├── Set timeline (pickup window, delivery deadline)
   ├── Define budget range (optional)
   ├── Select required services
   └── Publish requirement

3. RECEIVE BIDS
   ├── System notifies matching vendors
   ├── Vendors submit bids within deadline
   ├── View all bids on requirement page
   └── Compare by price, transit, rating

4. EVALUATE & AWARD
   ├── Shortlist top 3-5 bids
   ├── Request clarifications if needed
   ├── Accept winning bid
   └── Contract auto-generated

5. EXECUTION
   ├── Vendor starts execution
   ├── Track shipment in real-time
   ├── Receive documents (BL, Invoice)
   └── Customs clearance updates

6. SETTLEMENT
   ├── Confirm delivery
   ├── Release payment from escrow
   ├── Rate & review vendor
   └── Download final documents
```

### 9.2 Vendor Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                      VENDOR JOURNEY                              │
└─────────────────────────────────────────────────────────────────┘

1. REGISTRATION
   ├── Navigate to Register as Vendor
   ├── Company information
   ├── Compliance documents (GSTIN, PAN, IEC, License)
   ├── Capabilities & service areas
   ├── Submit for verification
   └── Await approval (1-3 business days)

2. PROFILE SETUP
   ├── Complete vendor profile
   ├── Add certifications & memberships
   ├── Upload company logo & documents
   └── Set up rate cards (optional)

3. BROWSE REQUIREMENTS
   ├── View marketplace dashboard
   ├── Filter by route, cargo type, mode
   ├── See requirements matching capabilities (ABAC)
   └── Set up alerts for new requirements

4. SUBMIT BID
   ├── Open requirement detail
   ├── Click "Submit Bid"
   ├── Enter charges breakdown
   ├── Specify transit time & validity
   ├── Add route & remarks
   └── Submit bid

5. WIN CONTRACT
   ├── Receive notification if shortlisted
   ├── Respond to clarifications
   ├── Receive notification if accepted
   └── Digital contract generated

6. EXECUTE & DELIVER
   ├── Coordinate pickup
   ├── Generate documents via FreightBox
   ├── Update shipment status
   ├── Complete delivery
   └── Upload POD

7. GET PAID & REVIEWED
   ├── Shipper confirms delivery
   ├── Payment released
   ├── Receive rating & review
   └── Respond to review (optional)
```

---

## 10. Deployment Guide

### 10.1 Prerequisites

```bash
# Required software
Node.js >= 18
PostgreSQL >= 14
Redis >= 6
PM2 (process manager)

# Environment variables
DATABASE_URL="postgresql://user:pass@localhost:5432/freightbox"
REDIS_URL="redis://localhost:6379"
GRAPHQL_URL="http://localhost:4003/graphql"
```

### 10.2 Backend Deployment

```bash
# Navigate to backend
cd /var/www/ankr-labs-nx/apps/freightbox/backend

# Install dependencies
npm install

# Generate Prisma client
npx prisma generate

# Apply migrations
npx prisma db push

# Start with PM2
pm2 start npm --name "freightbox-backend" -- run start -- --port 4003
```

### 10.3 Frontend Deployment

```bash
# Navigate to frontend
cd /var/www/ankr-labs-nx/apps/freightbox/frontend

# Install dependencies
npm install

# Build
npm run build

# Start with PM2
pm2 start npm --name "freightbox-frontend" -- run start -- -p 3001
```

### 10.4 Nginx Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name freightbox.org;

    ssl_certificate /etc/letsencrypt/live/freightbox.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/freightbox.org/privkey.pem;

    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api/graphql {
        proxy_pass http://localhost:4003/graphql;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }
}
```

---

## 11. Roadmap & Todo List

### Phase 1: Foundation (COMPLETED)

| Task | Status | Description |
|------|--------|-------------|
| Vendor Registration | ✅ Done | 4-step registration form, multi-type support |
| Shipper Portal | ✅ Done | 5-step requirement posting, cargo details |
| Bidding System | ✅ Done | Bid submission, shortlist, accept flow |
| Vendor Profiles | ✅ Done | Profile pages with ratings, reviews |
| Backend APIs | ✅ Done | GraphQL queries & mutations |
| Navigation | ✅ Done | Sidebar integration |

### Phase 2: Marketplace Enhancement (IN PROGRESS)

| Task | Status | Description |
|------|--------|-------------|
| ABAC Engine | 🔄 Pending | Attribute-based shipment visibility |
| Smart Matching | 🔄 Pending | ML-based vendor recommendation |
| Bid Scoring | 🔄 Pending | Auto-score bids (price, transit, rating) |
| Notifications | 🔄 Pending | Email/SMS for bid updates |
| Rate Cards | 🔄 Pending | Vendor published rates |

### Phase 3: Contracts & Payments (PLANNED)

| Task | Status | Description |
|------|--------|-------------|
| Contract Generation | 📋 Planned | Digital contract from accepted bid |
| E-Signature | 📋 Planned | DocuSign/custom signature |
| Escrow System | 📋 Planned | Hold payment until delivery |
| Payment Gateway | 📋 Planned | Razorpay/Stripe integration |
| Invoice Generation | 📋 Planned | Auto-generate from contract |

### Phase 4: Financial Services (PLANNED)

| Task | Status | Description |
|------|--------|-------------|
| Trade Finance | 📋 Planned | LC workflow with banks |
| Insurance | 📋 Planned | Marine/cargo insurance APIs |
| Forex | 📋 Planned | Multi-currency support |
| Credit Scoring | 📋 Planned | Vendor creditworthiness |

### Phase 5: Platform Scale (PLANNED)

| Task | Status | Description |
|------|--------|-------------|
| Multi-Tenant | 📋 Planned | Full tenant isolation |
| White Label | 📋 Planned | Custom branding per tenant |
| API Marketplace | 📋 Planned | Third-party integrations |
| Mobile App | 📋 Planned | React Native iOS/Android |
| Voice Interface | 📋 Planned | Hindi/regional via SUNOKAHOBOLO |
| Analytics | 📋 Planned | Business intelligence dashboard |

### Phase 6: AI & Intelligence (FUTURE)

| Task | Status | Description |
|------|--------|-------------|
| Rate Prediction | 🔮 Future | ML-based rate forecasting |
| Demand Forecasting | 🔮 Future | Predict shipment volumes |
| Route Optimization | 🔮 Future | Best routing suggestions |
| Risk Scoring | 🔮 Future | Shipment risk assessment |
| Chatbot | 🔮 Future | AI-powered customer support |

---

## 12. Business Model

### 12.1 Revenue Streams

```
┌─────────────────────────────────────────────────────────────────┐
│                    REVENUE MODEL                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. SaaS SUBSCRIPTIONS (FreightBox Core)                        │
│     ├── Free Tier: $0 (50 shipments/month)                      │
│     ├── Starter: $99/month (500 shipments, 5 users)             │
│     ├── Professional: $299/month (unlimited, 20 users)          │
│     └── Enterprise: Custom pricing                              │
│                                                                  │
│  2. MARKETPLACE FEES                                             │
│     ├── Transaction Fee: 1-3% of contract value                 │
│     ├── Minimum Fee: $10 per transaction                        │
│     ├── Premium Listing: $50-200 per requirement                │
│     └── Verified Badge: $99/month                               │
│                                                                  │
│  3. VALUE-ADDED SERVICES                                         │
│     ├── Trade Finance: Revenue share with banks                 │
│     ├── Insurance: Commission from insurers                     │
│     ├── Compliance Screening: $5-20 per check                   │
│     └── Premium Templates: $10-50 per document                  │
│                                                                  │
│  4. DATA & ANALYTICS                                             │
│     ├── Market Reports: $500-2000                               │
│     ├── Rate Benchmarking: $99/month                            │
│     └── API Access: Usage-based                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 12.2 Unit Economics

| Metric | Target |
|--------|--------|
| Customer Acquisition Cost (CAC) | < $200 |
| Lifetime Value (LTV) | > $5,000 |
| LTV/CAC Ratio | > 25x |
| Gross Margin | > 70% |
| Net Revenue Retention | > 120% |
| Payback Period | < 6 months |

### 12.3 Go-to-Market Strategy

```
Year 1: India Focus
├── Target: Exporters, FFs, CHAs in Mumbai, Delhi, Chennai
├── Strategy: Free tier + direct sales
└── Goal: 500 organizations, $5M GMV

Year 2: Middle East Expansion
├── Target: Dubai, Abu Dhabi logistics hubs
├── Strategy: Partnerships with FTZs
└── Goal: 2,000 organizations, $20M GMV

Year 3: Global Scale
├── Target: EU, USA, Southeast Asia
├── Strategy: API partnerships, white-label
└── Goal: 10,000 organizations, $100M GMV
```

---

## 13. Appendix

### 13.1 Glossary

| Term | Definition |
|------|------------|
| **FF** | Freight Forwarder - arranges shipments |
| **CHA** | Custom House Agent - handles customs |
| **NVOCC** | Non-Vessel Operating Common Carrier |
| **FCL** | Full Container Load |
| **LCL** | Less than Container Load |
| **BL** | Bill of Lading |
| **AWB** | Air Waybill |
| **LC** | Letter of Credit |
| **DG** | Dangerous Goods |
| **Reefer** | Refrigerated cargo |
| **Incoterm** | International Commercial Terms |
| **HS Code** | Harmonized System Code (tariff classification) |
| **IEC** | Import Export Code |
| **GSTIN** | GST Identification Number |
| **IATA** | International Air Transport Association |
| **FIATA** | International Federation of Freight Forwarders |

### 13.2 Vendor Types

| Type | Services |
|------|----------|
| FREIGHT_FORWARDER | International shipping coordination |
| CUSTOM_HOUSE_AGENT | Customs clearance, documentation |
| TRANSPORTER | Local trucking, first/last mile |
| INSURANCE_PROVIDER | Marine & cargo insurance |
| BANK_TRADE_FINANCE | LC, bank guarantee, forex |
| WAREHOUSE_OPERATOR | Storage, distribution |
| SHIPPING_LINE | Ocean container booking |
| AIRLINE | Air cargo capacity |
| NVOCC | Sea freight consolidation |
| SURVEYOR | Pre-shipment inspection |
| FUMIGATION_SERVICE | Pest treatment certification |

### 13.3 Freight Modes

| Mode | Use Case |
|------|----------|
| SEA_FCL | Full container, high volume |
| SEA_LCL | Partial container, consolidated |
| AIR | Urgent, high-value, perishables |
| ROAD | Domestic, cross-border trucking |
| RAIL | Bulk, long-distance domestic |
| MULTIMODAL | Combined modes |

### 13.4 API Endpoints Summary

```
GraphQL Endpoint: /api/graphql

Queries:
- vendor, vendors, vendorByCode, searchVendors, vendorStats
- shipmentRequirement, shipmentRequirements, openRequirements, myRequirements
- bid, bidsForRequirement, myBids, rankedBids
- marketplaceContract, vendorContracts, shipperContracts
- vendorReviews, marketplaceStats

Mutations:
- registerVendor, updateVendor, verifyVendor, suspendVendor
- createRateCard, updateRateCard, deleteRateCard
- createShipmentRequirement, updateShipmentRequirement
- publishRequirement, closeRequirement, cancelRequirement
- submitBid, updateBid, withdrawBid
- shortlistBid, acceptBid, rejectBid
- updateContractStatus, completeContract, raiseDispute
- submitReview, respondToReview
```

### 13.5 File Structure

```
/apps/freightbox/
├── backend/
│   ├── prisma/
│   │   └── schema.prisma          # Database models
│   ├── src/
│   │   └── main.ts                # GraphQL API
│   └── package.json
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   └── dashboard/
│   │   │       └── marketplace/   # All marketplace pages
│   │   ├── components/
│   │   │   └── layout/
│   │   │       └── DashboardLayout.tsx
│   │   └── lib/
│   │       └── graphql/
│   ├── next.config.js
│   └── package.json
├── FREIGHTBOX_VISION_2025.md
└── FREIGHTBOX_MARKETPLACE_COMPLETE_PROJECT.md  # This document
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 9, 2025 | Claude | Initial marketplace MVP |
| 2.0 | Jan 9, 2025 | Claude | Complete documentation, vision, roadmap |

---

**End of Document**

*For questions or support, contact the FreightBox team at ANKR Labs.*
