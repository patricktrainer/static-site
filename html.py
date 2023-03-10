import os
import httpx


def html_header(title):
    return f'''
    <!DOCTYPE html>
    <html>
        <head>
        <title>{title}</title>
        {stylesheet()}
        </head>
    <body>
    '''


def html_footer():
    return """
    </body>
    </html>
    """


def html_table(cols, data):
    html = f"""
    <table>
    <tr>
    {"".join([f"<th>{col}</th>" for col in cols])}
    </tr>
    """
    for row in data:
        html += f"""
        <tr>
        {"".join([f"<td>{col}</td>" for col in row])}
        </tr>
        """
    html += """
    </table>
    """
    return html


def html_page(title, content):
    return html_header(title) + content + html_footer()


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
    return """
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/dark.min.css"/>
    <link rel="stylesheet" href="https://unpkg.com/github-syntax-dark@latest/lib/github-dark.css"/>
    """


def html_style_css(style):
    return f"""<style type="text/css">{style}</style>"""


def get_posts(dir):
    posts = []
    for file in os.listdir(dir):
        if file.endswith(".md"):
            posts.append(os.path.join(dir, file))
    return posts


def get_post_title(file):
    # strip .md from file name
    return os.path.basename(file).replace(".md", "")


def github_md_to_html(body):
    response = httpx.post(
        "https://api.github.com/markdown",
        json={"text": body, "mode": "gfm"},
        headers={"Accept": "application/vnd.github+json"},
    )
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Error: {response.status_code} {response.text}")
    

def md_to_html(file):
    with open(file, "r") as f:
        md = f.read()
    return github_md_to_html(md)


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
    html_link(f"{post.replace('.md', '.html')}", get_post_title(post)) for post in posts
]
blog_path = [b.replace("static-site/posts", "blog") for b in post_links]
content = html_list(blog_path)
html = html_page("Blog", content)
with open("./index.html", "w") as f:
    f.write(html)
