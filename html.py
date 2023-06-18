import hashlib
import os
from jinja2 import Template
import markdown


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


def _md_to_html(body):
    # create a unique hash for the body content
    body_hash = hashlib.sha256(body.encode()).hexdigest()

    # use the hash as a filename
    cache_file = f"./cache/{body_hash}.html"

    # check if the file exists
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return f.read()

    # if it doesn't, convert it
    html = markdown.markdown(body)
    return html
    

def md_to_html(file):
    with open(file, "r") as f:
        md = f.read()
    return _md_to_html(md)


def main():
    posts = get_posts("./posts")

    # strip .md from post names, convert them to HTML, and create links
    html_posts = []
    for post in posts:
        html_content = md_to_html(post)  # convert the Markdown to HTML
        post_name = get_post_title(post)
        post_link = html_link(f"{post_name}.html", post_name)

        # Save the HTML to a new .html file
        with open(f"./blog/{post_name}.html", "w") as f:
            f.write(html_page(post_name, html_content))

        html_posts.append(post_link)

    content = html_list(html_posts)
    html = html_page("Blog", content)
    with open("./index.html", "w") as f:
        f.write(html)

if __name__ == "__main__":
    main()
