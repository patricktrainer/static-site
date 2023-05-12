# Developing a Single Page App with Flask and Vue.js | TestDriven.io

Created: Dec 16, 2019 5:13 PM
Tags: How To
URL: https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/a

![Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/developing_spa_flask_vue.png](Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/developing_spa_flask_vue.png)

## Developing a Single Page App with Flask and Vue.js

The following is a step-by-step walkthrough of how to set up a basic CRUD app with Vue and Flask. We'll start by scaffolding a new Vue application with the Vue CLI and then move on to performing the basic CRUD operations through a back-end RESTful API powered by Python and Flask.

*Final app*:

![Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/final.gif](Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/final.gif)

Main dependencies:

- Vue v2.6.10
- Vue CLI v3.7.0
- Node v12.1.0
- npm v6.9.0
- Flask v1.0.2
- Python v3.7.3

## Objectives

By the end of this tutorial, you will be able to:

1. Explain what Flask is
2. Explain what Vue is and how it compares to other UI libraries and front-end frameworks like React and Angular
3. Scaffold a Vue project using the Vue CLI
4. Create and render Vue components in the browser
5. Create a Single Page Application (SPA) with Vue components
6. Connect a Vue application to a Flask back-end
7. Develop a RESTful API with Flask
8. Style Vue Components with Bootstrap
9. Use the Vue Router to create routes and render components

## What is Flask?

[Flask](http://flask.pocoo.org/) is a simple, yet powerful micro web framework for Python, perfect for building RESTful APIs. Like [Sinatra](http://sinatrarb.com/) (Ruby) and [Express](https://expressjs.com/) (Node), it's minimal and flexible, so you can start small and build up to a more complex app as needed.

First time with Flask? Check out the following two resources:

## What is Vue?

[Vue](https://vuejs.org/) is an open-source JavaScript framework used for building user interfaces. It adopted some of the best practices from React and Angular. That said, compared to React and Angular, it's much more approachable, so beginners can get up and running quickly. It's also just as powerful, so it provides all the features you'll need to create modern front-end applications.

For more on Vue, along with the pros and cons of using it vs. React and Angular, review the following articles:

First time with Vue? Take a moment to read through the [Introduction](https://vuejs.org/v2/guide/index.html) from the official Vue guide.

## Flask Setup

Begin by creating a new project directory:

Within "flask-vue-crud", create a new directory called "server". Then, create and activate a virtual environment inside the "server" directory:

> The above commands may differ depending on your environment.

Install Flask along with the [Flask-CORS](https://flask-cors.readthedocs.io/) extension:

Add an *app.py* file to the newly created "server" directory:

Why do we need Flask-CORS? In order to make cross-origin requests -- e.g., requests that originate from a different protocol, IP address, domain name, or port -- you need to enable [Cross Origin Resource Sharing](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing) (CORS). Flask-CORS handles this for us.

> It's worth noting that the above setup allows cross-origin requests on all routes, from any domain, protocol, or port. In a production environment, you should only allow cross-origin requests from the domain where the front-end application is hosted. Refer to the Flask-CORS documentation for more info on this.

Run the app:

To test, point your browser at [http://localhost:5000/ping](http://localhost:5000/ping). You should see:

Back in the terminal, press Ctrl+C to kill the server and then navigate back to the project root. With that, let's turn our attention to the front-end and get Vue set up.

## Vue Setup

We'll be using the powerful [Vue CLI](https://cli.vuejs.org/) to generate a customized project boilerplate.

Install it globally:

> First time with npm? Review the official About npm guide.

Then, within "flask-vue-crud", run the following command to initialize a new Vue project called `client`:

This will require you to answer a few questions about the project. Use the down arrow key to highlight "Manually select features", and then press enter. Next, you'll need to select the features you'd like to install. For this tutorial, select "Babel", "Router", and "Linter / Formatter" like so:

Use the history mode for the router. Select "ESLint + Airbnb config" for the linter and "Lint on save". Finally, select the "In package.json" option so that configuration is placed in the *package.json* file instead of in separate configuration files.

You should see something similar to:

Take a quick look at the generated project structure. It may seem like a lot, but we'll *only* be dealing with the files and folders in the "src" folder along with the *index.html* file found in the "public" folder.

The *index.html* file is the starting point of our Vue application.

Take note of the `<div>` element with an `id` of `app`. This is a placeholder that Vue will use to attach the generated HTML and CSS to produce the UI.

Turn your attention to the folders inside the "src" folder:

Breakdown:

[Untitled](Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/Untitled%20Database%20d26b4f84df54484390e9c439d0ebc7dd.csv)

Review the *client/src/components/HelloWorld.vue* file. This is a [Single File](https://vuejs.org/v2/guide/single-file-components.html) component, which is broken up into three different sections:

1. *template*: for component-specific HTML
2. *script*: where the component logic is implemented via JavaScript
3. *style*: for CSS styles

Fire up the development server:

Navigate to [http://localhost:8080](http://localhost:8080/) in the browser of your choice. You should see the following:

![Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/default-vue-app.png](Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/default-vue-app.png)

To simplify things, remove the "views" folder. Then, add a new component to the "client/src/components" folder called Ping.vue:

Update *client/src/router.js* to map '/ping' to the `Ping` component like so:

Finally, within *client/src/App.vue*, remove the navigation:

You should now see `Hello!` in the browser at [http://localhost:8080/ping](http://localhost:8080/ping).

To connect the client-side Vue app with the back-end Flask app, we can use the [axios](https://github.com/axios/axios) library to send AJAX requests.

Start by installing it:

Update the `script` section of the component, in *Ping.vue*, like so:

Fire up the Flask app in a new terminal window. You should see `pong!` in the browser. Essentially, when a response is returned from the back-end, we set `msg` to the value of `data` from the response object.

## Bootstrap Setup

Next, let's add Bootstrap, a popular CSS framework, to the app so we can quickly add some style.

Install:

> Ignore the warnings for jquery and popper.js. Do NOT add either to your project. More on this later.

Import the Bootstrap styles to *client/src/main.js*:

Update the `style` section in *client/src/App.vue*:

Ensure Bootstrap is wired up correctly by using a [Button](https://getbootstrap.com/docs/4.0/components/buttons/) and [Container](https://getbootstrap.com/docs/4.0/layout/overview/#containers) in the `Ping` component:

Run the dev server:

You should see:

![Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/bootstrap.png](Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/bootstrap.png)

Next, add a new component called `Books` in a new file called *Books.vue*:

Update the router:

Test:

1. [http://localhost:8080/ping](http://localhost:8080/ping)

Finally, let's add a quick, Bootstrap-styled table to the `Books` component:

You should now see:

![Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/books-component-1.png](Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/books-component-1.png)

Now we can start building out the functionality of our CRUD app.

## What are we building?

Our goal is to design a back-end RESTful API, powered by Python and Flask, for a single resource -- books. The API itself should follow RESTful design principles, using the basic HTTP verbs: GET, POST, PUT, and DELETE.

We'll also set up a front-end application with Vue that consumes the back-end API:

> This tutorial only deals with the happy path. Handling errors is a separate exercise. Check your understanding and add proper error handling on both the front and back-end.

## GET Route

### Server

Add a list of books to *server/app.py*:

Add the route handler:

Run the Flask app, if it's not already running, and then manually test out the route at [http://localhost:5000/books](http://localhost:5000/books).

> Looking for an extra challenge? Write an automated test for this. Review this resource for more info on testing a Flask app.

### Client

Update the component:

After the component is initialized, the `getBooks()` method is called via the [created](https://vuejs.org/v2/api/#created) lifecycle hook, which fetches the books from the back-end endpoint we just set up.

> Review Instance Lifecycle Hooks for more on the component lifecycle and the available methods.

In the template, we iterated through the list of books via the [v-for](https://vuejs.org/v2/guide/list.html) directive, creating a new table row on each iteration. The index value is used as the [key](https://vuejs.org/v2/guide/list.html#key). Finally, [v-if](https://vuejs.org/v2/guide/conditional.html#v-if) is then used to render either `Yes` or `No`, indicating whether the user has read the book or not.

![Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/books-component-2.png](Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/books-component-2.png)

## Bootstrap Vue

In the next section, we'll use a modal to add a new book. We'll add on the [Bootstrap Vue](https://bootstrap-vue.js.org/) library for this, which provides a set of Vue components styled with Bootstrap-based HTML and CSS.

> Why Bootstrap Vue? Bootstrap's Modal component uses jQuery, which you should avoid using with Vue together in the same project since Vue uses the Virtual Dom to update the DOM. In other words, if you did use jQuery to manipulate the DOM, Vue would not know about it. At the very least, if you absolutely need to use jQuery, do not use Vue and jQuery together on the same DOM elements.

Install:

Enable the Bootstrap Vue library in *client/src/main.js*:

## POST Route

### Server

Update the existing route handler to handle POST requests for adding a new book:

Update the imports:

With the Flask server running, you can test the POST route in a new terminal tab:

You should see:

You should also see the new book in the response from the [http://localhost:5000/books](http://localhost:5000/books) endpoint.

> What if the title already exists? Or what if a title has more than one author? Check your understanding by handling these cases. Also, how would you handle an invalid payload where the title, author, and/or read is missing?

### Client

On the client-side, let's add that modal now for adding a new book to the `Books` component, starting with the HTML:

Add this just before the closing `div` tag. Take a quick look at the code. `v-model` is a directive used to [bind](https://vuejs.org/v2/guide/forms.html) input values back to the state. You'll see this in action shortly.

> What does hide-footer do? Review this on your own in the Bootstrap Vue docs.

Update the `script` section:

What's happening here?

1. `addBookForm` is [bound](https://vuejs.org/v2/guide/forms.html#Basic-Usage) to the form inputs via, again, `v-model`. When one is updated, the other will be updated as well, in other words. This is called two-way binding. Take a moment to read about it [here](https://stackoverflow.com/questions/13504906/what-is-two-way-binding). Think about the ramifications of this. Do you think this makes state management easier or harder? How do React and Angular handle this? In my opinion, two-way binding (along with mutability) makes Vue much more approachable than React, but less scaleable in the long run.
2. `onSubmit` is fired when the user submits the form successfully. On submit, we prevent the normal browser behavior (`evt.preventDefault()`), close the modal (`this.$refs.addBookModal.hide()`), fire the `addBook` method, and clear the form (`initForm()`).
3. `addBook` sends a POST request to `/books` to add a new book.
4. Review the rest of the changes on your own, referencing the Vue [docs](https://vuejs.org/v2/guide/) as necessary.

> Can you think of any potential errors on the client or server? Handle these on your own to improve user experience.

Finally, update the "Add Book" button in the template so that the modal is displayed when the button is clicked:

The component should now look like this:

Test it out! Try adding a book:

![Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/add-new-book.gif](Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/add-new-book.gif)

## Alert Component

Next, let's add an [Alert](https://bootstrap-vue.js.org/docs/components/alert/) component to display a message to the end user after a new book is added. We'll create a new component for this since it's likely that you'll use the functionality in a number of components.

Add a new file called *Alert.vue* to "client/src/components":

Then, import it into the `script` section of the `Books` component and register the component:

Now, we can reference the new component in the `template` section:

Refresh the browser. You should now see:

![Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/alert.png](Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/alert.png)

> Review Composing with Components from the official Vue docs for more info on working with components in other components.

Next, let's add the actual [b-alert](https://bootstrap-vue.js.org/docs/components/alert/) component to the template:

Take note of the [props](https://vuejs.org/v2/guide/components-props.html) option in the `script` section. We can pass a message down from the parent component (`Books`) like so:

Try this out:

![Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/alert-2.png](Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/alert-2.png)

To make it dynamic, so that a custom message is passed down, use a [binding expression](https://vuejs.org/v2/guide/syntax.html#v-bind-Shorthand) in *Books.vue*:

Add the `message` to the `data` options, in *Books.vue* as well:

Then, within `addBook`, update the message:

Finally, add a `v-if`, so the alert is only displayed if `showMessage` is true:

Add `showMessage` to the `data`:

Update `addBook` again, setting `showMessage` to `true`:

Test it out!

![Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/add-new-book-2.gif](Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/add-new-book-2.gif)

> Challenges:  Think about where showMessage should be set to false. Update your code. Try using the Alert component to display errors. Refactor the alert to be dismissible.

## PUT Route

### Server

For updates, we'll need to use a unique identifier since we can't depend on the title to be unique. We can use `uuid` from the Python [standard library](https://docs.python.org/3/library/uuid.html).

Update `BOOKS` in *server/app.py*:

Don't forget the import:

Refactor `all_books` to account for the unique id when a new book is added:

Add a new route handler:

Add the helper:

> Take a moment to think about how you would handle the case of an id not existing. What if the payload is not correct? Refactor the for loop in the helper as well so that it's more Pythonic.

### Client

Steps:

1. Add modal and form
2. Handle update button click
3. Wire up AJAX request
4. Alert user
5. Handle cancel button click

### (1) Add modal and form

First, add a new modal to the template, just below the first modal:

Add the form state to the `data` part of the `script` section:

> Challenge: Instead of using a new modal, try using the same modal for handling both POST and PUT requests.

### (2) Handle update button click

Update the "update" button in the table:

Add a new method to update the values in `editForm`:

Then, add a method to handle the form submit:

### (3) Wire up AJAX request

### (4) Alert user

Update `updateBook`:

### (5) Handle cancel button click

Add method:

Update `initForm`:

Make sure to review the code before moving on. Once done, test out the application. Ensure the modal is displayed on the button click and that the input values are populated correctly.

![Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/update-book.gif](Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/update-book.gif)

## DELETE Route

### Server

Update the route handler:

### Client

Update the "delete" button like so:

Add the methods to handle the button click and then remove the book:

Now, when the user clicks the delete button, the `onDeleteBook` method is fired, which, in turn, fires the `removeBook` method. This method sends the DELETE request to the back-end. When the response comes back, the alert message is displayed and `getBooks` is ran.

> Challenges:  Instead of deleting on the button click, add a confirmation alert. Display a message saying, like "No books! Please add one.", when no books are present.

![Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/delete-book.gif](Developing%20a%20Single%20Page%20App%20with%20Flask%20and%20Vue%20js%209fb52c8e3eaa47dbbb6ca81b176f08ef/delete-book.gif)

## Conclusion

This post covered the basics of setting up a CRUD app with Vue and Flask.

Check your understanding by reviewing the objectives from the beginning of this post and going through each of the challenges.

You can find the source code in the [flask-vue-crud](https://github.com/testdrivenio/flask-vue-crud) repo. Thanks for reading.

> Looking for more?  Check out the Accepting Payments with Stripe, Vue.js, and Flask blog post, which starts from where this post leaves off. Want to learn how to deploy this app to Heroku? Check out Deploying a Flask and Vue App to Heroku with Docker and Gitlab CI.