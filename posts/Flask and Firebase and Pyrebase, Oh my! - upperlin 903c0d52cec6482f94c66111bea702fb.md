# Flask and Firebase and Pyrebase, Oh my! - upperlinecode

Created: Mar 25, 2020 6:56 PM
URL: https://blog.upperlinecode.com/flask-and-firebase-and-pyrebase-oh-my-f30548d68ea9

![0*56yGK5rxndWlLYDF.jpg](Flask%20and%20Firebase%20and%20Pyrebase,%20Oh%20my!%20-%20upperlin%20903c0d52cec6482f94c66111bea702fb/056yGK5rxndWlLYDF.jpg)

I’ve been scouring the web for good resources on connecting a Flask application to Firebase, and I’m telling you, it’s slim pickings. In this post (or series of posts, if this gets too long), I’m going to show you how to build out a fully functioning CRUD application using Firebase. You could do this much more easily using Django or a more robust framework, but what’s the fun in that? I love the fact that Flask is such a lightweight framework and that it’s so open and flexible.

The project we’re going to be building out is a **community event event board**- a place where users (who are logged in) can post events for their neighbors. Think of it as the digital version one of those coffee shop bulletin boards where folks can see what is happening in their neighborhood.

Note: We’re assuming some knowledge of Flask already since we’re not starting from scratch. You should be able to create a basic app using routes, jinja2 templates, forms, and static files.

## Initial setup

We’re going to start by downloading and opening a template that will get us going without too much setup. Feel free to skip this if you don’t want to follow along.

Once you’ve done this, open the project in your text editor, and then run the following commands in the terminal to install the flask and python-dotenv (for our environment variables) packages:

## Run the application

Run the app by typing the following command in to your terminal:

```
flask run
```

This will fire up the local server, and get your app running at the default port 8080. Open it up in a browser by navigating to [http://localhost:8080/](http://localhost:8080/)

## Examine the existing codebase

Take a look at what currently exists. We’ll start at our controller: the `routes.py` file. In this file we see:

- Importing packages that we currently need.
- A global variable `events` that is holding an array of dictionaries with each event's information. We'll eventually replace this with a Firebase database.
- Our routes and the functions that are called when those routes are triggered by a url.
- When ‘/’ or ‘/index’ are triggered, the index() function is run and the `index.html` template is rendered. We pass in the `events` variable to be templated in using jinja2.

When ‘/events/new’ is triggered, the new_event.html page is rendered, with a form that posts event data back to the controller. In the controller, the form data is unpacked from the request and appended to the `events`variable. After this is done we redirect back to the '/' route.

Take some time to follow the flow of the code here.

## Database Setup

In order to replace our array of dictionaries with a real database, we need to do some basic setup on Firebase. Head to [firebase.google.com](https://gist.github.com/dfenjves/www.firebase.google.com), sign up, and then create a new project.

Go through the popup and give your project a (relevant) name:

Congratulations! You’ve initialized your first Firebase project! You’re not quite there yet though.

Once you see your dashboard, head over to the database section and click on “create database”.

You’ll want to start your database up in “test mode” so that you don’t need user authentication quite yet.

Once the database is created, make sure you switch the dropdown from “cloud firestore” to “realtime database”:

## Installing Pyrebase

We’re going to use a Python wrapper for the Firebase API called [Pyrebase](https://github.com/thisbejim/Pyrebase). Let’s add it to our project by running:

In our routes.py file, add `import pyrebase` to the import section at the top of the page.

## Connecting to your Firebase DB

To connect to your firebase database, you’ll need to set up a dictionary variable with your configuration data in your `routes.py` file. The `authDomain`, `databaseURL`, `projectId`, and `storageBucket` should all use the name you gave your firebase project during setup.

** Important: Do not expose your API Key or the JSON file with your private key! Put your API key in an environment variable in your `.env` file - and make sure not to upload that file to github (it is ignored by default in this repository)! **

This is what your .env file (in the root directory of your project) should look like:

You’ll also want to go to your settings -> Service Accounts and then generate a new private key. That will download a JSON file that you can connect to your config variables. In the example below, we renamed the JSON file `firebase-private-key.json` and we also added that file to the `.gitignore` so that it doesn't get tracked by git and uploaded to github.

Back to the routes.py file — once you’ve set up your config variable correctly, add the following code underneath:

This code connects to our project using our configuration data, and then creates a `db` variable to interact with the Firebase database that we created earlier.

You’ve hooked up your local application to your Firebase database using Pyrebase. Now it’s time to start using the `db`variable you created earlier to get and send data to the database.

## Sending data to Firebase

Let’s go back and take a look at what happens when the “New Event” form is posted to our controller.

We currently append the `new_event` variable (that comes from the form) to the `events` list that we created earlier on. Unfortunately that events list will not persist (save) our data, so we're going to replace this with a call to our firebase `db`variable:

To test if this worked (you won’t see anything change on the index page since we haven’t updated it yet), head to the Firebase Console and open up your project, clicking on the ‘database’ section. You should see that the event you submitted is now a “node” in your database, under the node “events” (which was created as well since this was your first upload to that node — future submissions to `db.child("events")` will just add on to that node).

Try submitting a few more events to see what this looks like in the Firebase console.

## Retrieving data from Firebase

Now let’s turn to pulling in our Firebase content, rather than sending new information to the database. We are currently doing this in the routing for our `/index` page by accessing the `events` list and sending it through to the template for rendering:

Go ahead and delete the events variable defined at the top of the page — you’re not going to need that anymore since you’re moving to Firebase. Next, inside of our `index()` method we'll create a new variabe called `db_events` that pulls in the data we want from Firebase (the "events" node), and we'll pass that in to our template for rendering:

Now reload your app and you should hopefully see data getting pulled in from your Firebase database!

You’re not going to get good at Flask and Firebase unless you get a lot of practice. Here are a few things you can try doing to solidify this knowledge:

- Add a ‘locations’ form on a new page where users can upload different locations events might take place. Save these to a new node in your firebase db.
- Add another field to your events form and then make sure that that content gets rendered correctly on your index page
- Build a similar app to inventory anything else you’re interested in: animals, groceries, todo items, etc.To test if this worked (you won’t see anything change on the index page since we haven’t updated it yet), head to the Firebase Console and open up your project, clicking on the ‘database’ section. You should see that the event you submitted is now a “node” in your database, under the node “events” (which was created as well since this was your first upload to that node — future submissions to `db.child("events")` will just add on to that node).

Try submitting a few more events to see what this looks like in the Firebase console.