'use client';

import React from 'react';
import { TrendingUp, TrendingDown, BarChart3 } from 'lucide-react';

interface TornadoParameter {
  high_impact: number;
  low_impact: number;
  max_impact: number;
  direction: 'positive' | 'negative';
}

interface TornadoChartProps {
  tornadoData?: {
    parameters: {
      [key: string]: TornadoParameter;
    };
    baseline_score: number;
  };
  onParameterClick?: (parameter: string) => void;
}

export const TornadoChart: React.FC<TornadoChartProps> = ({
  tornadoData,
  onParameterClick
}) => {
  const formatNumber = (num: number) => {
    return num.toFixed(1);
  };

  const getParameterName = (param: string) => {
    return param.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  };

  const getParameterDescription = (param: string) => {
    const descriptions: { [key: string]: string } = {
      'far': 'Floor Area Ratio - building density',
      'height': 'Building height in meters',
      'lot_coverage': 'Percentage of lot covered by buildings',
      'parking_ratio': 'Parking spaces per unit',
      'green_space_ratio': 'Percentage of green space',
      'mixed_use_ratio': 'Percentage of mixed-use development',
      'solar_coverage': 'Percentage of roof area with solar panels',
      'bike_infrastructure': 'Percentage of streets with bike lanes',
      'transit_priority': 'Transit priority level (0-1)',
      'inclusionary_housing': 'Percentage of affordable housing'
    };
    return descriptions[param] || 'Development parameter';
  };

  const getImpactColor = (impact: number) => {
    const absImpact = Math.abs(impact);
    if (absImpact >= 20) return 'text-red-600 bg-red-50 border-red-200';
    if (absImpact >= 10) return 'text-orange-600 bg-orange-50 border-orange-200';
    if (absImpact >= 5) return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    return 'text-green-600 bg-green-50 border-green-200';
  };

  const getBarColor = (impact: number) => {
    const absImpact = Math.abs(impact);
    if (absImpact >= 20) return 'bg-red-500';
    if (absImpact >= 10) return 'bg-orange-500';
    if (absImpact >= 5) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  if (!tornadoData) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Sensitivity Analysis</h2>
        <div className="text-center text-gray-500 py-8">
          <BarChart3 size={48} className="mx-auto mb-4 text-gray-300" />
          <p>No sensitivity analysis data available</p>
          <p className="text-sm">Run optimization to generate tornado chart</p>
        </div>
      </div>
    );
  }

  // Sort parameters by impact magnitude
  const sortedParameters = Object.entries(tornadoData.parameters)
    .sort(([, a], [, b]) => b.max_impact - a.max_impact);

  const maxImpact = Math.max(...Object.values(tornadoData.parameters).map(p => p.max_impact));

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">Sensitivity Analysis</h2>
      
      {/* Baseline Score */}
      <div className="mb-6 p-4 bg-blue-50 rounded-lg">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-medium text-blue-900">Baseline Score</h3>
            <p className="text-sm text-blue-700">
              Current scenario performance before optimization
            </p>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-blue-900">
              {formatNumber(tornadoData.baseline_score)}
            </div>
            <div className="text-sm text-blue-600">out of 100</div>
          </div>
        </div>
      </div>

      {/* Tornado Chart */}
      <div className="space-y-4">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Parameter Impact</h3>
        
        {sortedParameters.map(([parameter, data]) => (
          <div
            key={parameter}
            className="cursor-pointer hover:bg-gray-50 p-3 rounded-lg transition-colors"
            onClick={() => onParameterClick?.(parameter)}
          >
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center space-x-2">
                <h4 className="font-medium text-gray-900">
                  {getParameterName(parameter)}
                </h4>
                <div className={`px-2 py-1 rounded text-xs font-medium ${getImpactColor(data.max_impact)}`}>
                  {data.direction === 'positive' ? 'Positive' : 'Negative'} Impact
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm font-medium text-gray-900">
                  ±{formatNumber(data.max_impact)} pts
                </div>
                <div className="text-xs text-gray-500">
                  Max impact
                </div>
              </div>
            </div>

            {/* Parameter Description */}
            <p className="text-sm text-gray-600 mb-3">
              {getParameterDescription(parameter)}
            </p>

            {/* Impact Bars */}
            <div className="relative">
              <div className="flex items-center space-x-4">
                {/* Low Impact Bar */}
                <div className="flex-1">
                  <div className="flex items-center justify-between text-xs text-gray-500 mb-1">
                    <span>Low Value</span>
                    <span>{formatNumber(data.low_impact)} pts</span>
                  </div>
                  <div className="relative h-4 bg-gray-200 rounded">
                    <div
                      className={`h-full rounded transition-all duration-300 ${getBarColor(data.low_impact)}`}
                      style={{
                        width: `${Math.abs(data.low_impact) / maxImpact * 100}%`,
                        marginLeft: data.low_impact < 0 ? 'auto' : '0'
                      }}
                    />
                  </div>
                </div>

                {/* Center Line */}
                <div className="w-8 text-center">
                  <div className="w-0.5 h-4 bg-gray-400 mx-auto"></div>
                  <div className="text-xs text-gray-500 mt-1">0</div>
                </div>

                {/* High Impact Bar */}
                <div className="flex-1">
                  <div className="flex items-center justify-between text-xs text-gray-500 mb-1">
                    <span>{formatNumber(data.high_impact)} pts</span>
                    <span>High Value</span>
                  </div>
                  <div className="relative h-4 bg-gray-200 rounded">
                    <div
                      className={`h-full rounded transition-all duration-300 ${getBarColor(data.high_impact)}`}
                      style={{
                        width: `${Math.abs(data.high_impact) / maxImpact * 100}%`,
                        marginLeft: data.high_impact < 0 ? 'auto' : '0'
                      }}
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Impact Summary */}
            <div className="mt-3 flex items-center justify-between text-sm">
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-1">
                  {data.high_impact > data.low_impact ? (
                    <TrendingUp size={14} className="text-green-600" />
                  ) : (
                    <TrendingDown size={14} className="text-red-600" />
                  )}
                  <span className="text-gray-600">
                    {data.high_impact > data.low_impact ? 'Increasing' : 'Decreasing'} this parameter
                  </span>
                </div>
              </div>
              <div className="text-right">
                <span className="text-gray-600">Range: </span>
                <span className="font-medium text-gray-900">
                  {formatNumber(data.low_impact)} to {formatNumber(data.high_impact)}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Summary Statistics */}
      <div className="mt-8 pt-6 border-t border-gray-200">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Impact Summary</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* High Impact Parameters */}
          <div className="bg-red-50 p-4 rounded-lg">
            <h4 className="font-medium text-red-900 mb-2">High Impact (±10+ pts)</h4>
            <div className="space-y-1">
              {sortedParameters
                .filter(([, data]) => data.max_impact >= 10)
                .map(([param]) => (
                  <div key={param} className="text-sm text-red-700">
                    • {getParameterName(param)}
                  </div>
                ))}
            </div>
          </div>

          {/* Medium Impact Parameters */}
          <div className="bg-yellow-50 p-4 rounded-lg">
            <h4 className="font-medium text-yellow-900 mb-2">Medium Impact (±5-10 pts)</h4>
            <div className="space-y-1">
              {sortedParameters
                .filter(([, data]) => data.max_impact >= 5 && data.max_impact < 10)
                .map(([param]) => (
                  <div key={param} className="text-sm text-yellow-700">
                    • {getParameterName(param)}
                  </div>
                ))}
            </div>
          </div>

          {/* Low Impact Parameters */}
          <div className="bg-green-50 p-4 rounded-lg">
            <h4 className="font-medium text-green-900 mb-2">Low Impact (<5 pts)</h4>
            <div className="space-y-1">
              {sortedParameters
                .filter(([, data]) => data.max_impact < 5)
                .map(([param]) => (
                  <div key={param} className="text-sm text-green-700">
                    • {getParameterName(param)}
                  </div>
                ))}
            </div>
          </div>
        </div>

        {/* Recommendations */}
        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <h4 className="font-medium text-blue-900 mb-2">Optimization Recommendations</h4>
          <div className="text-sm text-blue-700 space-y-1">
            {sortedParameters.slice(0, 3).map(([param, data]) => (
              <div key={param}>
                • Focus on <strong>{getParameterName(param)}</strong> - 
                {data.direction === 'positive' ? ' increasing' : ' decreasing'} this parameter 
                can improve the score by up to {formatNumber(data.max_impact)} points
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
