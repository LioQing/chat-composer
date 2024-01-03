import inspect
import pathlib

from django.core.management.base import BaseCommand
from lazydocs import MarkdownGenerator
from lazydocs.generation import to_md_file

from engine.modules import composer, oai, vai

SRC_BASE_URL = "https://github.com/LioQing/chat-composer/blob/main/engine/"
OUT_PATH = "./docs"
MODULES = [oai, vai, composer]
INCLUDES = [
    "engine.modules.oai.api",
    "engine.modules.oai.enums",
    "engine.modules.oai.models",
    "engine.modules.vai.api",
    "engine.modules.vai.enums",
    "engine.modules.vai.models",
    "engine.modules.composer",
]


class Command(BaseCommand):
    """Generate docs for engine APIs."""

    help = "Generate docs for engine APIs."

    def handle(self, *args, **options):
        """Generate docs for engine APIs."""
        for doc_module in MODULES:
            doc_name = doc_module.__name__.split(".")[-1]
            self.generator = MarkdownGenerator(
                src_root_path="./engine/modules",
                src_base_url=SRC_BASE_URL,
            )

            # Create the directory for the docs if it doesn't exist
            pathlib.Path(f"{OUT_PATH}/{doc_name}").mkdir(
                parents=True, exist_ok=True
            )

            # Generate the doc for init
            self.gen_module(doc_name, "__init__", doc_module)

            # Generate the docs for each module
            for name, module in inspect.getmembers(
                doc_module, predicate=inspect.ismodule
            ):
                self.gen_module(doc_name, name, module)

            to_md_file(
                markdown_str=self.generator.overview2md()
                .replace("engine.modules.", "")
                .replace("#module-enginemodules", "#module-")
                .replace(f"{doc_name}.md#", "__init__.md#")
                .replace(f"{doc_name}.", "")
                .replace("API Overview", f"`{doc_name}` Overview"),
                filename="README.md",
                out_path=f"{OUT_PATH}/{doc_name}",
            )

    def gen_module(self, doc_name: str, name: str, module: object) -> bool:
        """Generate docs for a module."""
        if module.__name__ not in INCLUDES:
            return False

        try:
            to_md_file(
                markdown_str=self.generator.module2md(module).replace(
                    "engine.modules.", ""
                ),
                filename=f"{name}.md",
                out_path=f"{OUT_PATH}/{doc_name}",
            )
        except Exception as e:
            print(self.style.WARNING(f"Error generating docs for {name}: {e}"))
            return False

        return True
