'use client';

import React, { useState } from 'react';
import { MapPin, Clock, Users, AlertTriangle, CheckCircle, Route, Target, Home, Building } from 'lucide-react';

interface Persona {
  type: string;
  name: string;
  age_range: string;
  mobility_type: string;
  speed: number;
  max_distance: number;
  priorities: string[];
  barriers: string[];
  needs: string[];
  home_location: {
    coordinates: [number, number];
    properties: any;
  };
  destinations: {
    [key: string]: {
      coordinates: [number, number];
      type: string;
    };
  };
  preferences: {
    route_preference: string;
    time_preference: string;
    weather_sensitivity: string;
    crowd_tolerance: string;
    cost_sensitivity: string;
  };
}

interface JourneyAnalysis {
  journey_type: string;
  origin: any;
  destination: any;
  route: {
    distance: number;
    travel_time: number;
    route_factor: number;
    points: [number, number][];
    direct_distance: number;
  };
  route_quality: {
    safety_score: number;
    accessibility_score: number;
    comfort_score: number;
    efficiency_score: number;
    overall_score: number;
    barriers: Array<{
      type: string;
      severity: string;
      description: string;
      location: [number, number];
    }>;
    amenities: Array<{
      type: string;
      description: string;
      location: [number, number];
      usefulness: string;
    }>;
  };
  metrics: {
    distance_meters: number;
    travel_time_minutes: number;
    speed_mps: number;
    feasibility: boolean;
    energy_expenditure: number;
    carbon_footprint: number;
  };
}

interface BarrierAnalysis {
  physical_barriers: Array<{
    type: string;
    count: number;
    description: string;
    impact: string;
  }>;
  accessibility_barriers: Array<{
    type: string;
    count: number;
    description: string;
    impact: string;
  }>;
  safety_barriers: Array<{
    type: string;
    count: number;
    description: string;
    impact: string;
  }>;
  comfort_barriers: Array<{
    type: string;
    count: number;
    description: string;
    impact: string;
  }>;
  mitigation_suggestions: Array<{
    barrier_type: string;
    suggestion: string;
    priority: string;
    cost_estimate: string;
    implementation_time: string;
  }>;
}

interface PersonaJourneyProps {
  personas?: { [key: string]: Persona };
  journeyAnalysis?: { [key: string]: JourneyAnalysis };
  barrierAnalysis?: { [key: string]: BarrierAnalysis };
  onPersonaSelect?: (personaType: string) => void;
  onJourneySelect?: (journeyType: string) => void;
  onBarrierClick?: (barrier: any) => void;
  onMitigationClick?: (suggestion: any) => void;
}

export const PersonaJourney: React.FC<PersonaJourneyProps> = ({
  personas,
  journeyAnalysis,
  barrierAnalysis,
  onPersonaSelect,
  onJourneySelect,
  onBarrierClick,
  onMitigationClick
}) => {
  const [selectedPersona, setSelectedPersona] = useState<string | null>(null);
  const [selectedJourney, setSelectedJourney] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'personas' | 'journeys' | 'barriers'>('personas');

  const formatNumber = (num: number) => {
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + ' km';
    }
    return Math.round(num) + ' m';
  };

  const formatTime = (minutes: number) => {
    if (minutes >= 60) {
      const hours = Math.floor(minutes / 60);
      const mins = Math.round(minutes % 60);
      return `${hours}h ${mins}m`;
    }
    return Math.round(minutes) + ' min';
  };

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBackground = (score: number) => {
    if (score >= 0.8) return 'bg-green-100';
    if (score >= 0.6) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  const getPersonaIcon = (personaType: string) => {
    switch (personaType) {
      case 'child':
        return <Users size={20} />;
      case 'senior':
        return <Users size={20} />;
      case 'low_income':
        return <Users size={20} />;
      case 'assistive_mobility':
        return <Users size={20} />;
      case 'cyclist':
        return <Route size={20} />;
      default:
        return <Users size={20} />;
    }
  };

  const getJourneyIcon = (journeyType: string) => {
    switch (journeyType) {
      case 'home_to_work':
        return <Building size={16} />;
      case 'home_to_school':
        return <Building size={16} />;
      case 'home_to_shop':
        return <Building size={16} />;
      case 'home_to_healthcare':
        return <Building size={16} />;
      case 'home_to_recreation':
        return <Target size={16} />;
      default:
        return <Route size={16} />;
    }
  };

  const getBarrierIcon = (barrierType: string) => {
    switch (barrierType) {
      case 'unsafe_crossing':
      case 'no_bike_lanes':
        return <AlertTriangle size={16} />;
      case 'no_ramps':
      case 'narrow_paths':
        return <AlertTriangle size={16} />;
      default:
        return <AlertTriangle size={16} />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'text-red-600 bg-red-50 border-red-200';
      case 'medium':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'low':
        return 'text-green-600 bg-green-50 border-green-200';
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">Persona & Journey Analysis</h2>
      
      {/* Tab Navigation */}
      <div className="mb-6">
        <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
          {[
            { key: 'personas', label: 'Personas', icon: <Users size={16} /> },
            { key: 'journeys', label: 'Journeys', icon: <Route size={16} /> },
            { key: 'barriers', label: 'Barriers', icon: <AlertTriangle size={16} /> }
          ].map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key as any)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                activeTab === tab.key
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              {tab.icon}
              <span>{tab.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Personas Tab */}
      {activeTab === 'personas' && (
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-4">Persona Profiles</h3>
          
          {!personas || Object.keys(personas).length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              <Users size={48} className="mx-auto mb-4 text-gray-300" />
              <p>No personas available</p>
              <p className="text-sm">Generate personas to analyze user journeys</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(personas).map(([personaType, persona]) => (
                <div
                  key={personaType}
                  className={`p-4 border-2 rounded-lg cursor-pointer transition-all duration-200 hover:shadow-md ${
                    selectedPersona === personaType
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => {
                    setSelectedPersona(personaType);
                    onPersonaSelect?.(personaType);
                  }}
                >
                  {/* Persona Header */}
                  <div className="flex items-center space-x-3 mb-3">
                    {getPersonaIcon(personaType)}
                    <div>
                      <h4 className="font-semibold text-gray-900">{persona.name}</h4>
                      <p className="text-sm text-gray-600">{persona.age_range}</p>
                    </div>
                  </div>

                  {/* Persona Details */}
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Mobility:</span>
                      <span className="font-medium">{persona.mobility_type}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Speed:</span>
                      <span className="font-medium">{persona.speed} m/s</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Max Distance:</span>
                      <span className="font-medium">{formatNumber(persona.max_distance)}</span>
                    </div>
                  </div>

                  {/* Priorities */}
                  <div className="mt-3">
                    <p className="text-xs text-gray-500 mb-1">Priorities:</p>
                    <div className="flex flex-wrap gap-1">
                      {persona.priorities.slice(0, 3).map((priority) => (
                        <span
                          key={priority}
                          className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded"
                        >
                          {priority}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Destinations */}
                  <div className="mt-3">
                    <p className="text-xs text-gray-500 mb-1">Destinations:</p>
                    <div className="flex flex-wrap gap-1">
                      {Object.keys(persona.destinations).slice(0, 3).map((dest) => (
                        <span
                          key={dest}
                          className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded"
                        >
                          {dest}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Journeys Tab */}
      {activeTab === 'journeys' && (
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-4">Journey Analysis</h3>
          
          {!journeyAnalysis || Object.keys(journeyAnalysis).length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              <Route size={48} className="mx-auto mb-4 text-gray-300" />
              <p>No journey analysis available</p>
              <p className="text-sm">Analyze journeys for selected personas</p>
            </div>
          ) : (
            <div className="space-y-4">
              {Object.entries(journeyAnalysis).map(([journeyKey, journey]) => (
                <div
                  key={journeyKey}
                  className={`p-4 border-2 rounded-lg cursor-pointer transition-all duration-200 hover:shadow-md ${
                    selectedJourney === journeyKey
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => {
                    setSelectedJourney(journeyKey);
                    onJourneySelect?.(journeyKey);
                  }}
                >
                  {/* Journey Header */}
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-2">
                      {getJourneyIcon(journey.journey_type)}
                      <h4 className="font-semibold text-gray-900">
                        {journey.journey_type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </h4>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-gray-900">
                        {formatNumber(journey.metrics.distance_meters)}
                      </div>
                      <div className="text-xs text-gray-600">
                        {formatTime(journey.metrics.travel_time_minutes)}
                      </div>
                    </div>
                  </div>

                  {/* Route Quality Scores */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-3">
                    {[
                      { key: 'safety_score', label: 'Safety' },
                      { key: 'accessibility_score', label: 'Accessibility' },
                      { key: 'comfort_score', label: 'Comfort' },
                      { key: 'efficiency_score', label: 'Efficiency' }
                    ].map((score) => (
                      <div key={score.key} className="text-center">
                        <div className={`text-lg font-bold ${getScoreColor(journey.route_quality[score.key as keyof typeof journey.route_quality] as number)}`}>
                          {(journey.route_quality[score.key as keyof typeof journey.route_quality] as number * 100).toFixed(0)}%
                        </div>
                        <div className="text-xs text-gray-600">{score.label}</div>
                      </div>
                    ))}
                  </div>

                  {/* Overall Score */}
                  <div className="mb-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-gray-700">Overall Quality:</span>
                      <div className={`px-3 py-1 rounded-full text-sm font-medium ${getScoreBackground(journey.route_quality.overall_score)} ${getScoreColor(journey.route_quality.overall_score)}`}>
                        {(journey.route_quality.overall_score * 100).toFixed(0)}%
                      </div>
                    </div>
                  </div>

                  {/* Barriers and Amenities */}
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Barriers ({journey.route_quality.barriers.length}):</p>
                      <div className="space-y-1">
                        {journey.route_quality.barriers.slice(0, 2).map((barrier, index) => (
                          <div
                            key={index}
                            className="flex items-center space-x-1 text-xs text-red-600 cursor-pointer hover:text-red-700"
                            onClick={() => onBarrierClick?.(barrier)}
                          >
                            <AlertTriangle size={12} />
                            <span>{barrier.type.replace('_', ' ')}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Amenities ({journey.route_quality.amenities.length}):</p>
                      <div className="space-y-1">
                        {journey.route_quality.amenities.slice(0, 2).map((amenity, index) => (
                          <div
                            key={index}
                            className="flex items-center space-x-1 text-xs text-green-600"
                          >
                            <CheckCircle size={12} />
                            <span>{amenity.type}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Journey Metrics */}
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <div className="grid grid-cols-3 gap-2 text-xs">
                      <div className="text-center">
                        <div className="font-medium text-gray-900">
                          {journey.metrics.feasibility ? '✓' : '✗'}
                        </div>
                        <div className="text-gray-600">Feasible</div>
                      </div>
                      <div className="text-center">
                        <div className="font-medium text-gray-900">
                          {journey.metrics.energy_expenditure.toFixed(1)}
                        </div>
                        <div className="text-gray-600">Energy</div>
                      </div>
                      <div className="text-center">
                        <div className="font-medium text-gray-900">
                          {journey.metrics.carbon_footprint.toFixed(3)}
                        </div>
                        <div className="text-gray-600">CO₂</div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Barriers Tab */}
      {activeTab === 'barriers' && (
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-4">Barrier Analysis & Mitigation</h3>
          
          {!barrierAnalysis || Object.keys(barrierAnalysis).length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              <AlertTriangle size={48} className="mx-auto mb-4 text-gray-300" />
              <p>No barrier analysis available</p>
              <p className="text-sm">Detect barriers for selected personas</p>
            </div>
          ) : (
            <div className="space-y-6">
              {Object.entries(barrierAnalysis).map(([personaType, barriers]) => (
                <div key={personaType} className="border border-gray-200 rounded-lg p-4">
                  <h4 className="font-semibold text-gray-900 mb-3">
                    {personas?.[personaType]?.name || personaType} Barriers
                  </h4>

                  {/* Barrier Categories */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    {[
                      { key: 'safety_barriers', label: 'Safety Barriers', color: 'red' },
                      { key: 'accessibility_barriers', label: 'Accessibility Barriers', color: 'orange' },
                      { key: 'physical_barriers', label: 'Physical Barriers', color: 'yellow' },
                      { key: 'comfort_barriers', label: 'Comfort Barriers', color: 'blue' }
                    ].map((category) => (
                      <div key={category.key} className="space-y-2">
                        <h5 className="text-sm font-medium text-gray-700">{category.label}</h5>
                        {barriers[category.key as keyof BarrierAnalysis]?.map((barrier, index) => (
                          <div
                            key={index}
                            className="flex items-center space-x-2 p-2 bg-gray-50 rounded cursor-pointer hover:bg-gray-100"
                            onClick={() => onBarrierClick?.(barrier)}
                          >
                            {getBarrierIcon(barrier.type)}
                            <div className="flex-1">
                              <div className="text-sm font-medium text-gray-900">
                                {barrier.type.replace('_', ' ')}
                              </div>
                              <div className="text-xs text-gray-600">
                                {barrier.count} instances - {barrier.description}
                              </div>
                            </div>
                            <div className={`px-2 py-1 rounded text-xs font-medium ${
                              barrier.impact === 'high' ? 'bg-red-100 text-red-700' :
                              barrier.impact === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                              'bg-green-100 text-green-700'
                            }`}>
                              {barrier.impact}
                            </div>
                          </div>
                        ))}
                      </div>
                    ))}
                  </div>

                  {/* Mitigation Suggestions */}
                  <div className="border-t border-gray-200 pt-4">
                    <h5 className="text-sm font-medium text-gray-700 mb-3">Mitigation Suggestions</h5>
                    <div className="space-y-2">
                      {barriers.mitigation_suggestions.map((suggestion, index) => (
                        <div
                          key={index}
                          className="p-3 border rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
                          onClick={() => onMitigationClick?.(suggestion)}
                        >
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <div className="font-medium text-gray-900">
                                {suggestion.suggestion}
                              </div>
                              <div className="text-sm text-gray-600 mt-1">
                                Addresses: {suggestion.barrier_type.replace('_', ' ')}
                              </div>
                            </div>
                            <div className="ml-4 text-right">
                              <div className={`px-2 py-1 rounded text-xs font-medium ${getPriorityColor(suggestion.priority)}`}>
                                {suggestion.priority}
                              </div>
                              <div className="text-xs text-gray-500 mt-1">
                                {suggestion.cost_estimate} cost
                              </div>
                              <div className="text-xs text-gray-500">
                                {suggestion.implementation_time}
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
