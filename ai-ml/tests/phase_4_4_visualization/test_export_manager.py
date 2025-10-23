"""
Test Export Manager

Tests for multi-format data export functionality.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from services.risk_simulator.visualization.export_manager import (
    ExportManager,
    ExportFormat,
    ExportResult
)


class TestExportManager:
    """Test ExportManager class"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test exports"""
        temp_path = tempfile.mkdtemp()
        yield temp_path
        shutil.rmtree(temp_path)
    
    @pytest.fixture
    def sample_heatmap_data(self):
        """Sample heatmap data for testing"""
        return {
            'dimension_type': 'probability_impact',
            'x_categories': ['Low', 'Medium', 'High'],
            'y_categories': ['Minor', 'Major', 'Critical'],
            'matrix': [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]],
            'cells': [
                {
                    'x_value': 'Low',
                    'y_value': 'Minor',
                    'risk_score': 0.1,
                    'count': 2,
                    'severity': 'low',
                    'color_code': '#00FF00'
                }
            ],
            'statistics': {'total_risks': 10}
        }
    
    @pytest.fixture
    def sample_distribution_data(self):
        """Sample distribution data for testing"""
        return {
            'distribution_type': 'normal',
            'histogram': {
                'bin_edges': [0.0, 0.1, 0.2, 0.3],
                'bin_counts': [5, 10, 5],
                'bin_centers': [0.05, 0.15, 0.25],
                'density': [0.25, 0.5, 0.25]
            },
            'pdf_cdf': {
                'x_values': [0.0, 0.5, 1.0],
                'pdf_values': [0.1, 0.4, 0.1],
                'cdf_values': [0.0, 0.5, 1.0]
            },
            'statistics': {'mean': 0.5, 'std': 0.1}
        }
    
    @pytest.fixture
    def sample_timeline_data(self):
        """Sample timeline data for testing"""
        return {
            'start_date': '2025-01-01T00:00:00',
            'end_date': '2025-12-31T00:00:00',
            'time_series': [
                {
                    'timestamp': '2025-01-01T00:00:00',
                    'value': 0.5,
                    'confidence_lower': 0.4,
                    'confidence_upper': 0.6
                }
            ],
            'events': [
                {
                    'event_id': 'event1',
                    'timestamp': '2025-03-15T00:00:00',
                    'event_type': 'compliance_deadline',
                    'title': 'Deadline',
                    'severity': 'high',
                    'impact_score': 0.7
                }
            ],
            'action_plans': [
                {
                    'action_id': 'action1',
                    'title': 'Mitigation Action',
                    'start_date': '2025-01-15T00:00:00',
                    'due_date': '2025-03-15T00:00:00',
                    'status': 'in_progress',
                    'priority': 'high',
                    'completion_percentage': 50.0
                }
            ]
        }
    
    def test_initialization(self, temp_dir):
        """Test export manager initialization"""
        manager = ExportManager(output_directory=temp_dir)
        assert manager.output_directory == Path(temp_dir)
        assert manager.output_directory.exists()
    
    def test_export_heatmap_json(self, temp_dir, sample_heatmap_data):
        """Test heatmap export as JSON"""
        manager = ExportManager(output_directory=temp_dir)
        
        result = manager.export_heatmap(
            sample_heatmap_data,
            filename='test_heatmap',
            format=ExportFormat.JSON
        )
        
        assert result.success is True
        assert result.file_path is not None
        assert Path(result.file_path).exists()
        assert result.file_size_bytes > 0
        assert result.format == ExportFormat.JSON.value
    
    def test_export_heatmap_json_compressed(self, temp_dir, sample_heatmap_data):
        """Test heatmap export as compressed JSON"""
        manager = ExportManager(output_directory=temp_dir)
        
        result = manager.export_heatmap(
            sample_heatmap_data,
            filename='test_heatmap_compressed',
            format=ExportFormat.JSON_COMPRESSED
        )
        
        assert result.success is True
        assert result.file_path is not None
        assert result.file_path.endswith('.json.gz')
        assert result.compression_ratio is not None
        assert result.compression_ratio > 1.0  # Compressed should be smaller
    
    def test_export_heatmap_csv(self, temp_dir, sample_heatmap_data):
        """Test heatmap export as CSV"""
        manager = ExportManager(output_directory=temp_dir)
        
        result = manager.export_heatmap(
            sample_heatmap_data,
            filename='test_heatmap_csv',
            format=ExportFormat.CSV
        )
        
        assert result.success is True
        assert result.file_path is not None
        assert result.file_path.endswith('.csv')
        assert result.metadata is not None
        assert 'row_count' in result.metadata
    
    def test_export_distribution_json(self, temp_dir, sample_distribution_data):
        """Test distribution export as JSON"""
        manager = ExportManager(output_directory=temp_dir)
        
        result = manager.export_distribution(
            sample_distribution_data,
            filename='test_distribution',
            format=ExportFormat.JSON
        )
        
        assert result.success is True
        assert result.file_path is not None
        assert Path(result.file_path).exists()
    
    def test_export_timeline_json(self, temp_dir, sample_timeline_data):
        """Test timeline export as JSON"""
        manager = ExportManager(output_directory=temp_dir)
        
        result = manager.export_timeline(
            sample_timeline_data,
            filename='test_timeline',
            format=ExportFormat.JSON,
            separate_components=False
        )
        
        # Result should be ExportResult, not Dict
        assert isinstance(result, ExportResult)
        assert result.success is True
        assert result.file_path is not None
        assert Path(result.file_path).exists()
    
    def test_export_timeline_separate_components(self, temp_dir, sample_timeline_data):
        """Test timeline export with separate components"""
        manager = ExportManager(output_directory=temp_dir)
        
        results = manager.export_timeline(
            sample_timeline_data,
            filename='test_timeline_sep',
            format=ExportFormat.CSV,
            separate_components=True
        )
        
        assert isinstance(results, dict)
        assert 'time_series' in results
        assert 'events' in results
        assert 'action_plans' in results
        assert all(r.success for r in results.values())
    
    def test_export_batch(self, temp_dir, sample_heatmap_data):
        """Test batch export"""
        manager = ExportManager(output_directory=temp_dir)
        
        data_items = [sample_heatmap_data] * 3
        
        results = manager.export_batch(
            data_items,
            base_filename='batch_test',
            format=ExportFormat.JSON
        )
        
        assert len(results) == 3
        assert all(r.success for r in results)
        assert all(r.file_path is not None and Path(r.file_path).exists() for r in results)
    
    def test_load_exported_json(self, temp_dir, sample_heatmap_data):
        """Test loading exported JSON data"""
        manager = ExportManager(output_directory=temp_dir)
        
        # Export
        export_result = manager.export_heatmap(
            sample_heatmap_data,
            filename='test_load',
            format=ExportFormat.JSON
        )
        
        assert export_result.file_path is not None
        
        # Load
        loaded_data = manager.load_exported_data(export_result.file_path)
        
        assert isinstance(loaded_data, dict)
        assert 'dimension_type' in loaded_data
        assert loaded_data['dimension_type'] == sample_heatmap_data['dimension_type']
    
    def test_load_exported_json_compressed(self, temp_dir, sample_heatmap_data):
        """Test loading compressed JSON data"""
        manager = ExportManager(output_directory=temp_dir)
        
        # Export compressed
        export_result = manager.export_heatmap(
            sample_heatmap_data,
            filename='test_load_compressed',
            format=ExportFormat.JSON_COMPRESSED
        )
        
        assert export_result.file_path is not None
        
        # Load
        loaded_data = manager.load_exported_data(
            export_result.file_path,
            format=ExportFormat.JSON_COMPRESSED
        )
        
        assert isinstance(loaded_data, dict)
        assert 'dimension_type' in loaded_data
    
    def test_load_exported_csv(self, temp_dir, sample_heatmap_data):
        """Test loading CSV data"""
        manager = ExportManager(output_directory=temp_dir)
        
        # Export CSV
        export_result = manager.export_heatmap(
            sample_heatmap_data,
            filename='test_load_csv',
            format=ExportFormat.CSV
        )
        
        assert export_result.file_path is not None
        
        # Load
        loaded_data = manager.load_exported_data(
            export_result.file_path,
            format=ExportFormat.CSV
        )
        
        assert isinstance(loaded_data, dict)
        assert 'headers' in loaded_data
        assert 'rows' in loaded_data
    
    def test_export_without_metadata(self, temp_dir, sample_heatmap_data):
        """Test export without metadata"""
        manager = ExportManager(output_directory=temp_dir)
        
        result = manager.export_heatmap(
            sample_heatmap_data,
            filename='test_no_metadata',
            format=ExportFormat.JSON,
            include_metadata=False
        )
        
        assert result.success is True
        assert result.file_path is not None
        
        # Load and verify no export_metadata field
        loaded = manager.load_exported_data(result.file_path)
        assert 'export_metadata' not in loaded
    
    def test_file_size_tracking(self, temp_dir, sample_heatmap_data):
        """Test file size tracking"""
        manager = ExportManager(output_directory=temp_dir)
        
        result = manager.export_heatmap(
            sample_heatmap_data,
            filename='test_size',
            format=ExportFormat.JSON
        )
        
        assert result.file_path is not None
        actual_size = Path(result.file_path).stat().st_size
        assert result.file_size_bytes == actual_size
    
    def test_compression_ratio_calculation(self, temp_dir, sample_heatmap_data):
        """Test compression ratio calculation"""
        manager = ExportManager(output_directory=temp_dir)
        
        result = manager.export_heatmap(
            sample_heatmap_data,
            filename='test_compression',
            format=ExportFormat.JSON_COMPRESSED
        )
        
        assert result.compression_ratio is not None
        assert result.compression_ratio > 1.0
    
    def test_auto_format_detection(self, temp_dir, sample_heatmap_data):
        """Test automatic format detection when loading"""
        manager = ExportManager(output_directory=temp_dir)
        
        # Export JSON
        result = manager.export_heatmap(
            sample_heatmap_data,
            filename='test_auto_detect',
            format=ExportFormat.JSON
        )
        
        assert result.file_path is not None
        
        # Load without specifying format
        loaded_data = manager.load_exported_data(result.file_path, format=None)
        
        assert isinstance(loaded_data, dict)
        assert 'dimension_type' in loaded_data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
