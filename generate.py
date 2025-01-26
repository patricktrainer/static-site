import os
from jinja2 import Environment, FileSystemLoader
import markdown
from datetime import datetime


class Post:
    def __init__(self, title, date, content, url):
        self.title = title
        self.date = date
        self.content = content
        self.url = url


class PostLoader:
    def __init__(self, posts_dir):
        self.posts_dir = posts_dir

    def load_posts(self):
        posts = []
        for filename in os.listdir(self.posts_dir):
            if filename.endswith(".md"):
                post = self._parse_markdown_file(
                    os.path.join(self.posts_dir, filename)
                )
                posts.append(post)
        return sorted(posts, key=lambda x: x.date, reverse=True)
    
    def _parse_markdown_file(self, filepath):
        with open(filepath, "r") as file:
            content = file.read()
            md = markdown.Markdown(
                extensions=[
                    "meta",
                    "extra",
                    "nl2br",
                    "tables",
                    "markdown_checklist.extension",
                ]
            )
            html_content = md.convert(content)
            title = md.Meta["title"][0]
            date = datetime.strptime(md.Meta["date"][0], "%Y-%m-%d")
            url = f"{os.path.basename(filepath)[:-3]}.html"
            return Post(title, date, html_content, url)


class Renderer:
    def __init__(self, template_dir, output_dir):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.output_dir = output_dir

    def render_index(self, posts):
        template = self.env.get_template("index.html")
        output_path = os.path.join(self.output_dir, "index.html")
        self._render_template(template, output_path, posts=posts)

    def render_post(self, post):
        template = self.env.get_template("post.html")
        output_path = os.path.join(self.output_dir, post.url)
        self._render_template(template, output_path, post=post)

    def _render_template(self, template, output_path, **context):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write(template.render(**context))


class SiteGenerator:
    def __init__(self, posts_dir, template_dir, output_dir):
        self.posts_dir = posts_dir
        self.template_dir = template_dir
        self.output_dir = output_dir
        self.post_loader = PostLoader(posts_dir)
        self.renderer = Renderer(template_dir, output_dir)

    def generate_site(self):
        posts = self.post_loader.load_posts()
        self.renderer.render_index(posts)
        for post in posts:
            self.renderer.render_post(post)


if __name__ == "__main__":
    posts_dir = "posts"
    template_dir = "templates"
    output_dir = "output"
    generator = SiteGenerator(posts_dir, template_dir, output_dir)
    generator.generate_site()
