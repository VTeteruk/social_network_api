# Social Network API
The Social Network API project is a web-based application developed using Django and Django Rest Framework (DRF). It offers a RESTful API for user account management, post interactions, liking posts, and monitoring user activity.
___
# Features
* Liking System: Users can like and unlike posts.
* User Registration & Authentication: Users can register and authenticate to use the platform.
* User Profile: Users have profiles that can be updated and managed.
* Post Creation and Retrieval: Users can create posts, and posts can be retrieved.
* API Documentation: Detailed documentation of all API endpoints.
___
# How to Run
You must have installed:
1. Python 3
2. Docker

To get the project up and running, follow these steps:
1. Create venv ```python -m venv venv``` & activate it ```venv\Scripts\activate.bat```
2. Rename the [.env.sample](.env_sample) file to ``.env`` and provide the required environment variables.
3. Run the following command to build and start the project using Docker:
```
    docker-compose up --build
```
___
# API Documentation
You can access the API documentation by visiting the following URL:
[API Documentation](http://127.0.0.1:8000/api/schema/swagger/)
___
# How to Use the Bot
1. Run the server.
2. Execute the [bot.py](bot.py) script to interact with the API using a bot. You can customize the bot's behavior by modifying the [config.json](config.json) file.
