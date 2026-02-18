-- ═══════════════════════════════════════════════════════════════════════════════
-- WOWTRUCK 2.0 - DATABASE SCHEMA MIGRATION
-- ═══════════════════════════════════════════════════════════════════════════════
-- Run this SQL to create missing tables for WowTruck
-- Database: ankr_eon (Port 5433)
--
-- Usage:
--   PGPASSWORD='indrA@0612' psql -h localhost -p 5433 -U ankr -d ankr_eon -f wowtruck-schema-migration.sql
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- 1. CREATE SCHEMAS
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE SCHEMA IF NOT EXISTS freight;
CREATE SCHEMA IF NOT EXISTS wowtruck;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 2. FREIGHT EXCHANGE TABLES
-- ═══════════════════════════════════════════════════════════════════════════════

-- Carrier Profiles (Transporters/Fleet Owners)
CREATE TABLE IF NOT EXISTS freight.carrier_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_name VARCHAR(200) NOT NULL,
  contact_person VARCHAR(100),
  phone VARCHAR(20),
  email VARCHAR(100),
  gstin VARCHAR(20),
  pan VARCHAR(15),
  address TEXT,
  city VARCHAR(100),
  state VARCHAR(100),
  pincode VARCHAR(10),
  fleet_size INT DEFAULT 0,
  rating DECIMAL(2,1) DEFAULT 4.0,
  total_trips INT DEFAULT 0,
  total_km DECIMAL(12,2) DEFAULT 0,
  status VARCHAR(20) DEFAULT 'active',
  verified BOOLEAN DEFAULT false,
  verified_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Load Postings (Shippers posting loads)
CREATE TABLE IF NOT EXISTS freight.load_postings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  posting_code VARCHAR(50) UNIQUE NOT NULL,
  shipper_id UUID,
  origin_city VARCHAR(100) NOT NULL,
  origin_state VARCHAR(100),
  origin_pincode VARCHAR(10),
  origin_address TEXT,
  origin_lat DECIMAL(10,7),
  origin_lng DECIMAL(10,7),
  dest_city VARCHAR(100) NOT NULL,
  dest_state VARCHAR(100),
  dest_pincode VARCHAR(10),
  dest_address TEXT,
  dest_lat DECIMAL(10,7),
  dest_lng DECIMAL(10,7),
  cargo_type VARCHAR(50),
  cargo_description TEXT,
  vehicle_type VARCHAR(50),
  weight_mt DECIMAL(10,2),
  volume_cbm DECIMAL(10,2),
  budget_min DECIMAL(12,2),
  budget_max DECIMAL(12,2),
  pickup_date DATE,
  pickup_time_from TIME,
  pickup_time_to TIME,
  delivery_date DATE,
  status VARCHAR(20) DEFAULT 'active',
  priority VARCHAR(20) DEFAULT 'normal',
  notes TEXT,
  contact_name VARCHAR(100),
  contact_phone VARCHAR(20),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ
);

-- Truck Postings (Carriers posting available trucks)
CREATE TABLE IF NOT EXISTS freight.truck_postings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  posting_code VARCHAR(50) UNIQUE NOT NULL,
  carrier_id UUID REFERENCES freight.carrier_profiles(id),
  current_city VARCHAR(100) NOT NULL,
  current_state VARCHAR(100),
  current_pincode VARCHAR(10),
  current_lat DECIMAL(10,7),
  current_lng DECIMAL(10,7),
  vehicle_type VARCHAR(50) NOT NULL,
  vehicle_number VARCHAR(20),
  capacity_mt DECIMAL(10,2),
  capacity_cbm DECIMAL(10,2),
  expected_rate_per_km DECIMAL(10,2),
  min_rate DECIMAL(12,2),
  available_from DATE,
  available_until DATE,
  preferred_routes TEXT, -- JSON array of city pairs
  status VARCHAR(20) DEFAULT 'available',
  driver_name VARCHAR(100),
  driver_phone VARCHAR(20),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Bids on Load Postings
CREATE TABLE IF NOT EXISTS freight.bids (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  load_id UUID REFERENCES freight.load_postings(id) ON DELETE CASCADE,
  carrier_id UUID REFERENCES freight.carrier_profiles(id),
  truck_posting_id UUID REFERENCES freight.truck_postings(id),
  bid_amount DECIMAL(12,2) NOT NULL,
  proposed_vehicle VARCHAR(50),
  proposed_pickup_date DATE,
  estimated_delivery DATE,
  notes TEXT,
  status VARCHAR(20) DEFAULT 'pending', -- pending, accepted, rejected, withdrawn
  accepted_at TIMESTAMPTZ,
  rejected_at TIMESTAMPTZ,
  rejection_reason TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Surge/Dynamic Pricing
CREATE TABLE IF NOT EXISTS freight.surge_pricing (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  origin_city VARCHAR(100) NOT NULL,
  dest_city VARCHAR(100) NOT NULL,
  vehicle_type VARCHAR(50),
  surge_level VARCHAR(20) DEFAULT 'normal', -- low, normal, moderate, high, extreme
  surge_multiplier DECIMAL(3,2) DEFAULT 1.00,
  active_loads INT DEFAULT 0,
  available_trucks INT DEFAULT 0,
  demand_supply_ratio DECIMAL(5,2),
  suggested_rate_min DECIMAL(12,2),
  suggested_rate_max DECIMAL(12,2),
  base_rate_per_km DECIMAL(10,2),
  valid_from TIMESTAMPTZ DEFAULT NOW(),
  valid_until TIMESTAMPTZ,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 3. MRF RATE ENGINE TABLES
-- ═══════════════════════════════════════════════════════════════════════════════

-- MRF Contract Lanes (Master Rate File)
CREATE TABLE IF NOT EXISTS wowtruck.mrf_lanes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lane_code VARCHAR(50) UNIQUE,
  lane_name VARCHAR(200),
  source VARCHAR(100) NOT NULL,
  source_zip VARCHAR(10),
  source_state VARCHAR(100),
  destination VARCHAR(100) NOT NULL,
  destination_zip VARCHAR(10),
  destination_state VARCHAR(100),
  truck_type VARCHAR(50) NOT NULL,
  base_rate DECIMAL(12,2) NOT NULL,
  distance_km DECIMAL(10,2),
  transit_days DECIMAL(3,1),
  per_km_rate DECIMAL(10,2),
  loadability_mt DECIMAL(10,2),
  region VARCHAR(50),
  contract_id VARCHAR(50),
  customer_id UUID,
  effective_from DATE DEFAULT CURRENT_DATE,
  effective_to DATE,
  is_active BOOLEAN DEFAULT true,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Pincodes Master (if not using existing public.pincodes)
CREATE TABLE IF NOT EXISTS wowtruck.pincodes (
  id SERIAL PRIMARY KEY,
  pincode VARCHAR(10) NOT NULL,
  office_name VARCHAR(200),
  office_type VARCHAR(20),
  delivery VARCHAR(20),
  division_name VARCHAR(100),
  region_name VARCHAR(100),
  circle_name VARCHAR(100),
  district VARCHAR(100),
  state VARCHAR(100),
  latitude VARCHAR(20),
  longitude VARCHAR(20),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 4. PORTAL FEATURE TABLES (in public schema for Prisma compatibility)
-- ═══════════════════════════════════════════════════════════════════════════════

-- Transporter/Driver Ratings (by customers)
CREATE TABLE IF NOT EXISTS "TransporterRating" (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "tripId" UUID NOT NULL,
  "customerId" UUID,
  "transporterId" UUID,
  "driverId" UUID,
  rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
  punctuality INT CHECK (punctuality >= 1 AND punctuality <= 5),
  communication INT CHECK (communication >= 1 AND communication <= 5),
  "cargoCondition" INT CHECK ("cargoCondition" >= 1 AND "cargoCondition" <= 5),
  tags TEXT[], -- array of tags
  review TEXT,
  response TEXT,
  "createdAt" TIMESTAMPTZ DEFAULT NOW()
);

-- Customer Ratings (by transporters)
CREATE TABLE IF NOT EXISTS "CustomerRating" (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "tripId" UUID NOT NULL,
  "customerId" UUID,
  "ratedById" UUID,
  rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
  "paymentTimeliness" INT CHECK ("paymentTimeliness" >= 1 AND "paymentTimeliness" <= 5),
  communication INT CHECK (communication >= 1 AND communication <= 5),
  tags TEXT[],
  review TEXT,
  "createdAt" TIMESTAMPTZ DEFAULT NOW()
);

-- Electronic Proof of Delivery
CREATE TABLE IF NOT EXISTS "EPOD" (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "tripId" UUID NOT NULL,
  "photoType" VARCHAR(50) NOT NULL, -- front, back, left, right, cargo, signature, odometer
  "photoUrl" TEXT NOT NULL,
  latitude DECIMAL(10,7),
  longitude DECIMAL(10,7),
  accuracy DECIMAL(8,2),
  "uploadedBy" UUID,
  "uploadedAt" TIMESTAMPTZ DEFAULT NOW(),
  verified BOOLEAN DEFAULT false,
  "verifiedBy" UUID,
  "verifiedAt" TIMESTAMPTZ,
  "rejectionReason" TEXT
);

-- Vendor/Transporter Settlements
CREATE TABLE IF NOT EXISTS "Settlement" (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "vendorId" UUID NOT NULL,
  "settlementCode" VARCHAR(50) UNIQUE,
  "periodStart" DATE NOT NULL,
  "periodEnd" DATE NOT NULL,
  "tripCount" INT DEFAULT 0,
  "grossAmount" DECIMAL(14,2) DEFAULT 0,
  commission DECIMAL(14,2) DEFAULT 0,
  deductions DECIMAL(14,2) DEFAULT 0,
  tds DECIMAL(14,2) DEFAULT 0,
  "netAmount" DECIMAL(14,2) DEFAULT 0,
  status VARCHAR(20) DEFAULT 'pending', -- pending, approved, processing, paid, disputed
  "approvedBy" UUID,
  "approvedAt" TIMESTAMPTZ,
  "paymentMode" VARCHAR(50),
  "paymentRef" VARCHAR(100),
  "paidAt" TIMESTAMPTZ,
  notes TEXT,
  "createdAt" TIMESTAMPTZ DEFAULT NOW(),
  "updatedAt" TIMESTAMPTZ DEFAULT NOW()
);

-- Approval Requests (for invoices, expenses, etc.)
CREATE TABLE IF NOT EXISTS "ApprovalRequest" (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "entityType" VARCHAR(50) NOT NULL, -- invoice, expense, credit_note, refund
  "entityId" UUID NOT NULL,
  "requestedBy" UUID,
  "requestedAt" TIMESTAMPTZ DEFAULT NOW(),
  status VARCHAR(20) DEFAULT 'pending', -- pending, approved, rejected
  priority VARCHAR(20) DEFAULT 'normal', -- low, normal, high, urgent
  amount DECIMAL(14,2),
  description TEXT,
  "approvedBy" UUID,
  "approvedAt" TIMESTAMPTZ,
  "rejectedBy" UUID,
  "rejectionReason" TEXT,
  notes TEXT,
  "createdAt" TIMESTAMPTZ DEFAULT NOW(),
  "updatedAt" TIMESTAMPTZ DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 5. INDEXES
-- ═══════════════════════════════════════════════════════════════════════════════

-- Freight Exchange indexes
CREATE INDEX IF NOT EXISTS idx_freight_loads_status ON freight.load_postings(status);
CREATE INDEX IF NOT EXISTS idx_freight_loads_origin ON freight.load_postings(origin_city);
CREATE INDEX IF NOT EXISTS idx_freight_loads_dest ON freight.load_postings(dest_city);
CREATE INDEX IF NOT EXISTS idx_freight_loads_date ON freight.load_postings(pickup_date);
CREATE INDEX IF NOT EXISTS idx_freight_trucks_status ON freight.truck_postings(status);
CREATE INDEX IF NOT EXISTS idx_freight_trucks_city ON freight.truck_postings(current_city);
CREATE INDEX IF NOT EXISTS idx_freight_bids_load ON freight.bids(load_id);
CREATE INDEX IF NOT EXISTS idx_freight_bids_carrier ON freight.bids(carrier_id);
CREATE INDEX IF NOT EXISTS idx_freight_bids_status ON freight.bids(status);
CREATE INDEX IF NOT EXISTS idx_freight_surge_route ON freight.surge_pricing(origin_city, dest_city);

-- MRF indexes
CREATE INDEX IF NOT EXISTS idx_mrf_lanes_route ON wowtruck.mrf_lanes(source, destination);
CREATE INDEX IF NOT EXISTS idx_mrf_lanes_zip ON wowtruck.mrf_lanes(source_zip, destination_zip);
CREATE INDEX IF NOT EXISTS idx_mrf_lanes_truck ON wowtruck.mrf_lanes(truck_type);
CREATE INDEX IF NOT EXISTS idx_wowtruck_pincodes_pin ON wowtruck.pincodes(pincode);
CREATE INDEX IF NOT EXISTS idx_wowtruck_pincodes_district ON wowtruck.pincodes(district);
CREATE INDEX IF NOT EXISTS idx_wowtruck_pincodes_state ON wowtruck.pincodes(state);

-- Portal indexes
CREATE INDEX IF NOT EXISTS idx_transporter_rating_trip ON "TransporterRating"("tripId");
CREATE INDEX IF NOT EXISTS idx_transporter_rating_driver ON "TransporterRating"("driverId");
CREATE INDEX IF NOT EXISTS idx_customer_rating_trip ON "CustomerRating"("tripId");
CREATE INDEX IF NOT EXISTS idx_epod_trip ON "EPOD"("tripId");
CREATE INDEX IF NOT EXISTS idx_settlement_vendor ON "Settlement"("vendorId");
CREATE INDEX IF NOT EXISTS idx_settlement_status ON "Settlement"(status);
CREATE INDEX IF NOT EXISTS idx_approval_status ON "ApprovalRequest"(status);
CREATE INDEX IF NOT EXISTS idx_approval_entity ON "ApprovalRequest"("entityType", "entityId");

-- ═══════════════════════════════════════════════════════════════════════════════
-- 6. SAMPLE DATA (Optional - uncomment to seed)
-- ═══════════════════════════════════════════════════════════════════════════════

-- Sample MRF Lanes (Mumbai routes)
INSERT INTO wowtruck.mrf_lanes (lane_name, source, source_zip, destination, destination_zip, truck_type, base_rate, distance_km, transit_days, per_km_rate, region, is_active)
VALUES
  ('Mumbai-Delhi', 'Mumbai', '400001', 'Delhi', '110001', '32FT_MXL', 85000, 1420, 2.5, 60, 'North', true),
  ('Mumbai-Bangalore', 'Mumbai', '400001', 'Bangalore', '560001', '32FT_MXL', 55000, 980, 2, 56, 'South', true),
  ('Mumbai-Chennai', 'Mumbai', '400001', 'Chennai', '600001', '32FT_MXL', 70000, 1340, 2.5, 52, 'South', true),
  ('Mumbai-Kolkata', 'Mumbai', '400001', 'Kolkata', '700001', '32FT_MXL', 95000, 1990, 3, 48, 'East', true),
  ('Mumbai-Ahmedabad', 'Mumbai', '400001', 'Ahmedabad', '380001', '32FT_MXL', 25000, 520, 1, 48, 'West', true),
  ('Delhi-Mumbai', 'Delhi', '110001', 'Mumbai', '400001', '32FT_MXL', 85000, 1420, 2.5, 60, 'West', true),
  ('Delhi-Bangalore', 'Delhi', '110001', 'Bangalore', '560001', '32FT_MXL', 115000, 2150, 3.5, 53, 'South', true),
  ('Chennai-Delhi', 'Chennai', '600001', 'Delhi', '110001', '32FT_MXL', 120000, 2200, 3.5, 54, 'North', true)
ON CONFLICT DO NOTHING;

-- Sample Carrier Profile
INSERT INTO freight.carrier_profiles (company_name, contact_person, phone, city, state, fleet_size, rating, status)
VALUES
  ('ABC Logistics Pvt Ltd', 'Ramesh Kumar', '+919876543210', 'Mumbai', 'Maharashtra', 25, 4.5, 'active'),
  ('Fast Track Transport', 'Suresh Sharma', '+919876543211', 'Delhi', 'Delhi', 15, 4.2, 'active'),
  ('Southern Express', 'Venkat Rao', '+919876543212', 'Chennai', 'Tamil Nadu', 30, 4.7, 'active')
ON CONFLICT DO NOTHING;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 7. GRANT PERMISSIONS
-- ═══════════════════════════════════════════════════════════════════════════════

GRANT ALL ON SCHEMA freight TO ankr;
GRANT ALL ON SCHEMA wowtruck TO ankr;
GRANT ALL ON ALL TABLES IN SCHEMA freight TO ankr;
GRANT ALL ON ALL TABLES IN SCHEMA wowtruck TO ankr;
GRANT ALL ON ALL SEQUENCES IN SCHEMA freight TO ankr;
GRANT ALL ON ALL SEQUENCES IN SCHEMA wowtruck TO ankr;

-- ═══════════════════════════════════════════════════════════════════════════════
-- DONE
-- ═══════════════════════════════════════════════════════════════════════════════

SELECT 'Migration complete! Created schemas: freight, wowtruck' AS status;
SELECT 'Tables created in freight schema:' AS info;
SELECT tablename FROM pg_tables WHERE schemaname = 'freight' ORDER BY tablename;
SELECT 'Tables created in public schema for portals:' AS info;
SELECT tablename FROM pg_tables WHERE tablename IN ('TransporterRating', 'CustomerRating', 'EPOD', 'Settlement', 'ApprovalRequest');
