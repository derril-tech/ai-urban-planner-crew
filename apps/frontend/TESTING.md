# Testing Documentation - AI Urban Planner Crew

## Overview

This document outlines the comprehensive testing strategy for the AI Urban Planner Crew application, covering E2E testing, load testing, chaos testing, and security testing.

## Test Types

### 1. E2E Testing (Playwright)

**Purpose**: End-to-end testing of the complete urban planning workflow from site intake to export.

**Coverage**:
- Complete workflow: intake → parcelize → zoning → network → models → optimize → export
- Error handling and edge cases
- Performance and responsiveness
- Cross-browser compatibility

**Files**:
- `playwright.config.ts` - Test configuration
- `tests/e2e/urban-planner-workflow.spec.ts` - Main workflow tests
- `tests/fixtures/` - Test data files

**Commands**:
```bash
# Run all E2E tests
npm run test:e2e

# Run with UI
npm run test:e2e:ui

# Run in headed mode
npm run test:e2e:headed

# Install browsers
npm run test:install

# Show test report
npm run test:report
```

**Test Scenarios**:
1. **Site Intake**: Upload site boundary, set parameters
2. **Parcelization**: Grid/irregular strategies, parameter validation
3. **Zoning & Capacity**: Land use mix, development parameters
4. **Network Analysis**: Connectivity, walkability assessment
5. **Energy & Utilities**: Solar potential, water demand
6. **Budget & Sustainability**: Cost calculation, scoring
7. **Optimization**: Multi-objective optimization, Pareto frontier
8. **Personas & Journeys**: Citizen personas, barrier detection
9. **Reports & Export**: PDF generation, data export
10. **Error Handling**: Invalid data, network timeouts
11. **Performance**: Large sites, concurrent operations

### 2. Load Testing (k6)

**Purpose**: Performance testing under various load conditions.

**Coverage**:
- Concurrent model runs and map edits
- Optimizer bursts
- API endpoint performance
- Database connection handling
- Resource utilization

**Files**:
- `k6-load-test.js` - Main load test script

**Commands**:
```bash
# Run load tests
npm run test:load

# Run with custom base URL
BASE_URL=http://localhost:3000 k6 run k6-load-test.js
```

**Test Stages**:
1. **Ramp Up**: 0 → 10 users (2 minutes)
2. **Sustained Load**: 10 users (5 minutes)
3. **Peak Load**: 10 → 20 users (2 minutes)
4. **High Load**: 20 users (5 minutes)
5. **Ramp Down**: 20 → 0 users (2 minutes)

**Thresholds**:
- 95% of requests must complete below 2 seconds
- Error rate must be below 10%
- Custom error rate must be below 10%

### 3. Chaos Testing (k6)

**Purpose**: Testing system resilience with malformed data and edge cases.

**Coverage**:
- Malformed GeoJSON handling
- Huge polygons and performance issues
- Intersecting layers
- Network holes and connectivity issues
- Invalid parameters
- System recovery scenarios

**Files**:
- `tests/chaos/chaos-test.js` - Chaos testing script

**Commands**:
```bash
# Run chaos tests
npm run test:chaos
```

**Test Scenarios**:
1. **Malformed GeoJSON**: Invalid geometry, self-intersecting polygons
2. **Huge Polygons**: Performance testing with large datasets
3. **Intersecting Layers**: Multiple overlapping geometries
4. **Network Holes**: Disconnected network segments
5. **Invalid Parameters**: Negative values, invalid types
6. **Recovery Scenarios**: System recovery after errors

**Thresholds**:
- Allow up to 30% chaos errors
- At least 70% recovery success

### 4. Security Testing (k6)

**Purpose**: Testing for common security vulnerabilities.

**Coverage**:
- SQL injection prevention
- XSS protection
- Path traversal attacks
- Command injection
- Authentication bypass
- Authorization controls
- Input validation
- Object store scope

**Files**:
- `tests/security/security-test.js` - Security testing script

**Commands**:
```bash
# Run security tests
npm run test:security
```

**Test Scenarios**:
1. **SQL Injection**: Various SQL injection payloads
2. **XSS**: Cross-site scripting attacks
3. **Path Traversal**: Directory traversal attempts
4. **Command Injection**: Shell command injection
5. **Authentication**: Token validation, expired tokens
6. **Authorization**: Role-based access control
7. **Input Validation**: Large inputs, malformed data
8. **Object Store**: File access scope enforcement

**Thresholds**:
- Should have very few security vulnerabilities (< 10%)
- Authentication failures should be low (< 20%)

## Test Data

### Fixtures

Located in `tests/fixtures/`:

- `sample-site-boundary.geojson` - Standard test site
- `large-site-boundary.geojson` - Performance testing site
- `invalid-boundary.txt` - Error handling test

### Test Sites

The load testing uses three predefined test sites with different characteristics:

1. **Load Test Site 1**: 2.0 hectares, standard complexity
2. **Load Test Site 2**: 3.5 hectares, medium complexity
3. **Load Test Site 3**: 1.8 hectares, simple complexity

## Configuration

### Playwright Configuration

Key settings in `playwright.config.ts`:

- **Base URL**: `http://localhost:3000` (configurable via `PLAYWRIGHT_BASE_URL`)
- **Browsers**: Chrome, Firefox, Safari, Mobile Chrome, Mobile Safari
- **Parallel Execution**: Enabled
- **Retries**: 2 on CI, 0 locally
- **Reporting**: HTML, JSON, JUnit formats
- **Traces**: On first retry
- **Screenshots**: On failure
- **Videos**: Retain on failure

### k6 Configuration

Key settings in load test scripts:

- **Stages**: Ramp up, sustained load, peak load, ramp down
- **Thresholds**: Response time, error rate, custom metrics
- **Base URL**: Configurable via `BASE_URL` environment variable
- **Headers**: Authentication, content type
- **Sleep**: Random delays between requests

## Running Tests

### Prerequisites

1. Install dependencies:
```bash
npm install
```

2. Install Playwright browsers:
```bash
npm run test:install
```

3. Start the application:
```bash
npm run dev
```

### Test Execution

#### E2E Tests
```bash
# Run all E2E tests
npm run test:e2e

# Run specific test file
npx playwright test tests/e2e/urban-planner-workflow.spec.ts

# Run with specific browser
npx playwright test --project=chromium
```

#### Load Tests
```bash
# Run load tests
npm run test:load

# Run with custom parameters
k6 run --env BASE_URL=http://localhost:3000 k6-load-test.js
```

#### Chaos Tests
```bash
# Run chaos tests
npm run test:chaos

# Run with custom parameters
k6 run --env BASE_URL=http://localhost:3000 tests/chaos/chaos-test.js
```

#### Security Tests
```bash
# Run security tests
npm run test:security

# Run with custom parameters
k6 run --env BASE_URL=http://localhost:3000 tests/security/security-test.js
```

## Test Reports

### Playwright Reports

After running E2E tests, view the HTML report:
```bash
npm run test:report
```

The report includes:
- Test results and status
- Screenshots and videos
- Traces for failed tests
- Performance metrics
- Browser compatibility results

### k6 Reports

k6 generates console output with:
- Request metrics (count, rate, duration)
- Error rates and thresholds
- Custom metrics
- Performance statistics

For detailed analysis, k6 can output to various formats:
```bash
# JSON output
k6 run --out json=results.json k6-load-test.js

# InfluxDB output
k6 run --out influxdb=http://localhost:8086/k6 k6-load-test.js
```

## Continuous Integration

### GitHub Actions

The testing suite can be integrated into CI/CD pipelines:

```yaml
name: Test Suite
on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - run: npm run test:install
      - run: npm run test:e2e

  load:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: grafana/k6-action@v0.3.0
        with:
          filename: k6-load-test.js
          flags: --env BASE_URL=http://localhost:3000
```

### Test Environment

For CI/CD, ensure:
- Application is running and accessible
- Database is properly seeded
- External services are mocked or available
- Environment variables are set correctly

## Best Practices

### Test Data Management

1. **Isolation**: Each test should be independent
2. **Cleanup**: Clean up test data after tests
3. **Realistic Data**: Use realistic but manageable test data
4. **Variety**: Test with different data sizes and types

### Performance Testing

1. **Baseline**: Establish performance baselines
2. **Monitoring**: Monitor system resources during tests
3. **Gradual Increase**: Ramp up load gradually
4. **Recovery**: Test system recovery after load

### Security Testing

1. **Regular Scans**: Run security tests regularly
2. **Vulnerability Tracking**: Track and fix vulnerabilities
3. **Input Validation**: Test all input validation
4. **Access Control**: Verify authorization controls

### Error Handling

1. **Graceful Degradation**: Test system behavior under stress
2. **Error Messages**: Verify appropriate error messages
3. **Recovery**: Test system recovery after errors
4. **Logging**: Ensure proper error logging

## Troubleshooting

### Common Issues

1. **Timeout Errors**: Increase timeout values in configuration
2. **Browser Issues**: Reinstall Playwright browsers
3. **Network Errors**: Check application accessibility
4. **Resource Limits**: Adjust k6 resource limits

### Debugging

1. **Playwright Debug**: Use `--headed` or `--ui` flags
2. **k6 Debug**: Use `--verbose` flag for detailed output
3. **Logs**: Check application logs for errors
4. **Traces**: Use Playwright traces for failed tests

## Maintenance

### Regular Tasks

1. **Update Dependencies**: Keep testing libraries updated
2. **Review Tests**: Regularly review and update tests
3. **Performance Baselines**: Update performance baselines
4. **Security Scans**: Regular security vulnerability scans

### Test Maintenance

1. **Test Data**: Update test data as application evolves
2. **Selectors**: Update selectors when UI changes
3. **API Changes**: Update API tests when endpoints change
4. **Thresholds**: Adjust performance thresholds as needed
