'use client';

import React from 'react';
import { TrendingUp, TrendingDown, Minus, DollarSign, Users, Building, Leaf, Zap } from 'lucide-react';

interface KPIMetric {
  label: string;
  value: number | string;
  unit?: string;
  trend?: 'up' | 'down' | 'neutral';
  change?: number;
  color?: 'green' | 'red' | 'blue' | 'orange' | 'purple';
  icon?: React.ReactNode;
}

interface KPIGridProps {
  capacityMetrics?: {
    total_units: number;
    total_population: number;
    total_jobs: number;
    total_floor_area: number;
  };
  budgetMetrics?: {
    total: number;
    cost_per_unit: number;
    cost_per_sqm: number;
  };
  energyMetrics?: {
    energy_self_sufficiency: number;
    emissions_reduction_percent: number;
    solar_potential_kw: number;
  };
  networkMetrics?: {
    intersection_density: number;
    connectivity_ratio: number;
    avg_block_area: number;
  };
}

export const KPIGrid: React.FC<KPIGridProps> = ({
  capacityMetrics,
  budgetMetrics,
  energyMetrics,
  networkMetrics
}) => {
  const formatNumber = (num: number) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toLocaleString();
  };

  const formatCurrency = (usd: number) => {
    if (usd >= 1000000) {
      return '$' + (usd / 1000000).toFixed(1) + 'M';
    } else if (usd >= 1000) {
      return '$' + (usd / 1000).toFixed(1) + 'K';
    }
    return '$' + Math.round(usd).toLocaleString();
  };

  const formatPercentage = (value: number) => {
    return (value * 100).toFixed(1) + '%';
  };

  const getTrendIcon = (trend?: 'up' | 'down' | 'neutral') => {
    switch (trend) {
      case 'up':
        return <TrendingUp size={16} className="text-green-500" />;
      case 'down':
        return <TrendingDown size={16} className="text-red-500" />;
      default:
        return <Minus size={16} className="text-gray-400" />;
    }
  };

  const getColorClasses = (color?: 'green' | 'red' | 'blue' | 'orange' | 'purple') => {
    switch (color) {
      case 'green':
        return 'bg-green-50 border-green-200 text-green-700';
      case 'red':
        return 'bg-red-50 border-red-200 text-red-700';
      case 'blue':
        return 'bg-blue-50 border-blue-200 text-blue-700';
      case 'orange':
        return 'bg-orange-50 border-orange-200 text-orange-700';
      case 'purple':
        return 'bg-purple-50 border-purple-200 text-purple-700';
      default:
        return 'bg-gray-50 border-gray-200 text-gray-700';
    }
  };

  const kpiMetrics: KPIMetric[] = [
    // Capacity Metrics
    {
      label: 'Total Units',
      value: capacityMetrics?.total_units || 0,
      unit: 'units',
      color: 'blue',
      icon: <Building size={20} />
    },
    {
      label: 'Population',
      value: capacityMetrics?.total_population || 0,
      unit: 'people',
      color: 'green',
      icon: <Users size={20} />
    },
    {
      label: 'Jobs',
      value: capacityMetrics?.total_jobs || 0,
      unit: 'jobs',
      color: 'purple',
      icon: <Building size={20} />
    },
    {
      label: 'Floor Area',
      value: capacityMetrics?.total_floor_area || 0,
      unit: 'm²',
      color: 'orange',
      icon: <Building size={20} />
    },
    
    // Budget Metrics
    {
      label: 'Total Budget',
      value: budgetMetrics?.total || 0,
      unit: 'USD',
      color: 'red',
      icon: <DollarSign size={20} />
    },
    {
      label: 'Cost per Unit',
      value: budgetMetrics?.cost_per_unit || 0,
      unit: 'USD',
      color: 'red',
      icon: <DollarSign size={20} />
    },
    {
      label: 'Cost per m²',
      value: budgetMetrics?.cost_per_sqm || 0,
      unit: 'USD/m²',
      color: 'red',
      icon: <DollarSign size={20} />
    },
    
    // Energy Metrics
    {
      label: 'Energy Self-Sufficiency',
      value: energyMetrics?.energy_self_sufficiency || 0,
      unit: '%',
      color: 'green',
      icon: <Zap size={20} />
    },
    {
      label: 'Emissions Reduction',
      value: energyMetrics?.emissions_reduction_percent || 0,
      unit: '%',
      color: 'green',
      icon: <Leaf size={20} />
    },
    {
      label: 'Solar Potential',
      value: energyMetrics?.solar_potential_kw || 0,
      unit: 'kW',
      color: 'orange',
      icon: <Zap size={20} />
    },
    
    // Network Metrics
    {
      label: 'Intersection Density',
      value: networkMetrics?.intersection_density || 0,
      unit: 'per km',
      color: 'blue',
      icon: <TrendingUp size={20} />
    },
    {
      label: 'Network Connectivity',
      value: networkMetrics?.connectivity_ratio || 0,
      unit: '%',
      color: 'purple',
      icon: <TrendingUp size={20} />
    },
    {
      label: 'Avg Block Size',
      value: networkMetrics?.avg_block_area || 0,
      unit: 'm²',
      color: 'orange',
      icon: <Building size={20} />
    }
  ];

  const renderMetricValue = (metric: KPIMetric) => {
    if (typeof metric.value === 'number') {
      if (metric.unit === 'USD') {
        return formatCurrency(metric.value);
      } else if (metric.unit === '%') {
        return formatPercentage(metric.value);
      } else {
        return formatNumber(metric.value);
      }
    }
    return metric.value;
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">Key Performance Indicators</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {kpiMetrics.map((metric, index) => (
          <div
            key={index}
            className={`p-4 rounded-lg border ${getColorClasses(metric.color)}`}
          >
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center space-x-2">
                {metric.icon}
                <span className="text-sm font-medium">{metric.label}</span>
              </div>
              {getTrendIcon(metric.trend)}
            </div>
            
            <div className="text-2xl font-bold mb-1">
              {renderMetricValue(metric)}
            </div>
            
            {metric.unit && (
              <div className="text-xs opacity-75">
                {metric.unit}
              </div>
            )}
            
            {metric.change !== undefined && (
              <div className="text-xs mt-1">
                {metric.change > 0 ? '+' : ''}{metric.change.toFixed(1)}% from baseline
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Summary Section */}
      <div className="mt-8 pt-6 border-t border-gray-200">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Performance Summary</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Capacity Summary */}
          <div className="bg-blue-50 p-4 rounded-lg">
            <h4 className="font-medium text-blue-900 mb-2">Capacity</h4>
            <div className="space-y-1 text-sm">
              <div className="flex justify-between">
                <span>Density:</span>
                <span className="font-medium">
                  {capacityMetrics ? Math.round(capacityMetrics.total_population / (capacityMetrics.total_floor_area / 10000)) : 0} people/ha
                </span>
              </div>
              <div className="flex justify-between">
                <span>Jobs Ratio:</span>
                <span className="font-medium">
                  {capacityMetrics ? (capacityMetrics.total_jobs / capacityMetrics.total_population).toFixed(2) : 0}
                </span>
              </div>
            </div>
          </div>

          {/* Financial Summary */}
          <div className="bg-red-50 p-4 rounded-lg">
            <h4 className="font-medium text-red-900 mb-2">Financial</h4>
            <div className="space-y-1 text-sm">
              <div className="flex justify-between">
                <span>Cost Efficiency:</span>
                <span className="font-medium">
                  {budgetMetrics ? formatCurrency(budgetMetrics.cost_per_unit) : '$0'}/unit
                </span>
              </div>
              <div className="flex justify-between">
                <span>Area Efficiency:</span>
                <span className="font-medium">
                  {budgetMetrics ? formatCurrency(budgetMetrics.cost_per_sqm) : '$0'}/m²
                </span>
              </div>
            </div>
          </div>

          {/* Sustainability Summary */}
          <div className="bg-green-50 p-4 rounded-lg">
            <h4 className="font-medium text-green-900 mb-2">Sustainability</h4>
            <div className="space-y-1 text-sm">
              <div className="flex justify-between">
                <span>Energy Independence:</span>
                <span className="font-medium">
                  {energyMetrics ? formatPercentage(energyMetrics.energy_self_sufficiency) : '0%'}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Carbon Reduction:</span>
                <span className="font-medium">
                  {energyMetrics ? formatPercentage(energyMetrics.emissions_reduction_percent) : '0%'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
