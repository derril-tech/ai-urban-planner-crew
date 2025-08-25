# Created automatically by Cursor AI (2025-08-25)
import React, { useState, useEffect } from 'react';
import { 
  Download, 
  FileText, 
  Share2, 
  Copy, 
  Trash2, 
  Eye, 
  Calendar,
  File,
  Archive,
  Globe,
  Database,
  Code,
  BarChart3,
  Map,
  CheckCircle,
  AlertCircle,
  Clock
} from 'lucide-react';

interface ExportFormat {
  id: string;
  name: string;
  description: string;
  icon: React.ReactNode;
  extensions: string[];
  mimeType: string;
}

interface ExportHistory {
  id: string;
  export_format: string;
  filename: string;
  file_size: number;
  created_at: string;
  file_url: string;
  expires_at: string;
}

interface ShareLink {
  id: string;
  scenario_id: string;
  token: string;
  is_public: boolean;
  expires_at: string;
  created_at: string;
  access_count: number;
}

interface ExportHubProps {
  scenarioId: string;
  scenarioName: string;
  onExportComplete?: (exportData: any) => void;
  onShareLinkCreated?: (shareLink: ShareLink) => void;
}

export const ExportHub: React.FC<ExportHubProps> = ({
  scenarioId,
  scenarioName,
  onExportComplete,
  onShareLinkCreated
}) => {
  const [activeTab, setActiveTab] = useState<'export' | 'history' | 'share'>('export');
  const [selectedFormats, setSelectedFormats] = useState<string[]>(['geojson']);
  const [includeAnalysis, setIncludeAnalysis] = useState(true);
  const [includeMetadata, setIncludeMetadata] = useState(true);
  const [isExporting, setIsExporting] = useState(false);
  const [exportHistory, setExportHistory] = useState<ExportHistory[]>([]);
  const [shareLinks, setShareLinks] = useState<ShareLink[]>([]);
  const [isCreatingShare, setIsCreatingShare] = useState(false);
  const [sharePublic, setSharePublic] = useState(false);
  const [shareExpiry, setShareExpiry] = useState('7d');
  const [copiedLink, setCopiedLink] = useState<string | null>(null);

  const exportFormats: ExportFormat[] = [
    {
      id: 'geojson',
      name: 'GeoJSON',
      description: 'Geospatial data in GeoJSON format',
      icon: <Globe className="w-5 h-5" />,
      extensions: ['.geojson'],
      mimeType: 'application/geo+json'
    },
    {
      id: 'shapefile',
      name: 'Shapefile',
      description: 'ESRI Shapefile format for GIS applications',
      icon: <Map className="w-5 h-5" />,
      extensions: ['.shp', '.shx', '.dbf', '.prj'],
      mimeType: 'application/zip'
    },
    {
      id: 'gpkg',
      name: 'GeoPackage',
      description: 'OGC GeoPackage format for spatial data',
      icon: <Database className="w-5 h-5" />,
      extensions: ['.gpkg'],
      mimeType: 'application/geopackage+sqlite3'
    },
    {
      id: 'dxf',
      name: 'DXF',
      description: 'AutoCAD DXF format for CAD applications',
      icon: <Code className="w-5 h-5" />,
      extensions: ['.dxf'],
      mimeType: 'application/dxf'
    },
    {
      id: 'csv',
      name: 'CSV',
      description: 'Comma-separated values for tabular data',
      icon: <BarChart3 className="w-5 h-5" />,
      extensions: ['.csv'],
      mimeType: 'text/csv'
    },
    {
      id: 'zip',
      name: 'ZIP Archive',
      description: 'Compressed archive with multiple formats',
      icon: <Archive className="w-5 h-5" />,
      extensions: ['.zip'],
      mimeType: 'application/zip'
    }
  ];

  useEffect(() => {
    loadExportHistory();
    loadShareLinks();
  }, [scenarioId]);

  const loadExportHistory = async () => {
    try {
      // Mock API call - replace with actual API
      const response = await fetch(`/api/scenarios/${scenarioId}/exports`);
      const data = await response.json();
      setExportHistory(data.exports || []);
    } catch (error) {
      console.error('Error loading export history:', error);
    }
  };

  const loadShareLinks = async () => {
    try {
      // Mock API call - replace with actual API
      const response = await fetch(`/api/scenarios/${scenarioId}/shares`);
      const data = await response.json();
      setShareLinks(data.shares || []);
    } catch (error) {
      console.error('Error loading share links:', error);
    }
  };

  const handleFormatToggle = (formatId: string) => {
    setSelectedFormats(prev => 
      prev.includes(formatId) 
        ? prev.filter(id => id !== formatId)
        : [...prev, formatId]
    );
  };

  const handleExport = async () => {
    if (selectedFormats.length === 0) return;

    setIsExporting(true);
    try {
      const exportData = {
        scenario_id: scenarioId,
        formats: selectedFormats,
        include_analysis,
        include_metadata
      };

      // Mock API call - replace with actual API
      const response = await fetch('/api/exports', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(exportData)
      });

      const result = await response.json();
      
      if (result.success) {
        onExportComplete?.(result.data);
        loadExportHistory();
      }
    } catch (error) {
      console.error('Error exporting data:', error);
    } finally {
      setIsExporting(false);
    }
  };

  const handleDownload = async (exportItem: ExportHistory) => {
    try {
      // Create temporary link and trigger download
      const link = document.createElement('a');
      link.href = exportItem.file_url;
      link.download = exportItem.filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Error downloading file:', error);
    }
  };

  const handleDeleteExport = async (exportId: string) => {
    try {
      // Mock API call - replace with actual API
      await fetch(`/api/exports/${exportId}`, { method: 'DELETE' });
      loadExportHistory();
    } catch (error) {
      console.error('Error deleting export:', error);
    }
  };

  const handleCreateShare = async () => {
    setIsCreatingShare(true);
    try {
      const shareData = {
        scenario_id: scenarioId,
        is_public: sharePublic,
        expiry_days: parseInt(shareExpiry.replace('d', ''))
      };

      // Mock API call - replace with actual API
      const response = await fetch('/api/shares', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(shareData)
      });

      const result = await response.json();
      
      if (result.success) {
        onShareLinkCreated?.(result.data);
        loadShareLinks();
      }
    } catch (error) {
      console.error('Error creating share link:', error);
    } finally {
      setIsCreatingShare(false);
    }
  };

  const handleCopyLink = async (shareLink: ShareLink) => {
    const shareUrl = `${window.location.origin}/scenarios/${scenarioId}/shared/${shareLink.token}`;
    
    try {
      await navigator.clipboard.writeText(shareUrl);
      setCopiedLink(shareLink.id);
      setTimeout(() => setCopiedLink(null), 2000);
    } catch (error) {
      console.error('Error copying link:', error);
    }
  };

  const handleDeleteShare = async (shareId: string) => {
    try {
      // Mock API call - replace with actual API
      await fetch(`/api/shares/${shareId}`, { method: 'DELETE' });
      loadShareLinks();
    } catch (error) {
      console.error('Error deleting share link:', error);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const isExpired = (expiryDate: string): boolean => {
    return new Date(expiryDate) < new Date();
  };

  const getStatusIcon = (expiryDate: string) => {
    if (isExpired(expiryDate)) {
      return <AlertCircle className="w-4 h-4 text-red-500" />;
    }
    return <CheckCircle className="w-4 h-4 text-green-500" />;
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">Export Hub</h2>
      
      {/* Tab Navigation */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('export')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'export'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <Download className="w-4 h-4 inline mr-2" />
            Export Data
          </button>
          <button
            onClick={() => setActiveTab('history')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'history'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <FileText className="w-4 h-4 inline mr-2" />
            Export History
          </button>
          <button
            onClick={() => setActiveTab('share')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'share'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <Share2 className="w-4 h-4 inline mr-2" />
            Share Links
          </button>
        </nav>
      </div>

      {/* Export Tab */}
      {activeTab === 'export' && (
        <div>
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Select Export Formats</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {exportFormats.map((format) => (
                <div
                  key={format.id}
                  className={`border rounded-lg p-4 cursor-pointer transition-colors ${
                    selectedFormats.includes(format.id)
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => handleFormatToggle(format.id)}
                >
                  <div className="flex items-center mb-2">
                    <div className={`mr-3 ${
                      selectedFormats.includes(format.id) ? 'text-blue-600' : 'text-gray-500'
                    }`}>
                      {format.icon}
                    </div>
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900">{format.name}</h4>
                      <p className="text-sm text-gray-500">{format.description}</p>
                    </div>
                    <div className={`w-5 h-5 rounded border-2 ${
                      selectedFormats.includes(format.id)
                        ? 'border-blue-500 bg-blue-500'
                        : 'border-gray-300'
                    }`}>
                      {selectedFormats.includes(format.id) && (
                        <CheckCircle className="w-4 h-4 text-white" />
                      )}
                    </div>
                  </div>
                  <div className="text-xs text-gray-400">
                    Extensions: {format.extensions.join(', ')}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Export Options</h3>
            <div className="space-y-4">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={includeAnalysis}
                  onChange={(e) => setIncludeAnalysis(e.target.checked)}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="ml-2 text-gray-700">Include analysis data (KPIs, scores, etc.)</span>
              </label>
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={includeMetadata}
                  onChange={(e) => setIncludeMetadata(e.target.checked)}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="ml-2 text-gray-700">Include metadata and documentation</span>
              </label>
            </div>
          </div>

          <div className="flex justify-end">
            <button
              onClick={handleExport}
              disabled={isExporting || selectedFormats.length === 0}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              {isExporting ? (
                <>
                  <Clock className="w-4 h-4 mr-2 animate-spin" />
                  Exporting...
                </>
              ) : (
                <>
                  <Download className="w-4 h-4 mr-2" />
                  Export Data
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* History Tab */}
      {activeTab === 'history' && (
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-4">Export History</h3>
          {exportHistory.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <FileText className="w-12 h-12 mx-auto mb-4 text-gray-300" />
              <p>No exports found</p>
            </div>
          ) : (
            <div className="space-y-4">
              {exportHistory.map((exportItem) => (
                <div key={exportItem.id} className="border rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="text-blue-600">
                        {exportFormats.find(f => f.id === exportItem.export_format)?.icon || <File className="w-5 h-5" />}
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-900">{exportItem.filename}</h4>
                        <p className="text-sm text-gray-500">
                          {exportFormats.find(f => f.id === exportItem.export_format)?.name} • {formatFileSize(exportItem.file_size)}
                        </p>
                        <p className="text-xs text-gray-400">
                          <Calendar className="w-3 h-3 inline mr-1" />
                          {formatDate(exportItem.created_at)}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => handleDownload(exportItem)}
                        className="text-blue-600 hover:text-blue-700 p-2"
                        title="Download"
                      >
                        <Download className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDeleteExport(exportItem.id)}
                        className="text-red-600 hover:text-red-700 p-2"
                        title="Delete"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Share Tab */}
      {activeTab === 'share' && (
        <div>
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Create Share Link</h3>
            <div className="space-y-4">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={sharePublic}
                  onChange={(e) => setSharePublic(e.target.checked)}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="ml-2 text-gray-700">Public read-only access</span>
              </label>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Link Expiry
                </label>
                <select
                  value={shareExpiry}
                  onChange={(e) => setShareExpiry(e.target.value)}
                  className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                >
                  <option value="1d">1 day</option>
                  <option value="7d">7 days</option>
                  <option value="30d">30 days</option>
                  <option value="90d">90 days</option>
                  <option value="never">Never</option>
                </select>
              </div>
              <button
                onClick={handleCreateShare}
                disabled={isCreatingShare}
                className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
              >
                {isCreatingShare ? (
                  <>
                    <Clock className="w-4 h-4 mr-2 animate-spin" />
                    Creating...
                  </>
                ) : (
                  <>
                    <Share2 className="w-4 h-4 mr-2" />
                    Create Share Link
                  </>
                )}
              </button>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4">Active Share Links</h3>
            {shareLinks.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <Share2 className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                <p>No share links created</p>
              </div>
            ) : (
              <div className="space-y-4">
                {shareLinks.map((shareLink) => (
                  <div key={shareLink.id} className="border rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <div className="text-green-600">
                          {getStatusIcon(shareLink.expires_at)}
                        </div>
                        <div>
                          <h4 className="font-medium text-gray-900">
                            {shareLink.is_public ? 'Public' : 'Private'} Share Link
                          </h4>
                          <p className="text-sm text-gray-500">
                            Token: {shareLink.token.substring(0, 8)}...
                          </p>
                          <p className="text-xs text-gray-400">
                            <Calendar className="w-3 h-3 inline mr-1" />
                            Created: {formatDate(shareLink.created_at)}
                            {shareLink.expires_at !== 'never' && (
                              <>
                                • Expires: {formatDate(shareLink.expires_at)}
                              </>
                            )}
                          </p>
                          <p className="text-xs text-gray-400">
                            Access count: {shareLink.access_count}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => handleCopyLink(shareLink)}
                          className="text-blue-600 hover:text-blue-700 p-2"
                          title="Copy Link"
                        >
                          {copiedLink === shareLink.id ? (
                            <CheckCircle className="w-4 h-4" />
                          ) : (
                            <Copy className="w-4 h-4" />
                          )}
                        </button>
                        <button
                          onClick={() => handleDeleteShare(shareLink.id)}
                          className="text-red-600 hover:text-red-700 p-2"
                          title="Delete"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
