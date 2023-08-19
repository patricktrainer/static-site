from dataclasses import dataclass
from datetime import datetime
import markdown2


@dataclass
class Config:
    title: str
    description: str
    url: str
    in_path: str
    out_path: str


@dataclass
class Post:
    title: str
    date: datetime
    content: str

    def __post_init__(self):
        self.slug = self.title.lower().replace(" ", "-")

    def create(self):
        pass


# markdownPost implements the Post interface
class MarkdownPost(Post):
    def __init__(self, title: str, date: datetime, content: str):
        super().__init__(title, date, content)

    def create(self):
        pass

    


@dataclass
class Page:
    title: str
    slug: str
    posts: list[Post]

    def __post_init__(self):
        self.slug = self.title.lower().replace(" ", "-")

    def create(self):
        with open(self.slug + ".html", "w") as f:
            f.write("<h1>" + self.title + "</h1>")


@dataclass
class Site:
    config: Config
    pages: list[Page]

    def create(self):
        for page in self.pages:
            page.create()


    def add_page(self, page: Page):
        self.pages.append(page)

    def add_post(self, page: Page, post: Post):
        page.posts.append(post)

    def render(self):
        pass

    def publish(self):
        pass

    def serve(self, port: int = 8000):
        pass


class PostConverter:
    def __init__(self, config: Config, post: MarkdownPost):
        self.in_path = config.in_path
        self.out_path = config.out_path
        self.extras = [
            "fenced-code-blocks",
            "toc",
            "tables",
            "footnotes",
            "metadata",
        ]
        self.post = post
        self.extensions: dict[str, str] = {
            ".md": ".html",
            ".markdown": ".html",
        }

    def _convert(self):
        slug = self.post.slug + self.extensions[".md"]
        html: str = markdown2.markdown(
            text=self.post.content,
            extras=self.extras,
        )

        return (slug, html)
    
    def convert(self):
        slug, content = self._convert()
        with open(self.out_path + slug, "w") as f:
            f.write(content)
    

def main():
    config = Config(
        title="My Blog",
        description="A blog about stuff",
        url="https://example.com",
        in_path="posts/",
        out_path="out/",
    )
    site = Site(config=config, pages=[])
    page = Page(title="Home", slug="index", posts=[])
    site.add_page(page)
    post = MarkdownPost(
        title="My First Post",
        date=datetime.now(),
        content="This is my first post!",
    )
    site.add_post(page, post)


