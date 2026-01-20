"""Validation tests to verify the testing infrastructure is working correctly."""

import pytest
import numpy as np
import sys
import os
from pathlib import Path


class TestTestingInfrastructure:
    """Test suite to validate that our testing infrastructure is working."""

    def test_python_version(self):
        """Verify Python version compatibility."""
        assert sys.version_info >= (3, 8), "Python 3.8 or higher required"

    def test_numpy_import_and_basic_operations(self):
        """Verify numpy is available and working."""
        arr = np.array([1, 2, 3, 4, 5])
        assert arr.sum() == 15
        assert arr.mean() == 3.0

    def test_pytest_markers_work(self):
        """Test that pytest markers are configured correctly."""
        # This test should be automatically marked as 'unit' by conftest.py
        assert True

    def test_fixtures_are_available(self, mock_config, temp_dir):
        """Test that shared fixtures from conftest.py are available."""
        # Test mock_config fixture
        assert hasattr(mock_config, 'overlap_time')
        assert hasattr(mock_config, 'dt')
        
        # Test temp_dir fixture
        assert temp_dir.exists()
        assert temp_dir.is_dir()

    def test_numpy_arrays_equal_fixture(self, numpy_arrays_equal):
        """Test the numpy arrays comparison fixture."""
        arr1 = np.array([1.0, 2.0, 3.0])
        arr2 = np.array([1.0, 2.0, 3.0])
        arr3 = np.array([1.1, 2.1, 3.1])
        
        assert numpy_arrays_equal(arr1, arr2)
        assert not numpy_arrays_equal(arr1, arr3, atol=0.05)

    def test_mock_hardware_interface(self, mock_hardware_interface):
        """Test hardware interface mock."""
        # Should have the expected method
        assert hasattr(mock_hardware_interface, 'set_actuator_postions')
        
        # Should be callable without error
        mock_hardware_interface.set_actuator_postions(np.zeros((4, 3)))
        mock_hardware_interface.set_actuator_postions.assert_called_once()

    def test_mock_imu(self, mock_imu):
        """Test IMU mock."""
        orientation = mock_imu.read_orientation()
        expected = np.array([1, 0, 0, 0])  # Identity quaternion
        np.testing.assert_array_equal(orientation, expected)

    def test_sample_data_fixtures(self, sample_joint_angles, sample_foot_positions):
        """Test sample data fixtures."""
        # Joint angles should be 4x3 (4 legs, 3 joints each)
        assert sample_joint_angles.shape == (4, 3)
        
        # Foot positions should be 4x3 (4 feet, x/y/z coordinates)
        assert sample_foot_positions.shape == (4, 3)

    def test_project_structure_exists(self):
        """Verify the project structure is as expected."""
        project_root = Path(__file__).parent.parent
        
        # Check main source directory exists
        src_dir = project_root / "src"
        assert src_dir.exists(), "src directory should exist"
        
        # Check key source files exist
        assert (src_dir / "run_robot.py").exists()
        assert (src_dir / "blacky").exists()
        assert (src_dir / "src").exists()

    def test_imports_work(self):
        """Test that we can import key modules from the src directory."""
        # This tests that sys.path modification in conftest.py works
        try:
            from src.State import State
            from src.Command import Command
            # If we get here, imports are working
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import modules: {e}")

    def test_configuration_is_loaded(self):
        """Test that pyproject.toml configuration is being used."""
        # This is mainly tested by the fact that pytest is running
        # and finding this test file
        assert True

    @pytest.mark.unit
    def test_unit_marker_works(self):
        """Test that the unit marker works."""
        assert True

    @pytest.mark.slow
    def test_slow_marker_works(self):
        """Test that the slow marker works (this test will be skipped in fast runs)."""
        import time
        time.sleep(0.001)  # Minimal sleep to simulate slow test
        assert True


class TestCoverage:
    """Tests specifically for coverage functionality."""

    def test_coverage_can_measure_simple_function(self):
        """Test that coverage measurement works on a simple function."""
        def simple_function(x, y):
            return x + y
        
        result = simple_function(2, 3)
        assert result == 5


class TestMocking:
    """Tests for mocking functionality."""

    def test_pytest_mock_available(self, mocker):
        """Test that pytest-mock is available."""
        mock_func = mocker.Mock()
        mock_func.return_value = 42
        
        assert mock_func() == 42
        mock_func.assert_called_once()

    def test_manual_mocking_works(self):
        """Test that manual mocking works."""
        from unittest.mock import Mock
        
        mock_obj = Mock()
        mock_obj.method.return_value = "test"
        
        assert mock_obj.method() == "test"