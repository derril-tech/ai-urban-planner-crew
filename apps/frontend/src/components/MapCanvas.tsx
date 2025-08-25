'use client';

import React, { useEffect, useRef, useState } from 'react';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

interface MapCanvasProps {
  center?: [number, number];
  zoom?: number;
  onMapLoad?: (map: maplibregl.Map) => void;
  onFeatureClick?: (feature: any) => void;
  onFeatureHover?: (feature: any) => void;
  layers?: Array<{
    id: string;
    type: 'fill' | 'line' | 'circle' | 'symbol';
    source: {
      type: 'geojson';
      data: any;
    };
    paint?: any;
    layout?: any;
  }>;
}

export const MapCanvas: React.FC<MapCanvasProps> = ({
  center = [-74.006, 40.7128], // Default to NYC
  zoom = 12,
  onMapLoad,
  onFeatureClick,
  onFeatureHover,
  layers = []
}) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const [mapLoaded, setMapLoaded] = useState(false);

  useEffect(() => {
    if (!mapContainer.current) return;

    // Initialize map
    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          'osm': {
            type: 'raster',
            tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
            tileSize: 256,
            attribution: '© OpenStreetMap contributors'
          }
        },
        layers: [
          {
            id: 'osm-tiles',
            type: 'raster',
            source: 'osm',
            minzoom: 0,
            maxzoom: 22
          }
        ]
      },
      center,
      zoom,
      attributionControl: true
    });

    // Add navigation controls
    map.current.addControl(new maplibregl.NavigationControl(), 'top-right');

    // Add fullscreen control
    map.current.addControl(new maplibregl.FullscreenControl(), 'top-right');

    // Handle map load
    map.current.on('load', () => {
      setMapLoaded(true);
      onMapLoad?.(map.current!);
    });

    // Handle feature clicks
    if (onFeatureClick) {
      map.current.on('click', (e) => {
        const features = map.current!.queryRenderedFeatures(e.point);
        if (features.length > 0) {
          onFeatureClick(features[0]);
        }
      });
    }

    // Handle feature hover
    if (onFeatureHover) {
      map.current.on('mousemove', (e) => {
        const features = map.current!.queryRenderedFeatures(e.point);
        if (features.length > 0) {
          onFeatureHover(features[0]);
        }
      });
    }

    return () => {
      if (map.current) {
        map.current.remove();
      }
    };
  }, []);

  // Add layers when map is loaded
  useEffect(() => {
    if (!mapLoaded || !map.current) return;

    layers.forEach(layer => {
      // Add source if it doesn't exist
      if (!map.current!.getSource(layer.id)) {
        map.current!.addSource(layer.id, layer.source);
      }

      // Add layer if it doesn't exist
      if (!map.current!.getLayer(layer.id)) {
        map.current!.addLayer({
          id: layer.id,
          type: layer.type,
          source: layer.id,
          paint: layer.paint || {},
          layout: layer.layout || {}
        });
      }
    });
  }, [mapLoaded, layers]);

  return (
    <div className="relative w-full h-full">
      <div 
        ref={mapContainer} 
        className="w-full h-full rounded-lg shadow-lg"
      />
      {!mapLoaded && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-100 bg-opacity-75">
          <div className="text-gray-600">Loading map...</div>
        </div>
      )}
    </div>
  );
};
