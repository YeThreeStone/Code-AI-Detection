# Code-AI-Detection

## 环境配置

### 后端

**python3.8**

```
pip install dashscope

pip install requests langchain-community faiss-cpu python-dotenv
```

**FastAPI和Uvicorn**

```
pip install fastapi uvicorn python-multipart
```

### 前端

首先安装 **Nodejs**

```
# 安装 http-server
npm install -g http-server
```



## 项目启动

### 后端

```
cd backend 

uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 前端

```
cd frontend

http-server -c1 --cors
```



启动后访问 http://127.0.0.1:8080