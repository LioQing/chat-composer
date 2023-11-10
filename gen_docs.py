import inspect

from lazydocs import MarkdownGenerator
from lazydocs.generation import to_md_file

from engine import oai

SRC_BASE_URL = "https://github.com/LioQing/chat-composer/blob/main/engine/"
OUT_PATH = "./docs"


def main():
    """Generate docs for engine APIs."""
    doc_modules = [oai]
    md_str = "\n# API Overview\n\n"
    for doc_module in doc_modules:
        doc_name = doc_module.__name__.split(".")[-1]
        generator = MarkdownGenerator(
            src_root_path="./engine",
            src_base_url=SRC_BASE_URL,
        )

        for name, module in filter(
            lambda x: inspect.ismodule(x[1]), inspect.getmembers(doc_module)
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

        md_str += (
            f"- [{doc_name}](./{doc_name}/README.md): {doc_module.__doc__}\n"
        )

    to_md_file(
        markdown_str=md_str,
        filename="README.md",
        out_path=f"{OUT_PATH}",
    )


if __name__ == "__main__":
    main()
