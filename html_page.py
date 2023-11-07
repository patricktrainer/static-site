import os
from jinja2 import Template
from markdown2 import Markdown


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
                    <a href="https://github.com/patricktrainer">GitHub</a> 
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
    html = render(template, title=title, content=content, stylesheet=stylesheet())

    return html

def render(template, **kwargs):
    template = get_tempalate()
    html = template.render(**kwargs)
    return html




def html_list(items):
    html = """
    <ul>
    """
    for item in items:
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
    water = '''<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/dark.css"/>'''
    gh = '''<link rel="stylesheet" href="https://unpkg.com/github-syntax-dark@latest/lib/github-dark.css"/>'''
    return f'''
    {water}
    {gh}
    '''


def get_posts(dir):
    posts = []
    for file in os.listdir(dir):
        if file.endswith(".md"):
            posts.append(os.path.join(dir, file))
    return posts


def get_post_title(file):
    # strip .md from file name
    # use os.path.splitext to handle file extensions
    return os.path.splitext(os.path.basename(file))[0]


def _md_to_html(body):

    markdowner = Markdown(html4tags=True, extras=["fenced-code-blocks", "tables", 'target-blank-links',
                                                  'cuddled-lists', 'code-friendly', 'footnotes', 'metadata',
                                                   'task_list', 'mermaid' ])
    return markdowner.convert(body)



def md_to_html(file):
    with open(file, "r") as f:
        md = f.read()
    return _md_to_html(md)


def main():
    posts = get_posts("./posts")

    # write new html files for each post in blog directory
    for post in posts:
        title = get_post_title(post)
        content = md_to_html(post)
        html = html_page(title, content)
        with open(f"./blog/{title}.html", "w") as f:
            f.write(html)

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
