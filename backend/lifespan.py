import asyncio
import threading
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
from twisted.internet import reactor
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from db.engine import engine, Base, async_session
from utils.utils import create_default_admin
from tcp_connection.TCPClient import connect_to_server, send_command_to_server, sio
from tcp_connection.router import tcp_factories, tcp_factory_lock
from tcp_connection.manager import connection_manager
from client.models import LPR, Client


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[INFO] Starting lifespan")
    # Initialize database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("[INFO] Database tables created")

    # Create default admin user
    async with async_session() as session:
        await create_default_admin(session)

    print("[INFO] Default admin user created")
    # Initialize TCP clients for all LPRs
    global tcp_factories


    async def initialize_tcp_clients():
        """
        Initialize a TCP client for each server and store the factory.
        """
        # global tcp_factories
        # Get the current asyncio loop
        loop = asyncio.get_running_loop()
        # async def setup_lpr_clients():
        async with async_session() as session:
            result = await session.execute(select(Client))
            clients = result.scalars().all()

        for client in clients:
            # with tcp_factory_lock:
                factory = connect_to_server(client.ip, client.port, client.auth_token, loop)
                await connection_manager.add_connection(client.id, factory)
                # tcp_factories[lpr.id] = factory
        # asyncio.run(setup_lpr_clients())

    # Initialize connections to all servers
    await initialize_tcp_clients()
    # Start the Twisted reactor in a separate thread
    def start_reactor():
        reactor.run(installSignalHandlers=False)

    reactor_thread = threading.Thread(target=start_reactor, daemon=True)
    reactor_thread.start()


    # Allow some time for TCP clients to authenticate before FastAPI starts serving
    time.sleep(2)

    print("[INFO] TCP clients initialized")
    yield
    # Clean up resources
    await engine.dispose()
    # Close all TCP clients
    def stop_reactor():
        if reactor.running:
            print("[INFO] Stopping the Twisted reactor...")
            reactor.stop()

    reactor.callFromThread(stop_reactor)

    print("[INFO] Lifespan ended")
