"""Main module for the pipeline."""

import sys

import pipeline


def main():
    """Main function for the pipeline."""
    user_message = sys.argv[1]
    response = pipeline.run(user_message)
    print(response)


if __name__ == "__main__":
    main()
