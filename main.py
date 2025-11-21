import sys
import argparse
import asyncio
from extractor.extractor import GitHubExtractor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="GitHub username to extract")
    args = parser.parse_args()

    async def wrapper():
        extractor = GitHubExtractor()
        result = await extractor.extract(args.username)
        print(result)

    asyncio.run(wrapper())


if __name__ == "__main__":
    main()

# python3 main.py markush0f

