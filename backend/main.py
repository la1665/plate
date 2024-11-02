from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
from twisted.internet import reactor
import threading
import json
import uvicorn
from contextlib import asynccontextmanager
import time
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import socketio
from fastapi.staticfiles import StaticFiles

from lifespan import lifespan
from tcp_connection.TCPClient import connect_to_server, send_command_to_server, sio
from tcp_connection.router import tcp_router, tcp_factories, tcp_factory_lock
from authentication.routers import auth_router
from user.routers import admin_router
from building_gate.router import building_router, gate_router
from camera.settings_router import settings_router as camera_setting_router
from camera.cameras_router import camera_router
from client.router import lpr_router, client_router

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, tags=["Auth"])
app.include_router(admin_router, tags=["User"])
app.include_router(building_router, tags=["Buildings"])
app.include_router(gate_router, tags=["Gates"])
app.include_router(camera_setting_router, tags=["Camera Settings"])
app.include_router(camera_router, tags=["Cameras"])
app.include_router(lpr_router, tags=["LPRs"])
app.include_router(client_router, tags=["Clients"])
app.include_router(tcp_router, tags=["tcp"])

#app.mount("/", socketio.ASGIApp(sio))
app_socket = socketio.ASGIApp(
    sio,
    other_asgi_app=app,
    socketio_path="/socket.io"
)


# def main():
#     """
#     Main entry point for running the FastAPI app.
#     """
#     uvicorn.run("main:app_socket", host="0.0.0.0", port=8000, reload=True)


# if __name__ == "__main__":
#     main()
