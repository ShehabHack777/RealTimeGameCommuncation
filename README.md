# MyProject

This project is designed to provide real-time chat functionality and a leaderboard service. Follow the steps below to set up and run the project.

## Prerequisites

- Python 3.6 or higher installed
- Pip package manager installed

## Installation

1. Clone the repository to your local machine.
2. Navigate to the project directory.

## Setup

1. Create a virtual environment using the following command:

   ```
   python -m venv venv
   ```

2. Activate the virtual environment:

   - For Windows:

     ```
     venv\Scripts\activate.bat
     ```

   - For macOS and Linux:

     ```
     source venv/bin/activate
     ```

3. Install the required packages by running the following command:

   ```
   pip install -r requirements.txt
   ```

## Running the Project

1. Start the server by running the following command:

   ```
   uvicorn main:app --reload
   ```

2. Open Postman and make the following requests:

   - To test the real-time chat functionality, open a WebSocket connection to `ws://localhost:8000/chat`.
   - To verify the real-time leaderboard service, open a WebSocket connection to `ws://localhost:8000/ws`.
   - To see the real-time leaderboard without reloading the WebSocket endpoint, make a GET request to `http://localhost:8000/top_players/`.

3. Additionally, access the following URLs in your web browser:

   - To view the real-time chat running: `http://localhost:8000/chat` (open in Postman).
   - To view the real-time leaderboard: `http://localhost:8000/top_players/`.

That's it! You should now be able to test and explore the real-time chat and leaderboard functionality of the project.
