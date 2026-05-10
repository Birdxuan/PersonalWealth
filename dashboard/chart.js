/**
 * PersonalWealth 仪表板脚本
 * 加载数据并绘制图表
 */

let accountChart = null;
let categoryChart = null;
let trendChart = null;

// 模拟数据（实际应该从后端 API 获取）
const mockData = {
    total: {
        total_cny: 219420.00,
        stock_cny: 48000,
        fund_cny: 10000,
        cash_cny: 26000,
        crypto_cny: 135420
    },
    by_account: {
        '微信': 10000,
        '支付宝': 20000,
        'A股': 48000,
        'IBKR(盈透)': 46020,
        '众安银行': 6000,
        '其他': 89400
    },
    by_category: {
        '现金': 26000,
        '基金': 10000,
        '股票': 48000,
        '加密货币': 135420
    },
    snapshots: generateMockSnapshots()
};

// 生成模拟快照数据
function generateMockSnapshots() {
    const snapshots = [];
    const baseValue = 210000;
    const today = new Date();

    for (let i = 29; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        const dateStr = date.toISOString().split('T')[0];
        
        // 模拟每日波动
        const fluctuation = 1 + (i * 0.01) + (Math.random() - 0.5) * 0.02;
        snapshots.push({
            date: dateStr,
            total_cny: baseValue * fluctuation
        });
    }
    return snapshots;
}

// 更新总资产卡片
function updateTotalCards() {
    const total = mockData.total;
    const now = new Date();
    const timeStr = now.getHours().toString().padStart(2, '0') + ':' + 
                    now.getMinutes().toString().padStart(2, '0');

    document.getElementById('totalAssets').textContent = 
        '¥' + total.total_cny.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    document.getElementById('stockAssets').textContent = 
        '¥' + total.stock_cny.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    document.getElementById('fundAssets').textContent = 
        '¥' + total.fund_cny.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    document.getElementById('cashAssets').textContent = 
        '¥' + total.cash_cny.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    document.getElementById('cryptoAssets').textContent = 
        '¥' + total.crypto_cny.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    document.getElementById('updateTime').textContent = timeStr;
}

// 绘制账户分布饼图
function drawAccountChart() {
    const ctx = document.getElementById('accountChart').getContext('2d');
    const accounts = Object.keys(mockData.by_account);
    const values = Object.values(mockData.by_account);
    const colors = [
        '#09B981', '#3B82F6', '#F59E0B', '#8B5CF6', '#EC4899', '#6B7280'
    ];

    accountChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: accounts,
            datasets: [{
                data: values,
                backgroundColor: colors,
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: { size: 12 },
                        padding: 15
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const total = values.reduce((a, b) => a + b, 0);
                            const percentage = ((context.raw / total) * 100).toFixed(1);
                            return context.label + ': ¥' + 
                                context.raw.toLocaleString('zh-CN', { maximumFractionDigits: 0 }) + 
                                ' (' + percentage + '%)';
                        }
                    }
                }
            }
        }
    });
}

// 绘制资产类型分布饼图
function drawCategoryChart() {
    const ctx = document.getElementById('categoryChart').getContext('2d');
    const categories = Object.keys(mockData.by_category);
    const values = Object.values(mockData.by_category);
    const colors = ['#10B981', '#3B82F6', '#F59E0B', '#EF4444'];

    categoryChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: categories,
            datasets: [{
                data: values,
                backgroundColor: colors,
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: { size: 12 },
                        padding: 15
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const total = values.reduce((a, b) => a + b, 0);
                            const percentage = ((context.raw / total) * 100).toFixed(1);
                            return context.label + ': ¥' + 
                                context.raw.toLocaleString('zh-CN', { maximumFractionDigits: 0 }) + 
                                ' (' + percentage + '%)';
                        }
                    }
                }
            }
        }
    });
}

// 绘制趋势曲线
function drawTrendChart() {
    const ctx = document.getElementById('trendChart').getContext('2d');
    const snapshots = mockData.snapshots;
    const dates = snapshots.map(s => {
        const date = new Date(s.date);
        return (date.getMonth() + 1) + '/' + date.getDate();
    });
    const values = snapshots.map(s => s.total_cny);

    trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: '总资产',
                data: values,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: '#667eea',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        font: { size: 12 },
                        usePointStyle: true
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: { size: 12 },
                    bodyFont: { size: 12 },
                    callbacks: {
                        label: function(context) {
                            return '¥' + context.raw.toLocaleString('zh-CN', { maximumFractionDigits: 0 });
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return '¥' + (value / 1000).toFixed(0) + 'k';
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// 更新资产表格
function updateAssetsTable() {
    const mockAssets = [
        { account: '微信', category: '现金', symbol: 'CNY', quantity: 5000, avg_cost: 1.0, value: 5000, currency: 'CNY' },
        { account: '微信', category: '基金', symbol: '易方达沪深300', quantity: 1000, avg_cost: 5.0, value: 5000, currency: 'CNY' },
        { account: '支付宝', category: '现金', symbol: 'CNY', quantity: 15000, avg_cost: 1.0, value: 15000, currency: 'CNY' },
        { account: '支付宝', category: '基金', symbol: '余额宝', quantity: 5000, avg_cost: 1.0, value: 5000, currency: 'CNY' },
        { account: 'A股', category: '股票', symbol: '贵州茅台', quantity: 10, avg_cost: 1800, value: 18000, currency: 'CNY' },
        { account: 'A股', category: 'ETF', symbol: '沪深300', quantity: 100, avg_cost: 300, value: 30000, currency: 'CNY' },
        { account: 'IBKR(盈透)', category: '股票', symbol: 'AAPL', quantity: 10, avg_cost: 150, value: 10620, currency: 'USD' },
        { account: 'IBKR(盈透)', category: '现金', symbol: 'USD', quantity: 5000, avg_cost: 1.0, value: 35400, currency: 'USD' },
        { account: '众安银行', category: '现金', symbol: 'CNY', quantity: 6000, avg_cost: 1.0, value: 6000, currency: 'CNY' },
        { account: '其他', category: '加密货币', symbol: 'BTC', quantity: 0.5, avg_cost: 40000, value: 14200, currency: 'USD' },
        { account: '其他', category: '加密货币', symbol: 'ETH', quantity: 5, avg_cost: 2500, value: 88500, currency: 'USD' }
    ];

    const tbody = document.getElementById('assetsTableBody');
    tbody.innerHTML = '';

    mockAssets.forEach(asset => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${asset.account}</td>
            <td>${asset.category}</td>
            <td>${asset.symbol}</td>
            <td>${asset.quantity.toLocaleString('zh-CN', { maximumFractionDigits: 2 })}</td>
            <td>${asset.avg_cost.toLocaleString('zh-CN', { maximumFractionDigits: 2 })}</td>
            <td>¥${asset.value.toLocaleString('zh-CN', { maximumFractionDigits: 0 })}</td>
            <td>${asset.currency}</td>
        `;
        tbody.appendChild(row);
    });
}

// 初始化页面
function initDashboard() {
    console.log('正在初始化仪表板...');
    updateTotalCards();
    drawAccountChart();
    drawCategoryChart();
    drawTrendChart();
    updateAssetsTable();
    console.log('✅ 仪表板初始化完成！');
}

// 页面加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDashboard);
} else {
    initDashboard();
}
