import heapq
import json
import os

# Danh sách cố định các website
FIXED_WEBSITES = ["Google", "YouTube", "Facebook", "Instagram", "TikTok", "GitHub", "Reddit"]

def top_k_websites(data, k=5):
    if not data:
        print("⚠️ Chưa có dữ liệu website!")
        return []

    heap = []
    for name, visits in data:
        if len(heap) < k:
            heapq.heappush(heap, (visits, name))
        elif visits > heap[0][0]:
            heapq.heapreplace(heap, (visits, name))

    result = []
    while heap:
        visits, name = heapq.heappop(heap)
        result.append((name, visits))
    return result[::-1]

def input_websites_fixed():
    websites = []
    print(f"👉 Nhập lượt truy cập cho {len(FIXED_WEBSITES)} website phổ biến:")
    for name in FIXED_WEBSITES:
        while True:
            try:
                visits = int(input(f"{name}: "))
                if visits < 0:
                    print("❌ Lượt truy cập phải >= 0!")
                else:
                    break
            except ValueError:
                print("❌ Vui lòng nhập số nguyên!")
        websites.append((name, visits))
    print("✅ Đã nhập xong dữ liệu!")
    return websites

def save_websites(websites, filename="websites.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(websites, f, ensure_ascii=False, indent=4)
        print("💾 Dữ liệu đã được lưu vào file websites.json")
    except Exception as e:
        print(f"❌ Lỗi khi lưu dữ liệu: {e}")

def load_websites(filename="websites.json"):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Lỗi khi đọc dữ liệu: {e}")
    return []

def main():
    websites = load_websites()

    while True:
        print("\n===== MENU CHÍNH =====")
        print("1. Nhập lượt truy cập cho các website phổ biến")
        print("2. Xem danh sách website hiện có")
        print("3. Xem Top K website theo lượt truy cập")
        print("4. Lưu dữ liệu ra file")
        print("5. Thoát chương trình")
        choice = input("👉 Nhập lựa chọn (1-5): ")

        if choice == "1":
            new_data = input_websites_fixed()
            websites = new_data  # Ghi đè dữ liệu cũ

        elif choice == "2":
            if not websites:
                print("⚠️ Chưa có dữ liệu website!")
            else:
                print("\n📋 DANH SÁCH WEBSITE HIỆN CÓ")
                print("-" * 60)
                for name, visits in websites:
                    print(f"{name:<20} {visits:,}".replace(",", "."))
                print("-" * 60)

        elif choice == "3":
            if not websites:
                print("⚠️ Chưa có dữ liệu website để xếp hạng!")
            else:
                try:
                    k = int(input("Nhập số lượng Top K muốn xem: "))
                    if k > len(websites):
                        print(f"⚠️ Chỉ có {len(websites)} website, không đủ {k}!")
                        k = len(websites)
                    topk = top_k_websites(websites, k)
                    print(f"\n🔥 TOP {k} WEBSITE THEO LƯỢT TRUY CẬP 🔥")
                    print("-" * 60)
                    print(f"{'Hạng':<5} {'Website':<20} {'Lượt truy cập':>20}")
                    print("-" * 60)
                    for i, (name, visits) in enumerate(topk, 1):
                        visits_str = f"{visits:,}".replace(",", ".")
                        print(f"{i:<5} {name:<20} {visits_str:>20}")
                    print("-" * 60)
                except ValueError:
                    print("❌ Lỗi: Nhập số hợp lệ!")

        elif choice == "4":
            save_websites(websites)

        elif choice == "5":
            save_websites(websites)
            print("👋 Tạm biệt!")
            break

        else:
            print("⚠️ Lựa chọn không hợp lệ, vui lòng nhập lại!")

if __name__ == "__main__":
    main()