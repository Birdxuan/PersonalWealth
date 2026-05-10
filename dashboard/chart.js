/**
 * Dashboard chart and data loading logic
 * Using Chart.js library
 */

// Parse database data (simulated with sample data)
const sampleData = {
    accounts: [
        { name: '微信', value: 10000 },
        { name: '支付宝', value: 11800 },
        { name: 'A股', value: 29000 },
        { name: '盈透(IBKR)', value: 28900 },
        { name: '众安银行', value: 21300 },
        { name: '其他', value: 42000 }
    ],
    categories: {
        '现金': 15800,
        '基金': 11800,
        '股票': 79000,
        'ETH': 25000,
        'BTC': 42000
    },
    trend: [
        { date: '5-11', value: 195000 },
        { date: '5-12', value: 195500 },
        { date: '5-13', value: 195800 },
        { date: '5-14', value: 196200 },
        { date: '5-15', value: 196800 },
        { date: '5-16', value: 197200 },
        { date: '5-17', value: 197800 },
        { date: '5-18', value: 198300 },
        { date: '5-19', value: 198800 },
        { date: '5-20', value: 199200 }
    ]
};

let trendChart, accountChart, categoryChart;

// Initialize charts when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadDashboardData();
    initializeCharts();
});

// Load dashboard data
function loadDashboardData() {
    // Calculate totals
    const totalWealth = sampleData.accounts.reduce((sum, acc) => sum + acc.value, 0);
    const stockValue = 79000;
    const fundValue = 11800;
    const cashValue = 15800;
    const cryptoValue = 42000 + 25000;

    // Update stat cards
    document.getElementById('totalWealth').textContent = formatNumber(totalWealth);
    document.getElementById('stockValue').textContent = formatNumber(stockValue);
    document.getElementById('fundValue').textContent = formatNumber(fundValue);
    document.getElementById('cashValue').textContent = formatNumber(cashValue);
    document.getElementById('cryptoValue').textContent = formatNumber(cryptoValue);

    // Load assets table
    loadAssetsTable();
}

// Format numbers with thousands separator
function formatNumber(num) {
    return num.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// Load assets table data
function loadAssetsTable() {
    const tableBody = document.getElementById('assetsTableBody');
    const assets = [
        {
            account: '微信',
            category: '现金',
            symbol: 'CNY',
            quantity: 10000,
            avgCost: 1.0,
            currentPrice: 1.0,
            value: 10000,
            profit: 0,
            profitRate: 0
        },
        {
            account: '支付宝',
            category: '余额宝',
            symbol: 'CNY',
            quantity: 8000,
            avgCost: 1.0,
            currentPrice: 1.0,
            value: 8000,
            profit: 0,
            profitRate: 0
        },
        {
            account: '支付宝',
            category: '基金',
            symbol: '易方达沪深300',
            quantity: 1000,
            avgCost: 3.5,
            currentPrice: 3.8,
            value: 3800,
            profit: 300,
            profitRate: 8.57
        },
        {
            account: 'A股',
            category: '股票',
            symbol: '茅台',
            quantity: 10,
            avgCost: 2000,
            currentPrice: 2500,
            value: 25000,
            profit: 5000,
            profitRate: 25.0
        },
        {
            account: 'A股',
            category: 'ETF',
            symbol: '510300',
            quantity: 500,
            avgCost: 4.0,
            currentPrice: 4.8,
            value: 2400,
            profit: 400,
            profitRate: 20.0
        },
        {
            account: '盈透(IBKR)',
            category: '股票',
            symbol: 'AAPL',
            quantity: 100,
            avgCost: 120,
            currentPrice: 180,
            value: 12780,
            profit: 6000,
            profitRate: 50.0
        },
        {
            account: '盈透(IBKR)',
            category: '股票',
            symbol: 'TSLA',
            quantity: 50,
            avgCost: 200,
            currentPrice: 250,
            value: 8900,
            profit: 2500,
            profitRate: 25.0
        },
        {
            account: '盈透(IBKR)',
            category: '现金',
            symbol: 'USD',
            quantity: 5000,
            avgCost: 1.0,
            currentPrice: 7.1,
            value: 35500,
            profit: 0,
            profitRate: 0
        },
        {
            account: '众安银行',
            category: '现金',
            symbol: 'USD',
            quantity: 3000,
            avgCost: 1.0,
            currentPrice: 7.1,
            value: 21300,
            profit: 0,
            profitRate: 0
        },
        {
            account: '其他',
            category: '加密货币',
            symbol: 'BTC',
            quantity: 0.1,
            avgCost: 300000,
            currentPrice: 420000,
            value: 42000,
            profit: 12000,
            profitRate: 40.0
        },
        {
            account: '其他',
            category: '加密货币',
            symbol: 'ETH',
            quantity: 1.0,
            avgCost: 20000,
            currentPrice: 25000,
            value: 25000,
            profit: 5000,
            profitRate: 25.0
        }
    ];

    tableBody.innerHTML = assets.map(asset => `
        <tr>
            <td><strong>${asset.account}</strong></td>
            <td>${asset.category}</td>
            <td>${asset.symbol}</td>
            <td>${asset.quantity.toFixed(4)}</td>
            <td>¥${formatNumber(asset.avgCost)}</td>
            <td>¥${formatNumber(asset.currentPrice)}</td>
            <td>¥${formatNumber(asset.value)}</td>
            <td style="color: ${asset.profit >= 0 ? '#28a745' : '#dc3545'}">
                ${asset.profit >= 0 ? '+' : ''}¥${formatNumber(asset.profit)}
            </td>
            <td style="color: ${asset.profitRate >= 0 ? '#28a745' : '#dc3545'}">
                ${asset.profitRate >= 0 ? '+' : ''}${asset.profitRate.toFixed(2)}%
            </td>
        </tr>
    `).join('');
}

// Initialize all charts
function initializeCharts() {
    initTrendChart();
    initAccountChart();
    initCategoryChart();
}

// Trend chart (line chart)
function initTrendChart() {
    const ctx = document.getElementById('trendChart').getContext('2d');
    const dates = sampleData.trend.map(d => d.date);
    const values = sampleData.trend.map(d => d.value);
    const minValue = Math.min(...values);
    const maxValue = Math.max(...values);

    trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: '总资产 (CNY)',
                data: values,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 5,
                pointBackgroundColor: '#667eea',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        font: { size: 12, weight: 'bold' }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    min: minValue * 0.99,
                    max: maxValue * 1.01,
                    ticks: {
                        callback: function(value) {
                            return '¥' + formatNumber(value);
                        }
                    }
                }
            }
        }
    });
}

// Account distribution chart (pie chart)
function initAccountChart() {
    const ctx = document.getElementById('accountChart').getContext('2d');
    const labels = sampleData.accounts.map(a => a.name);
    const values = sampleData.accounts.map(a => a.value);
    const colors = [
        '#667eea',
        '#764ba2',
        '#f093fb',
        '#4facfe',
        '#00f2fe',
        '#43e97b'
    ];

    accountChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
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
                    position: 'right',
                    labels: {
                        padding: 15,
                        font: { size: 12 }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `¥${formatNumber(value)} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Category distribution chart (pie chart)
function initCategoryChart() {
    const ctx = document.getElementById('categoryChart').getContext('2d');
    const labels = Object.keys(sampleData.categories);
    const values = Object.values(sampleData.categories);
    const colors = [
        '#43e97b',
        '#38f9d7',
        '#fa709a',
        '#fee140',
        '#30b0fe'
    ];

    categoryChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
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
                    position: 'right',
                    labels: {
                        padding: 15,
                        font: { size: 12 }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `¥${formatNumber(value)} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}
