import multiprocessing
import os



name = "Gunicorn config FastAPI"

accesslog = "/home/klinika/Documents/Server/klinika/gunicorn-access.log"
errorlog = "/home/klinika/Documents/Server/klinika/gunicorn-error.log"

bind = "192.168.0.132:8000"

worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count() * 2 + 1
worker_connections = 1024
backlog = 2048
max_requests = 5120
timeout = 120
keepalive = 2

debug = True
reload = debug
preload_app = False
daemon = False
