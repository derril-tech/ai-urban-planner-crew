'use client';

import React from 'react';
import { Map, Draw } from 'maplibre-gl-draw';
import 'maplibre-gl-draw/dist/maplibre-gl-draw.css';
import { 
  Square, 
  Circle, 
  Type, 
  MousePointer, 
  Trash2, 
  Undo, 
  Redo 
} from 'lucide-react';

interface DrawToolbarProps {
  map: Map | null;
  onDrawCreate?: (event: any) => void;
  onDrawUpdate?: (event: any) => void;
  onDrawDelete?: (event: any) => void;
}

export const DrawToolbar: React.FC<DrawToolbarProps> = ({
  map,
  onDrawCreate,
  onDrawUpdate,
  onDrawDelete
}) => {
  const drawRef = React.useRef<Draw | null>(null);
  const [activeMode, setActiveMode] = React.useState<string>('simple_select');

  React.useEffect(() => {
    if (!map) return;

    // Initialize draw control
    drawRef.current = new Draw({
      displayControlsDefault: false,
      controls: {
        polygon: true,
        trash: true,
        undo: true,
        redo: true
      },
      styles: [
        // Polygon fill
        {
          id: 'gl-draw-polygon-fill-active',
          type: 'fill',
          filter: ['all', ['==', 'active', 'true'], ['==', '$type', 'Polygon']],
          paint: {
            'fill-color': '#3bb2d0',
            'fill-outline-color': '#3bb2d0',
            'fill-opacity': 0.1
          }
        },
        // Polygon outline
        {
          id: 'gl-draw-polygon-stroke-active',
          type: 'line',
          filter: ['all', ['==', 'active', 'true'], ['==', '$type', 'Polygon']],
          layout: {
            'line-cap': 'round',
            'line-join': 'round'
          },
          paint: {
            'line-color': '#3bb2d0',
            'line-dasharray': [0.2, 2],
            'line-width': 2
          }
        },
        // Polygon vertices
        {
          id: 'gl-draw-polygon-and-line-vertex-active',
          type: 'circle',
          filter: ['all', ['==', 'meta', 'vertex'], ['==', '$type', 'Point'], ['!=', 'mode', 'static']],
          paint: {
            'circle-radius': 5,
            'circle-color': '#fff',
            'circle-stroke-color': '#3bb2d0',
            'circle-stroke-width': 2
          }
        }
      ]
    });

    map.addControl(drawRef.current);

    // Add event listeners
    if (onDrawCreate) {
      map.on('draw.create', onDrawCreate);
    }
    if (onDrawUpdate) {
      map.on('draw.update', onDrawUpdate);
    }
    if (onDrawDelete) {
      map.on('draw.delete', onDrawDelete);
    }

    // Track mode changes
    map.on('draw.modechange', (e) => {
      setActiveMode(e.mode);
    });

    return () => {
      if (drawRef.current) {
        map.removeControl(drawRef.current);
      }
    };
  }, [map, onDrawCreate, onDrawUpdate, onDrawDelete]);

  const setMode = (mode: string) => {
    if (drawRef.current) {
      drawRef.current.changeMode(mode);
    }
  };

  const deleteAll = () => {
    if (drawRef.current) {
      drawRef.current.deleteAll();
    }
  };

  const undo = () => {
    if (drawRef.current) {
      drawRef.current.undo();
    }
  };

  const redo = () => {
    if (drawRef.current) {
      drawRef.current.redo();
    }
  };

  return (
    <div className="absolute top-4 left-4 bg-white rounded-lg shadow-lg p-2 flex flex-col gap-1">
      <button
        onClick={() => setMode('simple_select')}
        className={`p-2 rounded hover:bg-gray-100 transition-colors ${
          activeMode === 'simple_select' ? 'bg-blue-100 text-blue-600' : 'text-gray-600'
        }`}
        title="Select"
      >
        <MousePointer size={20} />
      </button>
      
      <button
        onClick={() => setMode('draw_polygon')}
        className={`p-2 rounded hover:bg-gray-100 transition-colors ${
          activeMode === 'draw_polygon' ? 'bg-blue-100 text-blue-600' : 'text-gray-600'
        }`}
        title="Draw Polygon"
      >
        <Square size={20} />
      </button>
      
      <button
        onClick={() => setMode('draw_circle')}
        className={`p-2 rounded hover:bg-gray-100 transition-colors ${
          activeMode === 'draw_circle' ? 'bg-blue-100 text-blue-600' : 'text-gray-600'
        }`}
        title="Draw Circle"
      >
        <Circle size={20} />
      </button>
      
      <button
        onClick={() => setMode('draw_point')}
        className={`p-2 rounded hover:bg-gray-100 transition-colors ${
          activeMode === 'draw_point' ? 'bg-blue-100 text-blue-600' : 'text-gray-600'
        }`}
        title="Add Point"
      >
        <Type size={20} />
      </button>
      
      <div className="border-t border-gray-200 my-1"></div>
      
      <button
        onClick={undo}
        className="p-2 rounded hover:bg-gray-100 transition-colors text-gray-600"
        title="Undo"
      >
        <Undo size={20} />
      </button>
      
      <button
        onClick={redo}
        className="p-2 rounded hover:bg-gray-100 transition-colors text-gray-600"
        title="Redo"
      >
        <Redo size={20} />
      </button>
      
      <button
        onClick={deleteAll}
        className="p-2 rounded hover:bg-red-100 transition-colors text-red-600"
        title="Delete All"
      >
        <Trash2 size={20} />
      </button>
    </div>
  );
};
