"""
Scout Tracker - A Cub Scout Advancement Tracking Application

This package provides a modular architecture for tracking Cub Scout advancement
across all ranks from Lion (Kindergarten) through Webelos (4th Grade).

Package Structure:
    config: Configuration constants and rank requirements
    data: Data loading, saving, and caching operations
    services: Business logic and advancement tracking services
    ui: Streamlit user interface components and pages

Usage:
    Import configuration constants:
        from scout_tracker.config import RANK_REQUIREMENTS, DATA_DIR
    
    Import data operations:
        from scout_tracker.data import load_roster, save_progress
    
    Import services:
        from scout_tracker.services import calculate_advancement
    
    Import UI components:
        from scout_tracker.ui import render_dashboard

Version: 2.0.0 (Modular Refactored)
"""

__version__ = "2.0.0"
__author__ = "Scout Tracker Development Team"

# Re-export key constants for convenience
from .config import (
    DATA_DIR,
    ROSTER_FILE,
    RANK_REQUIREMENTS,
)

__all__ = [
    "DATA_DIR",
    "ROSTER_FILE",
    "RANK_REQUIREMENTS",
]
