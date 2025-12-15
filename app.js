// 加载数据并渲染图表
let metricsData = {};
let explanationsData = {};

async function loadData() {
    try {
        const response = await fetch('/static/website_metrics.json');
        metricsData = await response.json();
        
        // 加载详细说明
        try {
            const explanationsResponse = await fetch('/static/detailed_explanations.json');
            explanationsData = await explanationsResponse.json();
        } catch (e) {
            console.warn('详细说明加载失败，使用默认说明');
            explanationsData = {};
        }
        
        updateMetrics();
        renderCharts();
        renderExplanations();
    } catch (error) {
        console.error('加载数据失败:', error);
        // 使用默认数据
        metricsData = getDefaultData();
        updateMetrics();
        renderCharts();
    }
}

function getDefaultData() {
    return {
        overview: {
            total_conversations: 800,
            total_messages: 13146,
            usage_days: 300,
            daily_avg_conversations: 3.4,
            daily_avg_messages: 53.2
        },
        conversation_types: {
            technical: { percentage: 57.9 },
            business: { percentage: 6.9 },
            creative: { percentage: 16.1 },
            learning: { percentage: 15.0 },
            daily: { percentage: 5.0 }
        },
        technical: {
            tool: { conversation_percentage: 43.4 }
        },
        interaction: {
            conversation_length: { average: 16.4 },
            interaction_modes: { collaborative: 40, guidance: 35, qa: 25 }
        },
        personality: {
            indices: { tech_depth: 26.6, creative_exploration: 30.9, workflow_integration: 61.4 }
        },
        time_patterns: {
            active_hours: {
                hourly_distribution: {}
            }
        }
    };
}

function updateMetrics() {
    const overview = metricsData.overview || {};
    const technical = metricsData.technical || {};
    const interaction = metricsData.interaction || {};
    const personality = metricsData.personality || {};

    document.getElementById('total-convs').textContent = overview.total_conversations || 800;
    document.getElementById('total-msgs').textContent = (overview.total_messages || 13146).toLocaleString();
    document.getElementById('usage-days').textContent = overview.usage_days || 300;
    document.getElementById('tool-usage').textContent = (technical.tool?.conversation_percentage || 43.4).toFixed(1) + '%';
    document.getElementById('avg-length').textContent = (interaction.conversation_length?.average || 16.4).toFixed(1);
    document.getElementById('tech-depth').textContent = (personality.indices?.tech_depth || 26.6).toFixed(1);
}

function renderCharts() {
    renderConversationTypesChart();
    renderTechnicalChart();
    renderTimeChart();
    renderInteractionChart();
    renderRadarChart();
}

// 对话类型分布饼图
function renderConversationTypesChart() {
    const ctx = document.getElementById('conversationTypesChart');
    const types = metricsData.conversation_types || {};
    
    const data = {
        labels: [
            '深度技术咨询',
            '商务文档优化',
            '创意设计协作',
            '专业知识学习',
            '日常实用咨询'
        ],
        datasets: [{
            data: [
                types.technical?.percentage || 57.9,
                types.business?.percentage || 6.9,
                types.creative?.percentage || 16.1,
                types.learning?.percentage || 15.0,
                types.daily?.percentage || 5.0
            ],
            backgroundColor: [
                '#6366f1',
                '#8b5cf6',
                '#ec4899',
                '#10b981',
                '#f59e0b'
            ],
            borderWidth: 2,
            borderColor: '#1e293b'
        }]
    };

    new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: '#cbd5e1',
                        font: { size: 14 },
                        padding: 15
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.label + ': ' + context.parsed + '%';
                        }
                    }
                }
            }
        }
    });
}

// 技术能力使用柱状图
function renderTechnicalChart() {
    const ctx = document.getElementById('technicalChart');
    const technical = metricsData.technical || {};
    
    const data = {
        labels: ['代码', '图片', '工具', '多模态'],
        datasets: [{
            label: '对话占比 (%)',
            data: [
                technical.code?.conversation_percentage || 20.0,
                technical.image?.conversation_percentage || 14.8,
                technical.tool?.conversation_percentage || 43.4,
                technical.multimodal?.conversation_percentage || 16.1
            ],
            backgroundColor: [
                'rgba(99, 102, 241, 0.8)',
                'rgba(236, 72, 153, 0.8)',
                'rgba(16, 185, 129, 0.8)',
                'rgba(245, 158, 11, 0.8)'
            ],
            borderColor: [
                '#6366f1',
                '#ec4899',
                '#10b981',
                '#f59e0b'
            ],
            borderWidth: 2
        }]
    };

    new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.parsed.y + '% 的对话使用了此功能';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 50,
                    ticks: {
                        color: '#cbd5e1',
                        callback: function(value) {
                            return value + '%';
                        }
                    },
                    grid: {
                        color: '#334155'
                    }
                },
                x: {
                    ticks: {
                        color: '#cbd5e1'
                    },
                    grid: {
                        color: '#334155'
                    }
                }
            }
        }
    });
}

// 时间使用折线图
function renderTimeChart() {
    const ctx = document.getElementById('timeChart');
    const timePatterns = metricsData.time_patterns || {};
    
    // 生成小时数据（如果没有数据，使用模拟数据）
    const hours = Array.from({ length: 24 }, (_, i) => i);
    const hourlyData = hours.map(h => {
        const dist = timePatterns.active_hours?.hourly_distribution || {};
        return dist[h] || Math.floor(Math.random() * 100);
    });
    
    // 找到最活跃的时段
    const maxIndex = hourlyData.indexOf(Math.max(...hourlyData));
    
    const data = {
        labels: hours.map(h => h + ':00'),
        datasets: [{
            label: '消息数量',
            data: hourlyData,
            borderColor: '#6366f1',
            backgroundColor: 'rgba(99, 102, 241, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.4,
            pointRadius: 4,
            pointHoverRadius: 6,
            pointBackgroundColor: '#6366f1',
            pointBorderColor: '#fff',
            pointBorderWidth: 2
        }]
    };

    new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.parsed.y + ' 条消息';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#cbd5e1'
                    },
                    grid: {
                        color: '#334155'
                    }
                },
                x: {
                    ticks: {
                        color: '#cbd5e1',
                        maxRotation: 45,
                        minRotation: 45
                    },
                    grid: {
                        color: '#334155'
                    }
                }
            }
        }
    });
}

// 交互模式饼图
function renderInteractionChart() {
    const ctx = document.getElementById('interactionChart');
    const interaction = metricsData.interaction || {};
    const modes = interaction.interaction_modes || { collaborative: 40, guidance: 35, qa: 25 };
    
    const data = {
        labels: ['协作型', '指导型', '问答型'],
        datasets: [{
            data: [modes.collaborative, modes.guidance, modes.qa],
            backgroundColor: [
                'rgba(99, 102, 241, 0.8)',
                'rgba(139, 92, 246, 0.8)',
                'rgba(236, 72, 153, 0.8)'
            ],
            borderColor: [
                '#6366f1',
                '#8b5cf6',
                '#ec4899'
            ],
            borderWidth: 2
        }]
    };

    new Chart(ctx, {
        type: 'pie',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#cbd5e1',
                        font: { size: 14 },
                        padding: 15
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.label + ': ' + context.parsed + '%';
                        }
                    }
                }
            }
        }
    });
}

// 个性化能力雷达图
function renderRadarChart() {
    const ctx = document.getElementById('radarChart');
    const personality = metricsData.personality || {};
    const indices = personality.indices || {};
    
    const data = {
        labels: ['技术深度', '创意探索', '工作流整合', '迭代优化', '多模态使用', '工具使用'],
        datasets: [{
            label: '能力指数',
            data: [
                indices.tech_depth || 26.6,
                indices.creative_exploration || 30.9,
                indices.workflow_integration || 61.4,
                personality.iterative_optimization?.percentage || 40.0,
                metricsData.technical?.multimodal?.conversation_percentage || 16.1,
                metricsData.technical?.tool?.conversation_percentage || 43.4
            ],
            backgroundColor: 'rgba(99, 102, 241, 0.2)',
            borderColor: '#6366f1',
            borderWidth: 2,
            pointBackgroundColor: '#6366f1',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: '#6366f1'
        }]
    };

    new Chart(ctx, {
        type: 'radar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.parsed.r.toFixed(1);
                        }
                    }
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        color: '#cbd5e1',
                        stepSize: 20
                    },
                    grid: {
                        color: '#334155'
                    },
                    pointLabels: {
                        color: '#cbd5e1',
                        font: { size: 12 }
                    }
                }
            }
        }
    });
}

// 渲染详细说明
function renderExplanations() {
    if (!explanationsData || Object.keys(explanationsData).length === 0) return;
    
    renderConversationTypesExplanation();
    renderTechnicalExplanation();
    renderTimeExplanation();
    renderInteractionExplanation();
    renderRadarExplanation();
}

function renderConversationTypesExplanation() {
    const container = document.getElementById('typeDetails');
    if (!container || !explanationsData.conversation_types_details) return;
    
    const types = explanationsData.conversation_types_details;
    const typeNames = {
        'technical': '深度技术咨询',
        'business': '商务文档优化',
        'creative': '创意设计协作',
        'learning': '专业知识学习',
        'daily': '日常实用咨询'
    };
    
    let html = '';
    for (const [key, data] of Object.entries(types)) {
        if (typeNames[key]) {
            html += `
                <div class="type-item">
                    <h4>${typeNames[key]}</h4>
                    <p>${data.description}</p>
                    <div class="keywords">
                        ${data.keywords.map(k => `<span class="keyword-tag">${k}</span>`).join('')}
                    </div>
                </div>
            `;
        }
    }
    container.innerHTML = html;
}

function renderTechnicalExplanation() {
    const container = document.getElementById('technicalDetails');
    if (!container || !explanationsData.technical_details) return;
    
    const details = explanationsData.technical_details;
    let html = '';
    
    if (details.languages) {
        html += '<div class="technical-detail-item"><h4>编程语言</h4><ul>';
        for (const [lang, desc] of Object.entries(details.languages)) {
            html += `<li><strong>${lang}:</strong> ${desc}</li>`;
        }
        html += '</ul></div>';
    }
    
    if (details.tools) {
        html += '<div class="technical-detail-item"><h4>工具使用</h4><ul>';
        for (const [tool, desc] of Object.entries(details.tools)) {
            html += `<li><strong>${tool}:</strong> ${desc}</li>`;
        }
        html += '</ul></div>';
    }
    
    if (details.modalities) {
        html += '<div class="technical-detail-item"><h4>多模态应用</h4>';
        for (const [mod, desc] of Object.entries(details.modalities)) {
            html += `<p>${desc}</p>`;
        }
        html += '</div>';
    }
    
    container.innerHTML = html;
}

function renderTimeExplanation() {
    const container = document.getElementById('timeAnalysisText');
    if (!container || !explanationsData.time_analysis) return;
    
    container.textContent = explanationsData.time_analysis;
}

function renderInteractionExplanation() {
    const container = document.getElementById('interactionDetails');
    if (!container || !explanationsData.interaction_details) return;
    
    const details = explanationsData.interaction_details;
    const modeNames = {
        'collaborative': '协作型',
        'guidance': '指导型',
        'qa': '问答型'
    };
    
    let html = '';
    for (const [key, data] of Object.entries(details)) {
        if (modeNames[key]) {
            html += `
                <div class="interaction-detail-item">
                    <h4>${modeNames[key]} (${data.description})</h4>
                    <div class="category-list">
                        ${data.top3_categories.map(c => `<div class="category-item">${c}</div>`).join('')}
                    </div>
                </div>
            `;
        }
    }
    container.innerHTML = html;
}

function renderRadarExplanation() {
    const container = document.getElementById('radarDetails');
    if (!container || !explanationsData.radar_explanations) return;
    
    const explanations = explanationsData.radar_explanations;
    const labels = {
        'tech_depth': '技术深度',
        'creative_exploration': '创意探索',
        'workflow_integration': '工作流整合',
        'iterative_optimization': '迭代优化',
        'multimodal_usage': '多模态使用',
        'tool_usage': '工具使用'
    };
    
    let html = '';
    for (const [key, data] of Object.entries(explanations)) {
        if (labels[key]) {
            html += `
                <div class="radar-detail-item">
                    <h4>${labels[key]}</h4>
                    <div class="interpretation">${data.interpretation}</div>
                    <div class="algorithm">算法: ${data.algorithm}</div>
                </div>
            `;
        }
    }
    container.innerHTML = html;
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', function() {
    loadData();
});

