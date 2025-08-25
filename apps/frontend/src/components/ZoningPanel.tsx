'use client';

import React, { useState } from 'react';
import { Settings, BarChart3, AlertTriangle, CheckCircle } from 'lucide-react';

interface CapacitySummary {
  total_units: number;
  total_population: number;
  total_jobs: number;
  total_floor_area: number;
  total_parking_spaces: number;
  units_by_use: Record<string, number>;
  jobs_by_use: Record<string, number>;
}

interface ZoningValidation {
  valid: boolean;
  issues: Array<{
    parcel_id: string;
    type: string;
    message: string;
  }>;
  warnings: Array<{
    parcel_id: string;
    type: string;
    message: string;
  }>;
  parcels_checked: number;
}

interface ZoningPanelProps {
  capacitySummary?: CapacitySummary;
  validation?: ZoningValidation;
  onCalculateCapacity: () => void;
  onValidateZoning: () => void;
  onApplyDefaults: () => void;
}

export const ZoningPanel: React.FC<ZoningPanelProps> = ({
  capacitySummary,
  validation,
  onCalculateCapacity,
  onValidateZoning,
  onApplyDefaults
}) => {
  const [activeTab, setActiveTab] = useState<'capacity' | 'validation' | 'settings'>('capacity');

  const formatNumber = (num: number) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toLocaleString();
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-900">Zoning & Capacity</h2>
        <div className="flex space-x-2">
          <button
            onClick={onCalculateCapacity}
            className="px-3 py-1 bg-blue-500 text-white text-sm rounded hover:bg-blue-600"
          >
            Calculate
          </button>
          <button
            onClick={onValidateZoning}
            className="px-3 py-1 bg-green-500 text-white text-sm rounded hover:bg-green-600"
          >
            Validate
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex space-x-1 mb-6">
        <button
          onClick={() => setActiveTab('capacity')}
          className={`px-4 py-2 text-sm font-medium rounded-md ${
            activeTab === 'capacity'
              ? 'bg-blue-100 text-blue-700'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          <BarChart3 size={16} className="inline mr-2" />
          Capacity
        </button>
        <button
          onClick={() => setActiveTab('validation')}
          className={`px-4 py-2 text-sm font-medium rounded-md ${
            activeTab === 'validation'
              ? 'bg-blue-100 text-blue-700'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          <AlertTriangle size={16} className="inline mr-2" />
          Validation
        </button>
        <button
          onClick={() => setActiveTab('settings')}
          className={`px-4 py-2 text-sm font-medium rounded-md ${
            activeTab === 'settings'
              ? 'bg-blue-100 text-blue-700'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          <Settings size={16} className="inline mr-2" />
          Settings
        </button>
      </div>

      {/* Capacity Tab */}
      {activeTab === 'capacity' && capacitySummary && (
        <div className="space-y-6">
          {/* Summary Cards */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">
                {formatNumber(capacitySummary.total_units)}
              </div>
              <div className="text-sm text-blue-700">Total Units</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                {formatNumber(capacitySummary.total_population)}
              </div>
              <div className="text-sm text-green-700">Population</div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">
                {formatNumber(capacitySummary.total_jobs)}
              </div>
              <div className="text-sm text-purple-700">Jobs</div>
            </div>
            <div className="bg-orange-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-orange-600">
                {formatNumber(Math.round(capacitySummary.total_floor_area / 1000))}
              </div>
              <div className="text-sm text-orange-700">Floor Area (K m²)</div>
            </div>
          </div>

          {/* Units by Use Type */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Units by Use Type</h3>
            <div className="space-y-2">
              {Object.entries(capacitySummary.units_by_use).map(([useType, units]) => (
                <div key={useType} className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 capitalize">{useType}</span>
                  <span className="text-sm font-medium">{formatNumber(units)}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Jobs by Use Type */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Jobs by Use Type</h3>
            <div className="space-y-2">
              {Object.entries(capacitySummary.jobs_by_use).map(([useType, jobs]) => (
                <div key={useType} className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 capitalize">{useType}</span>
                  <span className="text-sm font-medium">{formatNumber(jobs)}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Validation Tab */}
      {activeTab === 'validation' && validation && (
        <div className="space-y-4">
          {/* Validation Status */}
          <div className={`flex items-center p-4 rounded-lg ${
            validation.valid ? 'bg-green-50' : 'bg-red-50'
          }`}>
            {validation.valid ? (
              <CheckCircle size={20} className="text-green-500 mr-3" />
            ) : (
              <AlertTriangle size={20} className="text-red-500 mr-3" />
            )}
            <div>
              <div className={`font-medium ${
                validation.valid ? 'text-green-800' : 'text-red-800'
              }`}>
                {validation.valid ? 'Zoning is Valid' : 'Zoning Issues Found'}
              </div>
              <div className={`text-sm ${
                validation.valid ? 'text-green-600' : 'text-red-600'
              }`}>
                {validation.parcels_checked} parcels checked
              </div>
            </div>
          </div>

          {/* Issues */}
          {validation.issues.length > 0 && (
            <div>
              <h3 className="text-lg font-medium text-red-800 mb-2">Issues</h3>
              <div className="space-y-2">
                {validation.issues.map((issue, index) => (
                  <div key={index} className="bg-red-50 p-3 rounded border border-red-200">
                    <div className="text-sm font-medium text-red-800">
                      Parcel {issue.parcel_id}
                    </div>
                    <div className="text-sm text-red-600">{issue.message}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Warnings */}
          {validation.warnings.length > 0 && (
            <div>
              <h3 className="text-lg font-medium text-yellow-800 mb-2">Warnings</h3>
              <div className="space-y-2">
                {validation.warnings.map((warning, index) => (
                  <div key={index} className="bg-yellow-50 p-3 rounded border border-yellow-200">
                    <div className="text-sm font-medium text-yellow-800">
                      Parcel {warning.parcel_id}
                    </div>
                    <div className="text-sm text-yellow-600">{warning.message}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Settings Tab */}
      {activeTab === 'settings' && (
        <div className="space-y-4">
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Default Parameters</h3>
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Average Unit Floor Area (m²)
                </label>
                <input
                  type="number"
                  defaultValue="85"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Occupancy (persons per unit)
                </label>
                <input
                  type="number"
                  defaultValue="2.5"
                  step="0.1"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Building Efficiency (%)
                </label>
                <input
                  type="number"
                  defaultValue="85"
                  min="0"
                  max="100"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-gray-200">
            <button
              onClick={onApplyDefaults}
              className="w-full bg-gray-500 text-white px-4 py-2 rounded-md hover:bg-gray-600"
            >
              Apply Defaults to All Parcels
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
