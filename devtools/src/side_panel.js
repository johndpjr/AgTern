
// This is the script file for the side panel activated by pressing the extension's button.
// It has access to all the Chrome extension APIs.
// https://developer.chrome.com/docs/extensions/reference/sidePanel/

// Open a port to the service worker so that it knows when the side panel is closed
const service_worker = await chrome.runtime.connect( { name: "side_panel" } )

// Locate the input and output elements
const e = id => document.getElementById( id )
const xpath = e( "xpath" )
const linkify = e( "linkify" )
const regex = e( "regex" )
const ignore_case = e( "ignore-case" )
const multiline = e( "multiline" )
const dot_all = e( "dot-all" )
const format = e( "format" )
const num_results = e( "num-results" )
const result = e( "result" )

// Keep track of changes so that updates are only made when needed
let current_tab_id = chrome.tabs.TAB_ID_NONE
let previous_tab_id = chrome.tabs.TAB_ID_NONE
let previous_result = []
let previous_linkify = linkify.checked
let previous_sanity_check = true

function is_chrome()
{
    // "browser" is not available in Chrome, but it is an alias for "chrome" in Firefox
    return typeof chrome !== typeof browser
}

async function current_tab()
{
    const [ tab ] = await chrome.tabs.query( { currentWindow: true, active: true } )
    return tab
}

// Execute a function in the context of the previous tab and return the result
async function execute_on_previous_tab( func, args )
{
    if( previous_tab_id === chrome.tabs.TAB_ID_NONE || previous_tab_id === current_tab_id )
        return
    try {
        const [ query ] = await chrome.scripting.executeScript( {
            target: { tabId: previous_tab_id },
            func: func,
            args: args,
            world: is_chrome() ? "MAIN" : undefined
        } )
        if( query === undefined )
            return
        return query.result
    } catch {}
}

// Execute a function in the context of the current tab and return the result
async function execute_on_page( func, args )
{
    try {
        current_tab_id = ( await current_tab() ).id
    } catch {
        return
    }
    if( current_tab_id === chrome.tabs.TAB_ID_NONE )
        return
    const [ query ] = await chrome.scripting.executeScript( {
        target: { tabId: current_tab_id },
        func: func,
        args: args,
        world: is_chrome() ? "MAIN" : undefined
    } )
    previous_tab_id = current_tab_id
    if( query === undefined )
        return
    return query.result
}

async function sanity_check()
{
    try {
        return await execute_on_page( () => {
            try {
                return __agtern_devtools_ok__
            } catch {
                return false
            }
        }, [] )
    } catch {
        return false
    }
}

// Retrieve the result of scrape() or scrape_links(), filter with regex,
// substitute into the format string, and return the result
async function scrape( xpath )
{
    const scrape_result = await execute_on_page(
        linkify.checked ? ( x => scrape_links( x ) ) : ( x => scrape( x ) ),
        [ xpath ]
    )
    if( scrape_result === undefined || scrape_result === null )
        return
    let flags = ""
    if( ignore_case.checked )
        flags += "i"
    if( multiline.checked )
        flags += "m"
    if( dot_all.checked )
        flags += "s"
    const re = new RegExp( regex.value.length > 0 ? regex.value : ".*", flags )
    return scrape_result.map( text => {
        try {
            const groups = text.trim().match( re )
            return format.value.replaceAll( /\{(\d+)}/g, ( _, id ) => groups[id] )
        } catch {
            return text // TODO: Allow a default
        }
    } )
}

async function unhighlight_all()
{
    return await execute_on_page( x => unhighlight_all() )
}

function arrays_equal( a, b )
{
    if( a === undefined || b === undefined || a === null || b === null || a.length !== b.length )
        return false
    for( let i = 0; i < a.length; i++ )
        if( a[i] !== b[i] )
            return false
    return true
}

// Update the results list and highlighting on the page if needed
async function update_results()
{
    if( !( await sanity_check() ) )
    {
        if( previous_sanity_check )
        {
            num_results.innerText = "AgTern DevTools Unavailable"
            let message = document.createElement( "p" )
            message.innerText = "Try refreshing the page. You may also need to grant the extension access to this page."
            result.replaceChildren( message )
        }
        previous_sanity_check = false
        return
    }
    await execute_on_previous_tab( x => unhighlight_all() )
    const scrape_result = await scrape( xpath.value.replaceAll( "\n", "" ) )
    if( scrape_result === undefined || previous_sanity_check && arrays_equal( scrape_result, previous_result ) && linkify.checked === previous_linkify )
        return
    previous_result = scrape_result
    previous_linkify = linkify.checked
    previous_sanity_check = true
    num_results.innerText = scrape_result.length + " results"
    let result_elements = []
    for( let node of scrape_result )
    {
        let element = document.createElement( "div" )
        element.classList.add( "card", "result-item" )
        if( linkify.checked )
        {
            let link = document.createElement( "a" )
            link.innerText = node
            link.href = node
            const url = node
            if( is_chrome() )
                link.addEventListener( "click", async e => {
                    await chrome.tabs.create( {
                        url: url,
                        openerTabId: current_tab_id
                    } )
                } )
            element.appendChild( link )
        } else
            element.innerText = node
        result_elements.push( element )
    }
    result.replaceChildren( ...result_elements )
}

for( let e of document.getElementsByTagName( "input" ) )
    e.addEventListener( "input", update_results )

await chrome.tabs.onCreated.addListener( update_results )
await chrome.tabs.onActivated.addListener( update_results )
await chrome.tabs.onUpdated.addListener( update_results )
await chrome.tabs.onReplaced.addListener( update_results )
await chrome.tabs.onRemoved.addListener( update_results )
await update_results()
setInterval( update_results, 250 )
