'use client';

import React, { useState } from 'react';
import { Eye, EyeOff, Layers } from 'lucide-react';

interface Layer {
  id: string;
  name: string;
  visible: boolean;
  type: 'parcels' | 'boundaries' | 'roads' | 'context' | 'analysis';
}

interface LayerTogglesProps {
  layers: Layer[];
  onLayerToggle: (layerId: string, visible: boolean) => void;
  onLayerOpacityChange?: (layerId: string, opacity: number) => void;
}

export const LayerToggles: React.FC<LayerTogglesProps> = ({
  layers,
  onLayerToggle,
  onLayerOpacityChange
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [expandedLayer, setExpandedLayer] = useState<string | null>(null);

  const getLayerIcon = (type: Layer['type']) => {
    switch (type) {
      case 'parcels':
        return '🏠';
      case 'boundaries':
        return '📍';
      case 'roads':
        return '🛣️';
      case 'context':
        return '🗺️';
      case 'analysis':
        return '📊';
      default:
        return '📋';
    }
  };

  const getLayerColor = (type: Layer['type']) => {
    switch (type) {
      case 'parcels':
        return 'border-blue-500 bg-blue-50';
      case 'boundaries':
        return 'border-green-500 bg-green-50';
      case 'roads':
        return 'border-red-500 bg-red-50';
      case 'context':
        return 'border-purple-500 bg-purple-50';
      case 'analysis':
        return 'border-orange-500 bg-orange-50';
      default:
        return 'border-gray-500 bg-gray-50';
    }
  };

  return (
    <div className="absolute top-4 right-4">
      {/* Toggle button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="bg-white rounded-lg shadow-lg p-3 hover:bg-gray-50 transition-colors"
        title="Layer Controls"
      >
        <Layers size={20} className="text-gray-600" />
      </button>

      {/* Layer panel */}
      {isOpen && (
        <div className="absolute top-12 right-0 bg-white rounded-lg shadow-lg p-4 min-w-64 max-h-96 overflow-y-auto">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-gray-900">Layers</h3>
            <button
              onClick={() => setIsOpen(false)}
              className="text-gray-400 hover:text-gray-600"
            >
              ×
            </button>
          </div>

          <div className="space-y-2">
            {layers.map((layer) => (
              <div
                key={layer.id}
                className={`border rounded-lg p-3 ${getLayerColor(layer.type)}`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span className="text-lg">{getLayerIcon(layer.type)}</span>
                    <span className="text-sm font-medium text-gray-900">
                      {layer.name}
                    </span>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => setExpandedLayer(
                        expandedLayer === layer.id ? null : layer.id
                      )}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      {expandedLayer === layer.id ? '−' : '+'}
                    </button>
                    
                    <button
                      onClick={() => onLayerToggle(layer.id, !layer.visible)}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      {layer.visible ? (
                        <Eye size={16} />
                      ) : (
                        <EyeOff size={16} />
                      )}
                    </button>
                  </div>
                </div>

                {/* Expanded layer options */}
                {expandedLayer === layer.id && (
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    {onLayerOpacityChange && (
                      <div className="space-y-2">
                        <label className="text-xs text-gray-600">Opacity</label>
                        <input
                          type="range"
                          min="0"
                          max="1"
                          step="0.1"
                          defaultValue="1"
                          onChange={(e) => onLayerOpacityChange(
                            layer.id, 
                            parseFloat(e.target.value)
                          )}
                          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                        />
                      </div>
                    )}
                    
                    <div className="flex items-center justify-between text-xs text-gray-500 mt-2">
                      <span>Type: {layer.type}</span>
                      <span>ID: {layer.id}</span>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Layer groups */}
          <div className="mt-4 pt-4 border-t border-gray-200">
            <div className="space-y-2">
              <button
                onClick={() => layers.forEach(l => onLayerToggle(l.id, true))}
                className="w-full text-xs bg-blue-500 text-white rounded px-3 py-1 hover:bg-blue-600 transition-colors"
              >
                Show All
              </button>
              
              <button
                onClick={() => layers.forEach(l => onLayerToggle(l.id, false))}
                className="w-full text-xs bg-gray-500 text-white rounded px-3 py-1 hover:bg-gray-600 transition-colors"
              >
                Hide All
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
