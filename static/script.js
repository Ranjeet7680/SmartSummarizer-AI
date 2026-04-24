// Global variables
let selectedLength = 'medium';
let currentText = '';

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    updateInputStats();
});

function setupEventListeners() {
    // PDF Upload
    const uploadArea = document.getElementById('uploadArea');
    const pdfInput = document.getElementById('pdfInput');
    const inputText = document.getElementById('inputText');

    uploadArea.addEventListener('click', () => pdfInput.click());
    
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        const file = e.dataTransfer.files[0];
        if (file) {
            if (file.type === 'application/pdf') {
                handlePDFUpload(file);
            } else {
                showNotification('⚠️ Please upload a PDF file', 'warning');
            }
        }
    });

    pdfInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handlePDFUpload(file);
        }
    });

    // Text input stats
    inputText.addEventListener('input', updateInputStats);

    // Length buttons
    document.querySelectorAll('.length-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.length-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            selectedLength = this.dataset.length;
        });
    });
}

async function handlePDFUpload(file) {
    const formData = new FormData();
    formData.append('file', file);

    showNotification('📄 Extracting text from PDF...', 'info');

    try {
        const response = await fetch('/api/upload-pdf', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.success) {
            document.getElementById('inputText').value = data.text;
            currentText = data.text;
            updateInputStats();
            showNotification(`✅ Extracted ${data.word_count} words from PDF!`, 'success');
        } else {
            showNotification('❌ ' + (data.error || 'Failed to process PDF'), 'error');
        }
    } catch (error) {
        console.error('PDF upload error:', error);
        showNotification('❌ Error uploading PDF: ' + error.message, 'error');
    }
}

async function summarize() {
    const inputText = document.getElementById('inputText').value.trim();
    
    if (!inputText) {
        showNotification('⚠️ Please enter some text or upload a PDF', 'warning');
        return;
    }

    const btn = document.querySelector('.summarize-btn');
    const btnText = btn.querySelector('.btn-text');
    const loader = btn.querySelector('.loader');

    // Disable button and show loader
    btn.disabled = true;
    btnText.textContent = 'Generating Summary...';
    loader.style.display = 'inline-block';

    try {
        const response = await fetch('/api/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: inputText,
                length: selectedLength
            })
        });

        const data = await response.json();

        if (data.success) {
            displaySummary(data.summary, data.original_length, data.summary_length);
            showNotification('✅ Summary generated successfully!', 'success');
        } else {
            showNotification('❌ ' + data.error, 'error');
        }
    } catch (error) {
        showNotification('❌ Error: ' + error.message, 'error');
    } finally {
        // Re-enable button
        btn.disabled = false;
        btnText.textContent = '✨ Summarize';
        loader.style.display = 'none';
    }
}

function displaySummary(summary, originalLength, summaryLength) {
    const outputContent = document.getElementById('outputContent');
    const outputStats = document.getElementById('outputStats');
    
    // Display summary with typing effect
    outputContent.innerHTML = `<div class="summary-text">${summary}</div>`;
    
    // Update stats
    document.getElementById('outputWords').textContent = summaryLength;
    const reduction = Math.round((1 - summaryLength / originalLength) * 100);
    document.getElementById('reduction').textContent = reduction + '%';
    
    outputStats.style.display = 'flex';
}

function updateInputStats() {
    const text = document.getElementById('inputText').value;
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    const chars = text.length;
    
    document.getElementById('inputWords').textContent = words;
    document.getElementById('inputChars').textContent = chars;
}

function copySummary() {
    const summaryText = document.querySelector('.summary-text').textContent;
    navigator.clipboard.writeText(summaryText).then(() => {
        showNotification('📋 Summary copied to clipboard!', 'success');
    });
}

function toggleTheme() {
    document.body.classList.toggle('light-mode');
    const btn = document.querySelector('.theme-toggle');
    btn.textContent = document.body.classList.contains('light-mode') ? '☀️' : '🌙';
}

function showNotification(message, type) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        background: ${type === 'success' ? '#00b894' : type === 'error' ? '#d63031' : type === 'warning' ? '#fdcb6e' : '#6c5ce7'};
        color: white;
        border-radius: 10px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        z-index: 1000;
        animation: slideIn 0.3s ease;
        font-weight: 600;
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
