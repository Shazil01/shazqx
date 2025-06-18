// Connect to backend WebSocket
const socket = new WebSocket('ws://localhost:8000/ws');

// Chart initialization
const ctx = document.getElementById('price-chart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Price',
            borderColor: '#50fa7b',
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});

// Bot control
document.getElementById('start-bot').addEventListener('click', () => {
    const statusElement = document.getElementById('bot-status');
    if (statusElement.textContent === 'OFFLINE') {
        socket.send(JSON.stringify({ action: 'start_bot' }));
        statusElement.textContent = 'LIVE';
        statusElement.className = 'status LIVE';
    } else {
        socket.send(JSON.stringify({ action: 'stop_bot' }));
        statusElement.textContent = 'OFFLINE';
        statusElement.className = 'status OFFLINE';
    }
});

// WebSocket message handling
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data.type === 'price_update') {
        // Update chart
        chart.data.labels = data.labels;
        chart.data.datasets[0].data = data.prices;
        chart.update();
    } 
    else if (data.type === 'signal') {
        // Add new signal
        const signalElement = document.createElement('div');
        signalElement.className = 'signal';
        signalElement.innerHTML = `
            <strong>${data.direction} ${data.pair}</strong>
            <span>Entry: ${data.entry} | TP: ${data.tp} | SL: ${data.sl}</span>
        `;
        document.getElementById('signal-list').prepend(signalElement);
    }
};