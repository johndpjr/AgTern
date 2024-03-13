
// This is the service worker that manages the background processing of the extension.
// It has access to all the Chrome extension APIs.
// https://developer.chrome.com/docs/extensions/mv3/service_workers/

// Open the side panel when the extension's button is clicked and log errors
if( chrome.sidePanel )
    chrome.sidePanel.setPanelBehavior( { openPanelOnActionClick: true } ).catch( err => console.error( err ) )
else {
    browser.action.onClicked.addListener( async ( tab, info ) => {
        await browser.sidebarAction.open()
    } )
}

// Create the "Open AgTern DevTools" right-click menu action
chrome.runtime.onInstalled.addListener( () => {
    chrome.contextMenus.create( {
        id: "openSidePanel",
        title: "Open AgTern DevTools",
        contexts: [ "all" ]
    } )
} )

// Open the side panel when the "Open AgTern DevTools" right-click menu action is clicked
chrome.contextMenus.onClicked.addListener( ( info, tab ) => {
    if( info.menuItemId === "openSidePanel" )
        chrome.sidePanel.open( {
            windowId: tab.windowId,
            tabId: tab.id
        } )
} )

function is_chrome()
{
    // "browser" is not available in Chrome, but it is an alias for "chrome" in Firefox
    return typeof chrome !== typeof browser
}

// Execute a function in the context of the current tab and return the result
async function execute_on_page( func, args )
{
    const [ tab ] = await chrome.tabs.query( { currentWindow: true, active: true } )
    const [ query ] = await chrome.scripting.executeScript( {
        target: { tabId: tab.id },
        func: func,
        args: args,
        world: is_chrome() ? "MAIN" : undefined
    } )
    return query.result
}

// Make sure that highlights disappear when the side panel is closed
chrome.runtime.onConnect.addListener( port => {
    if( port.name === "side_panel" )
        port.onDisconnect.addListener( async port => {
            await execute_on_page( () => unhighlight_all() )
        } )
} )
