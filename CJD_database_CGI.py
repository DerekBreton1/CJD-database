#!/usr/bin/env python3

import cgi
import cgitb
import pymysql
from string import Template

#Enable CGI traceback
cgitb.enable()

#Create html home page
#leave space for the style, title, intro, form, summary, table, error message
html_home_page = Template(
"""
<html>    
    <head>
        <title>CJD Database</title>
        <link rel="icon" href="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Boston_University_seal.svg/280px-Boston_University_seal.svg.png" type="image/x-icon">
    
        ${style}

        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/chosen/1.8.7/chosen.min.css">
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/chosen/1.8.7/chosen.jquery.min.js"></script>
    </head>

    <body>
        <!--Create header for all pages in the website-->
        <div class="page-header">
            <div class="page-header-logo">
                <img src="https://www.bu.edu/brand/files/2019/06/master_logo.gif">
            </div>
            <div class="page-header-text">
                <h1>CJD Database</h1>
            </div>
            <!-- The following drop down menu uses AJAX to display -->
            <div class="menu-dropdown">
                <a style="text-decoration: none; margin-right: 25px; color: gray;" href="#" onclick="display_home()">HOME</a>
                <a style="text-decoration: none; margin-right: 25px; color: gray;" href="#" onclick="load_content('https://bioed.bu.edu/students_24/Team_12/about.html')">ABOUT</a>
                <a style="text-decoration: none; margin-right: 25px; color: gray;" href="#" onclick="load_content('https://bioed.bu.edu/students_24/Team_12/upload.html')">UPLOAD</a>
                <a style="text-decoration: none; color: gray;" href="#" onclick="load_content('https://bioed.bu.edu/students_24/Team_12/help.html')">HELP</a>
            </div>
        </div>
        
        <!--Display AJAXed page content-->
        <div id="page-content"></div>

        <!--Home page body content-->
        <div class="search" id="home-content">
            <div class="search-description">
                <h2>Fill out search parameters</h2>
            </div>
            <div class="search-form">${html_form}</div>
        </div>

        <script>
            //Function to display home page when the home tab is clicked
            function display_home() {
		document.getElementById('home-content').classList.remove('hidden');
                document.getElementById('page-content').classList.add('hidden');
            }

            // AJAX function to dynamically load the home, about, upload, and help pages
            function load_content(page) {
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        document.getElementById('page-content').classList.remove('hidden');
                        document.getElementById('page-content').innerHTML = this.responseText;

                        // Hide undesired page content when other pages are loaded
                        if (page == 'https://bioed.bu.edu/students_24/Team_12/about.html') {
                            document.getElementById('home-content').classList.add('hidden');
                            document.getElementById('about-content').classList.remove('hidden');
                            document.getElementById('upload-content').classList.add('hidden');
                            document.getElementById('help-content').classList.add('hidden');
                        }
                        if (page == 'https://bioed.bu.edu/students_24/Team_12/upload.html') {
                            document.getElementById('home-content').classList.add('hidden');
                            document.getElementById('about-content').classList.add('hidden');
                            document.getElementById('upload-content').classList.remove('hidden');
                            document.getElementById('help-content').classList.add('hidden');
                        
                        }
                        if (page == 'https://bioed.bu.edu/students_24/Team_12/help.html') {
                            document.getElementById('home-content').classList.add('hidden');
                            document.getElementById('about-content').classList.add('hidden');
                            document.getElementById('upload-content').classList.add('hidden');
                            document.getElementById('help-content').classList.remove('hidden');
                        }
                    }
                };
                xhttp.open('GET', page, true);
                xhttp.send();
            }

            $(document).ready(function() {
                $('#columns-returned').chosen({
                    width:"300px"
                })
            })
        </script>
    </body>
</html>
"""
)

style = """
        <style>
            .hidden {
                display: none;
            }
            .page-header {
                display: flex;
                align-items: center;
                background-color: white;
                padding: 10px 20px;
                box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
                font-family: Arial, Helvetica, sans-serif;
            }
            .page-header-logo {
                margin: 5px;
            }
            .page-header-text {
                margin: 0;
                color: gray;
                font-size: 20px;
                margin-left: 10px;
            }
            .menu-dropdown {
                margin-left: auto;
                margin-right: 30px;
                color: gray;
                font-size: 20px;
            }
            .search {
                font-family: Arial, Helvetica, sans-serif;
                font-size: 20px;
                padding: 10px;
                margin: 10px;
                background-color: lightgray;
            }
            .search-description {
                text-align: center;
            }
            .column-selector {
                display: flexbox;
		margin: 30px;
		text-align: center;
            }
	    .column-selector h3 {
		font-size: 25px;
		text-align: center;
		margin-top: 50px;
	    }
            .chosen-container-multi .chosen-choices{
                min-height: 30px;
            }
            .about-content {
                font-family: Arial, Helvetica, sans-serif;
                font-size: 20px;
            }
            .about-header {
                margin: 20px;
                text-align: center;
                color: gray;
            }
            .about-body {
                text-align: left;
                color: black;
		margin: 75px;
            }
            .upload-content {
                font-family: Arial, Helvetica, sans-serif;
                font-size: 20px;
            }
            .upload-header {
                margin: 20px;
                text-align: center;
                color: gray;
            }
            .upload-body {
                text-align: center;
                color: gray;
            }
            .help-content {
                font-family: Arial, Helvetica, sans-serif;
            }
            .help-header {
                text-align: center;
                font-size: 20px;
                color: gray;
            }
        </style>
"""

html_form = """
<form>
    <div class="column-selector">
	<h3>Output:</h3>
        <label for="columns-returned">Desired output columns: </label>
        <select id="columns-returned" multiple>
            <option value="chomosome_num">CHROM</option>
            <option value="position">POS</option>
            <option value="ID">ID</option>
            <option value=""></option>
            <option value=""></option>
            <option value=""></option>
        </select>
        <label style="margin-left: 10px;">or select all columns: </label>
        <input type="checkbox" id="all-cols">
    </div>
</form>
"""

#Establish database connection
connection = pymysql.connect(host='bioed.bu.edu',
                             user='dbreton',
                             password='Branquinho',
                             db='Team_12',
                             port=4253)

#Create cursor object
cursor = connection.cursor()

#Retrieve data
form = cgi.FieldStorage()

#Substitute values
html_output = html_home_page.safe_substitute(style=style, html_form=html_form)

#next line is always required as first part of html output
print("Content-type: text/html\n")

print(html_output)
