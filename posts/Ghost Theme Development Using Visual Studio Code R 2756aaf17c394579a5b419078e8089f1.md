# Ghost Theme Development Using Visual Studio Code Remote Development With Containers

Created: Apr 19, 2020 12:54 PM
URL: https://geeklearning.io/visual-studio-code-remote-development-ghost-theme-with-containers/

Earlier, I've introduced [Visual Studio Remote Developmen](https://geeklearning.io/introduction-to-visual-studio-code-remote-development/)t and you might be wondering what a practical use case would be. In this post, I'll try to guide you through using the support for development in Containers.

To showcase the scenario, I'll use a story about developing a theme for Ghost. Ghost is a popular blogging platform. One of its man feature is an awesome editor. It makes it possible to have the "Medium experience" on a self hosted blog.

When it comes to developing a custom theme, it can become quite unsavory. You need to install ghost, then build your theme and publish it to your blog (or copy the files directly to the location and restart the blog).

# Remote containers to the story

Before we jump into this, let me tell you what I was doing before Remote development on containers. I was actually already using containers with a customized set of gulp scripts. Here is a quick description of the steps it was running:

- Build the theme
- Copy it to a `.staging` directory
- Start a docker container with the database mounted to a `.data` and `.staging` mounted in the theme directory
- Watch for file changes, and repeat the step above.

The problem with that approach is that restarting the container and docker is slow :(. So that was definitely far from a fun dev experience.

# Remote containers to the rescue

Let's define the goals:

- I don't want ghost to be restarted.
- I want changes to be reflected as fast as possible.
- I still want to use a container though. I'm using a Macbook and a Surface book. I want to work easily on both.
- I want the install process to be as fast and simple as possible. Why? Because I still hope that one day @Mitch will help me, but if it takes more than 2 minutes to get started he will give up (he is a lazy bum).

To showcase what's next, I'll start from [the `London` theme](https://github.com/TryGhost/London).

## Configuring the container

Ghost already provides docker images, so we'll start from there. We will customize it as follow:

- Install Yarn so we can restore the theme dev dependencies
- Install `gscan` so we can validate our theme easily
- Configure `bash` as the default shell (who uses sh these days? zsh could be nice though)
- Define the URL environment variable for Ghost, so it will run nicely. In this instance we will user port `3001`.

`.devontainer/Dockerfile`:

```
FROM ghost

# Configure apt
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
   && apt-get -y install --no-install-recommends apt-utils 2>&1

# Verify git and process tools are installed
RUN apt-get install -y git procps

# Remove outdated yarn from /opt and install via package
# so it can be easily updated via apt-get upgrade yarn
RUN rm -rf /opt/yarn-* \
   && rm -f /usr/local/bin/yarn \
   && rm -f /usr/local/bin/yarnpkg \
   && apt-get install -y curl apt-transport-https lsb-release \
   && curl -sS https://dl.yarnpkg.com/$(lsb_release -is | tr '[:upper:]' '[:lower:]')/pubkey.gpg | apt-key add - 2>/dev/null \
   && echo "deb https://dl.yarnpkg.com/$(lsb_release -is | tr '[:upper:]' '[:lower:]')/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
   && apt-get update \
   && apt-get -y install --no-install-recommends yarn

RUN yarn global add gscan

# Clean up
RUN apt-get autoremove -y \
   && apt-get clean -y \
   && rm -rf /var/lib/apt/lists/*
ENV DEBIAN_FRONTEND=dialog

ENV SHELL /bin/bash

ENV url http://localhost:3001
```

## Visual Studio Code configuration

Visual Studio Code needs a `devcontainer.json` file to be able to understand what to do with you dockerfile. Its responsibility is to define options and to instruct the editor that the repo supports development in containers.

In this file, we will define:

- the `dockerFile`.
- the Visual Studio extension.
- the ports we want to expose or map. You can specify either just a number, in which case it will map the port from the container on the same port. Alternatively you can use the docker port mapping syntax.
- finally, we will define a command which runs just after VS Code and builds our container. In our case it will create a symlink between a .data directory and ghost's data folder, so we never loose our database and won't have to reconfigure Ghost. Finally, we will restore our theme dependencies using Yarn.

`.devontainer/devcontainer.json`:

```
{
    "dockerFile": "Dockerfile",
    "extensions": [],
    "appPort": [
        "3001:2368"
    ],
    "postCreateCommand": "ln -s /workspaces/geek-learning-io-casper/.data /var/lib/ghost/content/data && yarn install --production=false"
}
```

## Tweaking the gulp file

This step has nothing to do with Remote development and is only related to the ghost use case.

We will need to add two packages, `ps-list` and `@try-ghost/admin-api` which we will respectively use to find the current node running ghost and to upload the theme.

```
yarn add ps-list @tryghost/admin-api --dev --production=false
```

In `gulpfile.js` we will add the following imports:

```
const psList = require('ps-list');
const adminApiClient = require("@tryghost/admin-api");
const fs = require('fs');
const path = require('path');
```

Then we will replace the end section of the file with the following:

```
async function ghost() {
    var exec = require("child_process").exec;
    const processes = await psList();

    const ghostProcess = processes.filter(x => x.cmd == "/usr/local/bin/node current/index.js");

    if (ghostProcess.length) {
        process.kill(ghostProcess[0].pid)
    }

    exec(
        "node current/index.js",
        { cwd: process.env.GHOST_INSTALL, env: process.env, detached: true },
        function callback(error, stdout, stderr) {
        }
    );
};

async function deployThemeViaApi(done) {

    var targetDir = 'dist/';
    var themeName = require('./package.json').name;
    var filename = themeName + '.zip';

    const themePath = path.join(__dirname, targetDir, filename);

    const url = "http://localhost:2368";

    const client = new adminApiClient({
        url,
        key: fs.readFileSync(path.join(__dirname, '.token'), { encoding: 'utf8' }),
        version: "v2"
    });

    await client.themes.upload({ file: themePath });
};

const cssWatcher = () => watch('assets/css/**', css);
const hbsWatcher = () => watch(['*.hbs', 'partials/**/*.hbs', '!node_modules/**/*.hbs'], hbs);
const watcher = parallel(cssWatcher, hbsWatcher);
const build = series(css, js);
const dev = series(build, serve, watcher);

const zipBuild = series(build, zipper);

const dockerCssWatcher = () => watch('assets/css/**', series(zipBuild, deployThemeViaApi));
const dockerHbsWatcher = () => watch(['*.hbs', 'partials/**/*.hbs', '!node_modules/**/*.hbs'], series(zipBuild, deployThemeViaApi));
const dockerWatcher = parallel(dockerCssWatcher, dockerHbsWatcher);

const dockerDev = series(ghost, zipBuild, deployThemeViaApi, dockerWatcher);

exports.ghost = ghost;
exports.build = build;
exports.zip = zipBuild;
exports.dev = dev;
exports.default = dockerDev;
```

This will change the default gulp task to a task designed to build, zip and deploy the theme to the blog on changes.

## Updating the readme

![Ghost%20Theme%20Development%20Using%20Visual%20Studio%20Code%20R%202756aaf17c394579a5b419078e8089f1/aziz-acharki-gXndgCS-CGo-unsplash.jpg](Ghost%20Theme%20Development%20Using%20Visual%20Studio%20Code%20R%202756aaf17c394579a5b419078e8089f1/aziz-acharki-gXndgCS-CGo-unsplash.jpg)

Now we can upgrade the readme with the steps to get started, you'll notice that the longest part has to do we initializing ghost :) :

```
To develop on the theme we recommend that you use Visual Studio Code with the Remote development tools
* Install [VS Code](https://code.visualstudio.com/)
* Install [Remote Developement Extension Pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
* Clone this Repository (if not done already)
* Open it
* Hit `Ctrl/Command + Shift + P`, type Reopen
* `Reopen Folder in container` should appear, Select and Press enter
* Wait for the container to be build and start

If it's your first time, start ghost using yarn gulp ghost
* Open a browser on `https://localhost:3001` configure your blog and your account.
* In the admin UI head to `Integrations`
* Click on `Add Custom Integration` at the bottom of the page
* Choose a name, for example `Theme upload`
* Copy the admin API key
* at the root of the repo create a `.token` file and paste the api key inside the file. Save it.
* hit  `Ctrl/Command + C` to terminate the ghost command

To start developping:
* In the VS Code terminal
* run `yarn gulp`
```

# Conclusion

As you can see, we can streamline the experience in a pretty nice way thanks to these new VS Code plugins. Ideally there would be no manual steps and the blog would be initialized automatically.

Stay tuned for my next post on the same topic where we will use a compose file (multiple containers) and where I will share my struggles and solutions with the extension.