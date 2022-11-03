<!-- This license only applies to THIS file. Link to awesome README template: https://github.com/othneildrew/Best-README-Template
MIT License

Copyright (c) 2021 Othneil Drew

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
-->

<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/johndpjr/AgTern">
    <img src="images/agtern-logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">AgTern</h3>

  <p align="center">
    Howdy! AgTern is a program that helps students find, track, and apply to internships by scraping the web for job postings.
    Based off a student profile (major, graduation date, industry interests, etc.), it retrieves scraped internships that are most relevant to the student.
    AgTern was built because searching for internships that match your interests and situation can be hard.
    We wanted the process to be as seamless as possible so that students can focus on applying and not searching.
    <br />
    <a href="https://github.com/johndpjr/AgTern"><strong>Explore the docs (TODO)»</strong></a>
    <br />
    <a href="https://github.com/johndpjr/AgTern/wiki"><strong>Read the wiki »</strong></a>
    <br />
    <br />
    <a href="https://github.com/johndpjr/AgTern">View Demo (TODO)</a>
    ·
    <a href="https://github.com/johndpjr/AgTern/issues">Report Bug</a>
    ·
    <a href="https://github.com/johndpjr/AgTern/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#current-features">Current Features</a></li>
        <li><a href="#images">Images</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#running">Running</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

### Current Features
* Scrapes and displays all Tesla internships
* Displays relevant information about found internships
  * Company
  * Title
  * Date of internship (e.g. Summer 2023)
  * Link to apply

### Images
[![AgTern in Action][product-screenshot]]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python]][Python-url]
* [![FastAPI][FastAPI]][FastAPI-url]
* [![SQLite][SQLite]][SQLite-url]
* [![Tkinter][Tkinter]][Tkinter-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To set up your project locally and get it running, follow these simple steps.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/johndpjr/AgTern.git
   ```
2. Create a virtual environment (in the `AgTern` directory) and activate it
   ```sh
   virtualenv venv

   # Linux & MacOS
   source venv/bin/activate
   # Windows
   .\venv\Scripts\activate
   ```
3. Install all Python packages
   ```sh
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Running

If you are using PyCharm, run configurations are already defined in the `.idea` folder.

If you are running the program for the first time, you should populate the database with internships by running command (2) below:

Common commands to run the program (make sure you're in the `AgTern` directory):
1. Starts a server and a scraping instance in a separate thread and enters the GUI:

`python3 -m agtern --dev`

2. Only scrape and save the internships to the database:

`python3 -m agtern --dev --scrape-only --save-internships`

3. Run the GUI without scraping

`python3 -m agtern --dev --no-scrape`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
[//]: # (## Usage)

[//]: # (TODO: Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.)

[//]: # (_ TODO: For more examples, please refer to the [Documentation]&#40;https://example.com&#41;_)

[//]: # (<p align="right">&#40;<a href="#readme-top">back to top</a>&#41;</p>)



<!-- ROADMAP -->
## Roadmap

- [x] Minimum Viable Product (MVP)
  - [x] Store student profile in configuration file
  - [x] Create a minimal Graphical User Interface (GUI)
  - [x] Scrape one company for internships and store in `.csv` file
- [x] Improve the GUI look
- [x] Move to client-server architecture
  - [x] Develop an API server and API class
  - [x] Store internships into a database
  - [x] Integrate changes with GUI and scraping algorithm
- [ ] Scrape multiple companies
  - [x] Develop extendable algorithm for scraping
  - [ ] Apply algorithm to multiple companies
- [ ] Categorize internships and map them to major(s)
- [ ] Extend the API
    - [ ] Filter internships that are relevant to the student (i.e. matches their profile)
- [ ] Scape and extract more from internships
  - [ ] Qualifications
  - [ ] Duties
  - [ ] Deadline for applications
- [ ] Secure the program
  - [ ] Communicate over HTTPS
  - [ ] Enable authenticated API requests
  - [ ] Store sensitive keys securely (don't have sensitive keys yet)
- [ ] Move the server to AWS EC2 instance
- [ ] Enable students to interact with internships (instead of passively viewing them)
  - [ ] Save internships
  - [ ] Track internship status
  - [ ] Autofill application information
- [ ] Migrate GUI framework `tkinter` to Web Framework Angular
  - [ ] Retire the native GUI
  - [ ] Wireframe and make mockups for website
  - [ ] Develop Angular application and deploy (backend already built)

See the [open issues](https://github.com/johndpjr/AgTern/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions give life to the project: without them this project dies.

Our list of tasks can be found on our GitHub [projects page](https://github.com/users/johndpjr/projects/2/views/1).
Feel free to add issues to the project: these can be bugs, feature requests, or just observations.
If you are interested in a ticket (that is not assigned already), assign it to yourself, make your changes, and
create a pull request completing the task.

1. Assign the task to yourself and set the status as "In Progress"
2. Create your Feature Branch (`git checkout -b feature/ticket#/short-description`)
3. Commit your Changes (`git commit -m 'Add some feature`)
4. Push to the Branch (`git push origin feature/ticket#/short-description`)
5. Open a [Pull Request](https://github.com/johndpjr/AgTern/pulls)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Project Manager - John Powell - johndpowell02@gmail.com

Project Link: [https://github.com/johndpjr/AgTern](https://github.com/johndpjr/AgTern)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* All contributors: No matter the amount, each contributor on our team is appreciated for the work they do. Thank you!
* Aggie Coding Club: Continues to provide resources, contributors, and project advice. Thank you ACC!

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/johndpjr/AgTern.svg?style=for-the-badge
[contributors-url]: https://github.com/johndpjr/AgTern/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/johndpjr/AgTern.svg?style=for-the-badge
[forks-url]: https://github.com/johndpjr/AgTern/network/members
[stars-shield]: https://img.shields.io/github/stars/johndpjr/AgTern.svg?style=for-the-badge
[stars-url]: https://github.com/johndpjr/AgTern/stargazers
[issues-shield]: https://img.shields.io/github/issues/johndpjr/AgTern.svg?style=for-the-badge
[issues-url]: https://github.com/johndpjr/AgTern/issues

[product-screenshot]: images/agtern-gui.png
[Python]: https://img.shields.io/badge/python-306998?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[FastAPI]: https://img.shields.io/badge/fastapi-009485?style=for-the-badge&logo=fastapi&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com/
[SQLite]: https://img.shields.io/badge/sqlite-44a2d4?style=for-the-badge&logo=sqlite&logoColor=white
[SQLite-url]: https://www.sqlite.org/index.html
[Tkinter]: https://img.shields.io/badge/tkinter-ffffcc?style=for-the-badge
[Tkinter-url]: https://docs.python.org/3/library/tkinter.html

[//]: # ([Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white)
[//]: # ([Angular-url]: https://angular.io/)
