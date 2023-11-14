import inspect

from django.core.management.base import BaseCommand
from lazydocs import MarkdownGenerator
from lazydocs.generation import to_md_file

from engine import oai

SRC_BASE_URL = "https://github.com/LioQing/chat-composer/blob/main/engine/"
OUT_PATH = "./docs"
MODULES = [oai]


class Command(BaseCommand):
    """Generate docs for engine APIs."""

    help = "Generate docs for engine APIs."

    def handle(self, *args, **options):
        """Generate docs for engine APIs."""
        for doc_module in MODULES:
            doc_name = doc_module.__name__.split(".")[-1]
            generator = MarkdownGenerator(
                src_root_path="./engine",
                src_base_url=SRC_BASE_URL,
            )

            for name, module in filter(
                lambda x: inspect.ismodule(x[1]),
                inspect.getmembers(doc_module),
            ):
                to_md_file(
                    markdown_str=generator.module2md(module).replace(
                        "engine.", ""
                    ),
                    filename=f"{name}.md",
                    out_path=f"{OUT_PATH}/{doc_name}",
                )

            to_md_file(
                markdown_str=generator.overview2md()
                .replace("engine.", "")
                .replace(f"{doc_name}.", "")
                .replace("API Overview", f"`{doc_name}` Overview"),
                filename="README.md",
                out_path=f"{OUT_PATH}/{doc_name}",
            )
