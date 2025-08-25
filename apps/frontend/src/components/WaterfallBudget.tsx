'use client';

import React from 'react';
import { DollarSign, Building, Wrench, Leaf, FileText, TrendingUp, TrendingDown } from 'lucide-react';

interface BudgetCategory {
  name: string;
  amount: number;
  percentage: number;
  color: string;
  icon: React.ReactNode;
  breakdown?: {
    name: string;
    amount: number;
    percentage: number;
  }[];
}

interface WaterfallBudgetProps {
  budgetData?: {
    infrastructure: {
      total: number;
      streets?: { [key: string]: number };
      utilities?: { total: number };
      parks?: { total: number };
    };
    buildings: {
      total: number;
      [key: string]: number;
    };
    sustainability: {
      total: number;
      [key: string]: number;
    };
    soft_costs: {
      total: number;
      [key: string]: number;
    };
    total: {
      total: number;
      construction: number;
      soft_costs: number;
    };
  };
  unitMetrics?: {
    cost_per_unit: number;
    cost_per_sqm: number;
    total_units: number;
    total_area: number;
  };
}

export const WaterfallBudget: React.FC<WaterfallBudgetProps> = ({
  budgetData,
  unitMetrics
}) => {
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

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'infrastructure':
        return 'bg-blue-500';
      case 'buildings':
        return 'bg-green-500';
      case 'sustainability':
        return 'bg-purple-500';
      case 'soft_costs':
        return 'bg-orange-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'infrastructure':
        return <Wrench size={16} />;
      case 'buildings':
        return <Building size={16} />;
      case 'sustainability':
        return <Leaf size={16} />;
      case 'soft_costs':
        return <FileText size={16} />;
      default:
        return <DollarSign size={16} />;
    }
  };

  const budgetCategories: BudgetCategory[] = budgetData ? [
    {
      name: 'Infrastructure',
      amount: budgetData.infrastructure.total,
      percentage: budgetData.infrastructure.total / budgetData.total.total,
      color: 'bg-blue-500',
      icon: <Wrench size={16} />,
      breakdown: [
        { name: 'Streets', amount: Object.values(budgetData.infrastructure.streets || {}).reduce((a, b) => a + b, 0), percentage: 0 },
        { name: 'Utilities', amount: budgetData.infrastructure.utilities?.total || 0, percentage: 0 },
        { name: 'Parks', amount: budgetData.infrastructure.parks?.total || 0, percentage: 0 }
      ]
    },
    {
      name: 'Buildings',
      amount: budgetData.buildings.total,
      percentage: budgetData.buildings.total / budgetData.total.total,
      color: 'bg-green-500',
      icon: <Building size={16} />,
      breakdown: Object.entries(budgetData.buildings)
        .filter(([key]) => key !== 'total')
        .map(([key, value]) => ({
          name: key.charAt(0).toUpperCase() + key.slice(1).replace('_', ' '),
          amount: value,
          percentage: 0
        }))
    },
    {
      name: 'Sustainability',
      amount: budgetData.sustainability.total,
      percentage: budgetData.sustainability.total / budgetData.total.total,
      color: 'bg-purple-500',
      icon: <Leaf size={16} />,
      breakdown: Object.entries(budgetData.sustainability)
        .filter(([key]) => key !== 'total')
        .map(([key, value]) => ({
          name: key.charAt(0).toUpperCase() + key.slice(1).replace('_', ' '),
          amount: value,
          percentage: 0
        }))
    },
    {
      name: 'Soft Costs',
      amount: budgetData.soft_costs.total,
      percentage: budgetData.soft_costs.total / budgetData.total.total,
      color: 'bg-orange-500',
      icon: <FileText size={16} />,
      breakdown: Object.entries(budgetData.soft_costs)
        .filter(([key]) => key !== 'total')
        .map(([key, value]) => ({
          name: key.charAt(0).toUpperCase() + key.slice(1).replace('_', ' '),
          amount: value,
          percentage: 0
        }))
    }
  ] : [];

  // Calculate breakdown percentages
  budgetCategories.forEach(category => {
    if (category.breakdown) {
      category.breakdown.forEach(item => {
        item.percentage = item.amount / category.amount;
      });
    }
  });

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">Budget Breakdown</h2>
      
      {/* Total Budget Display */}
      <div className="mb-8">
        <div className="text-center">
          <div className="text-3xl font-bold text-gray-900 mb-2">
            {budgetData ? formatCurrency(budgetData.total.total) : '$0'}
          </div>
          <div className="text-sm text-gray-600">Total Project Budget</div>
        </div>
        
        {unitMetrics && (
          <div className="grid grid-cols-2 gap-4 mt-4">
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-lg font-semibold text-gray-900">
                {formatCurrency(unitMetrics.cost_per_unit)}
              </div>
              <div className="text-xs text-gray-600">per unit</div>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-lg font-semibold text-gray-900">
                {formatCurrency(unitMetrics.cost_per_sqm)}
              </div>
              <div className="text-xs text-gray-600">per m²</div>
            </div>
          </div>
        )}
      </div>

      {/* Waterfall Chart */}
      <div className="mb-8">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Cost Distribution</h3>
        
        <div className="space-y-4">
          {budgetCategories.map((category, index) => (
            <div key={index} className="space-y-2">
              {/* Category Header */}
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className={`p-1 rounded ${category.color} text-white`}>
                    {category.icon}
                  </div>
                  <span className="font-medium text-gray-900">{category.name}</span>
                </div>
                <div className="text-right">
                  <div className="font-semibold text-gray-900">
                    {formatCurrency(category.amount)}
                  </div>
                  <div className="text-sm text-gray-600">
                    {formatPercentage(category.percentage)}
                  </div>
                </div>
              </div>
              
              {/* Waterfall Bar */}
              <div className="relative h-8 bg-gray-100 rounded-lg overflow-hidden">
                <div
                  className={`h-full ${category.color} transition-all duration-300`}
                  style={{ width: `${category.percentage * 100}%` }}
                />
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-sm font-medium text-white drop-shadow">
                    {formatCurrency(category.amount)}
                  </span>
                </div>
              </div>
              
              {/* Breakdown */}
              {category.breakdown && category.breakdown.length > 0 && (
                <div className="ml-6 space-y-1">
                  {category.breakdown.map((item, itemIndex) => (
                    <div key={itemIndex} className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">{item.name}</span>
                      <div className="text-right">
                        <span className="font-medium text-gray-900">
                          {formatCurrency(item.amount)}
                        </span>
                        <span className="text-gray-500 ml-2">
                          ({formatPercentage(item.percentage)})
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Construction vs Soft Costs */}
      {budgetData && (
        <div className="mb-8">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Construction vs Soft Costs</h3>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 bg-green-50 rounded-lg">
              <div className="flex items-center space-x-2 mb-2">
                <Building size={20} className="text-green-600" />
                <span className="font-medium text-green-900">Construction</span>
              </div>
              <div className="text-2xl font-bold text-green-900">
                {formatCurrency(budgetData.total.construction)}
              </div>
              <div className="text-sm text-green-700">
                {formatPercentage(budgetData.total.construction / budgetData.total.total)} of total
              </div>
            </div>
            
            <div className="p-4 bg-orange-50 rounded-lg">
              <div className="flex items-center space-x-2 mb-2">
                <FileText size={20} className="text-orange-600" />
                <span className="font-medium text-orange-900">Soft Costs</span>
              </div>
              <div className="text-2xl font-bold text-orange-900">
                {formatCurrency(budgetData.total.soft_costs)}
              </div>
              <div className="text-sm text-orange-700">
                {formatPercentage(budgetData.total.soft_costs / budgetData.total.total)} of total
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Cost Efficiency Metrics */}
      {unitMetrics && (
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-4">Cost Efficiency</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <div className="flex items-center space-x-2 mb-2">
                <TrendingUp size={16} className="text-blue-600" />
                <span className="font-medium text-blue-900">Units</span>
              </div>
              <div className="text-lg font-bold text-blue-900">
                {unitMetrics.total_units.toLocaleString()}
              </div>
              <div className="text-sm text-blue-700">
                Total units
              </div>
            </div>
            
            <div className="p-4 bg-purple-50 rounded-lg">
              <div className="flex items-center space-x-2 mb-2">
                <TrendingDown size={16} className="text-purple-600" />
                <span className="font-medium text-purple-900">Cost/Unit</span>
              </div>
              <div className="text-lg font-bold text-purple-900">
                {formatCurrency(unitMetrics.cost_per_unit)}
              </div>
              <div className="text-sm text-purple-700">
                Per unit cost
              </div>
            </div>
            
            <div className="p-4 bg-indigo-50 rounded-lg">
              <div className="flex items-center space-x-2 mb-2">
                <DollarSign size={16} className="text-indigo-600" />
                <span className="font-medium text-indigo-900">Cost/m²</span>
              </div>
              <div className="text-lg font-bold text-indigo-900">
                {formatCurrency(unitMetrics.cost_per_sqm)}
              </div>
              <div className="text-sm text-indigo-700">
                Per area cost
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
