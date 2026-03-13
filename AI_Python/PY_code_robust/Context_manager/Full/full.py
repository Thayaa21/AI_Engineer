# # The Hotel Manager — controls room check in and check out
# class GPUHotel:
#     def __init__(self, room_name):
#         # Hotel built, room name registered
#         self.room_name = room_name
    
#     def __enter__(self):
#         # Guest checks in — GPU memory allocated, logged as occupied
#         print(f"HOTEL: '{self.room_name}' checked in — GPU memory allocated 🟢")
#         return self  # hand the key to the guest
    
#     def __exit__(self, error_type, error_value, error_trace):
#         # Guest checks out — GPU memory released, ALWAYS happens
#         print(f"HOTEL: '{self.room_name}' checked out — GPU memory released 🔴")
#         if error_type:
#             # Guest crashed the room — we still clean up
#             print(f"HOTEL: Room was crashed! Error: {error_value} — still cleaned up!")
#         return False  # let the error bubble up if it happened

# # Normal stay — check in, work, check out
# print("--- Normal guest ---")
# with GPUHotel("training_room") as room:
#     print(f"GUEST: Working in '{room.room_name}'...")
#     print("GUEST: Training model...")

# # Crashed stay — error occurs but room still freed
# print("\n--- Guest crashes the room ---")
# try:
#     with GPUHotel("inference_room") as room:
#         print(f"GUEST: Working in '{room.room_name}'...")
#         raise MemoryError("GPU overloaded!")  # guest crashes the room
#         print("GUEST: This never runs")
# except MemoryError as e:
#     print(f"CAUGHT: {e}")




from contextlib import contextmanager, ExitStack

# ═══════════════════════════════════════
# STYLE 1 — Single Room with @contextmanager
# Simple hotel manager using yield
# ═══════════════════════════════════════

@contextmanager
def gpu_room(room_name):
    # Check in — prepare the room before handing key
    print(f"HOTEL: '{room_name}' ready — GPU allocated 🟢")
    try:
        yield  # 🔑 key handed — guest works here
    finally:
        # Checkout — always happens, crash or not
        print(f"HOTEL: '{room_name}' cleaned — GPU released 🔴")

print("--- Single room, normal stay ---")
with gpu_room("training_room"):
    print("GUEST: Training model...")

print("\n--- Single room, crashed stay ---")
try:
    with gpu_room("inference_room"):
        print("GUEST: Running inference...")
        raise MemoryError("GPU overloaded!")  # guest crashes room
except MemoryError as e:
    print(f"CAUGHT: {e} — but room still cleaned!")

# ═══════════════════════════════════════
# STYLE 2 — Multiple Rooms with ExitStack
# Head of housekeeping — cleans ALL rooms
# ═══════════════════════════════════════

def process_data_files(file_paths):
    print(f"\nHOUSEKEEPING: Opening {len(file_paths)} rooms...")
    
    with ExitStack() as housekeeping:
        # Housekeeping opens all rooms — tracks all of them
        files = [housekeeping.enter_context(open(path, 'r')) 
                 for path in file_paths]
        
        # Guests work in all rooms simultaneously
        data = [f.read() for f in files]
        print(f"GUESTS: Read data from {len(files)} rooms")
        print(f"DATA: {data}")
    
    # All rooms cleaned automatically — no manual closing needed
    print("HOUSEKEEPING: All rooms cleaned! 🔴")

# Create some dummy files to test
import os
for i, content in enumerate(["AI data 1", "AI data 2", "AI data 3"]):
    with open(f"test_file_{i}.txt", "w") as f:
        f.write(content)

process_data_files(["test_file_0.txt", "test_file_1.txt", "test_file_2.txt"])

# Cleanup test files
for i in range(3):
    os.remove(f"test_file_{i}.txt")