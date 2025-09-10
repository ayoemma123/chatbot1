# 🏡 HomeInterior Chatbot 🤖

A machine learning powered chatbot built with **Django**, **React**, and **SVM (Support Vector Machine)** for intent classification.  
This chatbot helps users interact seamlessly while storing chat logs, handling unknown queries, and providing intelligent responses.

---

## 🚀 Features
- ✅ Intent classification using **SVM + TF-IDF**  
- ✅ REST API built with **Django REST Framework**  
- ✅ React frontend integration  
- ✅ Amazon RDS (**MySQL**) backend  
- ✅ Fallback responses for unknown queries  
- ✅ Chat logs stored in database  
- ✅ **Dockerized backend** for easy deployment  

---

## 🛠️ Tech Stack
- **Backend:** Django, Django REST API  
- **Frontend:** React  
- **Database:** MySQL (Amazon RDS)  
- **ML/NLP:** Scikit-learn (SVM, TF-IDF)  
- **Deployment:** Docker, GitHub  

---

## ⚙️ Installation & Setup (Without Docker)

### 1. Clone the repo
```bash
git clone https://github.com/technotrendng/homeinterior-chatbox.git
cd homeinterior-chatbox
```

### 2. Create a virtual environment & install dependencies
```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows

pip install -r requirements.txt
```

### 3. Apply migrations & run server
```bash
python manage.py migrate
python manage.py runserver
```

Backend will be available at → [http://localhost:8000](http://localhost:8000)

---

## 🐳 Dockerization (Backend)

Run the Django backend in a Docker container for easier deployment and portability.

### 1. Create a `Dockerfile`
```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
```

---

### 2. Create a `docker-compose.yml`
```yaml
version: '3.9'

services:
  web:
    build: .
    container_name: chatbot_backend
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: mysql:8.0
    container_name: chatbot_db
    restart: always
    environment:
      MYSQL_DATABASE: chatbot
      MYSQL_USER: chatbot_user
      MYSQL_PASSWORD: chatbot_pass
      MYSQL_ROOT_PASSWORD: rootpass
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql

volumes:
  db_data:
```

---

### 3. Run with Docker
```bash
# Build and start containers
docker-compose up --build

# Stop containers
docker-compose down
```

---

### 4. Access the app
- Django API → [http://localhost:8000](http://localhost:8000)  
- MySQL → available on port `3306`  

---

## 📂 Project Structure
```
homeinterior-chatbox/
│── backend/              # Django project
│   ├── chatbot/          # Chatbot ML logic (SVM, TF-IDF)
│   ├── api/              # Django REST API
│   └── manage.py
│
│── frontend/             # React frontend
│
│── requirements.txt      # Python dependencies
│── docker-compose.yml    # Docker setup
│── Dockerfile            # Backend Dockerfile
│── README.md             # Project documentation
```

---

## 🚀 Future Improvements
- Add **support for multiple languages**  
- Deploy with **Gunicorn + Nginx** in production  
- Improve ML model accuracy with **transformers (BERT/DistilBERT)**  
- Add **admin dashboard for chat analytics**  

---

## 📜 License
This project is licensed under the **MIT License** – free to use and modify.  
