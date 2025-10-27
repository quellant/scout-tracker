"""
Scout Tracker Application Entry Point

This is the main entry point for running the Scout Tracker application with Streamlit.
Run with: streamlit run app.py (for development)
Or run the compiled executable directly (for production)
"""

import sys
import os
import tempfile

if __name__ == "__main__":
    # Check if we're running as a PyInstaller executable
    if getattr(sys, 'frozen', False):
        # Running as compiled executable - start Streamlit server programmatically
        from streamlit.web import cli as stcli
        import atexit

        # Create a temporary Python script for Streamlit to execute
        # This is necessary because Streamlit needs a .py file to run
        temp_dir = tempfile.mkdtemp()
        temp_script = os.path.join(temp_dir, 'scout_tracker_app.py')

        # Write the UI code to the temporary script
        with open(temp_script, 'w', encoding='utf-8') as f:
            f.write('''
# Auto-generated Streamlit script for Scout Tracker executable
from scout_tracker.ui.app import main

if __name__ == "__main__":
    main()
''')

        # Clean up temp file on exit
        def cleanup():
            try:
                if os.path.exists(temp_script):
                    os.remove(temp_script)
                if os.path.exists(temp_dir):
                    os.rmdir(temp_dir)
            except:
                pass

        atexit.register(cleanup)

        # Configure Streamlit arguments
        sys.argv = [
            "streamlit",
            "run",
            temp_script,
            "--server.headless=true",
            "--browser.serverAddress=localhost",
            "--server.port=8501",
            "--global.developmentMode=false"
        ]

        # Start Streamlit CLI
        sys.exit(stcli.main())
    else:
        # Running as normal Python script - import and run the UI
        from scout_tracker.ui.app import main
        main()
