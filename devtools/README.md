# Installation

### Chrome (this only needs to be done once)
1. Go to `chrome://extensions/`
2. Click "Load unpacked" → Select `devtools`
3. Click the `⟳` button when changes are made

### Firefox (this needs to be done after each restart)
1. Change the following in `manifest.json`:
    ```diff
    {
      "background": {
    -    "service_worker": "src/service_worker.js"
    +    "scripts": [ "src/service_worker.js" ]
      }
    }
    ```
2. Go to `about:debugging`
3. Click "This Firefox" → "Load Temporary Add-on..." → Select `manifest.json`
4. Click "Reload" when changes are made
5. Go to `about:addons`
6. Click "Extensions" → "AgTern DevTools" → "Permissions"
7. Enable "Access your data for all websites" (if this is not done then the extension button needs to be clicked to give access)

# Usage

### Opening the Side Panel
The side panel can be accessed via the extension's button in the toolbar. This button can be pinned for easy access. You can also open it via the right-click menu on any page.

### Utilizing Scraping Functions
`agtern_devtools.js` and `agtern_devtools.css` are injected into every webpage while the extension is enabled. The functions in `agtern_devtools.js` such as `scrape(xpath)`, `scrape_links(xpath)`, and `scrape_elements(xpath)` can be used in the main devtools console.

### Troubleshooting
When the extension is first enabled, the proper scripts may not be injected properly until the page is refreshed. When in doubt, refresh the page and reopen the panel.

If the extension doesn't work on a single website (or breaks a single website), one of the function names in `agtern_devtools.js` may be clashing with a function name used by the website. An error will be logged if this occurs. Unfortunately, the only way to remedy this is to either rename the function or disable the extension.

### Debugging
The main devtools console will contain errors from `agtern_devtools.js`. The errors from `service_worker.js` can be found by inspecting the extension on `chrome://extensions/` or `about:debugging`. The errors from `side_panel.js` can be found by right-clicking on the side panel and inspecting it. Some manifest errors are expected due to the manifest format being slightly different between browsers.

### Demo
https://youtu.be/_af0a4QpDvY
