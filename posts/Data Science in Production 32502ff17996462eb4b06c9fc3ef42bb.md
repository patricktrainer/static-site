# Data Science in Production

Created: Feb 21, 2020 12:03 PM
URL: http://web.archive.org/web/20190308184428/http://www.makepit.com/ds_production

While there are many, many, **many** tutorials and resources on how to test and train models with all the various Python data science tools out there, there are fewer that go one step further and disuss what to do with those models to make them useful in a production environment.

This post, inspired by a post on Reddit's [/r/datascience](http://web.archive.org/web/20190308184428/https://www.reddit.com/r/datascience/) subreddit is an attempt to provide a broad but simple overview of a few tools that are useful for data scientists in taking their meticulously trained models and creating useful applications with them. While there are many ways to do this we'll take the approach of setting up a containerized server and creating an API that can be deployed anywhere. We'll talk about what this means in the next section.

### Topics

- Training Scikit-learn Models
    - In this section we'll create a model with scikit-learn. Since the focus of this post isn't around model-building, we'll make a very quick and simple toy model so that we have something to deploy into production. This will be the "brain" of our application later on - the part that creates output from some given input.
- Deploying Models with Flask
    - Flask is a web microframework that we'll use to quickly get a server up and running. But what does this *mean* you might ask! Well, if we have a model then we also have model input and model output. The "usual" way of using this model might be to fire up Python, write some code to get some input into the correct format, pass it into the model, and save our output to some easily handled format (probably a .csv file) to pass off to whatever the next step is. Instead of doing that, we'll have a server running that's providing the *service* of listening to incoming requests (with model input data) and responding with the model's output, which could be passed on to whatever the next step is (emailing to business stakeholder, passing it into another application, or maybe writing it to a database for further consumption down the line).
- Containerizing our Application
    - By this point we'll have a server running locally on our machine, so the next step is to wrap it up nicely to run in a Docker container. By doing this we'll make our application flexible enough to run anywhere, including any of the major cloud service providers or perhaps just on your own server. We'll use a couple of tools here to make our lives easier:
        - docker-compose: This tool will let us use a simple configuration file to define what we want our container to be. For us, this means defining a container that has Python 3.x installed, is running our Flask server, and is listening to requests coming from a port that we'll define.
        - docker-machine: This tool will let us spin up a virtual machine that runs our application. This is a virtual machine in the sense that you're likely familiar with - an operating system that is running *within* your own host operating system. The virtual machine will run our docker container, which contains our application. This final step facilitates deploying everything together in a nice configuration that will run on any machine, whether it's local or with a cloud service providers.

That's a lot of material to get through, so let's get started!

## Training scikit-learn models

This part should be familiar, so I'll mostly let the notebook do the talking. Using the boston_housing dataset we'll create a quick linear regression model that will take in a numerical AGE and output a predicted PRICE (in $1,000s)

[data:image/png;base64,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](data:image/png;base64,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)

# Use pickle to serialize and save model for later use

A useless model indeed, but that's not what matters for our purposes. What **does** matter is that we now have a serialized object that we can use in our application. In practice, this step is usually where most of our focus is - getting all the data together in a clean and useful way and then painstakingly creating a model that will acceptably perform for the task at hand.

For those of us that are unfamiliar with the pickle  package, it suffices to say that it is a convenient way to serialize/package/pickle objects in Python that we can later unpickle in the same state that we packaged them. Since we're sticking to Python tools for this entire tutorial, it's the perfect tool to use to store our model object to later put in our application.

## Deploying Models with Flask

We'll be using Flask as our framework to set up a server. As mentioned in the topics overview, this server will have the function of constantly listening for requests and responding to those requests with the right output. In our context a request will contain model input data and it will call to our model's `predict()` method, returning the corresponding output.

### Setting up a Flask Server

Since this part is likely unfamiliar to the typical data scientist we'll take it one step at a time. I work in a Ubuntu environment so I'll walk through what setup looks like in a Linux environment.

To start, we'll need to create a directory where our entire application will live:

```
mkdir ~/housing_app
```

Now we navigate into our newly created application directory:

```
cd housing_app
```

Before we start, we need to create a virtual environment to keep all of our dependencies neatly together. If you aren't using `virtualenv` yet, I can't stress enough how useful it is and how much you should be using it. [Real Python](http://web.archive.org/web/20190308184428/https://realpython.com/python-virtual-environments-a-primer/) has a great post on how to use them, so I recommend reading up on that before moving on here if you're not already familiar with the topic.

To create our environment we'll run:

```
virtualenv -p python3 .venv
```

Here we used the `-p python3` option to make sure that we're running Python 3 and not Python 2. I'll also take a moment here to recommend the use of [pyenv](http://web.archive.org/web/20190308184428/https://github.com/pyenv/pyenv), which faciliates the installation and use of multiple versions of Python, including Anaconda distributions and what seems to be every Python version release.

We'll notice that there's a new `~/housing_app/.venv` directory with all of our usual Python stuff in it. We'll make this virtualenv the current, active one by executing:

```
source .venv/bin/activate
```

You should notice that in the terminal now you'll see something like `(.venv) user@machine`. If you don't, go back and make sure your virtual environment is set up and activated correctly.

Finally, we can install Flask with pip:

```
pip install Flask
```

Equipped with our newfound Flask framework, we can already create the simplest of servers. We'll create an `app.py` file in our directory so that we end up with this directory structure:

├── housing_app
│ ├── app.py
│ └── .venv

In that file, we can copy/paste the following

```
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
```

Now we just need to tell our terminal which file to run:

```
export FLASK_APP=app.py
```

And finally, we can run our very simple server:

```
flask run
```

You should see a bit of output that looks like this:

And we should be able to navigate to 127.0.0.1:5000 in our browser to get our Hello, World! message!

Note that our application is running in "production" mode, but also warns us not to use the development server in a production environment. What does that mean Flask?! To put it briefly, Flask's built-in server is extremely useful for development but real web servers are generally expected to handle multiple concurrent users and requests, which the built-in server does NOT do. Thus, when actually deploying an application, it's highly recommended to use a WSGI (web server gateway interface) server. These WSGI servers are designed to act as the initial gateway that requests come into. The WSGI server then forwards on the request to the application, as shown in the diagram below:

Fortunately for us, we can gloss over the details here, and just know that we need an additional WSGI server if we want to deploy it into an environment that can scale. [Flask's own documentation](http://web.archive.org/web/20190308184428/http://flask.pocoo.org/docs/1.0/deploying/) does a good job of discussing many deployment options. Many cloud service providers (for example, AWS Elastic Beanstalk) handle this deployment on your behalf so that it is set up behind the scenes and all you have to do is make sure that your application runs as we've just done.

### Flask Basics

Getting back to business, let's re-examine our `app.py`:

```
# app.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
```

The biggest thing to note is `app.route()`. This decorator is used to create a method that binds to Flask's URLs. For our minimal example, we've only set `@app.route('/')`, which is the root URL for our application. This means it's the default route for any user that just navigates to our application.

We can add a new `/predict` route in our `app.py` to very easily extend our application.

```
# app.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/predict')
def predict():
    return 'We have not built this yet!'
```

Now we can navigate to our new route at `http://127.0.0.1:5000/predict` to make sure it works. Easy!

Note that the `hello_world()` and the `predict()` methods are just that - regular Python functions that can take any arbitrary logic. We can begin to imagine these functions are where we'll write the logic to handle model input, pass it into the model, and get some output back.

Since we're going to need to pass data to and from our application, we'll need to talk about the mechanisms for doing that. We're using a web server, so we'll be using a few HTTP methods. There's a lot of information on the topic, but for now we'll condense and simplify it to this - there are four most commonly used HTTP verbs: GET, POST, PUT, and DELETE. We can relate these to CRUD (create/read/update/delete) operations like you'd use in a database:

[Untitled](Data%20Science%20in%20Production%2032502ff17996462eb4b06c9fc3ef42bb/Untitled%20Database%2054135777308e4261a5b6977a129e216d.csv)

`GET` is the bread-and-butter of the internet. When you clicked on a link to get to this page, behind the scenes a GET request was sent and your browser received a bunch of HTML that it rendered into this long tutorial. Let's take a look at how it works in Flask.

```
#app.py
from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return('Hello, World!')

@app.route('/predict')
def predict():
    return('We have not built this yet!')

@app.route('/get_example/<some;_input>', methods=['GET'])
def get_example(some_input):
    if request.method == 'GET':
        return('You supplied the following input: ' + str(some_input))
```

We need to note a few things here. First off, we're now importing `request`, which facilitates interacting with the HTTP requests that are going on. We make use of it in our `get_example()` function to check that the request is a `GET` request before continuing on with our logic.

Another major thing to note is that our `/get_example` route is taking a dynamic `<some;_input>` input. This means that when we navigate to `127.0.0.1:5000/get_example/SOME_INPUT`, our `SOME_INPUT` is going to be read by our function. We can test this by navigating there and seeing it printed in our browser.

While this is a convenient method for many things, it's not ideal for our application where we may want to pass in lots of data and get a lot of data back. Enter the `POST` verb. Unlike `GET`, we can't just use the URL (nor would we want to) to pass in parameters.

The way `POST` requests work is that some payload object is attached to the request in the background. There are various ways to handle these objects, but we're going to use JSON payloads, which are generally the most common and are likely a format that we're already familiar with! We'll use [curl](http://web.archive.org/web/20190308184428/https://curl.haxx.se/), a ubiquitous tool for making these requests from the command line. To install simply run `sudo apt install curl`. To make sure that everything is working before we continue, let's make the exact same request that we were making from our browsers, but now with curl:

```
curl http://127.0.0.1:5000/get_example/input_data
```

As a response we should see "You supplied the following input: input_data" in the terminal, which is just what we saw in our browsers.

Now let's go back and adapt our `/predict` route to accept `POST` requests and do something with it.

```
#app.py
from flask import Flask, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def hello_world():
    return('Hello, World!')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        data = request.json

        house_id = data['house_id']
        age = data['age']

        return('House ID: ' + str(house_id) + '\nHouse Age: ' + str(age) + '\n')
```

Now our `/predict` route will accept some payload and all we're going to do for now is print some output. We can execute the following in our terminal to have curl send the `POST` request to our application. Note that we're passing in `{"house_id":"1001", "age":50}` as our JSON payload.

```
curl -XPOST -H "Content-Type: application/json" http://127.0.0.1:5000/predict -d '[{"house_id":"1001", "age":50}]'
```

As a response we'll get this in our terminal:

```
House ID: 1001
House Age: 50
```

Let's take it just one step further and instead of returning some parsed strings, let's take the input, convert it into a pandas dataframe, and return it as a dataframe. Before we do this, make sure to install pandas (`pip install pandas`) in our virtualenv. Now we can modify our `app.py` and run the same curl command as before.

```
#app.py
from flask import Flask, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def hello_world():
    return('Hello, World!')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        df = pd.DataFrame.from_records(request.json)
        return(str(df))
```

We can start to feel back at home now that we have a pandas dataframe to work with!

Now all we need to do is include our model, parse whatever input goes into it, and return our predicted prices. First let's go back and find our house_price_model and put it in the housing_app directory so that we have this:

├── housing_app
│ ├── app.py
│ ├── house_price_model
│ └── .venv

Now let's change our `app.py` to load the model and implement some predictions with it. Here's what that could look like:

```
#app.py
from flask import Flask, request
import pandas as pd
import pickle

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # turn json format into pandas dataframe
        df = pd.DataFrame.from_records(request.json)

        # make predictions and create a df out of them
        pred = house_price_model.predict(df[['age']]))
        pred = pd.DataFrame(pred, columns=['predicted_price'])

        # combine with original data to return it all together
        pred = pd.concat([df, pred], axis=1)

        return(str(pred))

@app.before_first_request
def load_model():
    global house_price_model
    with open('house_price_model', 'rb') as handle:
        house_price_model = (pickle.load(handle))
```

We've made several changes to our `app.py` that we need to look at.

First of all, we added a `load_model()` function with an `@app.before_first_request` decorator. This is a special Flask decorator that will execute the function once before executing any other request. We made `house_price_model` a global variable here so that we can access it from anywhere in our application, and then we simply loaded our pickled house_price_model.

In our `predict()` function we added a couple of lines to take our input dataframe, pass it into our `house_price_model`, and then combine it all back together and return it to the user.

Let's take our completed application for a whirl, this time with several records:

```
curl -XPOST -H "Content-Type: application/json" http://127.0.0.1:5000/predict -d '[{"house_id":1001,"age":50},{"house_id":1002,"age":75},{"house_id":1003,"age":100}]'
```

In response to this, we'll see the following in our terminal:

```
age  house_id  predicted_price
0   50      1001        24.901049
1   75      1002        22.065760
2  100      1003        19.230470
```

Look at us go! We have a running application that will take in a `POST` request with house_id and age and return predicted prices! We've come a long way already, but we're not done yet! In the next section we'll discuss putting our application into a Docker container and prepare it to deploy it into an AWS environment.

### Deploying Our Application with Containers

Before we get started, let's install all the Docker tools that we'll need:

- Docker (engine)
- This is the base engine and is what the other two tools leverage for creating containers. You can use this alone to start creating containers, but we'll largely use docker-compose to orchestrate container creation.
- Docker Compose
- This is the tool we'll focus on to quickly configure and create multiple containers at once that work together to function as an application.
- Docker Machine
- We'll leverage docker-machine to create virtual machines that run our containers, both locally and on the cloud.

Before we continue, make sure to test your installations with:

```
docker-compose --version
docker-machine --version
```

Now that we have everything installed, let's take a look at what our new directory structure should be.

```
└── housing_app
    ├── docker-compose.yml
    ├── nginx
    │   ├── Dockerfile
    │   └── sites-enabled
    │       └── housing_app
    └── web
        ├── Dockerfile
        ├── app.py
        ├── house_price_model
        └── requirements.txt
```

We have a lot of new stuff here, so let's take it one step at a time.

First, we note that we've created two new directories - `nginx` and `web`, with all of our Flask files in the `web` directory. We've done this because each directory within the `~/housing_app` directory now represents a Docker container - we'll have a `web` container that contains our Flask web application, and we have a new `nginx` container that is going to contain an [nginx](http://web.archive.org/web/20190308184428/https://www.nginx.com/) instance.

Nginx is a server that we will use as a reverse proxy. This means that requests that come in will go through our nginx server, which will forward those requests to our actual Flask server. Because this is meant to be a production environment, we'll also be moving away from Flask's built-in server and use [gunicorn](http://web.archive.org/web/20190308184428/https://gunicorn.org/), which is a WSGI server. Remember - while Flask's built-in server is great for quickly developing something, it does not handle concurrent users/requests. For that we need to use a WSGI server, like gunicorn, to deploy our Flask application. It sounds complicated and like a lot to take in, but we'll see that the implementation is rather simple.

### Dockerfile

Within each of our two container directories, we'll notice that we have a Dockerfile for each of them. These Dockerfiles are configuration files so that Docker knows how to build that container. Let's first look at the Dockerfile for our `web` container:

```
FROM python:3.6-onbuild
```

Yep - that's it! All we're telling Docker is that we want an image called `python:3.6-onbuild`, which it will go out and find from [Docker Hub](http://web.archive.org/web/20190308184428/https://hub.docker.com/_/python), which is a repository of many types of images that anybody can put up. Fortunately for us, there are all kinds of Python images that we can just grab without worrying about creating them ourselves.

Let's look at the Dockerfile for our nginx container now:

```
FROM tutum/nginx
RUN rm /etc/nginx/sites-enabled/default
ADD sites-enabled/ /etc/nginx/sites-enabled
```

Here we're also starting with a `FROM` statement, but instead of a Python image, we're grabbing an nginx image. The next two lines are also quite simple - first, we see a `RUN` command, which instructs Docker to run `rm /etc/nginx/sites-enabled/default` within that container. If you're familiar with basic Linux commands you'll recognize that we're just deleting a file here and then adding a new one in the very next `ADD` command. In the `ADD` command note this - we're instructing Docker to take `sites-enables`, which is the directory in `~/housing_app/nginx/` and copy it into the Docker container's `/etc/nginx/` directory. Remember - these Docker containers are just minimal Linux machines.

### docker-compose.yml

As you might have guessed, this is the configuration file that docker-compose will use to create all of your Docker containers. Think of it as a script that defines how your containers will be created and how they will interact with each other. Let's jump in and take a look at it:

```
version:2
services:
  web:
    restart: always
    build: ./web
    expose:
      - "8000"
    command: /usr/local/bin/gunicorn -b :8000 app:app

  nginx:
    restart: always
    build: ./nginx
    ports:
      - "80:80"
    links:
      - "web"
```

Naturally, we've defined two services here - web and nginx, which correspond to the containers that we're making, and under each of these services we've defined some basic configuration options. There's a lot we can do here, but for now we've left it pretty simple, with a few key commands:

- **build**: this tells Docker which directory to build the container from
- **expose**: this makes port 8000 available to other containers - this is key if containers need to interact with each other
- **command**: this is the final command that is run after the container is created - for out web container we need to create the container, but then also need the Flask application to run, using gunicorn
- **ports**: unlike **expose** this is making port 80 (for HTTP) available to us as the users, rather than available to other containers
- **links**: this creates a link between containers so that we can refer to 'web' simply as 'web' and not worry about the actual IP address

### Deployment

We're finally here! Let's first create a local virtual machine to test out our application configurations - we'll use the following docker-machine command to spin up a virtualbox VM named housing-app-vm. This will likely take a little while since things will need to be downloaded and set up.

```
docker-machine create -d virtualbox housing-app-vm
```

Once it's done you can check that your new VM exists by doing:

```
docker-machine ls
```

Now that it's created we just need to make it our current active VM by executing:

```
eval "$(docker-machine env housing-app-vm)"
```

With our `housing_app_vm` VM created and running, we'll execute the following from `~/housing_app` (the location of docker-compose.yml):

```
docker-compose build
docker-compose up -d
```

We'll see a lot of magic happening in the terminal, but when it's done, our containers will be running on our VM and we'll be able to interact with them. Check to see which IP address your VM is running on with `docker-machine ls` and navigate to it in your browser - for me it's 192.168.99.100. We should see our same 'Hello, World!' message as before if everything is running correctly.

We should also be able to execute our same curl command to get house price predictions back, just like before:

```
curl -XPOST -H "Content-Type: application/json" http://192.168.99.100/predict -d '[{"house_id":1001,"age":50},{"house_id":1002,"age":75},{"house_id":1003,"age":100}]'
```

### Cloud Deployment

We promised cloud deployment, and [here it is.](http://web.archive.org/web/20190308184428/https://docs.docker.com/machine/get-started-cloud/) If you've been following along so far, it's essentially a repeat of what we just did with our VM locally, but rather than using a virtualbox driver to create the VM, we'll use a cloud service provider's. This is what it would look like to deploy on AWS:

Create a VM running on EC2:htop

```
docker-machine create --driver amazonec2 --amazonec2-access-key AKI******* --amazonec2-secret-key 8T93C*******  housing-app-aws
```

Note here that this is assuming that you've created an account and have your access-key and secret-key.

Now the rest is just like before - make your new AWS VM active, build, and deploy!

```
eval "$(docker-machine env housing-app-aws)"
```

```
docker-compose build
docker-compose up -d
```

Not so bad, huh?

### Final Thoughts

While getting this very basic application has been a useful demonstration of the overall structure and frameworks that can be used, it's far from something that should be put into production. At best, it may serve as a template to start building out a robust, production-quality application that can be used reliably.

So what's missing, you might ask? Here are a few topics that you can look into that would definitely be desirable in a robust application:

- Token-based authentication
- No matter the application, we would definitely want to control who can use it and what access they have.
- Type-checking and error-catching
- In the demo we assumed that our input would always be precisely in the correct format and would be the proper datatypes. In reality we should check input and have at least some basic error handling. If data is coming from sources that we don't control it would also be valuable to have some quality checks on the data that is coming in so we can be more sure that out application's output will be reasonable.
- Persitent input/output storage
- It's not hard to imagine a case where we'd want to see what data has been fed in as input and what has been produced as output. A couple of use cases for this may be for later auditing input/output, tracking model performance if we can later have a feedback to compare against our predictions, or even simply the facility to pull output related to any particular run.
- Robust application of REST principles
- In our demo we made a couple of routes and glossed over the details, but in reality there are REST principles that we should adhere to and there are tools, such as  [Connexion](http://web.archive.org/web/20190308184428/https://connexion.readthedocs.io/en/latest/) that we could use to facilitate the creation of APIs.
- API Documentation
- If you've ever used a poorly-documented API you'll know the heartaches involved with trying to parse together how it works. We wouldn't want to do that to any of our potential users, so rounding out the list is probaby the most important part - proper documentation, for both us to come back to later and for anyone that wants to make use of our cool application.