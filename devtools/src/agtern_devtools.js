
// This is a content script that is injected into every webpage when the extension is enabled.
// It shares variables with the webpage, so naming conflicts may occur with the functions below.
// This file only has access to a small subset of the Chrome APIs to avoid potential security vulnerabilities.
// All the functions below can be accessed in the Chrome console (ex: scrape_links("//a/@href")).
// https://developer.chrome.com/docs/extensions/mv3/content_scripts/

let __agtern_devtools_invalid_functions__ = [] // Hopefully no naming conflict

if( typeof highlight === "undefined" )
    function highlight( e )
    {
        if( !e.classList.contains( "agtern-devtools-selected" ) )
        {
            e.classList.add( "agtern-devtools-selected" )
            return true
        } else
            return false
    }
else
    __agtern_devtools_invalid_functions__.push( "highlight" )

if( typeof unhighlight === "undefined" )
    function unhighlight( e )
    {
        if( e.classList.contains( "agtern-devtools-selected" ) )
        {
            e.classList.remove( "agtern-devtools-selected" )
            return true
        } else
            return false
    }
else
    __agtern_devtools_invalid_functions__.push( "unhighlight" )

if( typeof highlight_all === "undefined" )
    function highlight_all( arr )
    {
        arr.forEach( highlight )
    }
else
    __agtern_devtools_invalid_functions__.push( "highlight_all" )


if( typeof unhighlight_all === "undefined" )
    function unhighlight_all()
    {
        document
            .querySelectorAll( ".agtern-devtools-selected" )
            .forEach( unhighlight )
    }
else
    __agtern_devtools_invalid_functions__.push( "unhighlight_all" )

if( typeof scrape_elements === "undefined" )
    function scrape_elements( xpath )
    {
        unhighlight_all()
        try
        {
            const snapshot = document.evaluate(
                xpath,
                document,
                null,
                XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
                null
            )
            return [ ...Array( snapshot.snapshotLength ) ].map( ( _, i ) => {
                const node = snapshot.snapshotItem( i )
                if( node.nodeType === Node.ATTRIBUTE_NODE )
                {
                    highlight( node.ownerElement )
                    return node.ownerElement
                } else {
                    highlight( node )
                    return node
                }
            } )
        } catch {
            return []
        }
    }
else
    __agtern_devtools_invalid_functions__.push( "scrape_elements" )

if( typeof scrape_text === "undefined" )
    function scrape_text( xpath )
    {
        unhighlight_all()
        try
        {
            const snapshot = document.evaluate(
                xpath,
                document,
                null,
                XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
                null
            )
            return [ ...Array( snapshot.snapshotLength ) ].map( ( _, i ) => {
                const node = snapshot.snapshotItem( i )
                if( node.nodeType === Node.ATTRIBUTE_NODE )
                {
                    highlight( node.ownerElement )
                    return node.value
                } else {
                    highlight( node )
                    return node.textContent
                }
            } )
        } catch {
            return []
        }
    }
else
    __agtern_devtools_invalid_functions__.push( "scrape_text" )

if( typeof scrape === "undefined" )
    function scrape( xpath )
    {
        return scrape_text( xpath )
    }
else
    __agtern_devtools_invalid_functions__.push( "scrape" )

if( typeof linkify === "undefined" )
    function linkify( link )
    {
        return new URL( link, window.location.href ).href
    }
else
    __agtern_devtools_invalid_functions__.push( "linkify" )

if( typeof scrape_links === "undefined" )
    function scrape_links( xpath )
    {
        return scrape( xpath ).map( linkify )
    }
else
    __agtern_devtools_invalid_functions__.push( "scrape_links" )

const __agtern_devtools_ok__ = __agtern_devtools_invalid_functions__.length === 0
if( __agtern_devtools_ok__ )
    console.log( "AgTern DevTools loaded!" )
else
    console.error( "[AgTern DevTools] The following functions were not loaded due to naming conflicts with this page: "
        + __agtern_devtools_invalid_functions__.join( ", " ) )
