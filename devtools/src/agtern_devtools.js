
// This is a content script that is injected into every webpage when the extension is enabled.
// It shares variables with the webpage, so naming conflicts may occur with the functions below.
// This file only has access to a small subset of the Chrome APIs to avoid potential security vulnerabilities.
// All the functions below can be accessed in the Chrome console (ex: scrape_links("//a/@href")).
// https://developer.chrome.com/docs/extensions/mv3/content_scripts/

function highlight( e )
{
    return e.classList.add( "agtern-devtools-selected" )
}

function unhighlight( e )
{
    e.classList.remove( "agtern-devtools-selected" )
}

function highlight_all( arr )
{
    arr.forEach( highlight )
}

function unhighlight_all()
{
    document
        .querySelectorAll( ".agtern-devtools-selected" )
        .forEach( unhighlight )
}

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

function scrape( xpath )
{
    return scrape_text( xpath )
}

function linkify( link )
{
    return new URL( link, window.location.href ).href
}

function scrape_links( xpath )
{
    return scrape( xpath ).map( linkify )
}

console.log( "AgTern DevTools loaded!" )
