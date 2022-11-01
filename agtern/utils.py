import tkinter
import selenium.webdriver.support.expected_conditions as condition
from selenium.webdriver.common.by import By
import tkinter as tk
from urllib.request import urlopen
url = str(input("Enter the url here:"))
def getfavicon(usedUrl):
    extensions = ['.com', '.net', '.org', '.eu', '.info', '.uk', '.gov']
    domainServer = ''
    image_links = []
    split_image = []
#Find the Domain Server via the Given Link
    for i in range(len(extensions)):
        stringSplit = (usedUrl.find(extensions[i])) + (len(extensions[i]))
        domainServer = usedUrl[:stringSplit]
        if (domainServer != url):
            break
#Read the HTML Data from the domain server
    page = urlopen(domainServer)
    html_raw_data = str(page.read())
#Find all instances of rel="icon" (rel="icon" is not included in the list element)
    rel_icons = (html_raw_data.split('<link rel="icon"'))
#Sort data based on the two most common ways of storing the file
    for i in range(len(rel_icons)):
        temp = rel_icons[i]
        temp_parts = temp.split('href="')
        for i in range(len(temp_parts)):
            if ((temp.find(".png") > temp.find(".ico"))):
                image_links.append(temp[7:temp.find(".png") + 4])
                break
            if (temp.find(".png") < temp.find(".ico")):
                image_links.append(temp[7:temp.find(".ico") + 4])
                break
#Break the current data segments into segments using the likeliest data tags
    for i in range(len(image_links)):
        temporary = str(image_links)
        split_image += temporary.split('content="')
    for i in range(len(split_image)):
        temp = str(split_image[i])
        split_temp = temp.split('href="')
#Look for an open-ended file directory, then append it to the domain server.
        for i in range(len(split_temp)):
            if temp[0] == '/':
                image_source_files.append(domainServer + temp[:temp.find('.png')+4])
    image_links += image_source_files
    return(image_links[-1])



#To-Do:
#Notify the Discord of the lengthy runtime, ask if it would be used to save the image links/files on the server.
print(getfavicon(url))