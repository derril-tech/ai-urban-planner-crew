'use client';

import React from 'react';
import { Zap, Car, Building, Droplets, Package, Shield, TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface CategoryScore {
  score: number;
  grade: string;
  metrics: {
    [key: string]: {
      value: number;
      score: number;
    };
  };
}

interface CategoryScorecardsProps {
  categoryScores?: {
    energy: CategoryScore;
    mobility: CategoryScore;
    land_use: CategoryScore;
    water: CategoryScore;
    materials: CategoryScore;
    resilience: CategoryScore;
  };
  weights?: {
    energy: number;
    mobility: number;
    land_use: number;
    water: number;
    materials: number;
    resilience: number;
  };
  onCategoryClick?: (category: string) => void;
}

export const CategoryScorecards: React.FC<CategoryScorecardsProps> = ({
  categoryScores,
  weights,
  onCategoryClick
}) => {
  const formatPercentage = (value: number) => {
    return (value * 100).toFixed(1) + '%';
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toLocaleString();
  };

  const getGradeColor = (grade: string) => {
    switch (grade) {
      case 'A+':
      case 'A':
      case 'A-':
        return 'text-green-600 bg-green-50 border-green-200';
      case 'B+':
      case 'B':
      case 'B-':
        return 'text-blue-600 bg-blue-50 border-blue-200';
      case 'C+':
      case 'C':
      case 'C-':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'D+':
      case 'D':
        return 'text-orange-600 bg-orange-50 border-orange-200';
      case 'F':
        return 'text-red-600 bg-red-50 border-red-200';
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-blue-600';
    if (score >= 40) return 'text-yellow-600';
    if (score >= 20) return 'text-orange-600';
    return 'text-red-600';
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'energy':
        return <Zap size={20} />;
      case 'mobility':
        return <Car size={20} />;
      case 'land_use':
        return <Building size={20} />;
      case 'water':
        return <Droplets size={20} />;
      case 'materials':
        return <Package size={20} />;
      case 'resilience':
        return <Shield size={20} />;
      default:
        return <TrendingUp size={20} />;
    }
  };

  const getCategoryName = (category: string) => {
    switch (category) {
      case 'energy':
        return 'Energy';
      case 'mobility':
        return 'Mobility';
      case 'land_use':
        return 'Land Use';
      case 'water':
        return 'Water';
      case 'materials':
        return 'Materials';
      case 'resilience':
        return 'Resilience';
      default:
        return category.charAt(0).toUpperCase() + category.slice(1).replace('_', ' ');
    }
  };

  const getMetricName = (metric: string) => {
    return metric.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  };

  const getMetricValue = (metric: string, value: number) => {
    if (metric.includes('ratio') || metric.includes('percent') || metric.includes('efficiency')) {
      return formatPercentage(value);
    } else if (metric.includes('density')) {
      return formatNumber(value) + ' per km²';
    } else if (metric.includes('reduction')) {
      return formatPercentage(value);
    } else {
      return formatNumber(value);
    }
  };

  const categories = [
    { key: 'energy', name: 'Energy', weight: weights?.energy || 0.25 },
    { key: 'mobility', name: 'Mobility', weight: weights?.mobility || 0.20 },
    { key: 'land_use', name: 'Land Use', weight: weights?.land_use || 0.20 },
    { key: 'water', name: 'Water', weight: weights?.water || 0.15 },
    { key: 'materials', name: 'Materials', weight: weights?.materials || 0.10 },
    { key: 'resilience', name: 'Resilience', weight: weights?.resilience || 0.10 }
  ];

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">Sustainability Categories</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {categories.map((category) => {
          const scoreData = categoryScores?.[category.key as keyof typeof categoryScores];
          
          if (!scoreData) {
            return (
              <div
                key={category.key}
                className="p-4 border-2 border-dashed border-gray-300 rounded-lg text-center"
                onClick={() => onCategoryClick?.(category.key)}
              >
                <div className="text-gray-400 mb-2">
                  {getCategoryIcon(category.key)}
                </div>
                <h3 className="font-medium text-gray-500">{category.name}</h3>
                <p className="text-sm text-gray-400">No data available</p>
              </div>
            );
          }

          return (
            <div
              key={category.key}
              className={`p-4 border-2 rounded-lg cursor-pointer transition-all duration-200 hover:shadow-md ${getGradeColor(scoreData.grade)}`}
              onClick={() => onCategoryClick?.(category.key)}
            >
              {/* Category Header */}
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-2">
                  {getCategoryIcon(category.key)}
                  <h3 className="font-semibold">{category.name}</h3>
                </div>
                <div className="text-right">
                  <div className={`text-2xl font-bold ${getScoreColor(scoreData.score)}`}>
                    {scoreData.score.toFixed(0)}
                  </div>
                  <div className="text-sm opacity-75">
                    {formatPercentage(category.weight)} weight
                  </div>
                </div>
              </div>

              {/* Grade Badge */}
              <div className="mb-4">
                <span className={`inline-block px-2 py-1 rounded text-sm font-medium ${getGradeColor(scoreData.grade)}`}>
                  Grade: {scoreData.grade}
                </span>
              </div>

              {/* Metrics Breakdown */}
              <div className="space-y-2">
                {Object.entries(scoreData.metrics).map(([metricKey, metricData]) => (
                  <div key={metricKey} className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">
                      {getMetricName(metricKey)}
                    </span>
                    <div className="text-right">
                      <div className="font-medium">
                        {getMetricValue(metricKey, metricData.value)}
                      </div>
                      <div className={`text-xs ${getScoreColor(metricData.score)}`}>
                        {metricData.score.toFixed(0)} pts
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Progress Bar */}
              <div className="mt-4">
                <div className="flex items-center justify-between text-xs text-gray-500 mb-1">
                  <span>Score</span>
                  <span>{scoreData.score.toFixed(0)}/100</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all duration-300 ${getScoreColor(scoreData.score).replace('text-', 'bg-')}`}
                    style={{ width: `${scoreData.score}%` }}
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Summary Section */}
      {categoryScores && (
        <div className="mt-8 pt-6 border-t border-gray-200">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Category Summary</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Best Performing Categories */}
            <div className="bg-green-50 p-4 rounded-lg">
              <h4 className="font-medium text-green-900 mb-3">Top Performers</h4>
              <div className="space-y-2">
                {Object.entries(categoryScores)
                  .sort(([, a], [, b]) => b.score - a.score)
                  .slice(0, 3)
                  .map(([category, score]) => (
                    <div key={category} className="flex items-center justify-between">
                      <span className="text-sm text-green-700">
                        {getCategoryName(category)}
                      </span>
                      <div className="flex items-center space-x-2">
                        <span className="text-sm font-medium text-green-900">
                          {score.score.toFixed(0)}
                        </span>
                        <span className="text-xs text-green-600">
                          {score.grade}
                        </span>
                      </div>
                    </div>
                  ))}
              </div>
            </div>

            {/* Areas for Improvement */}
            <div className="bg-orange-50 p-4 rounded-lg">
              <h4 className="font-medium text-orange-900 mb-3">Areas for Improvement</h4>
              <div className="space-y-2">
                {Object.entries(categoryScores)
                  .sort(([, a], [, b]) => a.score - b.score)
                  .slice(0, 3)
                  .map(([category, score]) => (
                    <div key={category} className="flex items-center justify-between">
                      <span className="text-sm text-orange-700">
                        {getCategoryName(category)}
                      </span>
                      <div className="flex items-center space-x-2">
                        <span className="text-sm font-medium text-orange-900">
                          {score.score.toFixed(0)}
                        </span>
                        <span className="text-xs text-orange-600">
                          {score.grade}
                        </span>
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          </div>

          {/* Weight Distribution */}
          {weights && (
            <div className="mt-6">
              <h4 className="font-medium text-gray-900 mb-3">Category Weights</h4>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
                {categories.map((category) => (
                  <div key={category.key} className="text-center p-3 bg-gray-50 rounded-lg">
                    <div className="text-sm font-medium text-gray-900">
                      {category.name}
                    </div>
                    <div className="text-lg font-bold text-blue-600">
                      {formatPercentage(category.weight)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
