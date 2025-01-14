# python-compiler-service
A Python compiler service designed for seamless execution and integration.

## **Swagger Documentation**  
Access the API documentation with Swagger:  
- Development: [http://localhost:8000/docs](http://localhost:8000/docs)  
- Production: [http://localhost:8001/docs](http://localhost:8001/docs)  

## **Installation Guide**  

### **Requirements**  
- Python **3.13.1**  
- Docker (optional but recommended for sandbox environments)

### **Setup Instructions**  

#### **1. Clone the Project**  
```bash
git clone https://github.com/Silpakorn-Project/python-compiler-service.git
cd python-compiler-service
```

#### **2. Create a Virtual Environment**  
```bash
# Option 1: For Linux/macOS
python3 -m venv env

# Option 2: For Windows
python -m venv env
```

#### **3. Activate the Virtual Environment**  
```bash
# For Windows
env\Scripts\activate

# For macOS/Linux
source env/bin/activate
```

#### **4. Install Dependencies**  
```bash
pip install -r requirements.txt
```

---

## **Docker Sandbox Setup**  

### **1. Build the Python Sandbox Docker Image**  
```bash
docker build -t python-sandbox:latest -f Dockerfile.sandbox .
```

### **2. Run the Service with Docker Compose**  
If you have Docker installed, you can start the service using:  
```bash
docker-compose up --build
```

### **3. Running Without Docker Compose**  
For the sandbox functionality, ensure the Dockerfile is properly built and the image name is set to `python-sandbox`.  

---

## **Running the Service Locally**  

### **Development Mode**  
```bash
uvicorn app.main:app --reload
```

### **Production Mode**  
```bash
uvicorn app.main:app
```

---

## **File Structure**  

```plaintext
python-compiler-service/
├── app/
│   ├── main.py       # Entry point for the FastAPI application
│   └── ...           # Other application files
├── Dockerfile.sandbox # Dockerfile for the sandbox environment
├── requirements.txt   # Dependencies list
└── README.md          # Project documentation
```

---

## **Notes**  

1. Ensure the Docker image is built with the correct name (`python-sandbox`) before attempting to run the sandbox environment.  
2. For production, configure the application to use proper security settings and environment variables.  

---
