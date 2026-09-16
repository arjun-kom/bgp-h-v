
# def test_detector():
#     # Reset state before testing
#     routing_state.clear()
#     reported_events.clear()

#     # --------------------------------------------------
#     # TEST 1: First announcement
#     # Expected: No suspicious event
#     # --------------------------------------------------
#     fake_update_1 = {
#         "data": {
#             "timestamp": 1000,
#             "peer_asn": 64500,
#             "path": [64500, 64501, 64502],
#             "announcements": [
#                 {
#                     "prefixes": [
#                         "203.0.113.0/24"
#                     ]
#                 }
#             ],
#             "withdrawals": []
#         }
#     }

#     print("\n" + "=" * 60)
#     print("TEST 1: First announcement")
#     print("=" * 60)

#     result = extract_update(fake_update_1)
#     print("Detected events:", result)
#     print("Routing state:", dict(routing_state))


#     # --------------------------------------------------
#     # TEST 2: Same-peer origin change
#     # Expected: One suspicious event
#     # --------------------------------------------------
#     fake_update_2 = {
#         "data": {
#             "timestamp": 1001,
#             "peer_asn": 64500,
#             "path": [64500, 64510, 64600],
#             "announcements": [
#                 {
#                     "prefixes": [
#                         "203.0.113.0/24"
#                     ]
#                 }
#             ],
#             "withdrawals": []
#         }
#     }

#     print("\n" + "=" * 60)
#     print("TEST 2: Same-peer origin change")
#     print("=" * 60)

#     result = extract_update(fake_update_2)
#     print("Detected events:", result)
#     print("Routing state:", dict(routing_state))


#     # --------------------------------------------------
#     # TEST 3: Repeated same update
#     # Expected: Empty list because of duplicate checking
#     # --------------------------------------------------
#     print("\n" + "=" * 60)
#     print("TEST 3: Repeated same update")
#     print("=" * 60)

#     result = extract_update(fake_update_2)
#     print("Detected events:", result)


#     # --------------------------------------------------
#     # TEST 4: Multiple prefixes in one message
#     # Expected: All three prefixes stored
#     # --------------------------------------------------
#     fake_multiple_prefixes = {
#         "data": {
#             "timestamp": 1002,
#             "peer_asn": 64500,
#             "path": [64500, 64501, 64700],
#             "announcements": [
#                 {
#                     "prefixes": [
#                         "203.0.113.0/24",
#                         "203.0.114.0/24",
#                         "203.0.115.0/24"
#                     ]
#                 }
#             ],
#             "withdrawals": []
#         }
#     }

#     print("\n" + "=" * 60)
#     print("TEST 4: Multiple prefixes")
#     print("=" * 60)

#     result = extract_update(fake_multiple_prefixes)
#     print("Detected events:", result)
#     print("Routing state:", dict(routing_state))


#     # --------------------------------------------------
#     # TEST 5: Change only one prefix
#     # Expected: Only 203.0.114.0/24 creates an event
#     # --------------------------------------------------
#     fake_one_prefix_change = {
#         "data": {
#             "timestamp": 1003,
#             "peer_asn": 64500,
#             "path": [64500, 64510, 64800],
#             "announcements": [
#                 {
#                     "prefixes": [
#                         "203.0.114.0/24"
#                     ]
#                 }
#             ],
#             "withdrawals": []
#         }
#     }

#     print("\n" + "=" * 60)
#     print("TEST 5: Change only one prefix")
#     print("=" * 60)

#     result = extract_update(fake_one_prefix_change)
#     print("Detected events:", result)
#     print("Routing state:", dict(routing_state))


#     # --------------------------------------------------
#     # TEST 6: Withdrawal
#     # Expected: 203.0.113.0/24 removed
#     # --------------------------------------------------
#     fake_withdrawal = {
#         "data": {
#             "timestamp": 1004,
#             "peer_asn": 64500,
#             "path": [],
#             "announcements": [],
#             "withdrawals": [
#                 "203.0.113.0/24"
#             ]
#         }
#     }

#     print("\n" + "=" * 60)
#     print("TEST 6: Withdrawal")
#     print("=" * 60)

#     print("Before withdrawal:")
#     print(dict(routing_state))

#     result = extract_update(fake_withdrawal)

#     print("Detected events:", result)

#     print("After withdrawal:")
#     print(dict(routing_state))


#     # --------------------------------------------------
#     # TEST 7: Withdrawal of a prefix with multiple peers
#     # Expected: Prefix remains because another peer exists
#     # --------------------------------------------------

#     # Add another peer for the same prefix manually
#     routing_state["203.0.115.0/24"][64600] = 64800

#     fake_multiple_peer_withdrawal = {
#         "data": {
#             "timestamp": 1005,
#             "peer_asn": 64500,
#             "path": [],
#             "announcements": [],
#             "withdrawals": [
#                 "203.0.115.0/24"
#             ]
#         }
#     }

#     print("\n" + "=" * 60)
#     print("TEST 7: Withdrawal with multiple peers")
#     print("=" * 60)

#     print("Before withdrawal:")
#     print(dict(routing_state))

#     result = extract_update(fake_multiple_peer_withdrawal)

#     print("Detected events:", result)

#     print("After withdrawal:")
#     print(dict(routing_state))


#     # --------------------------------------------------
#     # TEST 8: New peer with different origin
#     # Expected: Suspicious event
#     # --------------------------------------------------

#     fake_new_peer = {
#         "data": {
#             "timestamp": 1006,
#             "peer_asn": 64900,
#             "path": [64900, 64901, 65000],
#             "announcements": [
#                 {
#                     "prefixes": [
#                         "203.0.114.0/24"
#                     ]
#                 }
#             ],
#             "withdrawals": []
#         }
#     }

#     print("\n" + "=" * 60)
#     print("TEST 8: New peer with different origin")
#     print("=" * 60)

#     result = extract_update(fake_new_peer)
#     print("Detected events:", result)
#     print("Routing state:", dict(routing_state))

# test_detector()