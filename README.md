# AI Urban Planner Crew

> Multi-agent planning studio that turns briefs into fully specified concept plans with zoning, mobility, utilities, and more.

## Overview

AI Urban Planner Crew is a comprehensive urban planning platform that uses CrewAI multi-agent orchestration to transform planning briefs into detailed concept plans. The system generates zoning plans, mobility networks, utility systems, sustainability scores, and exportable CAD/GIS/CSV/PDF bundles.

## Architecture

- **Frontend**: Next.js 14 with MapLibre GL for interactive maps
- **API Gateway**: NestJS with OpenAPI 3.1, RBAC, and rate limiting
- **Orchestrator**: FastAPI with CrewAI agents (Architect, City Planner, Sustainability Expert, Economist, Citizen Advocate)
- **Workers**: Python services for GIS processing, modeling, and optimization
- **Infrastructure**: Postgres+PostGIS, Redis, NATS, MinIO

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-urban-planner-crew
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start infrastructure**
   ```bash
   npm run docker:up
   ```

4. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Start development servers**
   ```bash
   npm run dev
   ```

### Services

- **Frontend**: http://localhost:3000
- **API Gateway**: http://localhost:3001
- **Orchestrator**: http://localhost:8000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **NATS**: localhost:4222
- **MinIO**: http://localhost:9000

## Development

### Project Structure

```
ai-urban-planner-crew/
├── apps/
│   ├── frontend/          # Next.js 14 frontend
│   ├── gateway/           # NestJS API gateway
│   ├── orchestrator/      # FastAPI + CrewAI
│   └── workers/           # Python workers
├── packages/
│   └── sdk/              # Shared TypeScript SDK
├── docker-compose.dev.yml # Development infrastructure
└── package.json          # Monorepo configuration
```

### Available Scripts

- `npm run dev` - Start all development servers
- `npm run build` - Build all packages
- `npm run lint` - Lint all packages
- `npm run test` - Run tests
- `npm run docker:up` - Start infrastructure
- `npm run docker:down` - Stop infrastructure

## Features

### Core Capabilities

- **Site Intake**: Boundary drawing/upload, context layers, constraints
- **Zoning Editor**: Parcel-level zoning with use mix, FAR, heights, setbacks
- **Network Design**: Street hierarchy, transit priority, bike/ped infrastructure
- **Utility Planning**: Solar siting, water systems, waste management
- **Analytics**: Population/jobs allocation, 15-minute access, sustainability scoring
- **Optimization**: Trade-off exploration, Pareto frontier analysis
- **Export**: PDF reports, GeoPackage, DXF, CSV data

### AI Agents

- **Architect**: Massing logic, ground-floor activation, parcel patterns
- **City Planner**: Zoning compliance, density optimization, policy alignment
- **Sustainability Expert**: Green infrastructure, energy systems, resilience
- **Economist**: Cost analysis, financing, ROI calculations
- **Citizen Advocate**: Accessibility, equity, community needs

## API Documentation

- **Gateway API**: http://localhost:3001/api (Swagger)
- **Orchestrator API**: http://localhost:8000/docs (FastAPI docs)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

[License information]

## Support

For questions and support, please [create an issue](link-to-issues).
