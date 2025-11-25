import heapq
import json
import os
import threading
import time
import logging
import random

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

from flask import Flask, send_from_directory
from flask_socketio import SocketIO

app = Flask(__name__, static_url_path='', static_folder='.')
socketio = SocketIO(app, cors_allowed_origins="*")

DATA_FILE = "websites.json"
FIXED_WEBSITES = [] 
global_websites_data = []

# --- KHO LƯU TRỮ (THÙNG RÁC) ---
# Lưu tạm các web bị xóa để khôi phục nếu cần
ARCHIVED_DATA = {} 

DEFAULT_DATA = [
    {"name": "Google",    "logo": "https://logo.clearbit.com/google.com", "access": [3.2, 3.3, 3.4, 3.5, 3.2], "search": [16.1, 16.2, 16.3, 16.4, 16.1], "transaction": [0.89, 0.90, 0.91, 0.92, 0.89], "interaction": [18.5, 18.6, 18.7, 18.8, 18.5], "chart": None, "labels": ["", "", "", "", "Now"]},
    {"name": "YouTube",   "logo": "https://logo.clearbit.com/youtube.com", "access": [3.15, 3.16, 3.17, 3.18, 3.15], "search": [18.8, 18.9, 19.0, 19.1, 18.8], "transaction": [0.68, 0.69, 0.70, 0.71, 0.68], "interaction": [34.6, 34.7, 34.8, 34.9, 34.6], "chart": None, "labels": ["", "", "", "", "Now"]},
    {"name": "Facebook",  "logo": "https://logo.clearbit.com/facebook.com", "access": [2.98, 2.99, 3.00, 3.01, 2.98], "search": [11.2, 11.3, 11.4, 11.5, 11.2], "transaction": [0.58, 0.59, 0.60, 0.61, 0.58], "interaction": [19.8, 19.9, 20.0, 20.1, 19.8], "chart": None, "labels": ["", "", "", "", "Now"]},
    {"name": "Instagram", "logo": "https://logo.clearbit.com/instagram.com", "access": [2.05, 2.06, 2.07, 2.08, 2.05], "search": [8.9, 9.0, 9.1, 9.2, 8.9], "transaction": [0.42, 0.43, 0.44, 0.45, 0.42], "interaction": [16.8, 16.9, 17.0, 17.1, 16.8], "chart": None, "labels": ["", "", "", "", "Now"]},
    {"name": "TikTok",    "logo": "https://logo.clearbit.com/tiktok.com", "access": [1.68, 1.69, 1.70, 1.72, 1.68], "search": [9.8, 9.9, 10.0, 10.1, 9.8], "transaction": [0.31, 0.32, 0.33, 0.34, 0.31], "interaction": [28.7, 28.8, 28.9, 29.0, 28.7], "chart": None, "labels": ["", "", "", "", "Now"]},
    {"name": "GitHub",    "logo": "https://logo.clearbit.com/github.com", "access": [0.42, 0.43, 0.44, 0.45, 0.42], "search": [0.38, 0.39, 0.40, 0.41, 0.38], "transaction": [0.085, 0.086, 0.087, 0.088, 0.085], "interaction": [0.95, 0.96, 0.97, 0.98, 0.95], "chart": None, "labels": ["", "", "", "", "Now"]},
    {"name": "Reddit",    "logo": "https://logo.clearbit.com/reddit.com", "access": [0.38, 0.39, 0.40, 0.41, 0.38], "search": [0.44, 0.45, 0.46, 0.47, 0.44], "transaction": [0.028, 0.029, 0.030, 0.031, 0.028], "interaction": [1.42, 1.43, 1.44, 1.45, 1.42], "chart": None, "labels": ["", "", "", "", "Now"]}
]

def load_data_from_file():
    global global_websites_data, FIXED_WEBSITES
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                global_websites_data = json.load(f)
        except Exception:
            global_websites_data = DEFAULT_DATA
    else:
        global_websites_data = DEFAULT_DATA
    
    FIXED_WEBSITES = [site['name'] for site in global_websites_data]

def save_data_to_file():
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(global_websites_data, f, ensure_ascii=False, indent=4)
    except Exception: pass

def top_k_websites(data, k=5):
    if not data: return []
    heap = []
    for name, visits in data:
        if len(heap) < k: heapq.heappush(heap, (visits, name))
        elif visits > heap[0][0]: heapq.heapreplace(heap, (visits, name))
    result = []
    while heap:
        visits, name = heapq.heappop(heap)
        result.append((name, visits))
    return result[::-1]

def sync_data_to_web(simple_data):
    global global_websites_data
    for name, visits in simple_data:
        for site in global_websites_data:
            if site['name'] == name:
                traffic_val = visits 
                site['access'].append(traffic_val)
                site['search'].append(traffic_val * 2)
                site['transaction'].append(traffic_val * 0.1)
                site['interaction'].append(traffic_val * 5)
                if len(site['access']) > 20:
                    site['access'].pop(0)
                    site['search'].pop(0)
                    site['transaction'].pop(0)
                    site['interaction'].pop(0)
    
    save_data_to_file()
    socketio.emit('update_data', global_websites_data)

def input_websites_fixed():
    websites = []
    print(f"\n👉 Nhập lượt truy cập (Đơn vị: Tỷ):")
    for name in FIXED_WEBSITES:
        while True:
            try:
                current_val = 0
                found = False
                for s in global_websites_data:
                    if s['name'] == name:
                        current_val = s['access'][-1]
                        found = True
                        break
                if not found: break 
                user_input = input(f"{name} (Hiện tại: {current_val:.3f}): ")
                if user_input.strip() == "": visits = current_val
                else: visits = float(user_input)
                if visits < 0: print("❌ Phải >= 0!")
                else: break
            except ValueError: print("❌ Nhập số!")
        websites.append((name, visits))
    print("✅ Đã nhập xong!")
    sync_data_to_web(websites)
    return websites

@socketio.on('add_new_site')
def handle_add_site(data):
    global global_websites_data, FIXED_WEBSITES, ARCHIVED_DATA
    
    for site in global_websites_data:
        if site['name'].lower() == data['name'].lower(): return 

    # --- CHECK KHO LƯU TRỮ ---
    # Nếu web đã từng bị xóa, lấy lại dữ liệu cũ từ kho
    site_name_key = data['name']
    restored_site = None
    
    for key, val in ARCHIVED_DATA.items():
        if key.lower() == site_name_key.lower():
            restored_site = val
            break
    
    if restored_site:
        print(f"\n♻️ KHÔI PHỤC TỪ KHO: {data['name']}")
        global_websites_data.append(restored_site)
    else:
        # Nếu là web mới tinh
        base_traffic = data['access'][0]
        fake_access = [base_traffic * 0.9, base_traffic * 0.95, base_traffic * 0.98, base_traffic, base_traffic]
        new_site = {
            "name": data['name'], "logo": data['logo'],
            "access": fake_access, 
            "search": [x * 2 for x in fake_access],
            "transaction": [x * 0.1 for x in fake_access],
            "interaction": [x * 5 for x in fake_access],
            "chart": None, "labels": ["", "", "", "", "Now"]
        }
        global_websites_data.append(new_site)

    if data['name'] not in FIXED_WEBSITES: FIXED_WEBSITES.append(data['name'])
    
    save_data_to_file()
    socketio.emit('update_data', global_websites_data)

@socketio.on('delete_site')
def handle_delete_site(site_name):
    global global_websites_data, FIXED_WEBSITES, ARCHIVED_DATA
    
    # 1. Cất vào kho trước khi xóa
    for site in global_websites_data:
        if site['name'] == site_name:
            ARCHIVED_DATA[site_name] = site 
            break

    # 2. Xóa khỏi danh sách hiển thị
    global_websites_data[:] = [s for s in global_websites_data if s['name'] != site_name]
    
    # 3. Xóa khỏi Menu
    if site_name in FIXED_WEBSITES: FIXED_WEBSITES.remove(site_name)
    
    print(f"\n🗑️ ĐÃ XÓA VÀO KHO: {site_name}")
    save_data_to_file()
    socketio.emit('update_data', global_websites_data)

@app.route('/')
def index(): return send_from_directory('.', 'index.html')

@socketio.on('connect')
def handle_connect(): socketio.emit('update_data', global_websites_data)

def auto_simulation_thread():
    time.sleep(2)
    while True:
        time.sleep(2)
        for site in global_websites_data:
            delta = random.uniform(-0.003, 0.003) 
            current = site['access'][-1]
            new_val = max(0, current + delta) 
            site['access'].append(new_val)
            site['search'].append(new_val * 2)
            site['transaction'].append(new_val * 0.1)
            site['interaction'].append(new_val * 5)
            if len(site['access']) > 20:
                site['access'].pop(0)
                site['search'].pop(0)
                site['transaction'].pop(0)
                site['interaction'].pop(0)
        socketio.emit('update_data', global_websites_data)

def cli_thread_function():
    time.sleep(1)
    while True:
        print("\n===== 🎛️ BẢNG ĐIỀU KHIỂN =====")
        print("1. 🔴 Nhập số liệu")
        print("2. 📋 Xem danh sách")
        print("3. 🏆 Xem Top K")
        print("4. 💾 Lưu file")
        print("5. 🚪 Thoát")
        try: choice = input("👉 Chọn: ")
        except: continue

        if choice == "1": input_websites_fixed()
        elif choice == "2":
            print("-" * 40)
            for s in global_websites_data: print(f"{s['name']:<20} {s['access'][-1]:.3f} B")
            print("-" * 40)
        elif choice == "3":
            try:
                k = int(input("K (3): ") or 3)
                topk = top_k_websites([(s['name'], s['access'][-1]) for s in global_websites_data], k)
                print("-" * 40)
                for i, (n, v) in enumerate(topk, 1): print(f"{i}. {n:<20} {v:.3f} B")
                print("-" * 40)
            except: pass
        elif choice == "4": save_data_to_file(); print("Đã lưu!")
        elif choice == "5": save_data_to_file(); os._exit(0)

if __name__ == "__main__":
    load_data_from_file()
    t1 = threading.Thread(target=cli_thread_function)
    t1.daemon = True
    t1.start()
    t2 = threading.Thread(target=auto_simulation_thread)
    t2.daemon = True
    t2.start()
    print("🌐 Server: http://127.0.0.1:5000")
    socketio.run(app, port=5000, debug=False, log_output=False)