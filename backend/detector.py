from collections import defaultdict
import requests

routing_state = defaultdict(dict)
reported_events = set()

def check_path(path):
    visited = set()
    for asn in path:
        if isinstance(asn, list):
            for i in asn:
                if i in visited:
                    return 1
                visited.add(i)
        else:
            if asn in visited:
                return 1
            visited.add(asn)
    return 0

def check_rpki(prefix, origin_asn):
    url = "https://stat.ripe.net/data/rpki-validation/data.json"
    params = {"resource": origin_asn, "prefix": prefix}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data["data"]["status"]
    except requests.RequestException as e:
        print("RPKI request failed: ", e)
        return "unknown"

def get_risk_level(score):
    if score >= 6:
        return "CRITICAL"

    elif score >= 4:
        return "HIGH"

    elif score >= 2:
        return "MEDIUM"

    else:
        return "LOW"


def extract_update(data):
    msg = data["data"]

    timestamp = msg["timestamp"]
    peer_asn = msg["peer_asn"]
    path = msg["path"]

    origin_asn = path[-1] if path else None

    announcements = []

    for announcement in msg["announcements"]:
        announcements.extend(announcement["prefixes"])

    withdrawals = msg["withdrawals"]

    events = []
    for prefix in announcements:

        old_origin = routing_state[prefix].get(peer_asn)
        known_origins = set(routing_state[prefix].values())

        score = check_path(path)
        same_peer_origin_change = (old_origin is not None and old_origin != origin_asn)
        new_peer_different_origin = (old_origin is None and len(known_origins) > 0 and origin_asn not in known_origins)

        if (same_peer_origin_change or new_peer_different_origin):
            if same_peer_origin_change:
                print("\nSame-peer origin change detected")

                score += 3
            elif new_peer_different_origin:
                print("\nNew peer with different origin detected")
                score += 2

            print("Prefix:", prefix)
            print("Peer ASN:", peer_asn)
            print("New origin:", origin_asn)
            print("Known origins:", known_origins)
            rpki_status = check_rpki(
                prefix,
                origin_asn
            )
            print("RPKI status:", rpki_status)
            if rpki_status.startswith("invalid"):
                print("Invalid RPKI detected!")
                score += 5

            if score > 0:
                event_key = (prefix, old_origin, origin_asn, peer_asn)
                if event_key not in reported_events:
                    reported_events.add(event_key)
                    event = {
                        "timestamp": timestamp,
                        "prefix": prefix,
                        "peer_asn": peer_asn,
                        "old_origin": old_origin,
                        "new_origin": origin_asn,
                        "known_origins": list(known_origins),
                        "rpki_status": rpki_status,
                        "path": path,
                        "score": score,
                        "risk_level": get_risk_level(score)
                    }
                    events.append(event)
        routing_state[prefix][peer_asn] = origin_asn

    for prefix in withdrawals:
        if prefix not in routing_state:
            continue
        routing_state[prefix].pop(peer_asn, None)
        
        if not routing_state[prefix]:
            del routing_state[prefix]
    return events