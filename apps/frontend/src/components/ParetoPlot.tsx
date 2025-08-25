'use client';

import React, { useState } from 'react';
import { Scatter, ScatterChart, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, Legend } from 'recharts';
import { TrendingUp, Target, DollarSign, Users, Zap } from 'lucide-react';

interface ParetoSolution {
  name: string;
  sustainability_score: number;
  cost_efficiency: number;
  density: number;
  accessibility: number;
  total_score: number;
  budget: number;
  units: number;
  area: number;
  parameters?: { [key: string]: number };
}

interface ParetoPlotProps {
  paretoSolutions?: ParetoSolution[];
  tradeOffs?: {
    correlations: { [key: string]: number };
    trade_off_ratios: { [key: string]: number };
    solution_count: number;
  };
  onSolutionClick?: (solution: ParetoSolution) => void;
  onAdoptSolution?: (solution: ParetoSolution) => void;
}

export const ParetoPlot: React.FC<ParetoPlotProps> = ({
  paretoSolutions,
  tradeOffs,
  onSolutionClick,
  onAdoptSolution
}) => {
  const [selectedAxis, setSelectedAxis] = useState<'sustainability_cost' | 'density_accessibility' | 'score_budget'>('sustainability_cost');
  const [selectedSolution, setSelectedSolution] = useState<ParetoSolution | null>(null);

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

  const getAxisConfig = () => {
    switch (selectedAxis) {
      case 'sustainability_cost':
        return {
          xAxis: 'sustainability_score',
          yAxis: 'cost_efficiency',
          xLabel: 'Sustainability Score',
          yLabel: 'Cost Efficiency',
          xIcon: <Zap size={16} />,
          yIcon: <DollarSign size={16} />
        };
      case 'density_accessibility':
        return {
          xAxis: 'density',
          yAxis: 'accessibility',
          xLabel: 'Density',
          yLabel: 'Accessibility',
          xIcon: <Users size={16} />,
          yIcon: <TrendingUp size={16} />
        };
      case 'score_budget':
        return {
          xAxis: 'total_score',
          yAxis: 'budget',
          xLabel: 'Total Score',
          yLabel: 'Budget',
          xIcon: <Target size={16} />,
          yIcon: <DollarSign size={16} />
        };
    }
  };

  const getSolutionColor = (solution: ParetoSolution) => {
    if (solution.name === 'Baseline') return '#3B82F6'; // Blue
    if (solution.total_score >= 80) return '#10B981'; // Green
    if (solution.total_score >= 60) return '#F59E0B'; // Yellow
    return '#EF4444'; // Red
  };

  const getSolutionSize = (solution: ParetoSolution) => {
    if (solution.name === 'Baseline') return 8;
    return 6;
  };

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const solution = payload[0].payload as ParetoSolution;
      return (
        <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-lg">
          <h3 className="font-semibold text-gray-900 mb-2">{solution.name}</h3>
          <div className="space-y-1 text-sm">
            <div className="flex justify-between">
              <span>Total Score:</span>
              <span className="font-medium">{solution.total_score.toFixed(1)}</span>
            </div>
            <div className="flex justify-between">
              <span>Sustainability:</span>
              <span className="font-medium">{solution.sustainability_score.toFixed(1)}</span>
            </div>
            <div className="flex justify-between">
              <span>Cost Efficiency:</span>
              <span className="font-medium">{solution.cost_efficiency.toFixed(1)}</span>
            </div>
            <div className="flex justify-between">
              <span>Density:</span>
              <span className="font-medium">{solution.density.toFixed(1)}</span>
            </div>
            <div className="flex justify-between">
              <span>Accessibility:</span>
              <span className="font-medium">{solution.accessibility.toFixed(1)}</span>
            </div>
            <div className="flex justify-between">
              <span>Budget:</span>
              <span className="font-medium">{formatCurrency(solution.budget)}</span>
            </div>
            <div className="flex justify-between">
              <span>Units:</span>
              <span className="font-medium">{solution.units.toLocaleString()}</span>
            </div>
          </div>
          {solution.parameters && (
            <div className="mt-2 pt-2 border-t border-gray-200">
              <div className="text-xs text-gray-600">Key Parameters:</div>
              {Object.entries(solution.parameters).slice(0, 3).map(([key, value]) => (
                <div key={key} className="text-xs">
                  {key.replace('_', ' ')}: {value.toFixed(2)}
                </div>
              ))}
            </div>
          )}
        </div>
      );
    }
    return null;
  };

  if (!paretoSolutions || paretoSolutions.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Pareto Optimal Solutions</h2>
        <div className="text-center text-gray-500 py-8">
          <Target size={48} className="mx-auto mb-4 text-gray-300" />
          <p>No Pareto solutions available</p>
          <p className="text-sm">Run optimization to generate Pareto frontier</p>
        </div>
      </div>
    );
  }

  const axisConfig = getAxisConfig();
  const chartData = paretoSolutions.map(solution => ({
    ...solution,
    x: solution[axisConfig.xAxis as keyof ParetoSolution] as number,
    y: solution[axisConfig.yAxis as keyof ParetoSolution] as number
  }));

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">Pareto Optimal Solutions</h2>
      
      {/* Axis Selection */}
      <div className="mb-6">
        <h3 className="text-lg font-medium text-gray-900 mb-3">View Options</h3>
        <div className="flex space-x-2">
          {[
            { key: 'sustainability_cost', label: 'Sustainability vs Cost' },
            { key: 'density_accessibility', label: 'Density vs Accessibility' },
            { key: 'score_budget', label: 'Score vs Budget' }
          ].map((option) => (
            <button
              key={option.key}
              onClick={() => setSelectedAxis(option.key as any)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedAxis === option.key
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {option.label}
            </button>
          ))}
        </div>
      </div>

      {/* Pareto Chart */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-medium text-gray-900">
            {axisConfig.xLabel} vs {axisConfig.yLabel}
          </h3>
          <div className="flex items-center space-x-4 text-sm text-gray-600">
            <div className="flex items-center space-x-1">
              {axisConfig.xIcon}
              <span>{axisConfig.xLabel}</span>
            </div>
            <div className="flex items-center space-x-1">
              {axisConfig.yIcon}
              <span>{axisConfig.yLabel}</span>
            </div>
          </div>
        </div>

        <div className="h-96">
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart
              data={chartData}
              margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                type="number"
                dataKey="x"
                name={axisConfig.xLabel}
                tickFormatter={(value) => 
                  axisConfig.xAxis === 'budget' ? formatCurrency(value) : value.toFixed(0)
                }
              />
              <YAxis
                type="number"
                dataKey="y"
                name={axisConfig.yLabel}
                tickFormatter={(value) => 
                  axisConfig.yAxis === 'budget' ? formatCurrency(value) : value.toFixed(0)
                }
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              <Scatter
                dataKey="y"
                fill="#8884d8"
                onClick={(data) => {
                  setSelectedSolution(data);
                  onSolutionClick?.(data);
                }}
              >
                {chartData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={getSolutionColor(entry)}
                    r={getSolutionSize(entry)}
                  />
                ))}
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Selected Solution Details */}
      {selectedSolution && (
        <div className="mb-6 p-4 bg-blue-50 rounded-lg">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-medium text-blue-900">Selected Solution: {selectedSolution.name}</h3>
            <button
              onClick={() => onAdoptSolution?.(selectedSolution)}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
            >
              Adopt Solution
            </button>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <div className="text-blue-700">Total Score</div>
              <div className="font-medium text-blue-900">{selectedSolution.total_score.toFixed(1)}</div>
            </div>
            <div>
              <div className="text-blue-700">Budget</div>
              <div className="font-medium text-blue-900">{formatCurrency(selectedSolution.budget)}</div>
            </div>
            <div>
              <div className="text-blue-700">Units</div>
              <div className="font-medium text-blue-900">{selectedSolution.units.toLocaleString()}</div>
            </div>
            <div>
              <div className="text-blue-700">Area</div>
              <div className="font-medium text-blue-900">{formatNumber(selectedSolution.area)} m²</div>
            </div>
          </div>
        </div>
      )}

      {/* Trade-off Analysis */}
      {tradeOffs && (
        <div className="mb-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Trade-off Analysis</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Correlations */}
            <div className="bg-gray-50 p-4 rounded-lg">
              <h4 className="font-medium text-gray-900 mb-3">Objective Correlations</h4>
              <div className="space-y-2">
                {Object.entries(tradeOffs.correlations).map(([pair, correlation]) => (
                  <div key={pair} className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">
                      {pair.replace('_', ' vs ').replace('_', ' ')}
                    </span>
                    <span className={`font-medium ${
                      correlation > 0.7 ? 'text-green-600' :
                      correlation > 0.3 ? 'text-yellow-600' :
                      correlation > -0.3 ? 'text-gray-600' :
                      correlation > -0.7 ? 'text-orange-600' : 'text-red-600'
                    }`}>
                      {correlation.toFixed(2)}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Trade-off Ratios */}
            <div className="bg-gray-50 p-4 rounded-lg">
              <h4 className="font-medium text-gray-900 mb-3">Trade-off Ratios</h4>
              <div className="space-y-2">
                {Object.entries(tradeOffs.trade_off_ratios).map(([pair, ratio]) => (
                  <div key={pair} className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">
                      {pair.replace('_', ' vs ').replace('_', ' ')}
                    </span>
                    <span className="font-medium text-gray-900">
                      {ratio.toFixed(2)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Solution Summary */}
      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Solution Summary</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Best Solutions by Category */}
          <div className="bg-green-50 p-4 rounded-lg">
            <h4 className="font-medium text-green-900 mb-2">Best Sustainability</h4>
            {(() => {
              const best = paretoSolutions.reduce((max, current) => 
                current.sustainability_score > max.sustainability_score ? current : max
              );
              return (
                <div className="text-sm">
                  <div className="font-medium text-green-900">{best.name}</div>
                  <div className="text-green-700">{best.sustainability_score.toFixed(1)} pts</div>
                </div>
              );
            })()}
          </div>

          <div className="bg-blue-50 p-4 rounded-lg">
            <h4 className="font-medium text-blue-900 mb-2">Best Cost Efficiency</h4>
            {(() => {
              const best = paretoSolutions.reduce((max, current) => 
                current.cost_efficiency > max.cost_efficiency ? current : max
              );
              return (
                <div className="text-sm">
                  <div className="font-medium text-blue-900">{best.name}</div>
                  <div className="text-blue-700">{best.cost_efficiency.toFixed(1)} pts</div>
                </div>
              );
            })()}
          </div>

          <div className="bg-purple-50 p-4 rounded-lg">
            <h4 className="font-medium text-purple-900 mb-2">Best Overall Score</h4>
            {(() => {
              const best = paretoSolutions.reduce((max, current) => 
                current.total_score > max.total_score ? current : max
              );
              return (
                <div className="text-sm">
                  <div className="font-medium text-purple-900">{best.name}</div>
                  <div className="text-purple-700">{best.total_score.toFixed(1)} pts</div>
                </div>
              );
            })()}
          </div>
        </div>

        {/* Solution Count */}
        <div className="mt-4 p-3 bg-gray-50 rounded-lg">
          <div className="text-sm text-gray-600">
            Generated <span className="font-medium text-gray-900">{paretoSolutions.length}</span> Pareto optimal solutions
          </div>
        </div>
      </div>
    </div>
  );
};
