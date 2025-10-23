"""
Multi-Format Export Manager

Handles exporting visualization data to multiple formats (JSON, CSV) with
optional compression. Pure backend data export for frontend integration.

Author: REGIQ AI/ML Team
Phase: 4.4 - Visualization & Reporting
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Union
from enum import Enum
import json
import csv
import gzip
from pathlib import Path
from datetime import datetime
import io


class ExportFormat(Enum):
    """Export format types"""
    JSON = "json"
    JSON_COMPRESSED = "json.gz"
    CSV = "csv"
    CSV_COMPRESSED = "csv.gz"


@dataclass
class ExportResult:
    """Export operation result"""
    success: bool
    file_path: Optional[str]
    file_size_bytes: int
    format: str
    compression_ratio: Optional[float] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ExportManager:
    """Manage data export to multiple formats"""
    
    def __init__(self, output_directory: Optional[str] = None):
        """
        Initialize export manager
        
        Args:
            output_directory: Base directory for exports (default: ./exports)
        """
        self.output_directory = Path(output_directory) if output_directory else Path("./exports")
        self.output_directory.mkdir(parents=True, exist_ok=True)
    
    def export_heatmap(
        self,
        heatmap_data: Dict[str, Any],
        filename: str,
        format: ExportFormat = ExportFormat.JSON,
        include_metadata: bool = True
    ) -> ExportResult:
        """
        Export heatmap data
        
        Args:
            heatmap_data: Heatmap data dictionary
            filename: Output filename (without extension)
            format: Export format
            include_metadata: Include metadata in export
            
        Returns:
            Export result
        """
        if format in [ExportFormat.JSON, ExportFormat.JSON_COMPRESSED]:
            return self._export_json(
                heatmap_data,
                filename,
                compress=format == ExportFormat.JSON_COMPRESSED,
                include_metadata=include_metadata
            )
        else:  # CSV formats
            # Convert heatmap to CSV-friendly format
            csv_data = self._heatmap_to_csv(heatmap_data)
            return self._export_csv(
                csv_data,
                filename,
                compress=format == ExportFormat.CSV_COMPRESSED
            )
    
    def export_distribution(
        self,
        distribution_data: Dict[str, Any],
        filename: str,
        format: ExportFormat = ExportFormat.JSON,
        include_metadata: bool = True
    ) -> ExportResult:
        """
        Export distribution analysis data
        
        Args:
            distribution_data: Distribution analysis dictionary
            filename: Output filename (without extension)
            format: Export format
            include_metadata: Include metadata in export
            
        Returns:
            Export result
        """
        if format in [ExportFormat.JSON, ExportFormat.JSON_COMPRESSED]:
            return self._export_json(
                distribution_data,
                filename,
                compress=format == ExportFormat.JSON_COMPRESSED,
                include_metadata=include_metadata
            )
        else:  # CSV formats
            # Convert distribution to CSV-friendly format
            csv_data = self._distribution_to_csv(distribution_data)
            return self._export_csv(
                csv_data,
                filename,
                compress=format == ExportFormat.CSV_COMPRESSED
            )
    
    def export_timeline(
        self,
        timeline_data: Dict[str, Any],
        filename: str,
        format: ExportFormat = ExportFormat.JSON,
        include_metadata: bool = True,
        separate_components: bool = False
    ) -> Union[ExportResult, Dict[str, ExportResult]]:
        """
        Export timeline projection data
        
        Args:
            timeline_data: Timeline projection dictionary
            filename: Output filename (without extension)
            format: Export format
            include_metadata: Include metadata in export
            separate_components: Export time series, events, and actions separately
            
        Returns:
            Export result or dict of results if separate_components=True
        """
        if not separate_components:
            if format in [ExportFormat.JSON, ExportFormat.JSON_COMPRESSED]:
                return self._export_json(
                    timeline_data,
                    filename,
                    compress=format == ExportFormat.JSON_COMPRESSED,
                    include_metadata=include_metadata
                )
            else:
                csv_data = self._timeline_to_csv(timeline_data)
                return self._export_csv(
                    csv_data,
                    filename,
                    compress=format == ExportFormat.CSV_COMPRESSED
                )
        else:
            # Export components separately
            results = {}
            
            # Time series
            if 'time_series' in timeline_data:
                results['time_series'] = self._export_csv(
                    {
                        'headers': ['timestamp', 'value', 'confidence_lower', 'confidence_upper'],
                        'rows': [
                            [
                                point['timestamp'],
                                point['value'],
                                point.get('confidence_lower', ''),
                                point.get('confidence_upper', '')
                            ]
                            for point in timeline_data['time_series']
                        ]
                    },
                    f"{filename}_time_series",
                    compress=format in [ExportFormat.CSV_COMPRESSED, ExportFormat.JSON_COMPRESSED]
                )
            
            # Events
            if 'events' in timeline_data:
                results['events'] = self._export_csv(
                    {
                        'headers': ['event_id', 'timestamp', 'event_type', 'title', 'severity', 'impact_score'],
                        'rows': [
                            [
                                event['event_id'],
                                event['timestamp'],
                                event['event_type'],
                                event['title'],
                                event['severity'],
                                event['impact_score']
                            ]
                            for event in timeline_data['events']
                        ]
                    },
                    f"{filename}_events",
                    compress=format in [ExportFormat.CSV_COMPRESSED, ExportFormat.JSON_COMPRESSED]
                )
            
            # Action plans
            if 'action_plans' in timeline_data:
                results['action_plans'] = self._export_csv(
                    {
                        'headers': ['action_id', 'title', 'start_date', 'due_date', 'status', 'priority', 'completion_percentage'],
                        'rows': [
                            [
                                plan['action_id'],
                                plan['title'],
                                plan['start_date'],
                                plan['due_date'],
                                plan['status'],
                                plan['priority'],
                                plan['completion_percentage']
                            ]
                            for plan in timeline_data['action_plans']
                        ]
                    },
                    f"{filename}_action_plans",
                    compress=format in [ExportFormat.CSV_COMPRESSED, ExportFormat.JSON_COMPRESSED]
                )
            
            return results
    
    def export_batch(
        self,
        data_items: List[Dict[str, Any]],
        base_filename: str,
        format: ExportFormat = ExportFormat.JSON
    ) -> List[ExportResult]:
        """
        Export multiple data items in batch
        
        Args:
            data_items: List of data dictionaries to export
            base_filename: Base filename (will be numbered)
            format: Export format
            
        Returns:
            List of export results
        """
        results = []
        
        for i, data_item in enumerate(data_items):
            filename = f"{base_filename}_{i+1:03d}"
            
            if format in [ExportFormat.JSON, ExportFormat.JSON_COMPRESSED]:
                result = self._export_json(
                    data_item,
                    filename,
                    compress=format == ExportFormat.JSON_COMPRESSED
                )
            else:
                # Attempt to convert to CSV based on data type
                csv_data = self._auto_convert_to_csv(data_item)
                result = self._export_csv(
                    csv_data,
                    filename,
                    compress=format == ExportFormat.CSV_COMPRESSED
                )
            
            results.append(result)
        
        return results
    
    def load_exported_data(
        self,
        file_path: str,
        format: Optional[ExportFormat] = None
    ) -> Dict[str, Any]:
        """
        Load previously exported data
        
        Args:
            file_path: Path to exported file
            format: Format hint (auto-detected if None)
            
        Returns:
            Loaded data dictionary
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Auto-detect format if not provided
        if format is None:
            if path.suffix == '.gz':
                if '.json' in path.suffixes:
                    format = ExportFormat.JSON_COMPRESSED
                elif '.csv' in path.suffixes:
                    format = ExportFormat.CSV_COMPRESSED
            elif path.suffix == '.json':
                format = ExportFormat.JSON
            elif path.suffix == '.csv':
                format = ExportFormat.CSV
        
        if format in [ExportFormat.JSON, ExportFormat.JSON_COMPRESSED]:
            return self._load_json(file_path, compressed=format == ExportFormat.JSON_COMPRESSED)
        else:
            return self._load_csv(file_path, compressed=format == ExportFormat.CSV_COMPRESSED)
    
    # Internal export methods
    
    def _export_json(
        self,
        data: Dict[str, Any],
        filename: str,
        compress: bool = False,
        include_metadata: bool = True
    ) -> ExportResult:
        """Export data as JSON"""
        try:
            # Add export metadata
            if include_metadata:
                export_data = {
                    **data,
                    'export_metadata': {
                        'exported_at': datetime.utcnow().isoformat(),
                        'format': 'json',
                        'compressed': compress
                    }
                }
            else:
                export_data = data
            
            # Serialize to JSON
            json_str = json.dumps(export_data, indent=2)
            json_bytes = json_str.encode('utf-8')
            
            # Determine file path
            extension = '.json.gz' if compress else '.json'
            file_path = self.output_directory / f"{filename}{extension}"
            
            # Write file
            if compress:
                with gzip.open(file_path, 'wb') as f:
                    f.write(json_bytes)
                compression_ratio = len(json_bytes) / file_path.stat().st_size
            else:
                with open(file_path, 'wb') as f:
                    f.write(json_bytes)
                compression_ratio = None
            
            return ExportResult(
                success=True,
                file_path=str(file_path),
                file_size_bytes=file_path.stat().st_size,
                format=ExportFormat.JSON_COMPRESSED.value if compress else ExportFormat.JSON.value,
                compression_ratio=compression_ratio,
                metadata={'original_size_bytes': len(json_bytes)}
            )
            
        except Exception as e:
            return ExportResult(
                success=False,
                file_path=None,
                file_size_bytes=0,
                format=ExportFormat.JSON_COMPRESSED.value if compress else ExportFormat.JSON.value,
                error_message=str(e)
            )
    
    def _export_csv(
        self,
        csv_data: Dict[str, Any],
        filename: str,
        compress: bool = False
    ) -> ExportResult:
        """Export data as CSV"""
        try:
            # Create CSV in memory
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write headers
            writer.writerow(csv_data['headers'])
            
            # Write rows
            writer.writerows(csv_data['rows'])
            
            csv_str = output.getvalue()
            csv_bytes = csv_str.encode('utf-8')
            
            # Determine file path
            extension = '.csv.gz' if compress else '.csv'
            file_path = self.output_directory / f"{filename}{extension}"
            
            # Write file
            if compress:
                with gzip.open(file_path, 'wb') as f:
                    f.write(csv_bytes)
                compression_ratio = len(csv_bytes) / file_path.stat().st_size
            else:
                with open(file_path, 'wb') as f:
                    f.write(csv_bytes)
                compression_ratio = None
            
            return ExportResult(
                success=True,
                file_path=str(file_path),
                file_size_bytes=file_path.stat().st_size,
                format=ExportFormat.CSV_COMPRESSED.value if compress else ExportFormat.CSV.value,
                compression_ratio=compression_ratio,
                metadata={
                    'row_count': len(csv_data['rows']),
                    'column_count': len(csv_data['headers'])
                }
            )
            
        except Exception as e:
            return ExportResult(
                success=False,
                file_path=None,
                file_size_bytes=0,
                format=ExportFormat.CSV_COMPRESSED.value if compress else ExportFormat.CSV.value,
                error_message=str(e)
            )
    
    def _load_json(self, file_path: str, compressed: bool = False) -> Dict[str, Any]:
        """Load JSON data"""
        if compressed:
            with gzip.open(file_path, 'rb') as f:
                return json.loads(f.read().decode('utf-8'))
        else:
            with open(file_path, 'r') as f:
                return json.load(f)
    
    def _load_csv(self, file_path: str, compressed: bool = False) -> Dict[str, Any]:
        """Load CSV data"""
        if compressed:
            with gzip.open(file_path, 'rt') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        else:
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        
        return {
            'headers': list(rows[0].keys()) if rows else [],
            'rows': rows
        }
    
    # Data conversion methods
    
    def _heatmap_to_csv(self, heatmap_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert heatmap data to CSV format"""
        headers = ['x_value', 'y_value', 'risk_score', 'count', 'severity', 'color_code']
        rows = []
        
        for cell in heatmap_data.get('cells', []):
            rows.append([
                cell['x_value'],
                cell['y_value'],
                cell['risk_score'],
                cell['count'],
                cell['severity'],
                cell['color_code']
            ])
        
        return {'headers': headers, 'rows': rows}
    
    def _distribution_to_csv(self, distribution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert distribution data to CSV format"""
        # Export histogram data
        headers = ['bin_center', 'bin_count', 'density']
        rows = []
        
        histogram = distribution_data.get('histogram', {})
        bin_centers = histogram.get('bin_centers', [])
        bin_counts = histogram.get('bin_counts', [])
        density = histogram.get('density', [])
        
        for i in range(len(bin_centers)):
            rows.append([
                bin_centers[i],
                bin_counts[i],
                density[i]
            ])
        
        return {'headers': headers, 'rows': rows}
    
    def _timeline_to_csv(self, timeline_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert timeline data to CSV format (time series only)"""
        headers = ['timestamp', 'value', 'confidence_lower', 'confidence_upper']
        rows = []
        
        for point in timeline_data.get('time_series', []):
            rows.append([
                point['timestamp'],
                point['value'],
                point.get('confidence_lower', ''),
                point.get('confidence_upper', '')
            ])
        
        return {'headers': headers, 'rows': rows}
    
    def _auto_convert_to_csv(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Automatically convert data to CSV format based on structure"""
        # Try to detect data type
        if 'cells' in data and 'matrix' in data:
            return self._heatmap_to_csv(data)
        elif 'histogram' in data and 'pdf_cdf' in data:
            return self._distribution_to_csv(data)
        elif 'time_series' in data and 'events' in data:
            return self._timeline_to_csv(data)
        else:
            # Generic conversion: flatten dict to single row
            headers = list(data.keys())
            rows = [[str(data[key]) for key in headers]]
            return {'headers': headers, 'rows': rows}
