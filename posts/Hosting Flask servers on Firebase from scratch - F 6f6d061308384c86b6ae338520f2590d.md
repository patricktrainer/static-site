# Hosting Flask servers on Firebase from scratch - Firebase Developers - Medium

Created: Mar 30, 2020 7:22 AM
URL: https://medium.com/firebase-developers/hosting-flask-servers-on-firebase-from-scratch-c97cfb204579

![1*9xKNnh6ZBJaEFpf1-3jKxg.png](Hosting%20Flask%20servers%20on%20Firebase%20from%20scratch%20-%20F%206f6d061308384c86b6ae338520f2590d/19xKNnh6ZBJaEFpf1-3jKxg.png)

## Python devs 🐍! Rejoice 🎉! Firebase Hosting 🔥 supports dynamic server backends with Cloud Run 🏃‍♂️! Alright. That’s enough emojis. Time to dive into the details.

**Nope!** Back in 2017 Firebase integrated Hosting with Cloud Functions to allow you to dynamically generate content on the server and send it back through their Content Delivery Network (CDN). This allowed you two mix and match a strategy of serving dynamic pages and plain ol’ static pages.

At the time, however, these functions were limited to a Node.js runtime. Today, Cloud Run allows you to do so much more.

## Any server backend with Cloud Run

With Firebase Hosting integrating with Cloud Run, you can generate content from anything that fits within a stateless Docker container. This means you can pick whatever language and server framework your heart desires.

This tutorial will show you how to get a Flask server working from scratch with Firebase Hosting and Cloud Run. Let’s get started!

## Note: You don’t need to install Docker

Cloud Run is a serverless way to run Docker containers. However, this tutorial will use Cloud Build to build and store your container for Cloud Run. No need to worry if you don’t have Docker installed.

Let’s get started off right with a simple project structure. You don’t need to create each file and folder upfront, but you can use this as a guide throughout the tutorial.

```
flask-fire (root dir)
├── server
| ├── src
|    └── app.py
|    └── templates
|       └── index.html 
| ├── Dockerfile
├── static
|  └── style.css 
├── firebase.json
├── .firebaserc
```

The split between `server` and `static` is important. We might be executing server code in some cases, but that doesn’t mean we want that code to serve our static files, too.

Create an `index.html` file in the `server/src/templates` directory and paste in the following code:

Then open or create `server/src/app.py` and paste in the following code.

This is just a simple Flask server that renders a template in response to the index (`/`) endpoint .The Flask server will automatically look in the `templates` folder and look for the `index.html` file. The template renders `"Flask + Firebase"` with the server’s current time.

Now that you have the code for a simple Flask server, let’s get it working in a Docker container.

Inside of `server` create a file called `Dockerfile`. No extension needed. If you’ve never worked with Docker before, think of Docker as a chef that builds delicious self-contained software environments and a `Dockerfile` as a recipe to run your server code.

Let’s go over each section.

1. This sets the base image of the container. Your code will run on a version of Python 3.7.
2. Install the needed dependencies to run the server: Flask and gunicorn.
3. Copy the server’s source files into a folder within the container named `app`. Then set the working directory to that `app` folder.
4. Set an environment variable for the port for 8080. Note: Cloud Run expects the port to be 8080.
5. Run `gunicorn` bound to the 8080 port.

With the Dockerfile written, let’s deploy!

If you don’t have a project in mind, go to the [Firebase Console](https://console.firebase.google.com/) and create a new project. Keep track of the project id, you’ll need this soon.

## Cloud Run has a free tier

To use Cloud Run with Firebase Hosting you currently need billing enabled, which requires putting a credit card on file. However! That doesn’t mean you’re going to get charged. **[Cloud Run comes with a free tier](https://cloud.google.com/run/pricing)**. You’ll likely operate in the free tier unless you are using it on a production site or sending large amounts of traffic to your site all month long.

With billing enabled, it’s time to let Cloud Build do the heavy work of building our server code into a Docker container.

To get Cloud Run to execute your container you need to store it in Google [Cloud’s Container Registry](https://cloud.google.com/container-registry/) (GCR). You can upload a local container, but that requires installing Docker, which this tutorial does not require. Instead you’ll send it to Cloud Build and it will build it and upload to GCR for you.

For this step you’ll need to install the [Google Cloud CLI](https://cloud.google.com/sdk/docs/quickstarts) (a.k.a `gcloud`). Once you have it installed you can use it to initialize the SDK to authorize to your account.

```
gcloud init
```

After you have initialized everything, open a terminal to the `server` directory and run the following command:

```
gcloud builds submit --tag gcr.io/<project-id>/flask-fire
```

Once you see a success message you’re ready to deploy to Cloud Run.

Inside the same `server` directory, run the following command to upload to Cloud Run.

```
gcloud beta run deploy --image gcr.io/<project-id>/flask-fire
```

You may be asked questions about enabling APIs and allowing unauthenticated access. Say yes to both. Don’t worry about the access; since this is a web server it needs to be publicly available.

After the deploy completes, you should see a service URL like this: `https://flask-fire-239532hash-us-central-1.a.run.app`. Paste that link into a new browser tab and you should see the bland `"Flask + Firebase"` text.

Now it’s time to set up Firebase Hosting to serve your static files and the content generated with Cloud Run.

To set up Firebase Hosting you’ll need the Firebase CLI installed via npm. You can do this locally, globally, or with even with`[npx](https://www.npmjs.com/package/npx)`. For the sake of simplicity I’ll cover a local install (global installs can sometimes be messy).

Open a terminal to the root of the project directory and run the following commands:

```
npm init -y # creates a package.json
npm install -D firebase-tools
```

This should create a `node_modules` folder with all kinds of dependencies in it. From here we can invoke the Firebase CLI to set up Hosting. From the root of the project run the following command:

```
./node_modules/.bin/firebase init hosting
```

This calls the locally installed Firebase CLI to set up Firebase Hosting within your project. You’ll be asked a few questions:

```
Select a default Firebase project for this directory: (Use arrow keys)
> your-project-idSelect a default Firebase project for this directory: <project-id>
What do you want to use as your public directory? static
Configure as a single-page app (rewrite all urls to /index.html)? N
```

This sets up your app to deploy to the proper Firebase project. The second question sets up Firebase Hosting to deploy the static directory. Responding no to that last question will not configure re-writes for a SPA (single-page web application). You should see a `firebase.json` and `.firebaserc` in the root of your project.

## Make sure no `index.html` exists!

The CLI may write a `404.html` and an `index.html` in the `static` directory. **If that happens make sure to delete the `index.html`.** Firebase Hosting serves static files first. This means if `index.html` exists, it will not call out to the Cloud Run container. To delete then file, run the following command from the root of the project:

```
rm static/index.html # Mac/Linux
del static/index.html # Windows
```

## Add a style.css in the static directory

To add some style to your web app, create a`static/style.css` file with the following contents:

With the project set up locally, we can hook up Cloud Run to Firebase Hosting.

Firebase Hosting calls out to Cloud Run when it finds a matching URL pattern rewrite in your `firebase.json` and no static file exists. This allows you to build your site with static and dynamic routes. Since this is a simple site, you’re going to serve every path through a re-write. You don’t need to worry about setting up routes for static assets since Firebase Hosting serves them first.

Open up your `firebase.json` and create a new re-write rule like below:

The `"rewrites"` section creates an array of rewrites with a single object. This object specifies that when a request comes in matching a `"source"` of `"**"` (which is everything), it will call out to Cloud Run to the container tagged `"flask-fire"` , which you previously deployed to Cloud Run.

Let’s serve this locally to see it work in action. Open a terminal to the root of your project and run the following command:

```
./node_modules/.bin/firebase serve
```

This will run your site on a port of `locahost:5000`. **Note:** While your static files are being served locally, the emulator is still making a call out to Cloud Run.

You’ll notice that the site still renders `"Firebase + Flask"` but it’s centered and has Lobster font! How lovely.

The next step is to set up custom caching control over your content in the CDN.

A huge advantage of using Cloud Run with Firebase Hosting is the control over the CDN cache. Firebase Hosting allows you to control how long a piece of content stays in the CDN cache via a `Cache-Control` header.

```
Cache-Control: public,max-age=300,s-maxage=600
```

The `s-maxage` property tells Firebase Hosting to keep the content in the cache for 10 minutes. During this 10 minute period Firebase Hosting will skip running your server code in Cloud Run and serve the cache content directly.

> What happens if I don’t set a Cache-Control header? If you don’t set a Cache-Control header (and no underlying system sets the header), Firebase Hosting will call out to Cloud Run each and every time.

Flask’s `make_response` make it easy to attach headers. Open up `app.py` and modify the `index()` route to the following:

The code above does the following:

1. Create the template given the context.
2. Create a response with the template.
3. Attach a `Cache-Control` header to control store the content for a 10 minute period in the local CDN edge server. This time period is referred to as a Time To Live or TTL.

Let’s get to the fun part! Deploying!

First you’ll need to redeploy the container since changes were made to the server code. Run the following commands:

```
gcloud builds submit --tag gcr.io/<project-id>/flask-fire
gcloud beta run deploy --image gcr.io/<project-id>/flask-fire
```

This build the container in Cloud Build and deploy to Cloud Run. Now run the Firebase deploy command

```
firebase deploy
```

That’s it! You have deployed a Flask app on to Firebase Hosting and possibly learned a thing or two about Docker and CDNs along the way.

You now have a deployed Flask app that only regenerates when the `Cache-Control` TTL has expired! The timestamp will stay the same until the TTL expires and the regeneration process begins again.

So there it is— with just a few simple steps, you can create a dynamic web site hosted entirely on Firebase Hosting. Does this inspire you to build your own website using Firebase and Flask? If so, I’d love to see what you created! Drop me a comment below, or [send me a tweet](https://twitter.com/_davideast)!