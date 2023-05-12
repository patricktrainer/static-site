# How to set up a custom domain for your homepage in Notion

Created: Jan 29, 2020 9:01 AM
Tags: How To
URL: https://medium.com/@TarasPyoneer/how-to-set-up-a-custom-domain-for-your-homepage-in-notion-53fa3d54f848

![1*gUv54okx1TF2BDd2rV3kmw.png](How%20to%20set%20up%20a%20custom%20domain%20for%20your%20homepage%20in%2047cee0c6913d45208fddd68a3cf998dd/1gUv54okx1TF2BDd2rV3kmw.png)

I love Notion. I use it for almost anything from planning my workouts to maintaining reading and movie lists with ratings. Even though Notion claims to be a great tool for taking notes, I think it is more of a private space or personal homepage. Being a member of the Notion Community on Facebook, it looks like that a lot of other people feel the same way. There you see people sharing some of their great takes on homepages and other things. I designed my homepage in Notion using some of the ideas from the group. I felt it would be cool to create my portfolio in Notion and connect it to my custom domain. Notion itself does not provide this function yet, according to their twitter we might see it someday:

Luckily I have found this [gist](https://gist.github.com/mayneyao/b9fefc9625b76f70488e5d8c2a99315d) from [mayneyao](https://gist.github.com/mayneyao). Even though I am a software engineer myself, I found it a bit hard to follow the instructions. Even though it worked out in the end, I thought that it might be quite difficult for someone else without a technical background. And this is why I decided to create a step by step guide on how to set up custom domains for Notion.

To follow this tutorial, you will need:

* Custom domain and access to the DNS settings * Page in Notion that should be your landing page * Account on [CloudFlare](https://www.cloudflare.com/)

Let’s start with the page itself. It does not matter which page you use, but it should be a public page. Enable the option of **Public Access**. If preferred, the switch **Allow Search Engines** can be enabled as well. Once you are finished, click on **Copy Page Link** and save the link for later use.

As far as I know, CloudFlare is used as a [CDN](https://en.wikipedia.org/wiki/Content_delivery_network) most of the times. It provides handy tools to deliver assets and it can also protect your page when it is under attack, like DDoS. In general, it grants you more control over your website or app. For our use case, we will make use of the **Workers** feature that will forward incoming requests from users to the public Notion page that we have created earlier. Let’s begin then.

First, you have to register on their [website](https://www.cloudflare.com/). Once registration is complete, add your domain by clicking on **Add site** at the top right. When it asks you to choose a plan, select the **Free** plan. After scrolling down, you should see this form:

Here, copy both fields **Nameserver 1** and **Nameserver 2** * *dom.ns.cloudflare.com* * *reza.ns.cloudflare.com*

> Make sure you copy the nameservers provided by CloudFlare, since they might differ!

For this post, I have purchased a cheap *.xyz* domain from *Namecheap*, but this provider is not mandatory. You can use any provider. Head to the settings to change the default nameservers. They are in the **DNS** settings of your domain provider. All you need to do here is to paste both nameservers that you have copied in *Step 2*. In this example using Namecheap, simply change the **Default DNS** select-box to **Custom DNS** and paste the nameservers one in each input field. Don’t forget to save the changes as well. From here, it might take a while for the changes to take place (in some cases up to 24 hours).

From here it becomes a little more tech-savvy. In this step, we will enter some code. Don’t worry, we will just **copy + paste** some code block and only make changes in two lines there. For the request to be forwarded to our Notion page, we need a proxy using a worker in CloudFlare. Head over to the **Workers** menu at the top and click on **Launch** **Editor**.

Then, click on **Add Scrip**t and name it something like *custom-domain-proxy*. On the left side of the editor, enter the following block of code:

You can leave most of the code as it is, except for the top 2 lines. Modify them using your domain in *your domain* and public Notion page in *start page url*. In my case, they look like this:*const MY_DOMAIN = “custom-domain.xyz”const START_PAGE = “[https://www.notion.so/tarassampleworkspace/Custom-Domain-xyz-a42e4c7466224475b7b15ee9cd41c317](https://www.notion.so/tarassampleworkspace/Custom-Domain-xyz-a42e4c7466224475b7b15ee9cd41c317)"*.

Click on **Save** and ignore the **Missing Route** warning for now if one pops up. The hard part is now finished and only one final step is missing, the routing. After saving, head back to the workers’ page.

In the final step, we need to tell the worker for which route(s) or URL the script should run. Just like before, instead of clicking on **Launch Editor**, click on **Add route** this time.

Here we set a rule for which routes the script should run. Simply set the route to *YOUR_DOMAIN/**. In this example, it’s *custom-domain.xyz/**. Then, select the script *custom-domain-proxy* which we saved in the previous step. The only thing we need to do now is to save the route and wait. This might take a few minutes or even hours to work. Just grab a cup of tea and come back later to see this success message in your Dashboard.

If everything went smoothly and the * Notion page is set to public * the nameservers on your domain provider were changed * CloufFlare successfully verified your domain

You should be able to see your public Notion page after entering your domain in the URL of your browser:

Each use-case is different. In my case, I just wanted to have my portfolio I had already created in Notion published. Whenever I make changes to it, it will immediately be updated. Hence, if you prioritize the mobile experience and fast loading times, this approach might not suit you since Notion pages aren’t that performant. Despite that, I hope Notion will launch a native feature for setting up custom domains.

*****Update from 25.10.2019***

After sharing the story at the Notion Facebook Group, I received some responses that should be mentioned here as well.

This workaround might only be useful in some cases. It perfectly suited mine, because I wanted a simple portfolio page that I can easily update.

If you plan to use it for something like a blog or anything else where you want to track user behaviour using Google Analytics, I would not recommend using this approach. It is not possible to embed any type of snippet that will work in the background.

— Feel free to ask me any questions, either here on Medium or my twitter [@TarasPyoneer](http://twitter.com/TarasPyoneer).