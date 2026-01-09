# Project Overview

This project is a single-page web application that serves as a dashboard to monitor and compare credit card transaction fees from popular financial entities in Argentina. The primary goal is to provide a unified view of official links, API documentation, and cost structures for payment processing.

The application is built with plain HTML, and styled with **Tailwind CSS**. It uses **Chart.js** for data visualization. All the data is currently hardcoded within the `index.html` file.

The `research_spanish.md` file contains the detailed research and analysis of the Argentinian payment processing market, which is the source of the data presented on the web page.

# Building and Running

This is a static web project. There is no build process. To run the project, you can open the `index.html` file directly in a web browser.

# Development Conventions

The project uses vanilla JavaScript for interactivity. The data is stored in a JavaScript array of objects in a `<script>` tag within the `index.html` file. Any changes to the data should be made directly in this array.

The styling is done using Tailwind CSS, loaded from a CDN. The application structure and styling choices are documented as comments within the `<head>` section of the `index.html` file.
