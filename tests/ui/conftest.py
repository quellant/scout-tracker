"""
Pytest configuration for Scout Tracker UI tests using Playwright.

This module provides fixtures for running Streamlit app and managing
browser automation for end-to-end testing.
"""

import subprocess
import time
import pytest
from pathlib import Path
import shutil
import tempfile


@pytest.fixture(scope="session")
def streamlit_app():
    """
    Start the Streamlit app for the test session.

    Yields the base URL of the running app, then stops it after tests complete.
    """
    # Start Streamlit in headless mode
    process = subprocess.Popen(
        ["streamlit", "run", "app.py", "--server.headless=true", "--server.port=8501"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Wait for the app to start
    max_wait = 30  # seconds
    start_time = time.time()
    app_ready = False

    while time.time() - start_time < max_wait:
        try:
            # Try to connect to the app
            import requests
            response = requests.get("http://localhost:8501", timeout=1)
            if response.status_code == 200:
                app_ready = True
                break
        except:
            pass
        time.sleep(0.5)

    if not app_ready:
        process.kill()
        raise RuntimeError("Streamlit app failed to start within 30 seconds")

    # Give it a moment to fully initialize
    time.sleep(2)

    yield "http://localhost:8501"

    # Cleanup: stop the Streamlit process
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()


@pytest.fixture(scope="function")
def page(playwright, streamlit_app):
    """
    Create a new browser page for each test.

    Args:
        playwright: Playwright instance
        streamlit_app: URL of the running Streamlit app

    Yields a configured browser page, then closes it after the test.
    """
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        user_agent="Mozilla/5.0 (Playwright Test)"
    )
    page = context.new_page()

    # Navigate to the app
    page.goto(streamlit_app)

    # Wait for the app to be ready
    page.wait_for_selector("text=Scout Tracker", timeout=10000)

    yield page

    # Cleanup
    context.close()
    browser.close()


@pytest.fixture(scope="function")
def test_data_backup():
    """
    Backup and restore tracker_data for tests that modify data.

    Creates a temporary backup of tracker_data before the test,
    then restores it after the test completes.
    """
    data_dir = Path("tracker_data")

    # Create backup if data exists
    backup_dir = None
    if data_dir.exists():
        backup_dir = Path(tempfile.mkdtemp(prefix="scout_tracker_backup_"))
        shutil.copytree(data_dir, backup_dir / "tracker_data")

    yield

    # Restore backup
    if backup_dir and backup_dir.exists():
        if data_dir.exists():
            shutil.rmtree(data_dir)
        shutil.copytree(backup_dir / "tracker_data", data_dir)
        shutil.rmtree(backup_dir)


def click_nav_item(page, item_text):
    """
    Helper function to click a navigation item.

    Args:
        page: Playwright page object
        item_text: Text of the navigation item to click
    """
    # Find the label containing the text
    page.evaluate(f"""
        () => {{
            const labels = Array.from(document.querySelectorAll('label'));
            const targetLabel = labels.find(label => label.textContent.includes('{item_text}'));
            if (targetLabel) {{
                const radio = targetLabel.querySelector('input[type="radio"]') ||
                             targetLabel.parentElement.querySelector('input[type="radio"]');
                if (radio) {{
                    radio.click();
                }}
            }}
        }}
    """)
    # Wait for page to update
    time.sleep(1)


def wait_for_streamlit(page, timeout=5000):
    """
    Wait for Streamlit to finish rendering.

    Args:
        page: Playwright page object
        timeout: Maximum time to wait in milliseconds
    """
    page.wait_for_timeout(timeout)
