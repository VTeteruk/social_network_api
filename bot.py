import json
import uuid
import logging
import requests
import random

logging.basicConfig(level=logging.INFO)


class Bot:
    def __init__(
        self, number_of_users, max_posts_per_user, max_likes_per_user, base_url
    ) -> None:
        self.number_of_users = number_of_users
        self.max_posts_per_user = max_posts_per_user
        self.max_likes_per_user = max_likes_per_user
        self.users_with_tokens = {}
        self.base_url = base_url

    @staticmethod
    def random_user_name() -> str:
        return f"Username-{uuid.uuid4()}"

    def create_user(self, username: str) -> dict:
        user_data = {
            "username": username,
            "email": "test@test.com",
            "first_name": "test",
            "last_name": "test",
            "password": "123456",
        }
        response = requests.post(
            f"{self.base_url}/users/register/", json=user_data
        )
        status_code = response.status_code

        if status_code == 201:
            user = response.json()
            logging.info(f"User {user['id']} was created")
            return user
        raise Exception(f"status_code: {status_code}")

    def authorize_user(self, user) -> None:
        username = user["username"]
        user_data = {"username": username, "password": "123456"}
        response = requests.post(
            f"{self.base_url}/users/token/", json=user_data
        )
        self.users_with_tokens[user["id"]] = response.json()["access"]

        logging.info(f"User {user['id']} was authorized")

    def get_headers(self, user_id: int) -> dict:
        return {"Authorization": f"Bearer {self.users_with_tokens[user_id]}"}

    def create_posts(self, user_id: int) -> None:
        headers = self.get_headers(user_id=user_id)
        num_posts = random.randint(1, self.max_posts_per_user)
        for _ in range(num_posts):
            post_data = {"title": "Title", "description": "New Post"}
            response = requests.post(
                f"{self.base_url}/posts/", headers=headers, json=post_data
            )
            if response.status_code != 201:
                logging.info(f"Failed to create post for user {user_id}")
            logging.info(f"Post was created by user {user_id}")

    def get_paginated_posts_id(self) -> list[int]:
        logging.info("Extracting paginated posts...")

        user_id = list(self.users_with_tokens.keys())[0]  # To be authorized
        headers = self.get_headers(user_id=user_id)
        posts = []
        page = 1
        while True:
            response = requests.get(
                f"{self.base_url}/posts/?limit=10&offset={10 * page}",
                headers=headers,
            ).json()
            posts += [post["id"] for post in response["results"]]

            if not response["next"]:
                return posts
            page += 1

    def like_posts(self, user_id: int, posts: list[int]) -> None:
        headers = self.get_headers(user_id=user_id)
        num_likes = random.randint(1, self.max_likes_per_user)
        for _ in range(num_likes):
            post_id = random.choice(posts)
            response = requests.post(
                f"{self.base_url}/posts/{post_id}/like/", headers=headers
            )
            logging.info(
                f"User {user_id}"
                + response.json()["message"][3:]
                + f" {str(post_id)}"
            )

    def start_bot(self) -> None:
        for _ in range(self.number_of_users):
            user = self.create_user(self.random_user_name())
            if user.get("id"):
                self.authorize_user(user)
                self.create_posts(user["id"])
            else:
                logging.info("Failed to create user")
        posts = self.get_paginated_posts_id()
        for user_id in self.users_with_tokens.keys():
            self.like_posts(user_id, posts)

        logging.info("Bot execution complete.")


if __name__ == "__main__":
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    bot = Bot(
        config["number_of_users"],
        config["max_posts_per_user"],
        config["max_likes_per_user"],
        config["base_url"],
    )

    bot.start_bot()
