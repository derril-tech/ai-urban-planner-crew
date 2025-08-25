# Created automatically by Cursor AI (2025-08-25)
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const chaosErrorRate = new Rate('chaos_errors');
const recoveryRate = new Rate('recovery_success');

// Test configuration
export const options = {
  stages: [
    { duration: '1m', target: 5 },  // Ramp up
    { duration: '3m', target: 5 },  // Chaos testing
    { duration: '1m', target: 0 },  // Ramp down
  ],
  thresholds: {
    chaos_errors: ['rate<0.3'],     // Allow up to 30% chaos errors
    recovery_success: ['rate>0.7'], // At least 70% recovery success
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';

// Malformed GeoJSON examples
const malformedGeoJSONs = [
  // Invalid geometry
  {
    type: 'FeatureCollection',
    features: [{
      type: 'Feature',
      properties: { name: 'Invalid Geometry' },
      geometry: {
        type: 'Polygon',
        coordinates: [[[0, 0], [1, 1]]] // Not closed
      }
    }]
  },
  // Self-intersecting polygon
  {
    type: 'FeatureCollection',
    features: [{
      type: 'Feature',
      properties: { name: 'Self-Intersecting' },
      geometry: {
        type: 'Polygon',
        coordinates: [[[0, 0], [2, 2], [0, 2], [2, 0], [0, 0]]]
      }
    }]
  },
  // Huge polygon (should cause performance issues)
  {
    type: 'FeatureCollection',
    features: [{
      type: 'Feature',
      properties: { name: 'Huge Polygon' },
      geometry: {
        type: 'Polygon',
        coordinates: [Array.from({ length: 10000 }, (_, i) => [i * 0.0001, i * 0.0001])]
      }
    }]
  },
  // Invalid JSON structure
  '{"invalid": "json", "missing": "features"}',
  // Empty feature collection
  { type: 'FeatureCollection', features: [] },
  // Null geometry
  {
    type: 'FeatureCollection',
    features: [{
      type: 'Feature',
      properties: { name: 'Null Geometry' },
      geometry: null
    }]
  }
];

// Intersecting layers data
const intersectingLayers = [
  {
    name: 'Layer 1',
    geometry: {
      type: 'Polygon',
      coordinates: [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
    }
  },
  {
    name: 'Layer 2',
    geometry: {
      type: 'Polygon',
      coordinates: [[[0.5, 0.5], [1.5, 0.5], [1.5, 1.5], [0.5, 1.5], [0.5, 0.5]]]
    }
  }
];

// Network with holes
const networkWithHoles = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      properties: { name: 'Main Street' },
      geometry: {
        type: 'LineString',
        coordinates: [[0, 0], [1, 0], [2, 0]]
      }
    },
    {
      type: 'Feature',
      properties: { name: 'Side Street' },
      geometry: {
        type: 'LineString',
        coordinates: [[1, 0], [1, 1]]
      }
    }
    // Missing connecting streets to create holes
  ]
};

export default function() {
  const testType = Math.floor(Math.random() * 6);
  
  switch (testType) {
    case 0:
      testMalformedGeoJSON();
      break;
    case 1:
      testHugePolygons();
      break;
    case 2:
      testIntersectingLayers();
      break;
    case 3:
      testNetworkHoles();
      break;
    case 4:
      testInvalidParameters();
      break;
    case 5:
      testRecoveryScenarios();
      break;
  }
  
  sleep(Math.random() * 2 + 1);
}

function testMalformedGeoJSON() {
  const malformedData = malformedGeoJSONs[Math.floor(Math.random() * malformedGeoJSONs.length)];
  
  const response = http.post(`${BASE_URL}/api/sites`, JSON.stringify({
    name: 'Chaos Test Site',
    area: '1.0',
    boundary: malformedData
  }), {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer test-token'
    }
  });
  
  check(response, {
    'malformed GeoJSON handled gracefully': (r) => {
      // Should either return 400 (bad request) or handle gracefully
      return r.status === 400 || r.status === 422 || (r.status === 201 && r.json('validation_errors'));
    },
    'malformed GeoJSON response time reasonable': (r) => r.timings.duration < 10000,
  }) || chaosErrorRate.add(1);
}

function testHugePolygons() {
  // Create a polygon with many vertices
  const hugePolygon = {
    type: 'FeatureCollection',
    features: [{
      type: 'Feature',
      properties: { name: 'Huge Test Polygon' },
      geometry: {
        type: 'Polygon',
        coordinates: [Array.from({ length: 5000 }, (_, i) => [
          -122.4194 + (i * 0.0001),
          37.7749 + (i * 0.0001)
        ])]
      }
    }]
  };
  
  const response = http.post(`${BASE_URL}/api/sites`, JSON.stringify({
    name: 'Huge Polygon Test',
    area: '50.0',
    boundary: hugePolygon
  }), {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer test-token'
    }
  });
  
  check(response, {
    'huge polygon handled with timeout or success': (r) => {
      return r.status === 201 || r.status === 408 || r.status === 413;
    },
    'huge polygon processing time reasonable': (r) => r.timings.duration < 30000,
  }) || chaosErrorRate.add(1);
}

function testIntersectingLayers() {
  // Test uploading multiple intersecting layers
  const response = http.post(`${BASE_URL}/api/sites`, JSON.stringify({
    name: 'Intersecting Layers Test',
    area: '2.0',
    boundary: intersectingLayers[0],
    additionalLayers: intersectingLayers.slice(1)
  }), {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer test-token'
    }
  });
  
  if (response.status === 201) {
    const siteId = response.json('id');
    
    // Try to run parcelization on intersecting layers
    const parcelizationResponse = http.post(`${BASE_URL}/api/sites/${siteId}/parcelize`, JSON.stringify({
      strategy: 'grid',
      parcelSize: 0.1,
      streetWidth: 20,
      handleIntersections: true
    }), {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token'
      }
    });
    
    check(parcelizationResponse, {
      'intersecting layers handled gracefully': (r) => {
        return r.status === 200 || r.status === 422 || r.status === 409;
      },
    }) || chaosErrorRate.add(1);
  }
}

function testNetworkHoles() {
  const response = http.post(`${BASE_URL}/api/sites`, JSON.stringify({
    name: 'Network Holes Test',
    area: '1.5',
    boundary: {
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        properties: { name: 'Test Site' },
        geometry: {
          type: 'Polygon',
          coordinates: [[[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]]
        }
      }]
    },
    network: networkWithHoles
  }), {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer test-token'
    }
  });
  
  if (response.status === 201) {
    const siteId = response.json('id');
    
    // Try to run network analysis on network with holes
    const networkResponse = http.post(`${BASE_URL}/api/sites/${siteId}/network-analysis`, JSON.stringify({
      analysisType: 'connectivity',
      includeWalkability: true,
      handleDisconnected: true
    }), {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token'
      }
    });
    
    check(networkResponse, {
      'network holes handled gracefully': (r) => {
        return r.status === 200 || r.status === 422;
      },
    }) || chaosErrorRate.add(1);
  }
}

function testInvalidParameters() {
  // Test with invalid parameters
  const invalidParams = [
    { parcelSize: -1, streetWidth: 20 },
    { parcelSize: 0.1, streetWidth: -5 },
    { residentialPercentage: 150, commercialPercentage: 50 },
    { far: 'invalid', buildingHeight: 'not_a_number' },
    { iterations: 0, objectives: [] },
    { includeSolar: 'yes', climateZone: 999 }
  ];
  
  const invalidParam = invalidParams[Math.floor(Math.random() * invalidParams.length)];
  
  // Create a valid site first
  const createResponse = http.post(`${BASE_URL}/api/sites`, JSON.stringify({
    name: 'Invalid Params Test',
    area: '1.0',
    boundary: {
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        properties: { name: 'Test Site' },
        geometry: {
          type: 'Polygon',
          coordinates: [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
        }
      }]
    }
  }), {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer test-token'
    }
  });
  
  if (createResponse.status === 201) {
    const siteId = createResponse.json('id');
    
    // Try different operations with invalid parameters
    const operations = [
      { endpoint: 'parcelize', data: invalidParam },
      { endpoint: 'zoning', data: invalidParam },
      { endpoint: 'optimize', data: invalidParam }
    ];
    
    const operation = operations[Math.floor(Math.random() * operations.length)];
    
    const response = http.post(`${BASE_URL}/api/sites/${siteId}/${operation.endpoint}`, JSON.stringify(operation.data), {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token'
      }
    });
    
    check(response, {
      'invalid parameters handled gracefully': (r) => {
        return r.status === 400 || r.status === 422;
      },
    }) || chaosErrorRate.add(1);
  }
}

function testRecoveryScenarios() {
  // Test system recovery after errors
  const validSite = {
    name: 'Recovery Test Site',
    area: '1.0',
    boundary: {
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        properties: { name: 'Valid Site' },
        geometry: {
          type: 'Polygon',
          coordinates: [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
        }
      }]
    }
  };
  
  // First, try with invalid data
  const invalidResponse = http.post(`${BASE_URL}/api/sites`, JSON.stringify({
    ...validSite,
    boundary: malformedGeoJSONs[0]
  }), {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer test-token'
    }
  });
  
  // Then try with valid data
  const validResponse = http.post(`${BASE_URL}/api/sites`, JSON.stringify(validSite), {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer test-token'
    }
  });
  
  check(validResponse, {
    'system recovers after invalid data': (r) => r.status === 201,
    'recovery response time reasonable': (r) => r.timings.duration < 5000,
  }) && recoveryRate.add(1);
}

export function setup() {
  console.log('Starting chaos testing for AI Urban Planner Crew');
  console.log(`Base URL: ${BASE_URL}`);
  console.log('Testing malformed data, huge polygons, intersecting layers, network holes, and recovery scenarios');
}

export function teardown(data) {
  console.log('Chaos testing completed');
  console.log(`Chaos error rate: ${data.metrics.chaos_errors.values.rate}`);
  console.log(`Recovery success rate: ${data.metrics.recovery_success.values.rate}`);
}
