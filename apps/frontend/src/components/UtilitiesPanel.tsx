'use client';

import React, { useState } from 'react';
import { Zap, Sun, Battery, TrendingDown, DollarSign } from 'lucide-react';

interface EnergyDemand {
  total_demand_kwh_day: number;
  total_demand_kwh_year: number;
  demand_by_use: Record<string, number>;
  avg_demand_per_unit: number;
}

interface SolarAnalysis {
  total_annual_energy_kwh: number;
  total_roof_area_m2: number;
  total_system_size_kw: number;
  avg_system_size_kw: number;
  solar_by_parcel: Array<{
    parcel_id: string;
    roof_area: number;
    available_area: number;
    system_size_kw: number;
    daily_energy_kwh: number;
    annual_energy_kwh: number;
  }>;
}

interface StorageAnalysis {
  daily_deficit_kwh: number;
  daily_surplus_kwh: number;
  storage_capacity_kwh: number;
  battery_power_kw: number;
  solar_cost_usd: number;
  battery_cost_usd: number;
  total_cost_usd: number;
  energy_self_sufficiency: number;
}

interface EmissionsAnalysis {
  grid_emissions_kg_co2_year: number;
  solar_emissions_kg_co2_year: number;
  emissions_reduction_kg_co2_year: number;
  emissions_reduction_percent: number;
  trees_equivalent: number;
  carbon_offset_value_usd: number;
}

interface UtilitiesPanelProps {
  energyDemand?: EnergyDemand;
  solarAnalysis?: SolarAnalysis;
  storageAnalysis?: StorageAnalysis;
  emissionsAnalysis?: EmissionsAnalysis;
  onAnalyzeEnergy: () => void;
}

export const UtilitiesPanel: React.FC<UtilitiesPanelProps> = ({
  energyDemand,
  solarAnalysis,
  storageAnalysis,
  emissionsAnalysis,
  onAnalyzeEnergy
}) => {
  const [activeTab, setActiveTab] = useState<'demand' | 'solar' | 'storage' | 'emissions'>('demand');

  const formatNumber = (num: number) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toLocaleString();
  };

  const formatEnergy = (kwh: number) => {
    if (kwh >= 1000000) {
      return (kwh / 1000000).toFixed(1) + ' GWh';
    } else if (kwh >= 1000) {
      return (kwh / 1000).toFixed(1) + ' MWh';
    }
    return Math.round(kwh) + ' kWh';
  };

  const formatPower = (kw: number) => {
    if (kw >= 1000) {
      return (kw / 1000).toFixed(1) + ' MW';
    }
    return Math.round(kw) + ' kW';
  };

  const formatCurrency = (usd: number) => {
    if (usd >= 1000000) {
      return '$' + (usd / 1000000).toFixed(1) + 'M';
    } else if (usd >= 1000) {
      return '$' + (usd / 1000).toFixed(1) + 'K';
    }
    return '$' + Math.round(usd).toLocaleString();
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-900">Utilities & Energy</h2>
        <button
          onClick={onAnalyzeEnergy}
          className="px-3 py-1 bg-blue-500 text-white text-sm rounded hover:bg-blue-600"
        >
          Analyze Energy
        </button>
      </div>

      {/* Tabs */}
      <div className="flex space-x-1 mb-6">
        <button
          onClick={() => setActiveTab('demand')}
          className={`px-4 py-2 text-sm font-medium rounded-md ${
            activeTab === 'demand'
              ? 'bg-blue-100 text-blue-700'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          <Zap size={16} className="inline mr-2" />
          Demand
        </button>
        <button
          onClick={() => setActiveTab('solar')}
          className={`px-4 py-2 text-sm font-medium rounded-md ${
            activeTab === 'solar'
              ? 'bg-blue-100 text-blue-700'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          <Sun size={16} className="inline mr-2" />
          Solar
        </button>
        <button
          onClick={() => setActiveTab('storage')}
          className={`px-4 py-2 text-sm font-medium rounded-md ${
            activeTab === 'storage'
              ? 'bg-blue-100 text-blue-700'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          <Battery size={16} className="inline mr-2" />
          Storage
        </button>
        <button
          onClick={() => setActiveTab('emissions')}
          className={`px-4 py-2 text-sm font-medium rounded-md ${
            activeTab === 'emissions'
              ? 'bg-blue-100 text-blue-700'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          <TrendingDown size={16} className="inline mr-2" />
          Emissions
        </button>
      </div>

      {/* Demand Tab */}
      {activeTab === 'demand' && energyDemand && (
        <div className="space-y-6">
          {/* Demand Summary Cards */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">
                {formatEnergy(energyDemand.total_demand_kwh_day)}
              </div>
              <div className="text-sm text-blue-700">Daily Energy Demand</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                {formatEnergy(energyDemand.total_demand_kwh_year)}
              </div>
              <div className="text-sm text-green-700">Annual Energy Demand</div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">
                {formatEnergy(energyDemand.avg_demand_per_unit)}
              </div>
              <div className="text-sm text-purple-700">Avg per Unit/Day</div>
            </div>
            <div className="bg-orange-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-orange-600">
                {Math.round(energyDemand.total_demand_kwh_day / 30)}
              </div>
              <div className="text-sm text-orange-700">Avg per Unit/Month</div>
            </div>
          </div>

          {/* Demand by Use Type */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Demand by Use Type</h3>
            <div className="space-y-2">
              {Object.entries(energyDemand.demand_by_use).map(([useType, demand]) => (
                <div key={useType} className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 capitalize">{useType}</span>
                  <span className="text-sm font-medium">{formatEnergy(demand)}/day</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Solar Tab */}
      {activeTab === 'solar' && solarAnalysis && (
        <div className="space-y-6">
          {/* Solar Summary Cards */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">
                {formatEnergy(solarAnalysis.total_annual_energy_kwh)}
              </div>
              <div className="text-sm text-blue-700">Annual Solar Generation</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                {formatPower(solarAnalysis.total_system_size_kw)}
              </div>
              <div className="text-sm text-green-700">Total System Size</div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">
                {Math.round(solarAnalysis.total_roof_area_m2)} m²
              </div>
              <div className="text-sm text-purple-700">Total Roof Area</div>
            </div>
            <div className="bg-orange-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-orange-600">
                {formatPower(solarAnalysis.avg_system_size_kw)}
              </div>
              <div className="text-sm text-orange-700">Avg System per Parcel</div>
            </div>
          </div>

          {/* Solar Potential Distribution */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Solar Potential by Parcel</h3>
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {solarAnalysis.solar_by_parcel.slice(0, 10).map((parcel) => (
                <div key={parcel.parcel_id} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                  <span className="text-sm text-gray-600 font-mono">
                    {parcel.parcel_id.slice(0, 8)}...
                  </span>
                  <div className="text-right">
                    <div className="text-sm font-medium">{formatPower(parcel.system_size_kw)}</div>
                    <div className="text-xs text-gray-500">{formatEnergy(parcel.annual_energy_kwh)}/year</div>
                  </div>
                </div>
              ))}
              {solarAnalysis.solar_by_parcel.length > 10 && (
                <div className="text-sm text-gray-500 text-center">
                  +{solarAnalysis.solar_by_parcel.length - 10} more parcels
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Storage Tab */}
      {activeTab === 'storage' && storageAnalysis && (
        <div className="space-y-6">
          {/* Storage Summary Cards */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">
                {formatEnergy(storageAnalysis.storage_capacity_kwh)}
              </div>
              <div className="text-sm text-blue-700">Storage Capacity</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                {formatPower(storageAnalysis.battery_power_kw)}
              </div>
              <div className="text-sm text-green-700">Battery Power</div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">
                {(storageAnalysis.energy_self_sufficiency * 100).toFixed(1)}%
              </div>
              <div className="text-sm text-purple-700">Energy Self-Sufficiency</div>
            </div>
            <div className="bg-orange-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-orange-600">
                {formatEnergy(storageAnalysis.daily_surplus_kwh)}
              </div>
              <div className="text-sm text-orange-700">Daily Energy Surplus</div>
            </div>
          </div>

          {/* Cost Analysis */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Cost Analysis</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Solar System Cost</span>
                <span className="text-sm font-medium">{formatCurrency(storageAnalysis.solar_cost_usd)}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Battery Storage Cost</span>
                <span className="text-sm font-medium">{formatCurrency(storageAnalysis.battery_cost_usd)}</span>
              </div>
              <div className="border-t border-gray-200 pt-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-900">Total System Cost</span>
                  <span className="text-sm font-bold text-gray-900">{formatCurrency(storageAnalysis.total_cost_usd)}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Energy Balance */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Energy Balance</h3>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Daily Energy Deficit</span>
                <span className="text-sm font-medium">{formatEnergy(storageAnalysis.daily_deficit_kwh)}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Daily Energy Surplus</span>
                <span className="text-sm font-medium">{formatEnergy(storageAnalysis.daily_surplus_kwh)}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Emissions Tab */}
      {activeTab === 'emissions' && emissionsAnalysis && (
        <div className="space-y-6">
          {/* Emissions Summary Cards */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-red-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-red-600">
                {formatNumber(emissionsAnalysis.grid_emissions_kg_co2_year)}
              </div>
              <div className="text-sm text-red-700">Grid Emissions (kg CO₂/year)</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                {formatNumber(emissionsAnalysis.emissions_reduction_kg_co2_year)}
              </div>
              <div className="text-sm text-green-700">Emissions Reduction (kg CO₂/year)</div>
            </div>
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">
                {emissionsAnalysis.emissions_reduction_percent.toFixed(1)}%
              </div>
              <div className="text-sm text-blue-700">Emissions Reduction</div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">
                {formatNumber(emissionsAnalysis.trees_equivalent)}
              </div>
              <div className="text-sm text-purple-700">Trees Equivalent</div>
            </div>
          </div>

          {/* Carbon Offset Value */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Carbon Offset Value</h3>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                {formatCurrency(emissionsAnalysis.carbon_offset_value_usd)}
              </div>
              <div className="text-sm text-green-700">Annual Carbon Offset Value</div>
            </div>
          </div>

          {/* Environmental Impact */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Environmental Impact</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Grid Emissions</span>
                <span className="text-sm font-medium text-red-600">
                  {formatNumber(emissionsAnalysis.grid_emissions_kg_co2_year)} kg CO₂/year
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Solar Manufacturing Emissions</span>
                <span className="text-sm font-medium text-orange-600">
                  {formatNumber(emissionsAnalysis.solar_emissions_kg_co2_year)} kg CO₂/year
                </span>
              </div>
              <div className="border-t border-gray-200 pt-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-900">Net Emissions Reduction</span>
                  <span className="text-sm font-bold text-green-600">
                    {formatNumber(emissionsAnalysis.emissions_reduction_kg_co2_year)} kg CO₂/year
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
