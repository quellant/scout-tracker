# Playwright MCP Setup Guide for WSL2
**Scout Tracker Application - Video Recording Setup**

Date: October 25, 2025

---

## Overview

This guide shows you how to set up Playwright MCP server with video recording capabilities on WSL2 to capture screen recordings of the Scout Tracker Streamlit application.

---

## Prerequisites

- WSL2 running on Windows
- Claude Code installed
- Scout Tracker application (this project)

---

## Step 1: Install Node.js in WSL2

First, check if Node.js is already installed:

```bash
node --version
npm --version
```

If not installed, install Node.js 18.x or later:

```bash
# Install Node.js using NodeSource repository
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
```

---

## Step 2: Install Playwright MCP Server

Install the Playwright MCP server globally:

```bash
npm install -g @executeautomation/playwright-mcp-server
```

**Note:** This package provides the Playwright MCP server that Claude Code can connect to.

---

## Step 3: Configure Claude Code MCP Settings

### Option A: Headless Mode (No visible browser)

Edit your Claude Code MCP configuration file:

**Location:** `~/.config/claude-code/mcp_settings.json` (Linux/WSL2)

Add this configuration:

```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": [
        "@executeautomation/playwright-mcp-server",
        "--save-video"
      ],
      "env": {
        "DISPLAY": ":0"
      }
    }
  }
}
```

### Option B: Headed Mode (Visible browser window)

For headed mode, you'll need an X server running on Windows.

**Install VcXsrv on Windows:**

1. Download VcXsrv from: https://sourceforge.net/projects/vcxsrv/
2. Install and launch XLaunch
3. Choose settings:
   - Multiple windows
   - Display number: 0
   - Start no client
   - **IMPORTANT:** Check "Disable access control"

**Configure WSL2 to use Windows X server:**

Add to your `~/.bashrc`:

```bash
# X Server configuration for WSL2
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
export LIBGL_ALWAYS_INDIRECT=1
```

Reload the configuration:

```bash
source ~/.bashrc
```

**MCP Configuration for headed mode:**

```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": [
        "@executeautomation/playwright-mcp-server",
        "--headless=false",
        "--save-video"
      ],
      "env": {
        "DISPLAY": ":0"
      }
    }
  }
}
```

---

## Step 4: Restart Claude Code

After editing the MCP configuration, restart Claude Code completely:

```bash
# Exit Claude Code
# Restart Claude Code
```

---

## Step 5: Verify Playwright MCP is Available

Once Claude Code restarts, Playwright tools should be available:

- `puppeteer_navigate` - Navigate to a URL
- `puppeteer_screenshot` - Take screenshots
- `puppeteer_click` - Click elements
- `puppeteer_fill` - Fill form fields
- `puppeteer_evaluate` - Run JavaScript
- And more...

**Video Recording:** Videos are automatically saved when using these tools with `--save-video` flag.

---

## Step 6: Test the Setup

### Simple Test

Ask Claude Code to:

```
Navigate to google.com with puppeteer and take a screenshot
```

This will:
1. Launch a browser
2. Navigate to Google
3. Take a screenshot
4. Save a video of the session

### Scout Tracker Test

To record your Scout Tracker application:

1. **Start the Scout Tracker application:**
   ```bash
   streamlit run scout_tracker/app.py
   ```

2. **Ask Claude Code:**
   ```
   Navigate to http://localhost:8501 with puppeteer and take screenshots of each page
   ```

This will create a video recording of Claude navigating through your Scout Tracker application.

---

## Video Output Location

Videos are saved to:

```
~/.config/playwright/videos/
```

Or check the Playwright output directory:

```bash
ls -la ~/.config/playwright/videos/
```

---

## Troubleshooting

### Issue: "Could not find browser"

**Solution:** Install Playwright browsers:

```bash
npx playwright install chromium
npx playwright install-deps chromium
```

### Issue: "Cannot open display" (Headed mode)

**Solution:**

1. Verify VcXsrv is running on Windows
2. Check DISPLAY variable:
   ```bash
   echo $DISPLAY
   ```
3. Test X server connection:
   ```bash
   xclock
   ```
   If xclock appears, X server is working.

### Issue: "Permission denied" for video directory

**Solution:**

```bash
mkdir -p ~/.config/playwright/videos
chmod 755 ~/.config/playwright/videos
```

---

## Usage Examples

### Example 1: Record Scout Tracker Dashboard

```
1. Start Scout Tracker: streamlit run scout_tracker/app.py
2. Ask Claude Code:
   "Navigate to http://localhost:8501 with puppeteer,
    take a screenshot of the dashboard,
    then click on 'Individual Reports' and take another screenshot"
```

### Example 2: Record User Interactions

```
Ask Claude Code:
"Navigate to http://localhost:8501 with puppeteer,
 fill in the scout name field with 'Test Scout',
 click the submit button,
 and take a screenshot of the result"
```

### Example 3: Export Video for Documentation

After recording:

```bash
# Videos are saved in ~/.config/playwright/videos/
# Copy to project for documentation
cp ~/.config/playwright/videos/latest.webm ~/projects/lion-tracker/demo_videos/
```

---

## Configuration Options

### Video Quality

Modify the MCP configuration to adjust video quality:

```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": [
        "@executeautomation/playwright-mcp-server",
        "--save-video",
        "--video-size=1920x1080"
      ]
    }
  }
}
```

### Viewport Size

Set custom viewport in Claude Code commands:

```
Navigate to http://localhost:8501 with puppeteer using viewport 1300x1500
```

---

## Best Practices

1. **Start Streamlit first** before recording
2. **Use specific viewports** (1300x1500 recommended for Streamlit apps)
3. **Organize videos** by copying them to your project directory
4. **Test headless first** - it's simpler and faster
5. **Use headed mode for debugging** - see what's happening in real-time

---

## Summary

You now have Playwright MCP configured with video recording capabilities!

**To record Scout Tracker:**

```bash
# Terminal 1: Start Scout Tracker
streamlit run scout_tracker/app.py

# Terminal 2 (or Claude Code): Ask Claude to navigate and interact
# Example: "Navigate to http://localhost:8501 with puppeteer and show me the dashboard"
```

Videos will be automatically saved to `~/.config/playwright/videos/`.

---

## Next Steps

- Test with simple navigation
- Record Scout Tracker demo
- Create documentation videos
- Share demos with your pack!

---

**Setup Complete!** You can now record browser sessions of your Scout Tracker application.
