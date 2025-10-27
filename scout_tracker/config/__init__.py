"""
Scout Tracker Configuration Package

This package provides all configuration constants and rank requirements
for the Scout Tracker application.

Exports:
    DATA_DIR: Path to the tracker data directory
    ROSTER_FILE: Path to the roster CSV file
    REQUIREMENT_KEY_FILE: Path to the requirement key CSV file
    MEETINGS_FILE: Path to the meetings CSV file
    ATTENDANCE_FILE: Path to the attendance CSV file
    RANK_REQUIREMENTS: Dictionary mapping rank names to their requirements
    LION_REQUIREMENTS: List of Lion Scout requirements
    TIGER_REQUIREMENTS: List of Tiger Scout requirements
    WOLF_REQUIREMENTS: List of Wolf Scout requirements
    BEAR_REQUIREMENTS: List of Bear Scout requirements
    WEBELOS_REQUIREMENTS: List of Webelos Scout requirements
"""

from .constants import (
    DATA_DIR,
    ROSTER_FILE,
    REQUIREMENT_KEY_FILE,
    MEETINGS_FILE,
    ATTENDANCE_FILE,
    RANK_REQUIREMENTS,
    LION_REQUIREMENTS,
    TIGER_REQUIREMENTS,
    WOLF_REQUIREMENTS,
    BEAR_REQUIREMENTS,
    WEBELOS_REQUIREMENTS,
)

__all__ = [
    "DATA_DIR",
    "ROSTER_FILE",
    "REQUIREMENT_KEY_FILE",
    "MEETINGS_FILE",
    "ATTENDANCE_FILE",
    "RANK_REQUIREMENTS",
    "LION_REQUIREMENTS",
    "TIGER_REQUIREMENTS",
    "WOLF_REQUIREMENTS",
    "BEAR_REQUIREMENTS",
    "WEBELOS_REQUIREMENTS",
]
