# Project Plan — AI URBAN PLANNER CREW

> Scope: Turn a brief (e.g., “Eco‑friendly neighborhood for 5,000 residents”) into a concept plan with **zoning, mobility, utilities & resilience, green‑blue network, CAPEX/OPEX & phasing, sustainability score, and citizen journeys**, delivered as **interactive maps + CAD/GIS/CSV/PDF**.

## Product Goal
Enable planners and master‑planning teams to author, simulate, and iterate site‑scale scenarios rapidly with transparent assumptions, explainable KPIs, and exportable data packages suitable for downstream CAD/GIS and stakeholder workshops.

## Safety & Policy Stance
- **Concept plan only** — not an engineering drawing, permit set, or legal/zoning advice.
- User‑provided overlays/regulations are optional; templates are jurisdiction‑agnostic.
- Redact/avoid PII in uploads. Clear disclaimers in app and exports.

## 80/20 Build Strategy
- **80% deterministic/code:** parcelization, capacity math, access indices, mobility/energy/water/waste heuristics, budget & QTO, score normalization, GIS validity.
- **20% generative/agents:** massing defaults, policy suggestions, persona narratives, report copy — all bounded by strict JSON tool contracts and guardrails.

## Immediate Next 3 Tasks
1) **Infra**: monorepo scaffold; `docker-compose.dev` (Postgres+PostGIS, Redis, NATS, MinIO); CI (lint/test/build; SBOM & signing); `.env.example`.
2) **Contracts**: NestJS gateway with OpenAPI 3.1, RBAC, Idempotency‑Key, Problem+JSON; signed upload URLs; WS channels.
3) **GIS core**: `gis-ingest` (GeoJSON/Shapefile→PostGIS + topology fix) and `parcelizer` MVP; MapLibre canvas with draw/edit.

## Phases
- **P0** Repo/infra/CI + typed contracts  
- **P1** DB schema + PostGIS + RLS  
- **P2** Site ingest, parcelizer, base grid proposal  
- **P3** Zoning editor + capacity calculator  
- **P4** Network editor + mobility sketch KPIs  
- **P5** Utilities (energy/water/waste) siting + models  
- **P6** Budget/QTO + sustainability score  
- **P7** Trade‑offs & Pareto optimizer  
- **P8** Personas & 15‑minute journeys  
- **P9** Reports & export bundles, observability, hardening

## Definition of Done (MVP)
- Upload/draw boundary → valid topology; optional context layers.
- Parcel fabric present; editable zoning attributes (use mix, FAR, height, setbacks, inclusionary, phase).
- Network authoring (classes, lanes, speeds, transit/bike flags) with live **block length** and **intersection density**.
- Models: **population/jobs allocation**, **15‑minute access**, **mobility sketch (VMT/mode share)**, **energy (PV/storage)**, **water (demand/runoff/reuse)**, **waste (diversion)**.
- Budget from QTO × unit costs; sustainability composite score with category breakdown.
- Trade‑off sliders with live recompute + tornado; Pareto set for (Score↑, CAPEX↓).
- Persona journeys (map overlays + narrative) and barriers list.
- Exports: **PDF report**, **GeoPackage/GeoJSON**, **DXF**, **CSV/JSON**; read‑only share link.
- **SLOs:** parcelize < **3 s P95**; single domain model < **5 s P95**; full recompute < **15 s P95**; first 10 Pareto pts < **12 s P95**; export < **20 s P95**.

## Non‑Goals (MVP)
- No external regulatory databases by default (users may upload).
- No detailed traffic assignment or CFD/energy simulation; sketch models only.
- No live tile hosting dependency; ship with in‑app basemap.

## Key Risks & Mitigations
- **Geometry validity:** always validate & auto‑repair (buffer/clean) before writes; block exports on invalid geometries with fix‑ups.
- **Black‑box skepticism:** show formulas/assumptions; expose sliders and QTO; audit log every model run.
- **Performance on large sites:** tile slicing, batched edits, server‑side geo ops; cache KPIs and QTO.

## KPIs (first 90 days)
- **Time‑to‑viable plan** (meets pop/jobs target & constraints) ≤ **30 min** median.
- **Sustainability score** improves **≥ +20%** vs baseline within 3 iterations.
- **Trade‑off usage** in ≥ **70%** sessions.
- **Export reliability** ≥ **99%**; geometry validity errors < **1%** of edits.
