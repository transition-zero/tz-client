from dotenv import load_dotenv
from tz.client.cli import auth, cli

__all__ = ["auth", "cli"]


def main():
    load_dotenv()
    cli.root()
