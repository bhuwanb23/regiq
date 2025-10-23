"""
Visualization Data Utilities

Shared utilities for data transformation, validation, and normalization
for visualization data structures. Pure backend utilities.

Author: REGIQ AI/ML Team
Phase: 4.4 - Visualization & Reporting
"""

from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from datetime import datetime, timedelta


class DataValidator:
    """Validate visualization data structures"""
    
    @staticmethod
    def validate_heatmap_data(heatmap_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate heatmap data structure
        
        Args:
            heatmap_data: Heatmap data to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        required_fields = ['dimension_type', 'x_categories', 'y_categories', 'matrix', 'cells']
        
        for field in required_fields:
            if field not in heatmap_data:
                return False, f"Missing required field: {field}"
        
        # Validate matrix dimensions
        y_len = len(heatmap_data['y_categories'])
        x_len = len(heatmap_data['x_categories'])
        matrix = heatmap_data['matrix']
        
        if len(matrix) != y_len:
            return False, f"Matrix rows ({len(matrix)}) don't match y_categories ({y_len})"
        
        for i, row in enumerate(matrix):
            if len(row) != x_len:
                return False, f"Matrix row {i} length ({len(row)}) doesn't match x_categories ({x_len})"
        
        # Validate cells
        expected_cells = x_len * y_len
        if len(heatmap_data['cells']) != expected_cells:
            return False, f"Cell count ({len(heatmap_data['cells'])}) doesn't match expected ({expected_cells})"
        
        return True, None
    
    @staticmethod
    def validate_distribution_data(distribution_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate distribution analysis data structure
        
        Args:
            distribution_data: Distribution data to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        required_fields = ['distribution_type', 'histogram', 'pdf_cdf', 'statistics']
        
        for field in required_fields:
            if field not in distribution_data:
                return False, f"Missing required field: {field}"
        
        # Validate histogram
        histogram = distribution_data['histogram']
        required_hist_fields = ['bin_edges', 'bin_counts', 'bin_centers']
        for field in required_hist_fields:
            if field not in histogram:
                return False, f"Missing histogram field: {field}"
        
        # Validate lengths
        num_bins = len(histogram['bin_counts'])
        if len(histogram['bin_centers']) != num_bins:
            return False, "Histogram bin_centers length doesn't match bin_counts"
        
        if len(histogram['bin_edges']) != num_bins + 1:
            return False, "Histogram bin_edges should be bin_counts + 1"
        
        # Validate PDF/CDF
        pdf_cdf = distribution_data['pdf_cdf']
        required_pdf_fields = ['x_values', 'pdf_values', 'cdf_values']
        for field in required_pdf_fields:
            if field not in pdf_cdf:
                return False, f"Missing PDF/CDF field: {field}"
        
        num_points = len(pdf_cdf['x_values'])
        if len(pdf_cdf['pdf_values']) != num_points:
            return False, "PDF values length doesn't match x_values"
        if len(pdf_cdf['cdf_values']) != num_points:
            return False, "CDF values length doesn't match x_values"
        
        return True, None
    
    @staticmethod
    def validate_timeline_data(timeline_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate timeline projection data structure
        
        Args:
            timeline_data: Timeline data to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        required_fields = ['start_date', 'end_date', 'time_series', 'events']
        
        for field in required_fields:
            if field not in timeline_data:
                return False, f"Missing required field: {field}"
        
        # Validate dates
        try:
            start_date = datetime.fromisoformat(timeline_data['start_date'])
            end_date = datetime.fromisoformat(timeline_data['end_date'])
            
            if start_date >= end_date:
                return False, "start_date must be before end_date"
        except Exception as e:
            return False, f"Invalid date format: {str(e)}"
        
        # Validate time series
        for point in timeline_data['time_series']:
            if 'timestamp' not in point or 'value' not in point:
                return False, "Time series point missing timestamp or value"
        
        # Validate events
        for event in timeline_data['events']:
            required_event_fields = ['event_id', 'timestamp', 'event_type', 'title']
            for field in required_event_fields:
                if field not in event:
                    return False, f"Event missing required field: {field}"
        
        return True, None


class DataTransformer:
    """Transform and normalize visualization data"""
    
    @staticmethod
    def normalize_risk_scores(
        risk_scores: List[float],
        target_range: Tuple[float, float] = (0.0, 1.0)
    ) -> List[float]:
        """
        Normalize risk scores to target range
        
        Args:
            risk_scores: Original risk scores
            target_range: Target min/max range
            
        Returns:
            Normalized risk scores
        """
        if not risk_scores:
            return []
        
        scores_array = np.array(risk_scores)
        min_score = np.min(scores_array)
        max_score = np.max(scores_array)
        
        if max_score == min_score:
            # All scores are the same
            return [float(np.mean(target_range))] * len(risk_scores)
        
        # Normalize to [0, 1]
        normalized = (scores_array - min_score) / (max_score - min_score)
        
        # Scale to target range
        target_min, target_max = target_range
        scaled = normalized * (target_max - target_min) + target_min
        
        return scaled.tolist()
    
    @staticmethod
    def aggregate_time_series(
        time_series: List[Dict[str, Any]],
        interval: str = 'daily'
    ) -> List[Dict[str, Any]]:
        """
        Aggregate time series to different intervals
        
        Args:
            time_series: Original time series data
            interval: Target interval ('hourly', 'daily', 'weekly', 'monthly')
            
        Returns:
            Aggregated time series
        """
        if not time_series:
            return []
        
        # Group by interval
        interval_data = {}
        
        for point in time_series:
            timestamp = datetime.fromisoformat(point['timestamp'])
            
            # Determine interval key
            if interval == 'hourly':
                key = timestamp.replace(minute=0, second=0, microsecond=0)
            elif interval == 'daily':
                key = timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
            elif interval == 'weekly':
                # Start of week (Monday)
                days_since_monday = timestamp.weekday()
                key = (timestamp - timedelta(days=days_since_monday)).replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
            elif interval == 'monthly':
                key = timestamp.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            else:
                key = timestamp
            
            if key not in interval_data:
                interval_data[key] = []
            interval_data[key].append(point)
        
        # Aggregate each interval
        aggregated = []
        for key in sorted(interval_data.keys()):
            points = interval_data[key]
            values = [p['value'] for p in points]
            
            aggregated.append({
                'timestamp': key.isoformat(),
                'value': float(np.mean(values)),
                'min_value': float(np.min(values)),
                'max_value': float(np.max(values)),
                'count': len(points),
                'metadata': {
                    'interval': interval,
                    'aggregated': True
                }
            })
        
        return aggregated
    
    @staticmethod
    def smooth_time_series(
        time_series: List[Dict[str, Any]],
        window_size: int = 7,
        method: str = 'moving_average'
    ) -> List[Dict[str, Any]]:
        """
        Smooth time series data
        
        Args:
            time_series: Original time series
            window_size: Smoothing window size
            method: Smoothing method ('moving_average', 'exponential')
            
        Returns:
            Smoothed time series
        """
        if not time_series or len(time_series) < window_size:
            return time_series
        
        values = np.array([point['value'] for point in time_series])
        
        if method == 'moving_average':
            # Simple moving average
            smoothed = np.convolve(values, np.ones(window_size)/window_size, mode='same')
        elif method == 'exponential':
            # Exponential moving average
            alpha = 2 / (window_size + 1)
            smoothed = np.zeros_like(values)
            smoothed[0] = values[0]
            for i in range(1, len(values)):
                smoothed[i] = alpha * values[i] + (1 - alpha) * smoothed[i-1]
        else:
            smoothed = values
        
        # Create smoothed time series
        result = []
        for i, point in enumerate(time_series):
            result.append({
                **point,
                'value': float(smoothed[i]),
                'original_value': point['value'],
                'metadata': {
                    **point.get('metadata', {}),
                    'smoothed': True,
                    'method': method,
                    'window_size': window_size
                }
            })
        
        return result
    
    @staticmethod
    def detect_outliers(
        values: List[float],
        method: str = 'iqr',
        threshold: float = 1.5
    ) -> List[bool]:
        """
        Detect outliers in data
        
        Args:
            values: Data values
            method: Detection method ('iqr', 'zscore')
            threshold: Threshold for outlier detection
            
        Returns:
            Boolean list indicating outliers
        """
        if not values:
            return []
        
        values_array = np.array(values)
        
        if method == 'iqr':
            # Interquartile range method
            q1 = np.percentile(values_array, 25)
            q3 = np.percentile(values_array, 75)
            iqr = q3 - q1
            
            lower_bound = q1 - threshold * iqr
            upper_bound = q3 + threshold * iqr
            
            return ((values_array < lower_bound) | (values_array > upper_bound)).tolist()
            
        elif method == 'zscore':
            # Z-score method
            mean = np.mean(values_array)
            std = np.std(values_array)
            
            if std == 0:
                return [False] * len(values)
            
            z_scores = np.abs((values_array - mean) / std)
            return (z_scores > threshold).tolist()
        
        else:
            return [False] * len(values)
    
    @staticmethod
    def interpolate_missing_values(
        time_series: List[Dict[str, Any]],
        method: str = 'linear'
    ) -> List[Dict[str, Any]]:
        """
        Interpolate missing values in time series
        
        Args:
            time_series: Time series with potential gaps
            method: Interpolation method ('linear', 'forward_fill')
            
        Returns:
            Time series with interpolated values
        """
        if not time_series:
            return []
        
        result = []
        
        for i, point in enumerate(time_series):
            if point.get('value') is None or np.isnan(point.get('value', 0)):
                # Need to interpolate
                if method == 'linear' and i > 0:
                    # Find next valid value
                    next_valid_idx = None
                    for j in range(i + 1, len(time_series)):
                        if time_series[j].get('value') is not None:
                            next_valid_idx = j
                            break
                    
                    if next_valid_idx is not None:
                        # Linear interpolation
                        prev_value = result[-1]['value']
                        next_value = time_series[next_valid_idx]['value']
                        steps = next_valid_idx - i + 1
                        interpolated = prev_value + (next_value - prev_value) / steps
                    else:
                        # Use previous value
                        interpolated = result[-1]['value'] if result else 0.0
                        
                elif method == 'forward_fill' and result:
                    interpolated = result[-1]['value']
                else:
                    interpolated = 0.0
                
                result.append({
                    **point,
                    'value': float(interpolated),
                    'metadata': {
                        **point.get('metadata', {}),
                        'interpolated': True,
                        'method': method
                    }
                })
            else:
                result.append(point)
        
        return result


class ColorMapper:
    """Map values to colors for visualization"""
    
    @staticmethod
    def map_risk_to_color(
        risk_score: float,
        color_scheme: str = 'red_yellow_green'
    ) -> str:
        """
        Map risk score to color
        
        Args:
            risk_score: Risk score [0, 1]
            color_scheme: Color scheme name
            
        Returns:
            Hex color code
        """
        if color_scheme == 'red_yellow_green':
            if risk_score >= 0.75:
                return '#D32F2F'  # Red (critical)
            elif risk_score >= 0.5:
                return '#F57C00'  # Orange (high)
            elif risk_score >= 0.25:
                return '#FBC02D'  # Yellow (medium)
            else:
                return '#388E3C'  # Green (low)
                
        elif color_scheme == 'heat':
            # Gradient from yellow to red
            if risk_score >= 0.75:
                return '#8B0000'  # Dark red
            elif risk_score >= 0.5:
                return '#FF4500'  # Orange red
            elif risk_score >= 0.25:
                return '#FFA500'  # Orange
            else:
                return '#FFD700'  # Gold
                
        elif color_scheme == 'blue_red':
            if risk_score >= 0.75:
                return '#B71C1C'  # Dark red
            elif risk_score >= 0.5:
                return '#D32F2F'  # Red
            elif risk_score >= 0.25:
                return '#1976D2'  # Blue
            else:
                return '#0D47A1'  # Dark blue
                
        else:
            # Default grayscale
            intensity = int((1 - risk_score) * 255)
            return f'#{intensity:02X}{intensity:02X}{intensity:02X}'
    
    @staticmethod
    def generate_gradient_colors(
        num_colors: int,
        start_color: str = '#00FF00',
        end_color: str = '#FF0000'
    ) -> List[str]:
        """
        Generate gradient colors
        
        Args:
            num_colors: Number of colors to generate
            start_color: Start color (hex)
            end_color: End color (hex)
            
        Returns:
            List of hex colors
        """
        # Convert hex to RGB
        start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
        end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
        
        colors = []
        for i in range(num_colors):
            ratio = i / max(1, num_colors - 1)
            r = int(start_rgb[0] + ratio * (end_rgb[0] - start_rgb[0]))
            g = int(start_rgb[1] + ratio * (end_rgb[1] - start_rgb[1]))
            b = int(start_rgb[2] + ratio * (end_rgb[2] - start_rgb[2]))
            colors.append(f'#{r:02X}{g:02X}{b:02X}')
        
        return colors


class DataAggregator:
    """Aggregate data for visualization"""
    
    @staticmethod
    def aggregate_by_category(
        data: List[Dict[str, Any]],
        category_field: str,
        value_field: str,
        aggregation: str = 'sum'
    ) -> Dict[str, float]:
        """
        Aggregate data by category
        
        Args:
            data: List of data items
            category_field: Field to group by
            value_field: Field to aggregate
            aggregation: Aggregation method ('sum', 'mean', 'max', 'min', 'count')
            
        Returns:
            Dictionary mapping categories to aggregated values
        """
        category_data = {}
        
        for item in data:
            category = item.get(category_field, 'Unknown')
            value = item.get(value_field, 0)
            
            if category not in category_data:
                category_data[category] = []
            category_data[category].append(value)
        
        # Aggregate
        result = {}
        for category, values in category_data.items():
            if aggregation == 'sum':
                result[category] = float(np.sum(values))
            elif aggregation == 'mean':
                result[category] = float(np.mean(values))
            elif aggregation == 'max':
                result[category] = float(np.max(values))
            elif aggregation == 'min':
                result[category] = float(np.min(values))
            elif aggregation == 'count':
                result[category] = float(len(values))
            else:
                result[category] = float(np.sum(values))
        
        return result
    
    @staticmethod
    def calculate_moving_statistics(
        values: List[float],
        window_size: int = 7
    ) -> Dict[str, List[float]]:
        """
        Calculate moving statistics
        
        Args:
            values: Data values
            window_size: Window size for calculations
            
        Returns:
            Dictionary of moving statistics
        """
        values_array = np.array(values)
        
        moving_mean = []
        moving_std = []
        moving_min = []
        moving_max = []
        
        for i in range(len(values)):
            window_start = max(0, i - window_size + 1)
            window = values_array[window_start:i+1]
            
            moving_mean.append(float(np.mean(window)))
            moving_std.append(float(np.std(window)))
            moving_min.append(float(np.min(window)))
            moving_max.append(float(np.max(window)))
        
        return {
            'moving_mean': moving_mean,
            'moving_std': moving_std,
            'moving_min': moving_min,
            'moving_max': moving_max
        }
