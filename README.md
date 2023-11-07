# final_project

## Video Demo: https://www.youtube.com/watch?v=_MhNXFVTSsI

## Description:

This final project is a website using Flask, Python, SQL and Javascript / HTML to offer a user experience centered on the discovery of labyrinths.

The core of the site is a python program core_maze.py, which generates a PNG maze according to defined parameters. These parameters are sent to the website on a given page, Maze. Parameters can be modified on the fly.
The generated labyrinth can be saved to the user's personal user account (password login required), then re-displayed from the list of labyrinths.
Finally, the user has an example of a SCRATCH game of one of these labyrinths used as support to help a knight find the way out and the treasure:

## core_maze.py

This file contains all the maze creation. A "Grid" class object is made up of "Cells" class objects. These Cells are initially all closed, and related to each other. Three algorithms are used to generate openings in the Cells, which will lead to the "knocking down of walls" and thus to the creation of the labyrinth.
The PIL module is used to generate PNG images, with precise resolution.
The most complicated part was to find the method for applying the three algorithms and translating it into code. The result is actually very simple once written, but identifying the code logic from the literal description of the algorithm (on the web) was complex. 

## Flask app.py

### Account management

Much of this code is inspired by the CS50 "Finance" project. Account creation via the "register" function, login and logout management. Flash() messages have been added to enhance the experience. Site web pages are @login_required.
A SQL table is dedicated to user management.

### "Maze" Page

On this page, the labyrinth is generated on the fly. Parameters (number of columns, number of rows and type of algorithm used) are requested via sliders and radio buttons in a dedicated div.
The maze is dynamically generated according to these values.
Enabling dynamic generation of the labyrinth was no easy task. I had to learn AJAX requests and make Javascript code, directly included in maze.html.
A javascript function (sliderOrRadioChanged()) sends a given value to generate the image as soon as the sliders are modified.
Below the generated maze is a "save maze" button. This button takes the values modified by the javascript function and exports them to a SQL table dedicated to saving mazes.
Displaying the image and treating it as a value required some coding. The choice was made to encode it in base64 text. This made it possible to manipulate and export the maze's img_data.
Everything is done with POST requests, but a GET request is possible and gives default values, unmodified by the javascript function.

### "Library" Page

This page displays the list of mazes saved by the user. The SQL query is simple, and displaying it as a table required some jinja code.
An "open" button opens a page (with a POST request) to display the maze in question.

### "Game" Page

this page displays the Scratch game "Maze For Adventurers", which is none other than my CS50 Week 0 project. I wanted to pay tribute to it to bring things full circle.
The mazes used in the game were generated by the earlier version of the python code core_maze.py.
The game is playable in its entirety, and allows a knight to move through a labyrinth, dodging minotaurs to reach the treasure in the final level!
