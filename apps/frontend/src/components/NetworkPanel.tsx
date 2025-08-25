'use client';

import React, { useState } from 'react';
import { Network, BarChart3, Map, TrendingUp } from 'lucide-react';

interface NetworkMetrics {
  total_length: number;
  avg_link_length: number;
  node_count: number;
  edge_count: number;
  connectivity_ratio: number;
  network_density: number;
  avg_degree: number;
  avg_betweenness_centrality: number;
  link_class_distribution: Record<string, number>;
}

interface BlockStats {
  total_blocks: number;
  avg_block_area: number;
  median_block_area: number;
  min_block_area: number;
  max_block_area: number;
  avg_block_perimeter: number;
  block_size_distribution: {
    small: number;
    medium: number;
    large: number;
  };
}

interface IntersectionDensity {
  intersection_count: number;
  total_network_length: number;
  intersection_density: number;
  avg_distance_between_intersections: number;
}

interface NetworkPanelProps {
  networkMetrics?: NetworkMetrics;
  blockStats?: BlockStats;
  intersectionDensity?: IntersectionDensity;
  onAnalyzeNetwork: () => void;
}

export const NetworkPanel: React.FC<NetworkPanelProps> = ({
  networkMetrics,
  blockStats,
  intersectionDensity,
  onAnalyzeNetwork
}) => {
  const [activeTab, setActiveTab] = useState<'network' | 'blocks' | 'intersections'>('network');

  const formatNumber = (num: number) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toLocaleString();
  };

  const formatDistance = (meters: number) => {
    if (meters >= 1000) {
      return (meters / 1000).toFixed(1) + ' km';
    }
    return Math.round(meters) + ' m';
  };

  const formatArea = (sqMeters: number) => {
    if (sqMeters >= 10000) {
      return (sqMeters / 10000).toFixed(1) + ' ha';
    }
    return Math.round(sqMeters) + ' m²';
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-900">Network & Mobility</h2>
        <button
          onClick={onAnalyzeNetwork}
          className="px-3 py-1 bg-blue-500 text-white text-sm rounded hover:bg-blue-600"
        >
          Analyze Network
        </button>
      </div>

      {/* Tabs */}
      <div className="flex space-x-1 mb-6">
        <button
          onClick={() => setActiveTab('network')}
          className={`px-4 py-2 text-sm font-medium rounded-md ${
            activeTab === 'network'
              ? 'bg-blue-100 text-blue-700'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          <Network size={16} className="inline mr-2" />
          Network
        </button>
        <button
          onClick={() => setActiveTab('blocks')}
          className={`px-4 py-2 text-sm font-medium rounded-md ${
            activeTab === 'blocks'
              ? 'bg-blue-100 text-blue-700'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          <Map size={16} className="inline mr-2" />
          Blocks
        </button>
        <button
          onClick={() => setActiveTab('intersections')}
          className={`px-4 py-2 text-sm font-medium rounded-md ${
            activeTab === 'intersections'
              ? 'bg-blue-100 text-blue-700'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          <BarChart3 size={16} className="inline mr-2" />
          Intersections
        </button>
      </div>

      {/* Network Tab */}
      {activeTab === 'network' && networkMetrics && (
        <div className="space-y-6">
          {/* Network Summary Cards */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">
                {formatDistance(networkMetrics.total_length)}
              </div>
              <div className="text-sm text-blue-700">Total Network Length</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                {networkMetrics.node_count}
              </div>
              <div className="text-sm text-green-700">Intersections</div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">
                {networkMetrics.edge_count}
              </div>
              <div className="text-sm text-purple-700">Street Segments</div>
            </div>
            <div className="bg-orange-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-orange-600">
                {formatDistance(networkMetrics.avg_link_length)}
              </div>
              <div className="text-sm text-orange-700">Avg Segment Length</div>
            </div>
          </div>

          {/* Network Quality Metrics */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Network Quality</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-50 p-3 rounded">
                <div className="text-sm text-gray-600">Connectivity Ratio</div>
                <div className="text-lg font-semibold">
                  {(networkMetrics.connectivity_ratio * 100).toFixed(1)}%
                </div>
              </div>
              <div className="bg-gray-50 p-3 rounded">
                <div className="text-sm text-gray-600">Network Density</div>
                <div className="text-lg font-semibold">
                  {(networkMetrics.network_density * 100).toFixed(1)}%
                </div>
              </div>
              <div className="bg-gray-50 p-3 rounded">
                <div className="text-sm text-gray-600">Average Degree</div>
                <div className="text-lg font-semibold">
                  {networkMetrics.avg_degree.toFixed(1)}
                </div>
              </div>
              <div className="bg-gray-50 p-3 rounded">
                <div className="text-sm text-gray-600">Betweenness Centrality</div>
                <div className="text-lg font-semibold">
                  {networkMetrics.avg_betweenness_centrality.toFixed(3)}
                </div>
              </div>
            </div>
          </div>

          {/* Link Class Distribution */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Street Hierarchy</h3>
            <div className="space-y-2">
              {Object.entries(networkMetrics.link_class_distribution).map(([linkClass, count]) => (
                <div key={linkClass} className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 capitalize">{linkClass}</span>
                  <span className="text-sm font-medium">{count} segments</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Blocks Tab */}
      {activeTab === 'blocks' && blockStats && (
        <div className="space-y-6">
          {/* Block Summary Cards */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">
                {blockStats.total_blocks}
              </div>
              <div className="text-sm text-blue-700">Total Blocks</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                {formatArea(blockStats.avg_block_area)}
              </div>
              <div className="text-sm text-green-700">Average Block Size</div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">
                {formatArea(blockStats.median_block_area)}
              </div>
              <div className="text-sm text-purple-700">Median Block Size</div>
            </div>
            <div className="bg-orange-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-orange-600">
                {formatDistance(blockStats.avg_block_perimeter)}
              </div>
              <div className="text-sm text-orange-700">Avg Block Perimeter</div>
            </div>
          </div>

          {/* Block Size Distribution */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Block Size Distribution</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Small Blocks (&lt; 1000 m²)</span>
                <span className="text-sm font-medium">{blockStats.block_size_distribution.small}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Medium Blocks (1000-10000 m²)</span>
                <span className="text-sm font-medium">{blockStats.block_size_distribution.medium}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Large Blocks (&gt; 10000 m²)</span>
                <span className="text-sm font-medium">{blockStats.block_size_distribution.large}</span>
              </div>
            </div>
          </div>

          {/* Block Size Range */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Block Size Range</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-50 p-3 rounded">
                <div className="text-sm text-gray-600">Smallest Block</div>
                <div className="text-lg font-semibold">{formatArea(blockStats.min_block_area)}</div>
              </div>
              <div className="bg-gray-50 p-3 rounded">
                <div className="text-sm text-gray-600">Largest Block</div>
                <div className="text-lg font-semibold">{formatArea(blockStats.max_block_area)}</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Intersections Tab */}
      {activeTab === 'intersections' && intersectionDensity && (
        <div className="space-y-6">
          {/* Intersection Summary Cards */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">
                {intersectionDensity.intersection_count}
              </div>
              <div className="text-sm text-blue-700">Total Intersections</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                {intersectionDensity.intersection_density.toFixed(1)}
              </div>
              <div className="text-sm text-green-700">Intersections per km</div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">
                {formatDistance(intersectionDensity.avg_distance_between_intersections)}
              </div>
              <div className="text-sm text-purple-700">Avg Distance Between</div>
            </div>
            <div className="bg-orange-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-orange-600">
                {formatDistance(intersectionDensity.total_network_length)}
              </div>
              <div className="text-sm text-orange-700">Total Network Length</div>
            </div>
          </div>

          {/* Walkability Assessment */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Walkability Assessment</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Intersection Density</span>
                <span className={`text-sm font-medium ${
                  intersectionDensity.intersection_density >= 100 ? 'text-green-600' :
                  intersectionDensity.intersection_density >= 50 ? 'text-yellow-600' : 'text-red-600'
                }`}>
                  {intersectionDensity.intersection_density.toFixed(1)} per km
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Average Block Size</span>
                <span className={`text-sm font-medium ${
                  blockStats && blockStats.avg_block_area <= 10000 ? 'text-green-600' :
                  blockStats && blockStats.avg_block_area <= 20000 ? 'text-yellow-600' : 'text-red-600'
                }`}>
                  {blockStats ? formatArea(blockStats.avg_block_area) : 'N/A'}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Network Connectivity</span>
                <span className={`text-sm font-medium ${
                  networkMetrics && networkMetrics.connectivity_ratio >= 1.5 ? 'text-green-600' :
                  networkMetrics && networkMetrics.connectivity_ratio >= 1.0 ? 'text-yellow-600' : 'text-red-600'
                }`}>
                  {networkMetrics ? (networkMetrics.connectivity_ratio * 100).toFixed(1) + '%' : 'N/A'}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
