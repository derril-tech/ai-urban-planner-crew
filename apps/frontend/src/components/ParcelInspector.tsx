'use client';

import React, { useState, useEffect } from 'react';
import { X, Save, RefreshCw } from 'lucide-react';

interface ParcelProperties {
  useMix: Record<string, number>;
  far: number;
  height: number;
  setbacks: Record<string, number>;
  inclusionary: number;
  phase: number;
  lotCoverage: number;
  groundFloorActivation: boolean;
  parkingRatio: number;
  density: number;
}

interface ParcelCapacity {
  units: number;
  population: number;
  jobs: number;
  floor_area: number;
  parking_spaces: number;
  units_by_use: Record<string, number>;
  jobs_by_use: Record<string, number>;
}

interface ParcelInspectorProps {
  parcelId: string;
  properties: ParcelProperties;
  capacity?: ParcelCapacity;
  onClose: () => void;
  onSave: (parcelId: string, properties: ParcelProperties) => void;
  onCalculateCapacity: (parcelId: string) => void;
}

export const ParcelInspector: React.FC<ParcelInspectorProps> = ({
  parcelId,
  properties,
  capacity,
  onClose,
  onSave,
  onCalculateCapacity
}) => {
  const [editedProperties, setEditedProperties] = useState<ParcelProperties>(properties);
  const [isDirty, setIsDirty] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    setEditedProperties(properties);
    setIsDirty(false);
  }, [properties]);

  const handlePropertyChange = (key: keyof ParcelProperties, value: any) => {
    setEditedProperties(prev => ({
      ...prev,
      [key]: value
    }));
    setIsDirty(true);
  };

  const handleUseMixChange = (useType: string, value: number) => {
    const newUseMix = { ...editedProperties.useMix };
    newUseMix[useType] = value;
    
    // Normalize to sum to 1.0
    const total = Object.values(newUseMix).reduce((sum, val) => sum + val, 0);
    if (total > 0) {
      Object.keys(newUseMix).forEach(key => {
        newUseMix[key] = newUseMix[key] / total;
      });
    }
    
    handlePropertyChange('useMix', newUseMix);
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      await onSave(parcelId, editedProperties);
      setIsDirty(false);
    } catch (error) {
      console.error('Error saving parcel:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const totalUseMix = Object.values(editedProperties.useMix).reduce((sum, val) => sum + val, 0);

  return (
    <div className="fixed inset-y-0 right-0 w-96 bg-white shadow-xl border-l border-gray-200 overflow-y-auto">
      <div className="p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold text-gray-900">Parcel Inspector</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <X size={20} />
          </button>
        </div>

        {/* Parcel ID */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Parcel ID
          </label>
          <div className="text-sm text-gray-500 font-mono bg-gray-50 p-2 rounded">
            {parcelId}
          </div>
        </div>

        {/* Use Mix */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Land Use Mix
          </label>
          <div className="space-y-2">
            {Object.entries(editedProperties.useMix).map(([useType, ratio]) => (
              <div key={useType} className="flex items-center space-x-2">
                <label className="text-sm text-gray-600 min-w-20 capitalize">
                  {useType}
                </label>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.01"
                  value={ratio}
                  onChange={(e) => handleUseMixChange(useType, parseFloat(e.target.value))}
                  className="flex-1"
                />
                <span className="text-sm text-gray-500 min-w-12">
                  {(ratio * 100).toFixed(0)}%
                </span>
              </div>
            ))}
          </div>
          <div className={`text-xs mt-1 ${Math.abs(totalUseMix - 1) > 0.01 ? 'text-red-500' : 'text-green-500'}`}>
            Total: {(totalUseMix * 100).toFixed(1)}%
          </div>
        </div>

        {/* FAR and Height */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              FAR
            </label>
            <input
              type="number"
              min="0"
              max="20"
              step="0.1"
              value={editedProperties.far}
              onChange={(e) => handlePropertyChange('far', parseFloat(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Height (m)
            </label>
            <input
              type="number"
              min="0"
              max="200"
              step="0.5"
              value={editedProperties.height}
              onChange={(e) => handlePropertyChange('height', parseFloat(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        {/* Setbacks */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Setbacks (m)
          </label>
          <div className="grid grid-cols-3 gap-2">
            {Object.entries(editedProperties.setbacks).map(([direction, distance]) => (
              <div key={direction}>
                <label className="block text-xs text-gray-600 capitalize mb-1">
                  {direction}
                </label>
                <input
                  type="number"
                  min="0"
                  max="50"
                  step="0.5"
                  value={distance}
                  onChange={(e) => handlePropertyChange('setbacks', {
                    ...editedProperties.setbacks,
                    [direction]: parseFloat(e.target.value)
                  })}
                  className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>
            ))}
          </div>
        </div>

        {/* Other Properties */}
        <div className="space-y-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Inclusionary Housing (%)
            </label>
            <input
              type="number"
              min="0"
              max="100"
              step="1"
              value={editedProperties.inclusionary}
              onChange={(e) => handlePropertyChange('inclusionary', parseFloat(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Lot Coverage (%)
            </label>
            <input
              type="number"
              min="0"
              max="100"
              step="1"
              value={editedProperties.lotCoverage * 100}
              onChange={(e) => handlePropertyChange('lotCoverage', parseFloat(e.target.value) / 100)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Parking Ratio
            </label>
            <input
              type="number"
              min="0"
              max="10"
              step="0.1"
              value={editedProperties.parkingRatio}
              onChange={(e) => handlePropertyChange('parkingRatio', parseFloat(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div className="flex items-center">
            <input
              type="checkbox"
              id="groundFloorActivation"
              checked={editedProperties.groundFloorActivation}
              onChange={(e) => handlePropertyChange('groundFloorActivation', e.target.checked)}
              className="mr-2"
            />
            <label htmlFor="groundFloorActivation" className="text-sm text-gray-700">
              Ground Floor Activation
            </label>
          </div>
        </div>

        {/* Capacity Display */}
        {capacity && (
          <div className="mb-6 p-4 bg-gray-50 rounded-lg">
            <h3 className="text-sm font-medium text-gray-900 mb-3">Capacity</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-600">Units:</span>
                <span className="ml-2 font-medium">{capacity.units}</span>
              </div>
              <div>
                <span className="text-gray-600">Population:</span>
                <span className="ml-2 font-medium">{capacity.population}</span>
              </div>
              <div>
                <span className="text-gray-600">Jobs:</span>
                <span className="ml-2 font-medium">{capacity.jobs}</span>
              </div>
              <div>
                <span className="text-gray-600">Floor Area:</span>
                <span className="ml-2 font-medium">{Math.round(capacity.floor_area)}m²</span>
              </div>
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="flex space-x-2">
          <button
            onClick={handleSave}
            disabled={!isDirty || isSaving}
            className="flex-1 bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            {isSaving ? (
              <RefreshCw size={16} className="animate-spin mr-2" />
            ) : (
              <Save size={16} className="mr-2" />
            )}
            Save
          </button>
          
          <button
            onClick={() => onCalculateCapacity(parcelId)}
            className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
          >
            Calculate
          </button>
        </div>
      </div>
    </div>
  );
};
