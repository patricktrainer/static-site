# And voilà! - Jupyter Blog

Created: Dec 8, 2019 11:10 AM
Tags: Data
URL: https://blog.jupyter.org/and-voil%C3%A0-f6a2c08a4a93

**… from Jupyter notebooks to standalone applications and dashboards**

The goal of Project Jupyter is to improve the workflows of researchers, educators, scientists, and other practitioners of scientific computing, from the ***exploratory phase*** of their work to the ***communication*** of the results.

But interactive notebooks are not the best communication tool for all audiences. While they have proven invaluable to provide a *narrative* alongside the source, they are not ideal to address ***non-technical readers***, who may be put off by the presence of code cells, or the need to run the notebook to see the results. Finally, following the order as the code often results in the most interesting content to be at the ***end*** of the document.

Another challenge with sharing notebooks is the ***security*** model. How can we offer the interactivity of a notebook making use of e.g. Jupyter widgets without allowing arbitrary code execution by the end user?

We set ourselves to solve these challenges, and we are happy to announce the first release of ***voilà***.

![And%20voila%CC%80!%20-%20Jupyter%20Blog%208ed19583163142d78575b6e369b0c8e7/1c1xwFRqy99o8nLVxDSqNZg.png](And%20voila%CC%80!%20-%20Jupyter%20Blog%208ed19583163142d78575b6e369b0c8e7/1c1xwFRqy99o8nLVxDSqNZg.png)

![And%20voila%CC%80!%20-%20Jupyter%20Blog%208ed19583163142d78575b6e369b0c8e7/1c1xwFRqy99o8nLVxDSqNZg%201.png](And%20voila%CC%80!%20-%20Jupyter%20Blog%208ed19583163142d78575b6e369b0c8e7/1c1xwFRqy99o8nLVxDSqNZg%201.png)

***Voilà*** turns Jupyter notebooks into standalone web applications.

- Voilà supports ***Jupyter interactive widgets***, including the roundtrips to the kernel.
- Voilà ***does not permit arbitrary code execution*** by consumers of dashboards.
- Built upon Jupyter standard protocols and file formats, voilà works with any Jupyter kernel (C++, Python, Julia), making it a ***language-agnostic*** dashboarding system.
- Voilà is extensible. It includes a flexible ***template system*** to produce rich application layouts.

Voilà can be installed from pypi:

```
pip install voila
```

or conda-forge:

```
conda install voila -c conda-forge
```

Upon installation, several components are installed, one of which is the `voila` command-line utility. You can try it by typing `voila notebook.ipynb`. It results in the browser opening to a new tornado application showing markdown cells, rich outputs, and interactive widgets.

As you can see in the screencast, Jupyter interactive widgets remain fully functional even when they require computation by the kernel.

You can immediately try out some of the command-line options to voilà

- with `--strip_sources=False`, input cells will be included in the resulting web application (as read-only pygment snippets).
- with `--theme=dark`, voilà will make use of the dark JupyterLab theme, which will apply to code cells, widgets and all other visible components.

Note that code is only shown, voilà does not allow users to edit or execute arbitrary code.

The execution model of voilà is the following: upon connection to a notebook URL, voilà launches the kernel for that notebook, and runs all the cells as it populates the notebook model with the outputs.

After the execution, the associated kernel is not shut down. The notebook is converted to HTML and served to the user. The rendered HTML includes JavaScript that establishes a connection to the kernel. Jupyter interactive widgets referred in cell outputs are rendered and connected to their counterpart in the kernel. The kernel is only shut down when the user closes their browser tab.

> The current version of voilà only responds to the initial GET request when all the cells have finished running, which may take a long time, but there is ongoing work on enabling progressive rendering, which should make it into a release soon.

An important aspect of this execution model is that the front-end does not determine what code is run by the backend. In fact, unless specified otherwise (with option `--strip-sources=False`), the source of the rendered notebook does not even make it to the front-end. The instance of the `jupyter_server` instantiated by voilà actually disallows execute requests by default.

Voilà can render custom Jupyter widget libraries, including (but not limited to) [bqplot](https://github.com/bloomberg/bqplot), [ipyleafet](https://github.com/jupyter-widgets/ipyleaflet), [ipyvolume](https://github.com/maartenbreddels/ipyvolume), [ipympl](https://github.com/matplotlib/jupyter-matplotlib/), [ipysheet](https://github.com/QuantStack/ipysheet), [plotly](https://github.com/plotly/plotly.py), [ipywebrtc](https://github.com/maartenbreddels/ipywebrtc), etc.

Together with [ipympl](https://github.com/matplotlib/jupyter-matplotlib/), voilà is actually a simple means to render interactive matplotlib figures in a standalone web application:

Voilà can be used to produce applications with any Jupyter kernel. The following screencast shows how voilà can be used to produce a simple dashboard in C++ making use of leaflet.js maps, with the [xeus-cling](https://github.com/QuantStack/xeus-cling) C++ kernel and the [xleaflet](https://github.com/QuantStack/xleaflet) package.

We hope that voilà will be a stimulant to other languages (R, Julia, JVM/Java) to provide stronger widgets support.

The main extension point to voilà is the custom ***template system***. The HTML served to the end-user is produced from the notebook model by applying a Jinja template, which can be defined by the user.

An example template for voilà is the `voila-gridstack` template, which can be installed from pypi with

```
pip install voila-gridstack
```

You can try it by typing `voila notebook.ipynb --template=gridstack`.

The [gridstack voilà template](https://github.com/QuantStack/voila-gridstack/) makes use of the cell metadata to lay out the application.

> A roadmap item for the gridstack voilà template is to support the entire spec for the deprecated jupyter dashboards and to create a WYSIWYG editor for these templates in the form of a JupyterLab extension.

Note that [voila-gridstack](https://github.com/QuantStack/voila-gridstack/) template is still at an early stage of development.

A voilà template is actually a ***folder*** placed in the standard directory`PREFIX/share/jupyter/voila/templates` and which may include

- `nbconvert` templates (the jinja templates used to transform the notebook into HTML)
- `static` resources
- custom `tornado` templates such as `404.html` etc.

All of these are optional. It may also contain a `conf.json` file to set up which template to use as a base. The directory structure for a voilà template is the following:

```
PREFIX/share/jupyter/voila/templates/template_name/|├── conf.json                # Template configuration file├── nbconvert_templates/     # Custom nbconvert templates├── static/                  # Static directory└── templates/               # Custom tornado templates
```

The voilà template system can be used to completely override the behavior of the front-end. One can make use of modern JavaScript frameworks such as [React](https://reactjs.org/) or [Vue.js](https://vuejs.org/) to produce modern UI including Jupyter widgets and outputs.

Another example template for voilà is `voila-vuetify`, which is built upon vue.js:

*The voila-gridstack and voila-vuetify templates are still at an early stage of development, but will be iterated upon quickly in the next weeks as we are exploring templates.*

Beyond the `voila` command-line utility, the voilà package also include a Jupyter ***server extension***, so that voilà dashboards can be served alongside the Jupyter notebook application.

When voilà is installed, a running Jupyter server will serve the voilà web application under `BASE_URL/voila`.

From June 3rd to June 6th 2019, a [community workshop on dashboarding](https://blog.jupyter.org/jupyter-community-workshop-dashboarding-with-project-jupyter-b0e421bdf164) with Project Jupyter took place in Paris. Over thirty Jupyter contributors and community members gathered to discuss dashboarding technologies and hack together.

Several dashboarding solutions such as Dash and Panel were presented during the workshop and featured at the [PyData Paris Meetup](https://www.meetup.com/PyData-Paris/events/261452824/) which was organized on the same week.

The workshop was also the occasion for several contributors to start working on voilà. Custom templates, a dashboard gallery, logos and UX mockups for JupyterLab extensions have been developed.

We will soon publish a more detailed post on the workshop, detailing the many tracks of development that have been explored!

There is a lot of planned work around voilà in the next weeks and months. Current work streams include better ***integration with JupyterHub*** for publicly sharing dashboard between users, as well as ***JupyterLab extensions*** (a [voilà "preview" extension for notebooks](https://github.com/QuantStack/voila/pull/217), and a WYSIWYG editor for dashboard layouts). There are also ongoing discussions with the [OVH](https://www.ovh.com/fr/) cloud provider (which already supports binder by handling some of its traffic) on hosting a binder-like service dedicated to voilà dashboards. So stay tuned for more exciting developments!

Last but not least, we are especially excited about what ***you*** will be building upon voilà!

The development of voilà and related packages at [QuantStack](https://twitter.com/QuantStack) is sponsored by **[Bloomberg](http://www.techatbloomberg.com/)**.

We are also grateful to the attendees of the **[Jupyter Community Workshop on Dashboarding](https://blog.jupyter.org/jupyter-community-workshop-dashboarding-with-project-jupyter-b0e421bdf164)** for their numerous contributions to voilà!

We would like to thank [Chris Holdgraf](https://twitter.com/choldgraf) for his work on improving documentation, and integration with JupyterHub.

We should mention [Yuvi Panda](https://twitter.com/yuvipanda) and [Pascal Bugnion](https://twitter.com/pascalbugnion) for getting the `voila-gallery`project off the ground during the workshop. We are grateful to [Zach Sailer](https://twitter.com/zrsailer) for his continued work on improving`jupyter_server`. We should finally not forget to mention the prior art by [Pascal Bugnion](https://twitter.com/pascalbugnion) with the Jupyter widgets server which was also an inspiration for voilà.

*[Sylvain Corlay](https://twitter.com/SylvainCorlay)* is the founder and CEO of [QuantStack](https://github.com/QuantStack/) and a core team member for Project Jupyter.

[Maarten Breddels](https://twitter.com/maartenbreddels) is an independent scientific software developer partnering with [QuantStack](https://github.com/QuantStack/) on numerous projects, and a core developer of Project Jupyter.