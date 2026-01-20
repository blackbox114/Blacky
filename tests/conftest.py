"""Shared pytest fixtures for the blacky robot testing suite."""

import pytest
import numpy as np
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock
import sys
import os

# Add src directory to Python path for imports during testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def mock_config():
    """Mock configuration object for robot tests."""
    config = Mock()
    config.overlap_time = 0.1
    config.swing_time = 0.2
    config.z_clearance = 0.05
    config.x_shift = 0.0
    config.dt = 0.01
    config.ps4_color = [0, 0, 255]
    config.ps4_deactivated_color = [255, 0, 0]
    return config


@pytest.fixture
def mock_hardware_interface():
    """Mock hardware interface for testing without actual hardware."""
    hardware = MagicMock()
    hardware.set_actuator_postions = Mock()
    return hardware


@pytest.fixture
def mock_imu():
    """Mock IMU interface for testing without actual hardware."""
    imu = MagicMock()
    imu.read_orientation.return_value = np.array([1, 0, 0, 0])  # Identity quaternion
    imu.flush_buffer = Mock()
    return imu


@pytest.fixture
def mock_joystick():
    """Mock joystick interface for testing without actual controller."""
    joystick = MagicMock()
    
    # Mock command object
    mock_command = Mock()
    mock_command.activate_event = 0
    mock_command.horizontal_velocity = np.array([0.0, 0.0])
    mock_command.yaw_rate = 0.0
    mock_command.height = 0.0
    mock_command.pitch = 0.0
    mock_command.roll = 0.0
    
    joystick.get_command.return_value = mock_command
    joystick.set_color = Mock()
    
    return joystick


@pytest.fixture
def sample_joint_angles():
    """Sample joint angles for testing kinematics."""
    return np.array([
        [0.0, 0.5, -1.0],  # Front left leg
        [0.0, 0.5, -1.0],  # Front right leg
        [0.0, 0.5, -1.0],  # Back left leg
        [0.0, 0.5, -1.0],  # Back right leg
    ])


@pytest.fixture
def sample_foot_positions():
    """Sample foot positions for testing kinematics."""
    return np.array([
        [0.1, 0.1, -0.16],   # Front left
        [0.1, -0.1, -0.16],  # Front right
        [-0.1, 0.1, -0.16],  # Back left
        [-0.1, -0.1, -0.16], # Back right
    ])


@pytest.fixture
def mock_state():
    """Mock robot state for testing."""
    state = Mock()
    state.quat_orientation = np.array([1, 0, 0, 0])
    state.joint_angles = np.zeros((4, 3))
    state.foot_locations = np.zeros((4, 3))
    state.behavior_state = "TROT"
    state.ticks = 0
    return state


@pytest.fixture
def numpy_arrays_equal():
    """Fixture providing a helper function to compare numpy arrays."""
    def _arrays_equal(a, b, rtol=1e-5, atol=1e-8):
        """Compare two numpy arrays for equality with tolerance."""
        return np.allclose(a, b, rtol=rtol, atol=atol)
    return _arrays_equal


@pytest.fixture(autouse=True)
def mock_pigpio():
    """Automatically mock pigpio library for all tests."""
    mock_pi = Mock()
    mock_pi.set_servo_pulsewidth = Mock()
    mock_pi.stop = Mock()
    
    # Mock the pigpio.pi() constructor
    with pytest.MonkeyPatch.context() as m:
        m.setattr('pigpio.pi', lambda: mock_pi)
        yield mock_pi


@pytest.fixture
def mock_serial():
    """Mock serial interface for IMU testing."""
    serial_mock = Mock()
    serial_mock.read = Mock(return_value=b'1.0,0.0,0.0,0.0\n')
    serial_mock.write = Mock()
    serial_mock.flush = Mock()
    serial_mock.close = Mock()
    return serial_mock


# Pytest configuration hooks
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "slow: Slow running tests")


def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on their location."""
    for item in items:
        # Mark tests in unit directory as unit tests
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        # Mark tests in integration directory as integration tests
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)