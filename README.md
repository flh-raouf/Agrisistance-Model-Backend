<p align="center">
  <img src="https://res.cloudinary.com/dmbnrpayf/image/upload/v1726179947/Agrisistance/Agrisistance-Logo.png" width="85" alt="Agrisistance Logo" />
  <img />
  <img />
  <img />
  <img />
  <img src="https://static-00.iconduck.com/assets.00/flask-icon-1594x2048-84mjydzf.png" width="85" alt="Flask Logo" />
</p>



# 🌱 AGRISISTANCE

**A2SV-Agrisistance** is an AI-driven web application aimed at helping African farmers optimize land use and boost crop productivity. Utilizing advanced machine learning algorithms and data analytics, AGRISISTANCE offers actionable insights and personalized recommendations tailored to individual farming needs.

## Features

### Optimizing Land Use

- 🌿 Analyzes soil properties, weather conditions, and historical crop data.
- 🌾 Provides recommendations for optimal crop selection and planting schedules.

### Boosting Crop Productivity

- 💧 Personalized advice on irrigation, fertilization, and pest management.
- 📈 AI-driven insights to enhance crop yields.

### Business Planning

- 💼 Financial forecasts, market trends, and cost-benefit analyses.
- 🗺️ Strategic planning and decision-making support.

### Resource Management

- 💧 Monitors water usage and tracks seed and fertilizer inventory.
- 📊 Tools for efficient resource management.

### Networking and Industrial Connections

- 🌍 Connects farmers with related industries, such as delivery services and processing factories.
- 🔗 Streamlines supply chain processes and builds valuable industrial connections.

## Getting Started

Follow these steps to set up and run the AGRISISTANCE project locally:

### Prerequisites

Before you begin, ensure you have the following installed:

- [Python](https://www.python.org/): This project requires Python to run. Download and install it from [python.org](https://www.python.org/).

- [Git](https://git-scm.com/): You’ll need Git to clone the repository. Download and install it from [git-scm.com](https://git-scm.com/).
- [Docker](https://docker.com/): Docker is required to run the databases.

## Cloning the Repository

1. **Clone the repository**: Open your terminal or command prompt and run the following command:

    ```bash
    git clone https://github.com/flh-raouf/agrisistance-model-microservice.git
    ```

2. **Navigate to the project directory**:

    ```bash
    cd https://github.com/flh-raouf/agrisistance-model-microservice
    ```

## Installing Dependencies

1. **Install project dependencies**: Run the following command to install all the required npm packages:

    ```bash
    pip install -r requirements.txt
    ```

## Setting Up Environment Variables

1. **Create a `.env` file** in the root directory of the project with the following structure:

    ```plaintext
        POSTGRES_USER = ''
        POSTGRES_PASSWORD = ''
        POSTGRES_LAND_DB = 'agrisistance_land_db'
        DATABASE_LAND_URL='postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@127.0.0.1:5434/${POSTGRES_LAND_DB}?schema=public'

        API_TOKEN = ''
        API_URL = 'https://api.afro.fit/api_v2/api_wrapper/chat/completions'

    ```
2. **Explanation of Environment Variables**:

    - `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_LAND_DB` : Configuration for PostgreSQL databases.
    - `API_TOKEN` : OpenAI token
    

## Running the Application

1. **Start Docker Containers for Database**:

  - Ensure that Docker is running, either in the foreground or background, before proceeding. 

    - Start the land database container:
      ```bash
      docker compose up agrisistance-land-db -d
      ```

    By following these steps, your databases should be up and running. To verify that everything is working correctly, run the following command:
    
    ```bash
        docker ps
    ```

2. **Run Prisma Migrations for Each Database**:

    - Migrate the land database if you haven't done this step in the NestJS miroservices:
      ```bash
      prisma migrate dev --schema=./prisma/schema.land.prisma
      ```

3. **Generate Types for the Project**:

    - Generate types for the land service:
      ```bash
        prisma generate --schema=./prisma/schema.land.prisma
      ```

    

4. **Launch Databases with Prisma Studio**:

    - Open Prisma Studio for the user service:
      ```bash
      prisma studio --schema=./prisma/schema.land.prisma
      ```

5. **Run the Project Services**:

    - Start the service:
      ```bash
      uvicorn server:asgi_app --host 0.0.0.0 --port 8000 --reload
      ```
    Your project should now be running at `http://localhost:8000`.

6. **Run the NestJS Microservices**:

    - The NestJS microservices handles user authentication and other functionalities. You can find the repository [here](https://github.com/flh-raouf/agrisistance-microservice).


 ## Postman Documentation

   After running the server, you can use the Postman collection to test the available endpoints. The Postman documentation provides a detailed overview of all the requests you can make to interact with the API.

   - You can find the Postman documentation for this project [here](https://documenter.getpostman.com/view/32136798/2sAXqngkQA).

   Make sure the server is running at `http://localhost:9090` before testing the endpoints in Postman.
    

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](./LICENSE) file for more information.
