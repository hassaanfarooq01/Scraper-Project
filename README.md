# Django Amazon Brand Scraper

## Features
- **Django Admin Interface**: Manage brands and view scraped products directly from the admin interface.
- **Asynchronous Scraping**: Uses Celery with Redis as a message broker to handle product scraping asynchronously.
- **Dockerized Environment**: Entire setup is containerized using Docker, simplifying deployment and scaling.
- **Scheduled Scraping**: Celery Beat triggers scraping at regular intervals for all registered brands.

## Technologies Used
- **Backend**: Django, Django REST Framework, Celery
- **Database**: PostgreSQL
- **Message Broker**: Redis
- **Scraping**: Selenium with BeautifulSoup
- **Containerization**: Docker, Docker Compose

---

## Setup and Installation

### Prerequisites
- **Docker**
- **Docker Compose**

### Step-by-Step Setup

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/hassaanfarooq01/yourproject.git
    cd yourproject
    ```

2. **Set Up Environment Variables:**
    - Create a `.env` file in the root directory and configure the following variables:

      ```dotenv
      SQL_ENGINE=django.db.backends.postgresql
      SQL_DATABASE=postgres
      SQL_USER=postgres
      SQL_PASSWORD=postgres
      SQL_HOST=db
      SQL_PORT=5432
      ```

3. **Build and Run the Docker Containers:**
    ```bash
    docker-compose up --build
    ```

4. **Create a Superuser:**
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

5. **Access the Application:**
    - **Django Admin Panel**: [http://localhost:8005/admin](http://localhost:8005/admin)
    - **API or Web Interface**: [http://localhost:8005](http://localhost:8005)

---

## Running the Application
To start all services (web, database, Redis, Celery worker, Celery beat):
```bash
docker-compose up
