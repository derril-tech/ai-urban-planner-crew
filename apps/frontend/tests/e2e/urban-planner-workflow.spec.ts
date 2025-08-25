# Created automatically by Cursor AI (2025-08-25)
import { test, expect } from '@playwright/test';

test.describe('AI Urban Planner Crew - Complete Workflow', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the application
    await page.goto('/');
    
    // Wait for the application to load
    await page.waitForSelector('[data-testid="app-loaded"]', { timeout: 10000 });
  });

  test('Complete urban planning workflow: intake → parcelize → zoning → network → models → optimize → export', async ({ page }) => {
    const testData = {
      siteName: 'Test Development Site',
      siteArea: '2.5', // hectares
      targetUnits: '150',
      targetJobs: '75'
    };

    // Step 1: Site Intake
    await test.step('Site Intake', async () => {
      // Click on "New Project" or "Create Site"
      await page.click('[data-testid="new-project-btn"]');
      
      // Fill in site details
      await page.fill('[data-testid="site-name-input"]', testData.siteName);
      await page.fill('[data-testid="site-area-input"]', testData.siteArea);
      
      // Upload site boundary (GeoJSON)
      const fileInput = page.locator('[data-testid="site-boundary-upload"]');
      await fileInput.setInputFiles('tests/fixtures/sample-site-boundary.geojson');
      
      // Submit site creation
      await page.click('[data-testid="create-site-btn"]');
      
      // Verify site was created
      await expect(page.locator('[data-testid="site-created-success"]')).toBeVisible();
    });

    // Step 2: Parcelization
    await test.step('Parcelization', async () => {
      // Navigate to parcelization panel
      await page.click('[data-testid="parcelization-tab"]');
      
      // Select parcelization strategy
      await page.selectOption('[data-testid="parcelization-strategy"]', 'grid');
      
      // Set parcel parameters
      await page.fill('[data-testid="parcel-size-input"]', '0.1'); // hectares
      await page.fill('[data-testid="street-width-input"]', '20'); // meters
      
      // Run parcelization
      await page.click('[data-testid="run-parcelization-btn"]');
      
      // Wait for parcelization to complete
      await page.waitForSelector('[data-testid="parcelization-complete"]', { timeout: 30000 });
      
      // Verify parcels were created
      const parcelCount = await page.locator('[data-testid="parcel-count"]').textContent();
      expect(parseInt(parcelCount || '0')).toBeGreaterThan(0);
    });

    // Step 3: Zoning & Capacity
    await test.step('Zoning & Capacity', async () => {
      // Navigate to zoning panel
      await page.click('[data-testid="zoning-tab"]');
      
      // Set land use mix
      await page.fill('[data-testid="residential-percentage"]', '60');
      await page.fill('[data-testid="commercial-percentage"]', '25');
      await page.fill('[data-testid="open-space-percentage"]', '15');
      
      // Set development parameters
      await page.fill('[data-testid="far-input"]', '2.5');
      await page.fill('[data-testid="building-height-input"]', '8'); // stories
      await page.fill('[data-testid="setback-input"]', '3'); // meters
      
      // Apply zoning to parcels
      await page.click('[data-testid="apply-zoning-btn"]');
      
      // Wait for capacity calculation
      await page.waitForSelector('[data-testid="capacity-calculated"]', { timeout: 15000 });
      
      // Verify capacity results
      const totalUnits = await page.locator('[data-testid="total-units"]').textContent();
      const totalJobs = await page.locator('[data-testid="total-jobs"]').textContent();
      
      expect(parseInt(totalUnits || '0')).toBeGreaterThan(0);
      expect(parseInt(totalJobs || '0')).toBeGreaterThan(0);
    });

    // Step 4: Network Analysis
    await test.step('Network Analysis', async () => {
      // Navigate to network panel
      await page.click('[data-testid="network-tab"]');
      
      // Run network analysis
      await page.click('[data-testid="run-network-analysis-btn"]');
      
      // Wait for analysis to complete
      await page.waitForSelector('[data-testid="network-analysis-complete"]', { timeout: 20000 });
      
      // Verify network metrics
      const connectivityScore = await page.locator('[data-testid="connectivity-score"]').textContent();
      const walkabilityScore = await page.locator('[data-testid="walkability-score"]').textContent();
      
      expect(parseFloat(connectivityScore || '0')).toBeGreaterThan(0);
      expect(parseFloat(walkabilityScore || '0')).toBeGreaterThan(0);
    });

    // Step 5: Energy & Utilities Models
    await test.step('Energy & Utilities Models', async () => {
      // Navigate to utilities panel
      await page.click('[data-testid="utilities-tab"]');
      
      // Run energy model
      await page.click('[data-testid="run-energy-model-btn"]');
      
      // Wait for energy analysis
      await page.waitForSelector('[data-testid="energy-analysis-complete"]', { timeout: 25000 });
      
      // Verify energy results
      const solarPotential = await page.locator('[data-testid="solar-potential"]').textContent();
      const energyDemand = await page.locator('[data-testid="energy-demand"]').textContent();
      
      expect(parseFloat(solarPotential || '0')).toBeGreaterThan(0);
      expect(parseFloat(energyDemand || '0')).toBeGreaterThan(0);
      
      // Run water model
      await page.click('[data-testid="run-water-model-btn"]');
      
      // Wait for water analysis
      await page.waitForSelector('[data-testid="water-analysis-complete"]', { timeout: 20000 });
      
      // Verify water results
      const waterDemand = await page.locator('[data-testid="water-demand"]').textContent();
      expect(parseFloat(waterDemand || '0')).toBeGreaterThan(0);
    });

    // Step 6: Budget & Sustainability
    await test.step('Budget & Sustainability', async () => {
      // Navigate to budget panel
      await page.click('[data-testid="budget-tab"]');
      
      // Run budget calculation
      await page.click('[data-testid="run-budget-calculation-btn"]');
      
      // Wait for budget calculation
      await page.waitForSelector('[data-testid="budget-calculation-complete"]', { timeout: 30000 });
      
      // Verify budget results
      const totalCost = await page.locator('[data-testid="total-cost"]').textContent();
      const costPerUnit = await page.locator('[data-testid="cost-per-unit"]').textContent();
      
      expect(parseFloat(totalCost || '0')).toBeGreaterThan(0);
      expect(parseFloat(costPerUnit || '0')).toBeGreaterThan(0);
      
      // Navigate to sustainability panel
      await page.click('[data-testid="sustainability-tab"]');
      
      // Run sustainability scoring
      await page.click('[data-testid="run-sustainability-scoring-btn"]');
      
      // Wait for sustainability calculation
      await page.waitForSelector('[data-testid="sustainability-scoring-complete"]', { timeout: 20000 });
      
      // Verify sustainability results
      const sustainabilityScore = await page.locator('[data-testid="sustainability-score"]').textContent();
      const sustainabilityGrade = await page.locator('[data-testid="sustainability-grade"]').textContent();
      
      expect(parseFloat(sustainabilityScore || '0')).toBeGreaterThan(0);
      expect(sustainabilityGrade).toMatch(/[A-F]/);
    });

    // Step 7: Optimization
    await test.step('Optimization', async () => {
      // Navigate to optimization panel
      await page.click('[data-testid="optimization-tab"]');
      
      // Set optimization parameters
      await page.fill('[data-testid="optimization-iterations"]', '50');
      await page.selectOption('[data-testid="optimization-objective"]', 'sustainability_cost_balance');
      
      // Run optimization
      await page.click('[data-testid="run-optimization-btn"]');
      
      // Wait for optimization to complete
      await page.waitForSelector('[data-testid="optimization-complete"]', { timeout: 60000 });
      
      // Verify optimization results
      const paretoPoints = await page.locator('[data-testid="pareto-points-count"]').textContent();
      const bestScenario = await page.locator('[data-testid="best-scenario-score"]').textContent();
      
      expect(parseInt(paretoPoints || '0')).toBeGreaterThan(0);
      expect(parseFloat(bestScenario || '0')).toBeGreaterThan(0);
    });

    // Step 8: Personas & Journeys
    await test.step('Personas & Journeys', async () => {
      // Navigate to personas panel
      await page.click('[data-testid="personas-tab"]');
      
      // Generate personas
      await page.click('[data-testid="generate-personas-btn"]');
      
      // Wait for persona generation
      await page.waitForSelector('[data-testid="personas-generated"]', { timeout: 15000 });
      
      // Verify personas were created
      const personaCount = await page.locator('[data-testid="persona-count"]').textContent();
      expect(parseInt(personaCount || '0')).toBeGreaterThan(0);
      
      // Run journey analysis
      await page.click('[data-testid="run-journey-analysis-btn"]');
      
      // Wait for journey analysis
      await page.waitForSelector('[data-testid="journey-analysis-complete"]', { timeout: 20000 });
      
      // Verify journey results
      const barrierCount = await page.locator('[data-testid="barrier-count"]').textContent();
      expect(parseInt(barrierCount || '0')).toBeGreaterThanOrEqual(0);
    });

    // Step 9: Reports & Export
    await test.step('Reports & Export', async () => {
      // Navigate to reports panel
      await page.click('[data-testid="reports-tab"]');
      
      // Generate executive summary
      await page.click('[data-testid="generate-executive-summary-btn"]');
      
      // Wait for report generation
      await page.waitForSelector('[data-testid="executive-summary-generated"]', { timeout: 30000 });
      
      // Verify report was created
      await expect(page.locator('[data-testid="report-download-link"]')).toBeVisible();
      
      // Navigate to export panel
      await page.click('[data-testid="export-tab"]');
      
      // Select export formats
      await page.check('[data-testid="export-geojson"]');
      await page.check('[data-testid="export-shapefile"]');
      await page.check('[data-testid="export-pdf"]');
      
      // Set export options
      await page.fill('[data-testid="export-name"]', 'Test Development Export');
      await page.selectOption('[data-testid="export-theme"]', 'professional');
      
      // Run export
      await page.click('[data-testid="run-export-btn"]');
      
      // Wait for export to complete
      await page.waitForSelector('[data-testid="export-complete"]', { timeout: 45000 });
      
      // Verify export was successful
      await expect(page.locator('[data-testid="export-download-link"]')).toBeVisible();
      
      // Verify export contains expected files
      const exportFiles = await page.locator('[data-testid="export-file"]').count();
      expect(exportFiles).toBeGreaterThan(0);
    });

    // Step 10: Final Verification
    await test.step('Final Verification', async () => {
      // Navigate to dashboard
      await page.click('[data-testid="dashboard-tab"]');
      
      // Verify all key metrics are present
      await expect(page.locator('[data-testid="total-units-metric"]')).toBeVisible();
      await expect(page.locator('[data-testid="total-jobs-metric"]')).toBeVisible();
      await expect(page.locator('[data-testid="sustainability-score-metric"]')).toBeVisible();
      await expect(page.locator('[data-testid="total-cost-metric"]')).toBeVisible();
      
      // Verify project status is complete
      const projectStatus = await page.locator('[data-testid="project-status"]').textContent();
      expect(projectStatus).toContain('Complete');
      
      // Verify all workflow steps are marked as complete
      const completedSteps = await page.locator('[data-testid="workflow-step-complete"]').count();
      expect(completedSteps).toBeGreaterThanOrEqual(8); // All major steps
    });
  });

  test('Error handling and edge cases', async ({ page }) => {
    await test.step('Handle invalid site boundary', async () => {
      await page.click('[data-testid="new-project-btn"]');
      
      // Try to upload invalid file
      const fileInput = page.locator('[data-testid="site-boundary-upload"]');
      await fileInput.setInputFiles('tests/fixtures/invalid-boundary.txt');
      
      // Verify error message
      await expect(page.locator('[data-testid="upload-error"]')).toBeVisible();
    });

    await test.step('Handle network timeout', async () => {
      // Mock slow network response
      await page.route('**/api/parcelization', route => 
        route.fulfill({ status: 408, body: 'Request Timeout' })
      );
      
      await page.click('[data-testid="run-parcelization-btn"]');
      
      // Verify timeout error handling
      await expect(page.locator('[data-testid="timeout-error"]')).toBeVisible();
    });

    await test.step('Handle insufficient data for optimization', async () => {
      // Try to run optimization without sufficient data
      await page.click('[data-testid="optimization-tab"]');
      await page.click('[data-testid="run-optimization-btn"]');
      
      // Verify insufficient data error
      await expect(page.locator('[data-testid="insufficient-data-error"]')).toBeVisible();
    });
  });

  test('Performance and responsiveness', async ({ page }) => {
    await test.step('Test large site handling', async () => {
      // Upload large site boundary
      const fileInput = page.locator('[data-testid="site-boundary-upload"]');
      await fileInput.setInputFiles('tests/fixtures/large-site-boundary.geojson');
      
      // Verify processing indicator
      await expect(page.locator('[data-testid="processing-indicator"]')).toBeVisible();
      
      // Verify completion within reasonable time
      await page.waitForSelector('[data-testid="site-created-success"]', { timeout: 60000 });
    });

    await test.step('Test concurrent operations', async () => {
      // Start multiple operations simultaneously
      await page.click('[data-testid="run-parcelization-btn"]');
      await page.click('[data-testid="run-network-analysis-btn"]');
      
      // Verify both operations can run concurrently
      await page.waitForSelector('[data-testid="parcelization-complete"]', { timeout: 30000 });
      await page.waitForSelector('[data-testid="network-analysis-complete"]', { timeout: 30000 });
    });
  });
});
