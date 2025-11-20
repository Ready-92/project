// Toggle menu sidebar
let list = document.querySelectorAll(".navigation li");
function activeLink() {
    list.forEach(item => item.classList.remove("hovered"));
    this.classList.add("hovered");
}
list.forEach(item => item.addEventListener("mouseenter", activeLink));

let toggle = document.querySelector(".toggle");
let navigation = document.querySelector(".navigation");
let main = document.querySelector(".main");

toggle.onclick = function () {
    navigation.classList.toggle("active");
    main.classList.toggle("active");
};


if (navigation) {
    navigation.addEventListener('mouseleave', () => {
        list.forEach(item => item.classList.remove('hovered'));
    });
}

// ==================== DỮ LIỆU 2025 ====================
const websites = [
    { name: "Google",     access: [3.2, 3.6, 4], search: [16.1, 16.4, 16.6], transaction: [0.89, 0.91, 0.93], interaction: [18.5, 18.7, 18.9], chart: null, labels: [] },
    { name: "YouTube",    access: [3.15, 3.18, 3.22], search: [18.8, 19.0, 19.2], transaction: [0.68, 0.70, 0.72], interaction: [34.6, 34.9, 35.2], chart: null, labels: [] },
    { name: "Facebook",   access: [2.98, 3.01, 3.04], search: [11.2, 11.3, 11.4], transaction: [0.58, 0.59, 0.61], interaction: [19.8, 20.0, 20.2], chart: null, labels: [] },
    { name: "Instagram",  access: [2.05, 2.08, 2.11], search: [8.9, 9.1, 9.2],    transaction: [0.42, 0.44, 0.46], interaction: [16.8, 17.1, 17.3], chart: null, labels: [] },
    { name: "Tiktok",     access: [1.68, 1.72, 1.78], search: [9.8, 10.1, 10.3],  transaction: [0.31, 0.33, 0.35], interaction: [28.7, 29.4, 30.1], chart: null, labels: [] },
    { name: "Github",     access: [0.42, 0.44, 0.46], search: [0.38, 0.40, 0.42], transaction: [0.085, 0.089, 0.092], interaction: [0.95, 0.98, 1.01], chart: null, labels: [] },
    { name: "Reddit",     access: [0.38, 0.40, 0.42], search: [0.44, 0.46, 0.48], transaction: [0.028, 0.030, 0.032], interaction: [1.42, 1.45, 1.48], chart: null, labels: [] }
];

let currentIndex = 0;
let activeChartIndex = 0;

// ==================== CẬP NHẬT CARD ====================
function updateCardData(index) {
    const site = websites[index];
    document.getElementById('access-card').querySelector('.numbers').textContent = `${site.access.at(-1).toFixed(2)} B`;
    document.getElementById('search-card').querySelector('.numbers').textContent = `${site.search.at(-1).toFixed(1)} B`;
    document.getElementById('transaction-card').querySelector('.numbers').textContent = `${site.transaction.at(-1).toFixed(2)} B`;
    document.getElementById('interaction-card').querySelector('.numbers').textContent = `${site.interaction.at(-1).toFixed(1)} B`;
}

document.addEventListener('DOMContentLoaded', () => {

    const mainContent = document.getElementById('main-content');
    const homeContent = document.getElementById('home-content');

    // ==================== FIX: LABELS BAN ĐẦU ====================
    websites.forEach(site => {
        site.labels = ["14:50 "];
    });

    // ==================== TẠO CHART ====================
    websites.forEach((site, index) => {
        const canvas = document.getElementById(`trafficChart${index}`);
        if (!canvas) return;

        const ctx = canvas.getContext('2d');

        const grad1 = ctx.createLinearGradient(0, 0, 0, 400);
        grad1.addColorStop(0, 'rgba(0, 255, 255, 0.6)');
        grad1.addColorStop(1, 'rgba(0, 255, 255, 0)');

        const grad2 = ctx.createLinearGradient(0, 0, 0, 400);
        grad2.addColorStop(0, 'rgba(255, 0, 170, 0.6)');
        grad2.addColorStop(1, 'rgba(255, 0, 170, 0)');

        const grad3 = ctx.createLinearGradient(0, 0, 0, 400);
        grad3.addColorStop(0, 'rgba(0, 255, 153, 0.6)');
        grad3.addColorStop(1, 'rgba(0, 255, 153, 0)');

        const grad4 = ctx.createLinearGradient(0, 0, 0, 400);
        grad4.addColorStop(0, 'rgba(255, 234, 0, 0.6)');
        grad4.addColorStop(1, 'rgba(255, 234, 0, 0)');

        site.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: site.labels,
                datasets: [
                    { label: 'Truy cập', data: site.access, borderColor: '#00ffff', backgroundColor: grad1, borderWidth: 3.5, fill: true, tension: 0.45 },
                    { label: 'Tìm kiếm', data: site.search, borderColor: '#ff00aa', backgroundColor: grad2, borderWidth: 3.5, fill: true, tension: 0.45 },
                    { label: 'Giao dịch', data: site.transaction, borderColor: '#00ff99', backgroundColor: grad3, borderWidth: 3.5, fill: true, tension: 0.45 },
                    { label: 'Tương tác', data: site.interaction, borderColor: '#ffea00', backgroundColor: grad4, borderWidth: 3.5, fill: true, tension: 0.45 }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { ticks: { color: '#808080' } },
                    y: { ticks: { color: '#808080' }, beginAtZero: true }
                }
            }
        });
    });

    // ==================== TRIGGER SHOW ====================
    window.showChart = function (index) {
        mainContent.style.display = 'block';
        homeContent.style.display = 'none';

        document.querySelectorAll('.chart-container').forEach(c => c.classList.remove('active'));
        document.getElementById(`chart${index}`).classList.add('active');

        currentIndex = index;
        activeChartIndex = index;

        updateCardData(currentIndex);
    };

    window.showHome = function () {
        mainContent.style.display = 'none';
        homeContent.style.display = 'block';
    };

    updateCardData(0);

setInterval(() => {
    const time = new Date().toLocaleTimeString('vi-VN', { 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit' 
    });

    websites.forEach((site, i) => {
        const delta = (Math.random() - 0.5) * 0.003;

        // 1. Lấy giá trị cuối cùng từ mảng dữ liệu gốc
        const lastAccess      = site.access.at(-1);
        const lastSearch      = site.search.at(-1);
        const lastTransaction = site.transaction.at(-1);
        const lastInteraction = site.interaction.at(-1);

        // 2. Tính toán và chặn số âm bằng Math.max(0, ...)
        // Sửa lỗi: Dùng đúng tên biến lastAccess, lastSearch...
        const newAccess       = Math.max(0, Number((lastAccess + delta).toFixed(3)));
        const newSearch       = Math.max(0, Number((lastSearch + delta * 8).toFixed(3)));
        const newTransaction  = Math.max(0, Number((lastTransaction + delta * 2).toFixed(3)));
        const newInteraction  = Math.max(0, Number((lastInteraction + delta * 4).toFixed(3)));

        // 3. QUAN TRỌNG: Cập nhật giá trị mới vào mảng gốc để vòng lặp sau có cái để tính tiếp
        site.access.push(newAccess);
        site.search.push(newSearch);
        site.transaction.push(newTransaction);
        site.interaction.push(newInteraction);

        // (Tùy chọn) Giữ mảng gốc không quá dài để nhẹ máy
        if (site.access.length > 50) {
            site.access.shift();
            site.search.shift();
            site.transaction.shift();
            site.interaction.shift();
        }

        // 4. Cập nhật biểu đồ (Chart.js)
        const chart = site.chart;
        if (chart) {
            if (chart.data.labels.length >= 10) {
                chart.data.labels.shift();
                chart.data.datasets.forEach(ds => ds.data.shift());
            }

            chart.data.labels.push(time);
            chart.data.datasets[0].data.push(newAccess);
            chart.data.datasets[1].data.push(newSearch);
            chart.data.datasets[2].data.push(newTransaction);
            chart.data.datasets[3].data.push(newInteraction);

            chart.update('none');
        }
    });

    // Cập nhật số liệu trên Card nếu đang xem chi tiết
    if (typeof currentIndex !== 'undefined') {
        updateCardData(currentIndex);
    }

}, 2000);

    // ==================== SEARCH ====================
    const searchInput = document.getElementById('search-input');

    if (searchInput) {
        searchInput.addEventListener('keyup', e => {
            if (e.key === 'Enter') {
                const q = searchInput.value.trim().toLowerCase();
                if (!q) return;

                const idx = websites.findIndex(s => s.name.toLowerCase().includes(q));

                if (idx !== -1) {
                    showChart(idx);
                    highlightAndScrollToSite(idx);
                } else {
                    alert("Không tìm thấy: " + q);
                }

                searchInput.value = '';
            }
        });
    }
});

// highlight nav item
function highlightAndScrollToSite(index) {
    const items = document.querySelectorAll('.navigation li');
    const navIndex = index + 2;

    items.forEach(el => el.classList.remove('hovered'));

    const target = items[navIndex];
    if (!target) return;

    target.classList.add('hovered');
    target.scrollIntoView({ behavior: 'smooth', block: 'center' });
}
