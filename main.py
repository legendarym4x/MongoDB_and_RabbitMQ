from typing import List

import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_author(author: str):
    print(f'Find quotes by {author}')
    authors = Author.objects(fullname__iregex=author)
    result = []
    for a in authors:
        quotes = Quote.objects(author=a)
        result.extend([q.quote for q in quotes])
    return result


@cache
def find_by_tag(tag: str) -> list[str | None]:
    print(f'Find quotes by {tag}')
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_tags(tags: List[str]) -> List[str | None]:
    print(f'Find quotes by {tags}')
    quotes = Quote.objects(tags__in=tags)
    result = [q.quote for q in quotes]
    return result


if __name__ == '__main__':
    # print(find_by_tags(['li', 'mi']))
    while True:
        user_input = input("Enter command: ")
        if ':' in user_input:
            command, value = user_input.split(':', maxsplit=1)
        else:
            command, value = user_input, ''

        if command == 'name':
            result = find_by_author(value.strip())
        elif command == 'tag':
            result = find_by_tag(value.strip())
        elif command == 'tags':
            tags = [tag.strip() for tag in value.split(',')]
            result = find_by_tags(tags)
        elif command == 'exit':
            print("Exiting the script.")
            break
        else:
            print("Unknown command. Try again.")
            continue

        if result:
            print("Results: ")
            for quote in result:
                print(quote)
        else:
            print("No results found.")
