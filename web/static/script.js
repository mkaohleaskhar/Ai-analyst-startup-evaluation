// Create floating particles
function createParticles() {
    const particlesContainer = document.getElementById('particles');
    if (!particlesContainer) return;
    const particleCount = 20;
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.width = Math.random() * 20 + 10 + 'px';
        particle.style.height = particle.style.width;
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 20 + 's';
        particle.style.animationDuration = Math.random() * 20 + 20 + 's';
        particlesContainer.appendChild(particle);
    }
}
createParticles();

// --- DOM ELEMENTS ---
const subtitle = document.getElementById('subtitle');
const showAnalysisBtn = document.getElementById('show-analysis-btn');
const showDealNotesBtn = document.getElementById('show-deal-notes-btn');

// Investment Analysis Elements
const uploadForm = document.getElementById('upload-form');
const dynamicFileInputContainer = document.getElementById('dynamic-file-input-container');
const addFileBtn = document.getElementById('add-file-btn');
const analyzeBtn = document.getElementById('analyze-btn');
const analyzeAnotherBtn = document.getElementById('analyze-another-btn');
const resultsContainer = document.getElementById('results-container');
const spinner = document.getElementById('spinner');
const reportsContainer = document.getElementById('reports-container');

// Deal Notes Elements
const dealNotesForm = document.getElementById('deal-notes-form');
const dealNotesFileInput = document.getElementById('deal-notes-file-input');
const dealNotesUploadArea = document.getElementById('deal-notes-upload-area');
const dealNotesSelectedFilesDiv = document.getElementById('deal-notes-selected-files');
const generateNotesBtn = document.getElementById('generate-notes-btn');
const generateAnotherBtn = document.getElementById('generate-another-btn');
const dealNotesResultsContainer = document.getElementById('deal-notes-results-container');
const dealNotesSpinner = document.getElementById('deal-notes-spinner');
const dealNotesReportContainer = document.getElementById('deal-notes-report-container');

// --- TOGGLE LOGIC ---
showAnalysisBtn.addEventListener('click', () => {
    uploadForm.classList.remove('hidden');
    dealNotesForm.classList.add('hidden');
    showAnalysisBtn.classList.add('active');
    showDealNotesBtn.classList.remove('active');
    subtitle.textContent = 'Upload one or more pitch decks (.txt or .pdf) to begin analysis';
});
showDealNotesBtn.addEventListener('click', () => {
    uploadForm.classList.add('hidden');
    dealNotesForm.classList.remove('hidden');
    showAnalysisBtn.classList.remove('active');
    showDealNotesBtn.classList.add('active');
    subtitle.textContent = 'Upload pitch decks, transcripts, emails, etc. to generate deal notes';
});

// --- INVESTMENT ANALYSIS DYNAMIC FILE INPUT LOGIC ---
addFileBtn.addEventListener('click', addFileInputRow);

function addFileInputRow() {
    const row = document.createElement('div');
    row.className = 'file-input-row';

    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.name = 'files[]'; // Use array notation for name
    fileInput.accept = '.txt,.pdf';
    fileInput.addEventListener('change', checkAnalyzeButtonState);

    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.className = 'remove-file-btn';
    removeBtn.textContent = '-';
    removeBtn.addEventListener('click', () => {
        row.remove();
        checkAnalyzeButtonState();
        if (dynamicFileInputContainer.children.length === 0) {
            addFileBtn.textContent = 'Add File';
        }
    });

    row.appendChild(fileInput);
    row.appendChild(removeBtn);
    dynamicFileInputContainer.appendChild(row);

    addFileBtn.textContent = 'Add Another File';
    checkAnalyzeButtonState();
}

function checkAnalyzeButtonState() {
    const allInputs = dynamicFileInputContainer.querySelectorAll('input[type="file"]');
    let hasFile = false;
    allInputs.forEach(input => {
        if (input.files.length > 0) {
            hasFile = true;
        }
    });
    analyzeBtn.disabled = !hasFile;
}

// --- DEAL NOTES FILE HANDLING (Original Logic) ---
setupDragAndDrop(dealNotesUploadArea, dealNotesFileInput, () => updateSelectedFiles(dealNotesFileInput, dealNotesSelectedFilesDiv, generateNotesBtn));
dealNotesFileInput.addEventListener('change', () => updateSelectedFiles(dealNotesFileInput, dealNotesSelectedFilesDiv, generateNotesBtn));

function setupDragAndDrop(area, input, callback) {
    area.addEventListener('dragover', (e) => { e.preventDefault(); area.classList.add('dragover'); });
    area.addEventListener('dragleave', () => { area.classList.remove('dragover'); });
    area.addEventListener('drop', (e) => {
        e.preventDefault();
        area.classList.remove('dragover');
        input.files = e.dataTransfer.files;
        callback();
    });
}
function updateSelectedFiles(input, container, button) {
    const files = Array.from(input.files);
    if (files.length > 0) {
        container.innerHTML = '<h3>Selected Files:</h3>';
        files.forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.innerHTML = `<span class="file-icon">📄</span> <span>${file.name} (${(file.size / 1024).toFixed(2)} KB)</span>`;
            container.appendChild(fileItem);
        });
        container.classList.add('show');
        button.disabled = false;
    } else {
        container.classList.remove('show');
        container.innerHTML = '';
        button.disabled = true;
    }
}

// --- FORM SUBMISSION ---
uploadForm.addEventListener('submit', handleAnalysisSubmit);
dealNotesForm.addEventListener('submit', handleDealNotesSubmit);

analyzeAnotherBtn.addEventListener('click', () => {
    resultsContainer.classList.add('hidden');
    reportsContainer.innerHTML = '';
    dynamicFileInputContainer.innerHTML = '';
    addFileBtn.textContent = 'Add File';
    analyzeBtn.disabled = true;
    analyzeAnotherBtn.classList.add('hidden');
});
generateAnotherBtn.addEventListener('click', () => resetForm(dealNotesResultsContainer, dealNotesReportContainer, dealNotesFileInput, dealNotesSelectedFilesDiv, generateNotesBtn, generateAnotherBtn));

function resetForm(results, reports, input, selected, submitBtn, anotherBtn) {
    results.classList.add('hidden');
    reports.innerHTML = '';
    input.value = '';
    selected.innerHTML = '';
    selected.classList.remove('show');
    submitBtn.disabled = true;
    anotherBtn.classList.add('hidden');
}

async function handleAnalysisSubmit(e) {
    e.preventDefault();
    const allInputs = dynamicFileInputContainer.querySelectorAll('input[type="file"]');
    const files = [];
    allInputs.forEach(input => {
        if (input.files.length > 0) {
            files.push(input.files[0]);
        }
    });

    if (files.length === 0) return;

    setLoadingState(analyzeBtn, 'Analyzing...', resultsContainer, spinner, reportsContainer);

    for (const file of files) {
        const formData = new FormData();
        formData.append('file', file);
        try {
            const response = await fetch('/analyze', { method: 'POST', body: formData });
            if (!response.ok) throw new Error((await response.json()).error || `HTTP error! status: ${response.status}`);
            displayAnalysisReport(await response.json(), file.name);
        } catch (error) {
            reportsContainer.innerHTML += createErrorCard(file.name, error.message);
        }
    }
    resetLoadingState(analyzeBtn, 'Analyze Pitch Decks', spinner, analyzeAnotherBtn);
}

async function handleDealNotesSubmit(e) {
    e.preventDefault();
    const files = Array.from(dealNotesFileInput.files);
    if (files.length === 0) return;

    setLoadingState(generateNotesBtn, 'Generating...', dealNotesResultsContainer, dealNotesSpinner, dealNotesReportContainer);
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));

    try {
        const response = await fetch('/deal-notes', { method: 'POST', body: formData });
        if (!response.ok) throw new Error((await response.json()).error || `HTTP error! status: ${response.status}`);
        displayDealNotes(await response.json());
    } catch (error) {
        dealNotesReportContainer.innerHTML = createErrorCard('Deal Notes Generation', error.message);
    }
    resetLoadingState(generateNotesBtn, 'Generate Deal Notes', dealNotesSpinner, generateAnotherBtn);
}

function setLoadingState(btn, text, results, spinner, reports) {
    btn.disabled = true;
    btn.textContent = text;
    results.classList.remove('hidden');
    results.classList.add('show');
    spinner.classList.remove('hidden');
    reports.innerHTML = '';
}

function resetLoadingState(btn, text, spinner, anotherBtn) {
    spinner.classList.add('hidden');
    btn.disabled = false;
    btn.textContent = text;
    anotherBtn.classList.remove('hidden');
}

// --- DISPLAY FUNCTIONS ---
// (Keep all the existing display functions: displayAnalysisReport, displayDealNotes, createErrorCard, createAnalysisReportCard, etc.)
function displayAnalysisReport(data, filename) {
    const reportCard = createAnalysisReportCard(data, reportsContainer.children.length, filename);
    reportsContainer.appendChild(reportCard);
}

function displayDealNotes(data) {
    const dealNotesCard = createDealNotesCard(data);
    dealNotesReportContainer.appendChild(dealNotesCard);
}

function createErrorCard(title, message) {
    return `<div class="report-card"><div class="report-header"><div class="report-title">${title}</div><div class="report-status" style="background: linear-gradient(135deg, #f44336, #e91e63);">Error</div></div><div class="report-content">Failed to process.<br><strong>Error:</strong> ${message}</div></div>`;
}

function createAnalysisReportCard(report, index, filename) {
    const card = document.createElement('div');
    card.className = 'report-card';
    card.style.animationDelay = `${index * 0.1}s`;

    const recommendation = report.recommendation || {};
    const rec_text = `${recommendation.recommendation || 'N/A'} (${recommendation.confidence || 'N/A'}%)`;

    card.innerHTML = `
        <div class="report-header">
            <div class="report-title">${filename}</div>
            <div class="report-status">${rec_text}</div>
        </div>
        <p><b>Rationale:</b> ${recommendation.investment_rationale || 'N/A'}</p>
        <div class="viz-container">
            <div class="risk-dashboard-container"></div>
            <div class="chart-container"><canvas id="radarChart-${index}"></canvas></div>
        </div>
        <div class="benchmark-container chart-container"><canvas id="bubbleChart-${index}"></canvas></div>
        <div class="accordion-title" id="accordion-title-${index}">Show/Hide Raw Data</div>
        <div class="accordion-content" id="accordion-content-${index}"></div>
    `;

    createRiskDashboard(report.risk, card.querySelector('.risk-dashboard-container'));
    createRadarChart(report, card.querySelector(`#radarChart-${index}`));
    createBubbleChart(report, card.querySelector(`#bubbleChart-${index}`));
    createDetailsAccordion(report, card.querySelector(`#accordion-content-${index}`), card.querySelector(`#accordion-title-${index}`));

    return card;
}

function createRiskDashboard(risk, container) {
    if (!risk || !container) return;
    const riskOrder = ['Financial', 'Market', 'Execution', 'Overall'];
    container.innerHTML = '<h5 class="chart-title">Risk Flag Dashboard</h5><div class="risk-dashboard"></div>';
    const dashboard = container.querySelector('.risk-dashboard');
    riskOrder.forEach(key => {
        const riskKey = `${key.toLowerCase()}_risk`;
        const level = (risk[riskKey] || 'LOW').toUpperCase();
        const flag = document.createElement('div');
        flag.className = `risk-flag ${level}`;
        flag.innerHTML = `<span>${key}</span>`;
        dashboard.appendChild(flag);
    });
}

function createRadarChart(report, canvas) {
    if (!report || !canvas) return;
    const riskToScore = (level) => ({ 'HIGH': 1, 'MEDIUM': 3, 'LOW': 5 }[level.toUpperCase()] || 0);
    const data = {
        labels: ['Financial', 'Market', 'Team', 'Execution', 'Benchmark'],
        datasets: [{
            label: 'Startup Score (out of 5)',
            data: [
                riskToScore(report.risk?.financial_risk || 'LOW'),
                riskToScore(report.risk?.market_risk || 'LOW'),
                (report.team?.founders_background?.includes('Error') ? 1 : 4),
                riskToScore(report.risk?.execution_risk || 'LOW'),
                (report.benchmark?.benchmark_summary?.includes('strong') ? 4 : 2)
            ],
            fill: true,
            backgroundColor: 'rgba(102, 126, 234, 0.2)',
            borderColor: 'rgb(102, 126, 234)',
            pointBackgroundColor: 'rgb(102, 126, 234)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(102, 126, 234)'
        }]
    };
    new Chart(canvas, { type: 'radar', data: data, options: { responsive: true, maintainAspectRatio: false, scales: { r: { beginAtZero: true, max: 5 } } } });
}

function createBubbleChart(report, canvas) {
    if (!report || !canvas) return;
    const parseCurrency = (str) => parseFloat(str?.replace(/[^\d.-]/g, '')) || 0;
    const tam = parseCurrency(report.metrics?.tam);
    const ltv = parseCurrency(report.metrics?.ltv);
    const cac = parseCurrency(report.metrics?.cac) || 1;
    const data = {
        datasets: [{
            label: report.company_name || 'This Startup',
            data: [{
                x: tam,
                y: ltv / cac,
                r: report.recommendation?.confidence || 50
            }],
            backgroundColor: 'rgba(118, 75, 162, 0.7)'
        }]
    };
    new Chart(canvas, { type: 'bubble', data: data, options: { responsive: true, maintainAspectRatio: false, plugins: { title: { display: true, text: 'Benchmark: Market Size vs. LTV/CAC Ratio' } }, scales: { x: { type: 'logarithmic', title: { display: true, text: 'Total Addressable Market (TAM) - Log Scale' } }, y: { title: { display: true, text: 'LTV / CAC Ratio' } } } } });
}

function createDetailsAccordion(report, contentContainer, title) {
    if (!report || !contentContainer || !title) return;
    const { recommendation, metrics, team, public_data, risk, benchmark } = report;
    contentContainer.innerHTML = `
        <h5>Metrics:</h5>
        <ul>
            <li>Revenue: ${metrics?.revenue || 'N/A'}</li>
            <li>CAC: ${metrics?.cac || 'N/A'}</li>
            <li>LTV: ${metrics?.ltv || 'N/A'}</li>
            <li>TAM: ${metrics?.tam || 'N/A'}</li>
            <li>SAM: ${metrics?.sam || 'N/A'}</li>
            <li>SOM: ${metrics?.som || 'N/A'}</li>
        </ul>
        <h5>Team:</h5> <p>${team?.founders_background || 'N/A'}</p>
        <h5>Public Data:</h5> <p>${public_data?.public_data_summary || 'N/A'}</p>
        <h5>Benchmark:</h5> <p>${benchmark?.benchmark_summary || 'N/A'}</p>
    `;
    title.addEventListener('click', () => {
        const isVisible = contentContainer.style.display === 'block';
        contentContainer.style.display = isVisible ? 'none' : 'block';
    });
}

function createDealNotesCard(data) {
    const card = document.createElement('div');
    card.className = 'report-card';
    card.innerHTML = `
        <div class="report-header"><div class="report-title">Consolidated Deal Notes</div><div class="report-status">Generated</div></div>
        <div class="report-content">
            <h4>Company Summary</h4><p>${data.company_summary || 'N/A'}</p>
            <h4>Recent Updates</h4><p>${data.recent_updates || 'N/A'}</p>
            <h4>Key Discussion Points</h4><p>${data.key_discussion_points || 'N/A'}</p>
            <h4>Action Items</h4><p>${data.action_items || 'N/A'}</p>
            <h4>Red Flags</h4><p>${data.red_flags || 'N/A'}</p>
        </div>
    `;
    return card;
}