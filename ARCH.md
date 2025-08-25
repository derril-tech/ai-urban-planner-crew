# Architecture — AI URBAN PLANNER CREW

## Topology
- **Frontend**: Next.js 14 (App Router, TS). MapLibre GL for maps, @turf in web workers. UI: shadcn + Tailwind. Data: TanStack Query; Zustand for canvas/optimizer state. Realtime: WS + SSE fallback.
- **API Gateway**: NestJS (REST; OpenAPI 3.1; Zod/AJV validation; RBAC; rate limits; Idempotency‑Key; Problem+JSON). Signed S3/R2 URLs.
- **Auth**: Auth.js (OAuth/passwordless) + short‑lived JWT; SAML/OIDC, SCIM optional.
- **Orchestrator**: FastAPI + CrewAI agents — **Architect, City Planner, Sustainability Expert, Economist, Citizen Advocate**.
- **Workers (Python)**: `gis-ingest`, `parcelizer`, `network-analyzer`, `mobility-model`, `energy-model`, `water-model`, `waste-model`, `budget-model`, `sustainability-score`, `optimizer`, `reporter`, `exporter`.
- **Infra**: Postgres + **PostGIS** (+ Timescale optional) + **pgvector**; Redis cache; NATS bus; Celery queues; S3/R2; OTel + Prometheus/Grafana + Sentry; secrets via KMS/Vault.

## Data Model (high level)
- **Tenancy**: `orgs`, `users`, `memberships` (Owner/Admin/Planner/Designer/Analyst/Facilitator/Viewer).
- **Plans/Scenarios**: `plans`, `scenarios`.
- **GIS**: `site_boundary`, `context_layers`, `parcels`, `links`, `open_space`, `energy_assets`, `water_assets`, `waste_assets` (GIST indexes, SRID 4326).
- **KPIs & Costing**: `kpis`, `unit_costs`, `qto`, `budget`, `phases`.
- **Personas**: `personas` (vector embeddings for retrieval).
- **Collab & Exports**: `comments`, `exports`, `audit_log`.

## API Surface (v1 highlights)
- **Auth/Orgs**: `POST /auth/login`, `POST /auth/refresh`, `GET /me`.
- **Plans/Scenarios**: `POST /plans`, `POST /plans/:id/scenarios`, `GET /scenarios/:id`.
- **GIS**: `POST /scenarios/:id/site`, `/context`, `/parcelize`, `/parcels`, `/links`, `/open-space`, `/assets/:domain`.
- **Models**: `POST /scenarios/:id/mobility/run`, `/energy/run`, `/water/run`, `/waste/run`, `/budget/run`, `/score/run`, `/optimize`.
- **KPIs & QTO**: `GET /scenarios/:id/kpis`, `/qto`.
- **Collab**: `POST /comments`, `GET /comments`.
- **Exports**: `POST /scenarios/:id/export`, `GET /exports/:id`.
**Conventions:** all mutations require **Idempotency‑Key**; Problem+JSON errors; cursor pagination; strict RLS.

## Agent Tool Contracts (strict JSON)
- `GIS.import(file|geojson)` → `{boundary, parcels?, roads?, water?, slope?}`
- `Parcel.plan(boundary, densityGoals, constraints)` → `{parcels[], defaults}`
- `Network.design(boundary, typologyParams)` → `{links[], classes}`
- `Mobility.estimate(graph, landUse, policies)` → `{VMT, modeShare, accessIndex, blockStats}`
- `Energy.simulate(parcels, massing, pvParams, storageParams)` → `{kWp, kWhYr, storage, selfSuffPct}`
- `Water.simulate(landCover, demandParams, BMPs)` → `{demand, runoff, reusePct}`
- `Waste.simulate(pop, landUse, diversionParams)` → `{diversionPct, routeLenKm}`
- `Budget.compute(qto, unitCosts, financeMix)` → `{CAPEX, OPEX, perHH, breakdown[]}`
- `Score.compute(kpis, weights)` → `{categories:{...}, composite}`
- `Optimize.search(paramRanges, objectives, constraints)` → `{paretoPoints[]}`
- `Report.render(planId)` / `Export.bundle(planId, targets[])` → `{links[]}`

## Deterministic Heuristics
- **Capacity**: units = parcel_area × FAR / avg_unit_floor_area × efficiency; population = units × occupancy; jobs via non‑res FAR × job density by use.
- **15‑minute access**: network distance (walk speed 1.2–1.4 m/s) to amenities; score = % of population within threshold by amenity class.
- **Mobility**: VMT = trip_rate × trip_length × (1 − non‑auto_share); mode share via parking ratio & street/bike quality elasticities.
- **Energy**: PV kWp = eligible_roof_area × panel_density; kWh/y via site irradiance factor; storage adequacy by peak‑to‑avg ratio.
- **Water**: demand = (res+nonres per‑capita) − reuse; runoff via SCS curve‑number proxy with BMP deltas.
- **Sustainability score**: weights sum to 1; normalize KPIs to 0–100 per category (energy, water, mobility, land‑use mix, inclusion, resilience, biodiversity/heat).

## Realtime Channels
- `scenario:{id}:gis` (ingest/parcelize progress)
- `scenario:{id}:models` (domain ticks, KPI deltas)
- `scenario:{id}:opt` (Pareto points stream)
- `scenario:{id}:export` (artifact status)
Presence + layer locks to prevent conflicting edits.

## Security & Compliance
RBAC; Postgres RLS; signed S3 URLs; SRID checks & geometry validation on write; PII‑light by design; immutable audit for edits/runs/exports; retention policies for uploads/exports. Supply chain hardening (SLSA, pinned deps, image signing).

## Deployment & SLOs
FE: Vercel. APIs/Workers: Render/Fly → GKE at scale (CPU pool for GIS/models, memory pool for exports, burst for optimizer).  
DB: Managed Postgres + PostGIS (+ pgvector). Cache: Upstash Redis. Bus: NATS.  
**SLOs** (1–3 km² sites): parcelize < **3 s P95**; single domain < **5 s P95**; full recompute < **15 s P95**; optimizer first 10 points < **12 s P95**; report < **20 s P95**; 5xx < **0.5%/1k**.
