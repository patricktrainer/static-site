import hashlib
import os
import requests
from jinja2 import Template


def get_tempalate():
    template = Template(
        """
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width">
            <title>{{ title }}</title>
            
            {{ stylesheet }}
        </head>
        <body>
            <header>
                <nav>
                    <a href="https://patricktrainer.github.io/static-site">Home</a> /
                    <a href="https://github.com/patricktrainer">GitHub</a> / 
                </nav>
            </header>
            {{ content }}
        </body>
    </html>
    """
    )

    return template


def html_footer():
    return """
    </body>
    </html>
    """


def html_elements(tag, elements):
    return "".join([f"<{tag}>{el}</{tag}>" for el in elements])


def html_table(cols, data):
    html = f"""
    <table>
    <tr>
    {html_elements('th', cols)}
    </tr>
    """
    for row in data:
        html += f"""
        <tr>
        {html_elements('td', row)}
        </tr>
        """
    html += "</table>"
    return html


def html_page(title, content):
    """Return a string containing the full HTML page."""
    template = get_tempalate()
    html = template.render(title=title, stylesheet=stylesheet(), content=content)

    return html


def html_list(items):
    html = """
    <ul>
    """
    for item in items:
        item = item.rsplit(None, 1)[0] 
        html += f"""
        <li>{item}</li>
        """
    html += """
    </ul>
    """
    return html


def html_link(url, text):
    return f"""<a href="{url}">{text.replace("-", " ")}</a>"""


def stylesheet():
    return """
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/open-fonts@1.1.1/fonts/inter.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@exampledev/new.css@1.1.2/new.min.css">
    <link rel="stylesheet" href="https://unpkg.com/github-syntax-dark@latest/lib/github-dark.css"/>
    """


def get_posts(dir):
    posts = []
    for file in os.listdir(dir):
        if file.endswith(".md"):
            posts.append(os.path.join(dir, file))
    return posts


def get_post_title(file):
    # strip .md from file name
    # use os.path.splitext to handle file extensions
    title = os.path.splitext(os.path.basename(file))[0]
    print(title)
    return title


def github_md_to_html(body):
    # create a unique hash for the body content
    body_hash = hashlib.sha256(body.encode()).hexdigest()

    # use the hash as a filename
    cache_file = f"./cache/{body_hash}.html"

    # check if the file exists
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return f.read()

    # if it doesn't, make a request to the API
    response = requests.post(
        "https://api.github.com/markdown",
        json={"text": body},
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + os.environ["GITHUB_TOKEN"],
        },
    )
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Error: {response.status_code} {response.text}")


def md_to_html(file):
    with open(file, "r") as f:
        md = f.read()
    return github_md_to_html(md)


def main():
    posts = get_posts("./posts")

    # write new html files for each post in blog directory
    # for post in posts:
    #     title = get_post_title(post)
    #     content = md_to_html(post)
    #     html = html_page(title, content)
    #     with open(f"./blog/{title}.html", "w") as f:
    #         f.write(html)

    # strip .md from post names and create links
    post_links = [
        html_link(f"{post.replace('.md', '.html')}", get_post_title(post))
        for post in posts
    ]
    blog_path = [b.replace("posts", "blog") for b in post_links]
    content = html_list(blog_path)
    html = html_page("Blog", content)
    with open("./index.html", "w") as f:
        f.write(html)


if __name__ == "__main__":

    main()
