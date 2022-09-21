# AgTern

Helps students find relevant internships web based off of their interests/situation (i.e. major, graduation date, industry interests, companies, etc.)

## Description

AgTern is a program that helps students find internships. It scrapes the web for internships that are relevant to the student (i.e. major, graduation date, industry interests, companies, etc.) and displays them in a helpful and convenient manner. Through AgTern, internships can be saved, removed, disliked, and much more!

AgTern was built because searching for internships that match can be hard. We wanted the process to be as seamless as possible so that students can focus on applying and not searching.

## Features

* Finds internships (via web-scraping) that are relevant to the student
* Displays relevant information about found internships
	* Title
	* Date range of internship (e.g. May 2023 - July 2023)
	* Description
	* Qualifications
	* Duties
	* Link to apply
	* Deadline for applications
* Interact with internships found
	* Save
	* View
	* Track status

## Python Packages Used

* Frontend: Desktop-native GUI application
	* Built with tkinter (GUI framework that binds with tcl/tk in Python)
* Backend Modules
	* requests (for downloading web pages using HTTP protocol)
	* BeautifulSoup w/ lxml (for parsing content from static web pages)
	* Selenium (for interacting with web sites that are not static (JavaScript necessary to interact))