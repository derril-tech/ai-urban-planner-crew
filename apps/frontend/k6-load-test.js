# Created automatically by Cursor AI (2025-08-25)
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

// Test configuration
export const options = {
  stages: [
    { duration: '2m', target: 10 }, // Ramp up to 10 users
    { duration: '5m', target: 10 }, // Stay at 10 users
    { duration: '2m', target: 20 }, // Ramp up to 20 users
    { duration: '5m', target: 20 }, // Stay at 20 users
    { duration: '2m', target: 0 },  // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'], // 95% of requests must complete below 2s
    http_req_failed: ['rate<0.1'],     // Error rate must be below 10%
    errors: ['rate<0.1'],              // Custom error rate must be below 10%
  },
};

// Base URL for the application
const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';

// Test data
const testSites = [
  {
    name: 'Load Test Site 1',
    area: '2.0',
    coordinates: [[-122.4194, 37.7749], [-122.4194, 37.7849], [-122.4094, 37.7849], [-122.4094, 37.7749], [-122.4194, 37.7749]]
  },
  {
    name: 'Load Test Site 2',
    area: '3.5',
    coordinates: [[-122.4294, 37.7649], [-122.4294, 37.7949], [-122.3994, 37.7949], [-122.3994, 37.7649], [-122.4294, 37.7649]]
  },
  {
    name: 'Load Test Site 3',
    area: '1.8',
    coordinates: [[-122.4394, 37.7549], [-122.4394, 37.7749], [-122.4194, 37.7749], [-122.4194, 37.7549], [-122.4394, 37.7549]]
  }
];

// Helper function to create GeoJSON
function createGeoJSON(site) {
  return {
    type: 'FeatureCollection',
    features: [{
      type: 'Feature',
      properties: {
        name: site.name,
        area_hectares: site.area
      },
      geometry: {
        type: 'Polygon',
        coordinates: [site.coordinates]
      }
    }]
  };
}

// Main test function
export default function() {
  const site = testSites[Math.floor(Math.random() * testSites.length)];
  const geoJSON = createGeoJSON(site);
  
  // Test 1: Site Creation
  const createSiteResponse = http.post(`${BASE_URL}/api/sites`, JSON.stringify({
    name: site.name,
    area: site.area,
    boundary: geoJSON
  }), {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer test-token'
    }
  });
  
  check(createSiteResponse, {
    'site creation status is 201': (r) => r.status === 201,
    'site creation response time < 2000ms': (r) => r.timings.duration < 2000,
  }) || errorRate.add(1);
  
  if (createSiteResponse.status === 201) {
    const siteId = createSiteResponse.json('id');
    
    // Test 2: Parcelization
    const parcelizationResponse = http.post(`${BASE_URL}/api/sites/${siteId}/parcelize`, JSON.stringify({
      strategy: 'grid',
      parcelSize: 0.1,
      streetWidth: 20
    }), {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token'
      }
    });
    
    check(parcelizationResponse, {
      'parcelization status is 200': (r) => r.status === 200,
      'parcelization response time < 30000ms': (r) => r.timings.duration < 30000,
    }) || errorRate.add(1);
    
    // Test 3: Zoning Application
    const zoningResponse = http.post(`${BASE_URL}/api/sites/${siteId}/zoning`, JSON.stringify({
      residentialPercentage: 60,
      commercialPercentage: 25,
      openSpacePercentage: 15,
      far: 2.5,
      buildingHeight: 8,
      setback: 3
    }), {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token'
      }
    });
    
    check(zoningResponse, {
      'zoning status is 200': (r) => r.status === 200,
      'zoning response time < 15000ms': (r) => r.timings.duration < 15000,
    }) || errorRate.add(1);
    
    // Test 4: Network Analysis
    const networkResponse = http.post(`${BASE_URL}/api/sites/${siteId}/network-analysis`, JSON.stringify({
      analysisType: 'connectivity',
      includeWalkability: true
    }), {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token'
      }
    });
    
    check(networkResponse, {
      'network analysis status is 200': (r) => r.status === 200,
      'network analysis response time < 20000ms': (r) => r.timings.duration < 20000,
    }) || errorRate.add(1);
    
    // Test 5: Energy Model
    const energyResponse = http.post(`${BASE_URL}/api/sites/${siteId}/energy-model`, JSON.stringify({
      includeSolar: true,
      includeStorage: true,
      climateZone: '3B'
    }), {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token'
      }
    });
    
    check(energyResponse, {
      'energy model status is 200': (r) => r.status === 200,
      'energy model response time < 25000ms': (r) => r.timings.duration < 25000,
    }) || errorRate.add(1);
    
    // Test 6: Budget Calculation
    const budgetResponse = http.post(`${BASE_URL}/api/sites/${siteId}/budget`, JSON.stringify({
      includeInfrastructure: true,
      includeBuildings: true,
      includeSustainability: true,
      location: 'San Francisco, CA'
    }), {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token'
      }
    });
    
    check(budgetResponse, {
      'budget calculation status is 200': (r) => r.status === 200,
      'budget calculation response time < 30000ms': (r) => r.timings.duration < 30000,
    }) || errorRate.add(1);
    
    // Test 7: Sustainability Scoring
    const sustainabilityResponse = http.post(`${BASE_URL}/api/sites/${siteId}/sustainability`, JSON.stringify({
      includeAllCategories: true,
      weightingScheme: 'balanced'
    }), {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token'
      }
    });
    
    check(sustainabilityResponse, {
      'sustainability scoring status is 200': (r) => r.status === 200,
      'sustainability scoring response time < 20000ms': (r) => r.timings.duration < 20000,
    }) || errorRate.add(1);
    
    // Test 8: Optimization (Heavy Load Test)
    const optimizationResponse = http.post(`${BASE_URL}/api/sites/${siteId}/optimize`, JSON.stringify({
      iterations: 25,
      objectives: ['sustainability', 'cost'],
      constraints: {
        minUnits: 100,
        maxCost: 50000000
      }
    }), {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token'
      }
    });
    
    check(optimizationResponse, {
      'optimization status is 200': (r) => r.status === 200,
      'optimization response time < 60000ms': (r) => r.timings.duration < 60000,
    }) || errorRate.add(1);
    
    // Test 9: Export Generation
    const exportResponse = http.post(`${BASE_URL}/api/sites/${siteId}/export`, JSON.stringify({
      formats: ['geojson', 'pdf'],
      theme: 'professional',
      includeMaps: true,
      includeCharts: true
    }), {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token'
      }
    });
    
    check(exportResponse, {
      'export generation status is 200': (r) => r.status === 200,
      'export generation response time < 45000ms': (r) => r.timings.duration < 45000,
    }) || errorRate.add(1);
  }
  
  // Random sleep between 1-3 seconds
  sleep(Math.random() * 2 + 1);
}

// Setup function (runs once at the beginning)
export function setup() {
  console.log('Starting load test for AI Urban Planner Crew');
  console.log(`Base URL: ${BASE_URL}`);
  console.log(`Test sites: ${testSites.length}`);
}

// Teardown function (runs once at the end)
export function teardown(data) {
  console.log('Load test completed');
  console.log(`Total requests: ${data.metrics.http_reqs.values.count}`);
  console.log(`Error rate: ${data.metrics.http_req_failed.values.rate}`);
}
