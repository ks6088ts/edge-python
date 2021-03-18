import argparse
import asyncio
import random

import websockets

DELTA_TIME = None


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="host", type=str, default="localhost")
    parser.add_argument("--dt", help="delta time[sec]", type=float, default=1.0)
    parser.add_argument(
        "--port",
        help="port number",
        type=int,
        default=8080,
    )
    args = parser.parse_args()
    return args.host, args.port, args.dt


async def time(websocket, path):  # pylint: disable=unused-argument
    while True:
        await websocket.send(f"{random.random()}, {random.random()}, {random.random()}")
        await asyncio.sleep(DELTA_TIME)


if __name__ == "__main__":
    host, port, DELTA_TIME = parse_arguments()
    start_server = websockets.serve(time, host, port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
