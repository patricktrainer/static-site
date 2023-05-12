# JavaScript, Jinja & Flask - Crawford Collins - Medium

Created: Feb 17, 2020 10:14 PM
URL: https://medium.com/@crawftv/javascript-jinja-flask-b0ebfdb406b3

![1*2QTOeryqlhZSGCU5SyvE0g.jpeg](JavaScript,%20Jinja%20&%20Flask%20-%20Crawford%20Collins%20-%20Med%20d567cdda2ab84700b96ab93ae89fae04/12QTOeryqlhZSGCU5SyvE0g.jpeg)

This article is guide for getting data from your python program to JavaScript inside of a Jinja HTML template . The solution is relatively simple, but until now there was not a good article explaining how to do it.

Example chart showing Python’s sentiment on hacker news over time.

## Step 1: Make sure to use the right Flask JSON module.

The flask library has two libraries for making JSON objects. If you have used Flask as a back-end, you might have used `jsonify.` However this does not work quite right for our goal. Technically this code uses the standard library JSON module, but it still needs to be imported through flask. Turn the data you need on the front-end into a JSON object with `json.dumps()`.

All the highlights from the file are included below.

## Step 2: Put JavaScript in your Jinja Template.

Get the template ready for the JavaScript code by adding a special JavaScript block content and adding script tags. **Make sure to add the closings for each.** Outside of the JS block, create the element to contain the chart. The canvas element is specifically for graphics, so that’s what I used. It is important to note that width and height values in the canvas are ratios. Load the objects like you would with a normal Jinja template i.e. {{object}} , but add `| tojson` . To make everything run smoothly, you need to pass the object to the `JSON.parse()` function. This example repo uses code from the [charts.js library](https://www.chartjs.org/docs/latest/).

[Untitled](JavaScript,%20Jinja%20&%20Flask%20-%20Crawford%20Collins%20-%20Med%20d567cdda2ab84700b96ab93ae89fae04/Untitled%20Database%2081493e718fa74c69b36c896b9be0d471.csv)

## Step 3: Admire your work

Being able to incorporate a little JavaScript into your Flask app makes it look 10 times better. By using only a few lines of JS, we created a responsive, interactive, and animated chart.