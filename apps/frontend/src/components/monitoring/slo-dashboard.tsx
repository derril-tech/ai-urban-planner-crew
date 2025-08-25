'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Activity, 
  AlertTriangle, 
  CheckCircle, 
  Clock, 
  Database, 
  HardDrive, 
  Network, 
  Server, 
  TrendingUp,
  TrendingDown,
  XCircle,
  Info
} from 'lucide-react';

interface SLOMetric {
  metric_name: string;
  window_hours: number;
  count: number;
  min: number;
  max: number;
  mean: number;
  median: number;
  p95: number;
  p99: number;
  status_distribution: {
    green: number;
    yellow: number;
    red: number;
  };
  current_status: 'green' | 'yellow' | 'red';
  unit: string;
}

interface SLOStatus {
  service: string;
  availability: {
    target: number;
    current: number;
    status: 'green' | 'yellow' | 'red';
  };
  latency: {
    p50: { target: number; current: number };
    p95: { target: number; current: number };
    p99: { target: number; current: number };
  };
  error_budget: {
    remaining: number;
    consumed: number;
    window: string;
  };
}

interface Alert {
  severity: 'critical' | 'warning';
  metric: string;
  message: string;
  count: number;
  timestamp: string;
}

interface SLODashboardData {
  timestamp: string;
  window_hours: number;
  slo_status: Record<string, SLOStatus>;
  metric_summaries: Record<string, SLOMetric>;
  alerts: Alert[];
}

const SLOStatusCard: React.FC<{ service: string; status: SLOStatus }> = ({ service, status }) => {
  const getStatusColor = (statusValue: 'green' | 'yellow' | 'red') => {
    switch (statusValue) {
      case 'green': return 'bg-green-500';
      case 'yellow': return 'bg-yellow-500';
      case 'red': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusIcon = (statusValue: 'green' | 'yellow' | 'red') => {
    switch (statusValue) {
      case 'green': return <CheckCircle className="h-4 w-4 text-green-600" />;
      case 'yellow': return <AlertTriangle className="h-4 w-4 text-yellow-600" />;
      case 'red': return <XCircle className="h-4 w-4 text-red-600" />;
      default: return <Info className="h-4 w-4 text-gray-600" />;
    }
  };

  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-lg">
          {getStatusIcon(status.availability.status)}
          {service.replace('_', ' ').toUpperCase()}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Availability */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium">Availability</span>
            <Badge variant={status.availability.status === 'green' ? 'default' : 'destructive'}>
              {status.availability.current.toFixed(2)}%
            </Badge>
          </div>
          <Progress 
            value={(status.availability.current / status.availability.target) * 100} 
            className="h-2"
          />
          <p className="text-xs text-muted-foreground mt-1">
            Target: {status.availability.target}%
          </p>
        </div>

        {/* Latency */}
        <div className="space-y-2">
          <h4 className="text-sm font-medium">Latency (seconds)</h4>
          <div className="grid grid-cols-3 gap-2 text-xs">
            <div>
              <span className="text-muted-foreground">P50:</span>
              <div className="font-mono">{status.latency.p50.current.toFixed(2)}</div>
            </div>
            <div>
              <span className="text-muted-foreground">P95:</span>
              <div className="font-mono">{status.latency.p95.current.toFixed(2)}</div>
            </div>
            <div>
              <span className="text-muted-foreground">P99:</span>
              <div className="font-mono">{status.latency.p99.current.toFixed(2)}</div>
            </div>
          </div>
        </div>

        {/* Error Budget */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium">Error Budget</span>
            <span className="text-xs text-muted-foreground">
              {status.error_budget.remaining.toFixed(2)}% remaining
            </span>
          </div>
          <Progress 
            value={status.error_budget.consumed * 100} 
            className="h-2"
          />
        </div>
      </CardContent>
    </Card>
  );
};

const MetricCard: React.FC<{ metric: SLOMetric }> = ({ metric }) => {
  const getStatusColor = (status: 'green' | 'yellow' | 'red') => {
    switch (status) {
      case 'green': return 'text-green-600';
      case 'yellow': return 'text-yellow-600';
      case 'red': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getStatusIcon = (status: 'green' | 'yellow' | 'red') => {
    switch (status) {
      case 'green': return <CheckCircle className="h-4 w-4" />;
      case 'yellow': return <AlertTriangle className="h-4 w-4" />;
      case 'red': return <XCircle className="h-4 w-4" />;
      default: return <Info className="h-4 w-4" />;
    }
  };

  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center justify-between text-sm">
          <span className="truncate">{metric.metric_name.replace(/_/g, ' ')}</span>
          <div className={`flex items-center gap-1 ${getStatusColor(metric.current_status)}`}>
            {getStatusIcon(metric.current_status)}
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {/* Current Value */}
        <div className="text-center">
          <div className="text-2xl font-bold">{metric.mean.toFixed(2)}</div>
          <div className="text-xs text-muted-foreground">{metric.unit}</div>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-2 gap-2 text-xs">
          <div>
            <span className="text-muted-foreground">Min:</span>
            <div className="font-mono">{metric.min.toFixed(2)}</div>
          </div>
          <div>
            <span className="text-muted-foreground">Max:</span>
            <div className="font-mono">{metric.max.toFixed(2)}</div>
          </div>
          <div>
            <span className="text-muted-foreground">P95:</span>
            <div className="font-mono">{metric.p95.toFixed(2)}</div>
          </div>
          <div>
            <span className="text-muted-foreground">P99:</span>
            <div className="font-mono">{metric.p99.toFixed(2)}</div>
          </div>
        </div>

        {/* Status Distribution */}
        <div className="space-y-1">
          <div className="flex justify-between text-xs">
            <span>Status Distribution</span>
            <span>{metric.count} samples</span>
          </div>
          <div className="flex gap-1">
            <div 
              className="h-2 bg-green-500 rounded" 
              style={{ width: `${(metric.status_distribution.green / metric.count) * 100}%` }}
            />
            <div 
              className="h-2 bg-yellow-500 rounded" 
              style={{ width: `${(metric.status_distribution.yellow / metric.count) * 100}%` }}
            />
            <div 
              className="h-2 bg-red-500 rounded" 
              style={{ width: `${(metric.status_distribution.red / metric.count) * 100}%` }}
            />
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

const AlertCard: React.FC<{ alert: Alert }> = ({ alert }) => {
  const getSeverityIcon = (severity: 'critical' | 'warning') => {
    switch (severity) {
      case 'critical': return <XCircle className="h-4 w-4" />;
      case 'warning': return <AlertTriangle className="h-4 w-4" />;
      default: return <Info className="h-4 w-4" />;
    }
  };

  return (
    <Alert variant={alert.severity === 'critical' ? 'destructive' : 'default'}>
      <div className="flex items-center gap-2">
        {getSeverityIcon(alert.severity)}
        <AlertTitle className="capitalize">{alert.severity}</AlertTitle>
      </div>
      <AlertDescription className="mt-2">
        <div className="font-medium">{alert.message}</div>
        <div className="text-sm text-muted-foreground mt-1">
          Metric: {alert.metric} • Count: {alert.count} • 
          {new Date(alert.timestamp).toLocaleString()}
        </div>
      </AlertDescription>
    </Alert>
  );
};

const SLODashboard: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<SLODashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        // Mock data - replace with actual API call
        const mockData: SLODashboardData = {
          timestamp: new Date().toISOString(),
          window_hours: 24,
          slo_status: {
            parcelization: {
              service: 'parcelization',
              availability: { target: 99.9, current: 99.8, status: 'green' },
              latency: {
                p50: { target: 30, current: 25 },
                p95: { target: 60, current: 45 },
                p99: { target: 120, current: 90 }
              },
              error_budget: { remaining: 0.08, consumed: 0.02, window: '30d' }
            },
            model_runs: {
              service: 'model_runs',
              availability: { target: 99.5, current: 99.2, status: 'yellow' },
              latency: {
                p50: { target: 300, current: 280 },
                p95: { target: 600, current: 650 },
                p99: { target: 1200, current: 1100 }
              },
              error_budget: { remaining: 0.3, consumed: 0.2, window: '30d' }
            },
            optimizer: {
              service: 'optimizer',
              availability: { target: 99.0, current: 98.5, status: 'yellow' },
              latency: {
                p50: { target: 1800, current: 1700 },
                p95: { target: 3600, current: 3800 },
                p99: { target: 7200, current: 7000 }
              },
              error_budget: { remaining: 0.5, consumed: 0.5, window: '30d' }
            },
            exports: {
              service: 'exports',
              availability: { target: 99.9, current: 99.9, status: 'green' },
              latency: {
                p50: { target: 60, current: 55 },
                p95: { target: 120, current: 110 },
                p99: { target: 300, current: 280 }
              },
              error_budget: { remaining: 0.1, consumed: 0.0, window: '30d' }
            }
          },
          metric_summaries: {
            parcelization_duration: {
              metric_name: 'parcelization_duration',
              window_hours: 24,
              count: 150,
              min: 15.2,
              max: 85.7,
              mean: 28.5,
              median: 26.1,
              p95: 45.2,
              p99: 78.3,
              status_distribution: { green: 140, yellow: 8, red: 2 },
              current_status: 'green',
              unit: 'seconds'
            },
            model_run_duration: {
              metric_name: 'model_run_duration',
              window_hours: 24,
              count: 75,
              min: 180.5,
              max: 1200.3,
              mean: 320.8,
              median: 295.2,
              p95: 580.1,
              p99: 980.5,
              status_distribution: { green: 65, yellow: 8, red: 2 },
              current_status: 'yellow',
              unit: 'seconds'
            },
            optimizer_duration: {
              metric_name: 'optimizer_duration',
              window_hours: 24,
              count: 25,
              min: 1200.0,
              max: 4800.0,
              mean: 2100.5,
              median: 1950.2,
              p95: 3200.8,
              p99: 4500.1,
              status_distribution: { green: 20, yellow: 4, red: 1 },
              current_status: 'yellow',
              unit: 'seconds'
            },
            export_duration: {
              metric_name: 'export_duration',
              window_hours: 24,
              count: 200,
              min: 25.1,
              max: 180.5,
              mean: 58.2,
              median: 52.8,
              p95: 95.3,
              p99: 150.7,
              status_distribution: { green: 195, yellow: 4, red: 1 },
              current_status: 'green',
              unit: 'seconds'
            }
          },
          alerts: [
            {
              severity: 'warning',
              metric: 'model_run_duration',
              message: 'Performance degradation detected for model runs',
              count: 5,
              timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString()
            },
            {
              severity: 'critical',
              metric: 'optimizer_duration',
              message: 'Critical threshold exceeded for optimizer',
              count: 3,
              timestamp: new Date(Date.now() - 1000 * 60 * 15).toISOString()
            }
          ]
        };

        setDashboardData(mockData);
        setError(null);
      } catch (err) {
        setError('Failed to load SLO dashboard data');
        console.error('Error fetching SLO dashboard data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
    
    // Refresh every 30 seconds
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <XCircle className="h-4 w-4" />
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  if (!dashboardData) {
    return null;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">SLO Dashboard</h1>
          <p className="text-muted-foreground">
            Service Level Objectives and Performance Metrics
          </p>
        </div>
        <div className="text-right">
          <div className="text-sm text-muted-foreground">Last Updated</div>
          <div className="font-mono text-sm">
            {new Date(dashboardData.timestamp).toLocaleString()}
          </div>
        </div>
      </div>

      {/* Alerts */}
      {dashboardData.alerts.length > 0 && (
        <div className="space-y-2">
          <h2 className="text-lg font-semibold">Active Alerts</h2>
          {dashboardData.alerts.map((alert, index) => (
            <AlertCard key={index} alert={alert} />
          ))}
        </div>
      )}

      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="metrics">Metrics</TabsTrigger>
          <TabsTrigger value="services">Services</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          {/* SLO Status Overview */}
          <div>
            <h2 className="text-lg font-semibold mb-4">Service Status</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {Object.entries(dashboardData.slo_status).map(([service, status]) => (
                <SLOStatusCard key={service} service={service} status={status} />
              ))}
            </div>
          </div>

          {/* Key Metrics Summary */}
          <div>
            <h2 className="text-lg font-semibold mb-4">Key Metrics</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {Object.entries(dashboardData.metric_summaries).map(([name, metric]) => (
                <MetricCard key={name} metric={metric} />
              ))}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="metrics" className="space-y-4">
          <div>
            <h2 className="text-lg font-semibold mb-4">Detailed Metrics</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(dashboardData.metric_summaries).map(([name, metric]) => (
                <MetricCard key={name} metric={metric} />
              ))}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="services" className="space-y-4">
          <div>
            <h2 className="text-lg font-semibold mb-4">Service Details</h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {Object.entries(dashboardData.slo_status).map(([service, status]) => (
                <SLOStatusCard key={service} service={service} status={status} />
              ))}
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default SLODashboard;
