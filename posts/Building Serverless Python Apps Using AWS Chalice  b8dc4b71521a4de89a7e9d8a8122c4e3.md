# Building Serverless Python Apps Using AWS Chalice – Real Python

Created: Feb 21, 2020 12:18 PM
URL: https://realpython.com/aws-chalice-serverless-python/

![Building%20Serverless%20Python%20Apps%20Using%20AWS%20Chalice%20%20b8dc4b71521a4de89a7e9d8a8122c4e3/Building-Server-less-Apps-in-Python-for-AWS-Lambda_Watermarked.6db2342b6524.jpg](Building%20Serverless%20Python%20Apps%20Using%20AWS%20Chalice%20%20b8dc4b71521a4de89a7e9d8a8122c4e3/Building-Server-less-Apps-in-Python-for-AWS-Lambda_Watermarked.6db2342b6524.jpg)

Table of Contents

Shipping a web application usually involves having your code up and running on single or multiple servers. In this model, you end up setting up processes for monitoring, provisioning, and scaling your servers up or down. Although this seems to work well, having all the logistics around a web application handled in an automated manner reduces a lot of manual overhead. Enter Serverless.

With [Serverless Architecture](https://aws.amazon.com/lambda/serverless-architectures-learn-more/), you don’t manage servers. Instead, you only need to ship the code or the executable package to the platform that executes it. It’s not really serverless. The servers do exist, but the developer doesn’t need to worry about them.

AWS introduced [Lambda Services](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html), a platform that enables developers to simply have their code executed in a particular runtime environment. To make the platform easy to use, many communities have come up with some really good frameworks around it in order to make the serverless apps a working solution.

**By the end of this tutorial, you’ll be able to**:

- Discuss the benefits of a serverless architecture
- Explore Chalice, a Python serverless framework
- Build a full blown serverless app for a real world use case
- Deploy to Amazon Web Services (AWS) Lambda
- Compare Pure and Lambda functions

**Free Bonus:** 5 Thoughts On Python Mastery, a free course for Python developers that shows you the roadmap and the mindset you'll need to take your Python skills to the next level.

## Getting Started With AWS Chalice

[Chalice](https://github.com/aws/chalice/), a Python Serverless Microframework developed by AWS, enables you to quickly spin up and deploy a working serverless app that scales up and down on its own as required using AWS Lambda.

### Why Chalice?

For Python developers accustomed to the Flask web framework, Chalice should be a breeze in terms of building and shipping your first app. Highly inspired by Flask, Chalice keeps it pretty minimalist in terms of defining what the service should be like and finally making an executable package of the same.

Enough theory! Let’s start with a basic `hello-world` app and kick-start our serverless journey.

Before diving into Chalice, you’ll set up a working environment on your local machine, which will set you up for the rest of the tutorial.

First, create and activate a virtual environment and install Chalice:

```
$ python3.6 -m venv env
$ source env/bin/activate
(env)$ pip install chalice
```

Follow our comprehensive guide on the [Pipenv packaging tool](https://realpython.com/pipenv-guide/).

**Note:** Chalice comes with a user-friendly CLI that makes it easy to play around with your serverless app.

Now that you have Chalice installed on your virtual environment, let’s use the Chalice CLI to generate some boilerplate code:

```
(env)$ chalice new-project
```

Enter the name of the project when prompted and hit return. A new directory is created with that name:

```
<project-name>/
|
├── .chalice/
│   └── config.json
|
├── .gitignore
├── app.py
└── requirements.txt
```

See how minimalist the Chalice codebase is. A `.chalice` directory, `app.py`, and `requirements.txt` is all that it requires to have a serverless app up and running. Let’s quickly run the app on our local machine.

Chalice CLI consists of really great utility functions allowing you to perform a number of operations from running locally to deploying in a Lambda environment.

### Build and Run Locally

You can simulate the app by running it locally using the `local` utility of Chalice:

```
(env)$ chalice local
Serving on 127.0.0.1:8000
```

By default, Chalice runs on port 8000. We can now check the index route by making a [curl request](http://www.codingpedia.org/ama/how-to-test-a-rest-api-from-command-line-with-curl/) to `http://localhost:8000/`:

```
$ curl -X GET http://localhost:8000/
{"hello": "world"}
```

Now if we look at `app.py`, we can appreciate the simplicity with which Chalice allows you to build a serverless service. All the complex stuff is handled by the decorators:

```
from chalice import Chalice
app = Chalice(app_name='serverless-sms-service')

@app.route('/')
def index():
    return {'hello': 'world'}
```

**Note**: We haven’t named our app `hello-world`, as we will build our SMS service on the same app.

Now, let’s move on to deploying our app on the AWS Lambda.

### Deploy on AWS Lambda

Chalice makes deploying your serverless app completely effortless. Using the `deploy` utility, you can simply instruct Chalice to deploy and create a Lambda function that can be accessible via a REST API.

Before we begin deployment, we need to make sure we have our AWS credentials in place, usually located at `~/.aws/config`. The contents of the file look as follows:

```
[default]
aws_access_key_id=<your-access-key-id>
aws_secret_access_key=<your-secret-access-key>
region=<your-region>
```

With AWS credentials in place, let’s begin our deployment process with just a single command:

```
(env)$ chalice deploy
Creating deployment package.
Updating policy for IAM role: hello-world-dev
Creating lambda function: hello-world-dev
Creating Rest API
Resources deployed:
  - Lambda ARN: arn:aws:lambda:ap-south-1:679337104153:function:hello-world-dev
  - Rest API URL: https://fqcdyzvytc.execute-api.ap-south-1.amazonaws.com/api/
```

**Note**: The generated ARN and API URL in the above snippet will vary from user to user.

Wow! Yes, it is really this easy to get your serverless app up and running. To verify simply make a curl request on the generated Rest API URL:

```
$ curl -X GET https://fqcdyzvytc.execute-api.ap-south-1.amazonaws.com/api/
{"hello": "world"}
```

Typically, this is all that you need to get your serverless app up and running. You can also go to your AWS console and see the Lambda function created under the Lambda service section. Each Lambda service has a unique REST API endpoint that can be consumed in any web application.

Next, you will begin building your Serverless SMS Sender service using Twilio as an SMS service provider.

## Building a Serverless SMS Sender Service

With a basic `hello-world` app deployed, let’s move on to building a more real-world application that can be used along with everyday web apps. In this section, you’ll build a completely serverless SMS-sending app that can be plugged into any system and work as expected as long as the input parameters are correct.

In order to send SMS, we will be using [Twilio](https://www.twilio.com/), a developer-friendly SMS service. Before we begin using Twilio, we need to take care of a few prerequisites:

- Create an account and acquire `ACCOUNT_SID` and `AUTH_TOKEN`.
- Get a mobile phone number, which is available for free at Twilio for minor testing stuff.
- Install the `twilio` package in our virtual environment using `pip install twilio`.

With all the above prerequisites checked, you can start building your SMS service client using Twilio’s Python library. Let’s begin by cloning the [repository](https://github.com/realpython/materials/pull/16) and creating a new feature branch:

```
$ git clone <project-url>
$ cd <project-dir>
$ git checkout tags/1.0 -b twilio-support
```

Now make the following changes to `app.py` to evolve it from a simple `hello-world` app to enable support for Twilio service too.

First, let’s include all the import statements:

```
from os import environ as env

# 3rd party imports
from chalice import Chalice, Response
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Twilio Config
ACCOUNT_SID = env.get('ACCOUNT_SID')
AUTH_TOKEN = env.get('AUTH_TOKEN')
FROM_NUMBER = env.get('FROM_NUMBER')
TO_NUMBER = env.get('TO_NUMBER')
```

Next, you’ll encapsulate the Twilio API and use it to send SMS:

```
app = Chalice(app_name='sms-shooter')

# Create a Twilio client using account_sid and auth token
tw_client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.route('/service/sms/send', methods=['POST'])
def send_sms():
    request_body = app.current_request.json_body
    if request_body:
        try:
            msg = tw_client.messages.create(
                from_=FROM_NUMBER,
                body=request_body['msg'],
                to=TO_NUMBER)

            if msg.sid:
                return Response(status_code=201,
                                headers={'Content-Type': 'application/json'},
                                body={'status': 'success',
                                      'data': msg.sid,
                                      'message': 'SMS successfully sent'})
            else:
                return Response(status_code=200,
                                headers={'Content-Type': 'application/json'},
                                body={'status': 'failure',
                                      'message': 'Please try again!!!'})
        except TwilioRestException as exc:
            return Response(status_code=400,
                            headers={'Content-Type': 'application/json'},
                            body={'status': 'failure',
                                  'message': exc.msg})
```

In the above snippet, you simply create a Twilio client object using `ACCOUNT_SID` and `AUTH_TOKEN` and use it to send messages under the `send_sms` view. `send_sms` is a bare bones function that uses the Twilio client’s API to send the SMS to the specified destination. Before proceeding further, let’s give it a try and run it on our local machine.

### Build and Run Locally

Now you can run your app on your machine using the `local` utility and verify that everything is working fine:

```
(env)$ chalice local
```

Now make a curl POST request to `http://localhost:8000/service/sms/send` with a specific payload and test the app locally:

```
$ curl -H "Content-Type: application/json" -X POST -d '{"msg": "hey mate!!!"}' http://localhost:8000/service/sms/send
```

The above request responds as follows:

```
{
  "status": "success",
  "data": "SM60f11033de4f4e39b1c193025bcd5cd8",
  "message": "SMS successfully sent"
}
```

The response indicates that the message was successfully sent. Now, let’s move on to deploying the app on AWS Lambda.

### Deploy on AWS Lambda

As suggested in the previous deployment section, you just need to issue the following command:

```
(env)$ chalice deploy
Creating deployment package.
Updating policy for IAM role: sms-shooter-dev
Creating lambda function: sms-shooter-dev
Creating Rest API
Resources deployed:
  - Lambda ARN: arn:aws:lambda:ap-south-1:679337104153:function:sms-shooter-dev
  - Rest API URL: https://qtvndnjdyc.execute-api.ap-south-1.amazonaws.com/api/
```

**Note**: The above command succeeds, and you have your API URL in the output as expected. Now on testing the URL, the API throws an error message. **What went wrong?**

As per AWS [Lambda logs](https://www.dropbox.com/s/ectzx2std57toaf/Screenshot%202018-11-08%20at%208.35.18%20PM.png?dl=0), `twilio` package is not found or installed, so you need to tell the Lambda service to install the dependencies. To do so, you need to add `twilio` as a dependency to `requirements.txt`:

```
twilio==6.18.1
```

Other packages such as Chalice and its dependencies should not be included in `requirements.txt`, as they are not a part of Python’s WSGI runtime. Instead, we should maintain a `requirements-dev.txt`, which is applicable to only the development environment and contains all Chalice-related dependencies. To learn more, check out [this GitHub issue](https://github.com/aws/chalice/issues/803).

Once all the package dependencies are sorted, you need to make sure all the environment variables are also shipped along and set correctly during the Lambda runtime. To do so, you have to add all the environment variables in `.chalice/config.json` in the following manner:

```
{
  "version": "2.0",
  "app_name": "sms-shooter",
  "stages": {
    "dev": {
      "api_gateway_stage": "api",
      "environment_variables": {
          "ACCOUNT_SID": "<your-account-sid>",
          "AUTH_TOKEN": "<your-auth-token>",
          "FROM_NUMBER": "<source-number>",
          "TO_NUMBER": "<destination-number>"
      }
    }
  }
}
```

Now we’re good to deploy:

```
Creating deployment package.
Updating policy for IAM role: sms-shooter-dev
Updating lambda function: sms-shooter-dev
Updating rest API
Resources deployed:
  - Lambda ARN: arn:aws:lambda:ap-south-1:679337104153:function:sms-shooter-dev
  - Rest API URL: https://fqcdyzvytc.execute-api.ap-south-1.amazonaws.com/api/
```

Do a sanity check by making a curl request to the generated API endpoint:

```
$ curl -H "Content-Type: application/json" -X POST -d '{"msg": "hey mate!!!"}' https://fqcdyzvytc.execute-api.ap-south-1.amazonaws.com/api/service/sms/send
```

The above request responds as expected:

```
{
  "status": "success",
  "data": "SM60f11033de4f4e39b1c193025bcd5cd8",
  "message": "SMS successfully sent"
}
```

Now, you have a completely serverless SMS sending service up and running. With the front end of this service being a REST API, it can be used in other applications as a plug-and-play feature that is scalable, secure, and reliable.

## Refactoring

Finally, we will refactor our SMS app to not contain all the business logic in `app.py` completely. Instead, we will follow the Chalice prescribed best practices and abstract the business logic under the `chalicelib/` directory.

Let’s begin by creating a new branch:

```
$ git checkout tags/2.0 -b sms-app-refactor
```

First, create a new directory in the root directory of the project named `chalicelib/` and create a new file named `sms.py`:

```
(env)$ mkdir chalicelib
(env)$ touch chalicelib/sms.py
```

Update the above created `chalicelib/sms.py` with the SMS sending logic by abstracting things from `app.py`:

```
from os import environ as env
from twilio.rest import Client

# Twilio Config
ACCOUNT_SID = env.get('ACCOUNT_SID')
AUTH_TOKEN = env.get('AUTH_TOKEN')
FROM_NUMBER = env.get('FROM_NUMBER')
TO_NUMBER = env.get('TO_NUMBER')

# Create a twilio client using account_sid and auth token
tw_client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send(payload_params=None):
    """ send sms to the specified number """
    msg = tw_client.messages.create(
        from_=FROM_NUMBER,
        body=payload_params['msg'],
        to=TO_NUMBER)

    if msg.sid:
        return msg
```

The above snippet only accepts the input params and responds as required. Now to make this work, we need to make changes to `app.py` as well:

```
# Core imports
from chalice import Chalice, Response
from twilio.base.exceptions import TwilioRestException

# App level imports
from chalicelib import sms

app = Chalice(app_name='sms-shooter')

@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/service/sms/send', methods=['POST'])
def send_sms():
    request_body = app.current_request.json_body
    if request_body:
        try:
            resp = sms.send(request_body)
            if resp:
                return Response(status_code=201,
                                headers={'Content-Type': 'application/json'},
                                body={'status': 'success',
                                      'data': resp.sid,
                                      'message': 'SMS successfully sent'})
            else:
                return Response(status_code=200,
                                headers={'Content-Type': 'application/json'},
                                body={'status': 'failure',
                                      'message': 'Please try again!!!'})
        except TwilioRestException as exc:
            return Response(status_code=400,
                            headers={'Content-Type': 'application/json'},
                            body={'status': 'failure',
                                  'message': exc.msg})
```

In the above snippet, all the SMS sending logic is invoked from the `chalicelib.sms` module, making the view layer a lot cleaner in terms of readability. This abstraction lets you add much more complex business logic and customize the functionality as required.

## Sanity Check

After refactoring our code, let’s ensure it is running as expected.

### Build and Run Locally

Run the app once again using the `local` utility:

```
(env)$ chalice local
```

Make a curl request and verify. Once that’s done, move on to deployment.

### Deploy on AWS Lambda

Once you are sure everything is working as expected, you can now finally deploy your app:

```
(env)$ chalice deploy
```

As usual, the command executes successfully and you can verify the endpoint.

## Conclusion

You now know how to do the following:

- Build a serverless application using AWS Chalice in accordance with best practices
- Deploy your working app on the Lambda runtime environment

Lambda services under the hood are analogous to pure functions, which have a certain behavior on a set of input/output. Developing precise Lambda services allows for better testing, readability, and atomicity. Since Chalice is a minimalist framework, you can just focus on the business logic, and the rest is taken care of, from deployment to IAM policy generation. This is all with just a single command deployment!

Moreover, Lambda services are mostly focused on heavy CPU bound processing and scale in a self-governed manner, as per the number of requests in a unit of time. Using serverless architecture allows your codebase to be more like SOA (Service Oriented Architecture). Using [AWS’s](https://realpython.com/python-boto3-aws-s3/) other products in their ecosystem that plug in well with Lambda functions is even more powerful.