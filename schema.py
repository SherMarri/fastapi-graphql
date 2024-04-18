# schema.py

from tartiflette_asgi import TartifletteApp
from tartiflette import Resolver

# Define the GraphQL schema using SDL (Schema Definition Language)
schema_sdl = """
type Book {
    id: ID!
    title: String!
    author: String!
}

type Query {
    allBooks: [Book!]!
    bookById(id: ID!): Book
}

type Mutation {
    createBook(title: String!, author: String!): Book!
    updateBook(id: ID!, title: String, author: String): Book
}
"""

dummy_books = {
    "1": {"id": "1", "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    "2": {"id": "2", "title": "Don Quixote", "author": "Miguel de Cervantes"},
    "3": {"id": "3", "title": "Nineteen Eighty-Four", "author": "George Orwell"},
    "4": {"id": "4", "title": "The Catcher in the Rye", "author": "A. D. Salinger"},
}


# Define the resolvers for the schema
@Resolver("Query.allBooks")
async def resolver_all_books(parent, args, ctx, info):
    return list(dummy_books.values())


@Resolver("Query.bookById")
async def resolver_book_by_id(parent, args, ctx, info):
    return dummy_books.get(args["id"])


@Resolver("Mutation.createBook")
async def resolver_create_book(parent, args, ctx, info):
    new_id = str(len(dummy_books) + 1)
    new_book = {"id": new_id, "title": args["title"], "author": args["author"]}
    dummy_books[new_id] = new_book
    return new_book


@Resolver("Mutation.updateBook")
async def resolver_update_book(parent, args, ctx, info):
    book_id = args["id"]
    if book_id not in dummy_books:
        return None
    updated_book = dummy_books[book_id]
    if "title" in args:
        updated_book["title"] = args["title"]
    if "author" in args:
        updated_book["author"] = args["author"]
    return updated_book


# Create the Tartiflette app
tartiflette_app = TartifletteApp(sdl=schema_sdl)
