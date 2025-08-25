// Created automatically by Cursor AI (2025-08-25)

export interface Plan {
  id: string;
  name: string;
  description?: string;
  createdAt: string;
  updatedAt: string;
}

export interface Scenario {
  id: string;
  planId: string;
  name: string;
  description?: string;
  createdAt: string;
  updatedAt: string;
}

export interface GeoJSON {
  type: 'FeatureCollection' | 'Feature' | 'Geometry';
  features?: any[];
  geometry?: any;
  properties?: Record<string, any>;
}

export interface Parcel {
  id: string;
  scenarioId: string;
  geometry: GeoJSON;
  properties: {
    useMix: Record<string, number>;
    far: number;
    height: number;
    setbacks: Record<string, number>;
    inclusionary: number;
    phase: number;
  };
}
