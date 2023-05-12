# Official Ghost + GitHub Integration

Created: Apr 23, 2020 2:28 PM
URL: https://ghost.org/integrations/github/

Set up simple continuous integration of your Ghost theme to deploy directly to your Ghost website with [GitHub Actions](https://github.com/features/actions). Share code snippets with [GitHub Gists](https://gist.github.com/).

## Use GitHub Actions to deploy your theme

GitHub Actions allow you to build simple automation on top of any repository, including running a build command on a theme and pushing the compiled zipfile to the Ghost Admin API.

In Ghost Admin, navigate to `Integrations` and create a new custom integration called **GitHub Actions**:

![Official%20Ghost%20+%20GitHub%20Integration%206ed6ffe4415a496bbc80774fa0e090b2/image-1.png](Official%20Ghost%20+%20GitHub%20Integration%206ed6ffe4415a496bbc80774fa0e090b2/image-1.png)

### Set your Ghost integration credentials in GitHub

Next, copy and paste your integration details into your GitHub repository's environment variables. You can find these under `Settings > Secrets`

![Official%20Ghost%20+%20GitHub%20Integration%206ed6ffe4415a496bbc80774fa0e090b2/image-2.png](Official%20Ghost%20+%20GitHub%20Integration%206ed6ffe4415a496bbc80774fa0e090b2/image-2.png)

Create one secret called `GHOST_ADMIN_API_URL` with the **API URL** from your custom integration, and another secret called `GHOST_ADMIN_API_KEY` with the **Admin API Key** from your custom integration.

Last step! Copy and paste the following code into a new file in your repository under `.github/workflows/main.yml` - this will automatically use the official [Ghost GitHub Action](https://github.com/marketplace/actions/deploy-ghost-theme) from GitHub's Marketplace:

```
name: Deploy Theme
on:
  push:	
    branches:	
      - master
jobs:
  deploy:
    runs-on: ubuntu-18.04
    steps:
      - uses: actions/checkout@master
      - uses: TryGhost/action-deploy-theme@v1.0.0
        with:
          api-url: ${{ secrets.GHOST_ADMIN_API_URL }}
          api-key: ${{ secrets.GHOST_ADMIN_API_KEY }}

```

Now, every time you push changes to your theme repository, your theme will automatically build and deploy to Ghost Admin.

Navigate to `Settings > Design` in Ghost Admin to make sure that the theme you're uploading from GitHub is the currently active theme, and you should be all set!

To see a working example take a look at our theme default [Casper](https://github.com/TryGhost/Casper), which uses GitHub Actions and the same [GitHub Workflow](https://github.com/TryGhost/Casper/blob/master/.github/workflows/deploy-theme.yml).

## Use Github Gists to share code snippets

[GitHub Gists](https://gist.github.com/) are a simple way of sharing code snippets with other developers. Once you've created a new public Gist, it will be available to be shared with others.

![Official%20Ghost%20+%20GitHub%20Integration%206ed6ffe4415a496bbc80774fa0e090b2/Creating-a-Gist.png](Official%20Ghost%20+%20GitHub%20Integration%206ed6ffe4415a496bbc80774fa0e090b2/Creating-a-Gist.png)

To share a Gist in Ghost, locate the embed option from the dropdown in the top navigation and copy the HTML embed code to your clipboard:

![Official%20Ghost%20+%20GitHub%20Integration%206ed6ffe4415a496bbc80774fa0e090b2/Gist-embed-code-1.png](Official%20Ghost%20+%20GitHub%20Integration%206ed6ffe4415a496bbc80774fa0e090b2/Gist-embed-code-1.png)

### Paste it into a HTML card in the editor

Create a new HTML block in the Ghost editor on the post you would like to embed your code snippet and paste in the embed code.

![Official%20Ghost%20+%20GitHub%20Integration%206ed6ffe4415a496bbc80774fa0e090b2/image-3.png](Official%20Ghost%20+%20GitHub%20Integration%206ed6ffe4415a496bbc80774fa0e090b2/image-3.png)

That's all there is to it! Ghost allows you to paste embed code directly into the HTML block to share a Gist code snippet with your readers.

This is the quickest way to embed a Gist in Ghost. If you're using the default theme, Casper, then this will look great without further styling. For other themes, you may want to make some styling adjustments in your theme.

Here's an example of the end result:

## Do more with Zapier

Power up your site even further using [Zapier](https://zapier.com/). If you're already using GitHub, then you might also like some of these complimentary automations: