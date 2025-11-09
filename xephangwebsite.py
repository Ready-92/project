import heapq

# Dữ liệu mẫu: danh sách website + lượt truy cập
websites = [
    ("google.com", 85000000000),
    ("youtube.com", 34000000000),
    ("facebook.com", 12000000000),
    ("wikipedia.org", 6500000000),
    ("tiktok.com", 2500000000),
    ("shopee.vn", 800000000),
    ("lazada.vn", 500000000),
    ("zalo.me", 300000000),
    ("vnexpress.net", 200000000),
    ("example.com", 500000),
]

# Hàm tìm Top K dùng Heap
def top_k_websites(data, k=5):
    # Tạo min-heap: chỉ giữ K phần tử lớn nhất
    heap = []
    for name, visits in data:
        if len(heap) < k:
            heapq.heappush(heap, (visits, name))
        elif visits > heap[0][0]:                      # Nếu lớn hơn web nhỏ nhất trong group thì sẽ thay thế bằng cái mới -> heap vẫn giữ K phần tử lớn nhất 
            heapq.heapreplace(heap, (visits, name))
    
    # Lấy ra và sắp xếp giảm dần
    result = []
    while heap:
        visits, name = heapq.heappop(heap)
        result.append((name, visits))
    return result[::-1]  # Đảo ngược: cao → thấp

# CHẠY CHƯƠNG TRÌNH
print("XẾP HẠNG TOP 5 WEBSITE THEO LƯỢT TRUY CẬP (DÙNG HEAP)")
print("-" * 60)
print(f"{'Hạng':<5} {'Website':<20} {'Lượt truy cập':>20}")
print("-" * 60)

top5 = top_k_websites(websites, k=5)

for i, (name, visits) in enumerate(top5, 1):
    visits_str = f"{visits:,}".replace(",", ".")
    print(f"{i:<5} {name:<20} {visits_str:>20}")
print("-" * 60)