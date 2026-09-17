import asyncio
import websockets
import json
from backend.detector import extract_update

URI = ("wss://ris-live.ripe.net/v1/ws/" "?client=bgp-hijack-visualizer")

async def stop_after_seconds(seconds):
    await asyncio.sleep(seconds)
    print(f"\n{seconds} seconds reached. " "Stopping collector...")
    raise SystemExit

def print_data(event):
    print("\n" + "=" * 50)
    print("SUSPICIOUS BGP EVENT")
    print("=" * 50)
    print("Prefix:", event["prefix"])
    print("Peer ASN:", event["peer_asn"])
    print("Old origin:", event["old_origin"])
    print("New origin:", event["new_origin"])
    print("RPKI status:", event["rpki_status"])
    print("AS path:", event["path"])
    print("Score:", event["score"])
    print("Risk level:", event["risk_level"])
    print("Timestamp:", event["timestamp"])


async def collect():
    async with websockets.connect(URI) as ws:
        subscribe_msg = {
            "type": "ris_subscribe",
            "data": {
                "type": "UPDATE"
            }
        }
        await ws.send(json.dumps(subscribe_msg))
        print("Connected to RIPE RIS!")

        buffer = []
        try:
            with open("data/updates.jsonl", "a") as f:
                async for messages in ws:
                    data = json.loads(messages)
                    update = extract_update(data)
                    for event in update:
                        buffer.append(json.dumps(event))
                        print_data(event)
                    if len(buffer) >= 50:
                        f.write("\n".join(buffer) + "\n")
                        f.flush()
                        buffer.clear()
                if buffer:
                    f.write("\n".join(buffer) + "\n")
                    f.flush()
                    buffer.clear()
        finally:
            if buffer:
                with open("data/updates.jsonl", "a") as f:
                    f.write("\n".join(buffer) + "\n")
                    f.flush()
                buffer.clear()

async def run():
    stop_task = asyncio.create_task(stop_after_seconds(10))
    collector_task = asyncio.create_task(collect())
    await asyncio.gather(stop_task, collector_task)

asyncio.run(run())