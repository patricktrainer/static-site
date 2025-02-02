import argparse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader


@dataclass
class Post:
    title: str
    date: datetime
    content: str
    url: str


class PostLoader:
    def __init__(self, posts_dir: Path):
        self.posts_dir = Path(posts_dir)

    def load_posts(self):
        posts = []
        for filepath in self.posts_dir.glob("*.md"):
            try:
                post = self._parse_markdown_file(filepath)
                posts.append(post)
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
        # Sort posts by date (newest first)
        return sorted(posts, key=lambda p: p.date, reverse=True)

    def _parse_markdown_file(self, filepath: Path) -> Post:
        """
        Parse a Markdown file and return a Post object.
        Expects the Markdown file to have 'title' and 'date' metadata.
        """
        with filepath.open("r", encoding="utf-8") as file:
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
        try:
            title = md.Meta["title"][0]
            date = datetime.strptime(md.Meta["date"][0], "%Y-%m-%d")
        except KeyError as e:
            raise ValueError(f"Missing metadata in {filepath}: {e}")

        # Use the stem of the filename as the URL (e.g., "post1.md" -> "post1.html")
        url = f"{filepath.stem}.html"
        return Post(title, date, html_content, url)


class Renderer:
    def __init__(self, template_dir: Path, output_dir: Path):
        self.env = Environment(loader=FileSystemLoader(str(template_dir)))
        self.output_dir = Path(output_dir)

    def render_index(self, posts):
        template = self.env.get_template("index.html")
        output_path = self.output_dir / "index.html"
        self._render_template(template, output_path, posts=posts)

    def render_post(self, post: Post):
        template = self.env.get_template("post.html")
        output_path = self.output_dir / post.url
        self._render_template(template, output_path, post=post)

    def _render_template(self, template, output_path: Path, **context):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as f:
            f.write(template.render(**context))


class SiteGenerator:
    def __init__(self, posts_dir, template_dir, output_dir):
        self.posts_dir = Path(posts_dir)
        self.template_dir = Path(template_dir)
        self.output_dir = Path(output_dir)
        self.post_loader = PostLoader(self.posts_dir)
        self.renderer = Renderer(self.template_dir, self.output_dir)

    def generate_site(self):
        posts = self.post_loader.load_posts()
        self.renderer.render_index(posts)
        for post in posts:
            self.renderer.render_post(post)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a static site from Markdown posts."
    )
    parser.add_argument(
        "--posts", default="posts", help="Directory containing Markdown posts"
    )
    parser.add_argument(
        "--templates", default="templates", help="Directory containing Jinja2 templates"
    )
    parser.add_argument(
        "--output", default="output", help="Directory to output the generated site"
    )
    args = parser.parse_args()

    generator = SiteGenerator(args.posts, args.templates, args.output)
    generator.generate_site()
