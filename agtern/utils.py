import tkinter

import selenium.webdriver.support.expected_conditions as condition
from selenium.webdriver.common.by import By
import tkinter as tk
url = 'google.com/images'
extensions = ['.com', '.net', '.org', '.eu', '.info', '.uk', '.gov']
domainServer = ''

def getfavicon(usedUrl):
    for i in range(len(extensions)):
        stringSplit = (usedUrl.find(extensions[i])) + (len(extensions[i]))
        domainServer = usedUrl[:stringSplit]
        if (domainServer != url):
            break
    domainServer += "/favicon.ico"
    image = tk.PhotoImage(file=domainServer)
    return(image)

