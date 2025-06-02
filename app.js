// ML Project Dashboard JavaScript

// Project data
const projectData = {
  timeline: [
    {"Date": "2025-06-02", "Day": 1, "Phase": "Setup e Planejamento", "Activity": "Setup do repositório e ambiente", "Responsible": "Leonardo", "Priority": "MUST", "Urgency": "High", "Complexity": "Medium", "Estimated_Hours": 8},
    {"Date": "2025-06-03", "Day": 2, "Phase": "Setup e Planejamento", "Activity": "Criação de dataset mínimo", "Responsible": "Nathan", "Priority": "MUST", "Urgency": "High", "Complexity": "Low", "Estimated_Hours": 6},
    {"Date": "2025-06-04", "Day": 3, "Phase": "Coleta e Processamento", "Activity": "Coleta de dados principal", "Responsible": "Nathan", "Priority": "MUST", "Urgency": "High", "Complexity": "Medium", "Estimated_Hours": 8},
    {"Date": "2025-06-05", "Day": 4, "Phase": "Coleta e Processamento", "Activity": "Rotulagem inicial", "Responsible": "Letícia, Luan", "Priority": "MUST", "Urgency": "High", "Complexity": "High", "Estimated_Hours": 12},
    {"Date": "2025-06-06", "Day": 5, "Phase": "Coleta e Processamento", "Activity": "Pipeline de processamento", "Responsible": "Nathan, Luan", "Priority": "MUST", "Urgency": "High", "Complexity": "Medium", "Estimated_Hours": 10},
    {"Date": "2025-06-07", "Day": 6, "Phase": "Modelo Básico", "Activity": "Baseline com DistilBERT", "Responsible": "Leonardo, Letícia", "Priority": "MUST", "Urgency": "High", "Complexity": "High", "Estimated_Hours": 12},
    {"Date": "2025-06-08", "Day": 7, "Phase": "Modelo Básico", "Activity": "Avaliação inicial", "Responsible": "Carlos, Letícia", "Priority": "MUST", "Urgency": "Medium", "Complexity": "Medium", "Estimated_Hours": 6},
    {"Date": "2025-06-09", "Day": 8, "Phase": "Modelo Básico", "Activity": "Ajustes e refinamentos", "Responsible": "Leonardo, Letícia", "Priority": "SHOULD", "Urgency": "Medium", "Complexity": "High", "Estimated_Hours": 8},
    {"Date": "2025-06-10", "Day": 9, "Phase": "Multi-Label e Interface", "Activity": "Classificação multi-label", "Responsible": "Letícia, Luan", "Priority": "SHOULD", "Urgency": "Medium", "Complexity": "High", "Estimated_Hours": 10},
    {"Date": "2025-06-11", "Day": 10, "Phase": "Multi-Label e Interface", "Activity": "Interface Streamlit", "Responsible": "Carlos, Luan", "Priority": "SHOULD", "Urgency": "Medium", "Complexity": "Low", "Estimated_Hours": 6},
    {"Date": "2025-06-12", "Day": 11, "Phase": "Multi-Label e Interface", "Activity": "Documentação inicial", "Responsible": "Carlos", "Priority": "MUST", "Urgency": "Low", "Complexity": "Low", "Estimated_Hours": 4},
    {"Date": "2025-06-13", "Day": 12, "Phase": "Refinamento e Testes", "Activity": "Refinamento de modelos", "Responsible": "Leonardo, Letícia", "Priority": "COULD", "Urgency": "Medium", "Complexity": "High", "Estimated_Hours": 8},
    {"Date": "2025-06-14", "Day": 13, "Phase": "Refinamento e Testes", "Activity": "Testes extensivos", "Responsible": "Carlos, Nathan", "Priority": "SHOULD", "Urgency": "High", "Complexity": "Medium", "Estimated_Hours": 8},
    {"Date": "2025-06-15", "Day": 14, "Phase": "Finalização", "Activity": "Revisão de código", "Responsible": "Leonardo", "Priority": "MUST", "Urgency": "High", "Complexity": "Low", "Estimated_Hours": 6},
    {"Date": "2025-06-16", "Day": 15, "Phase": "Finalização", "Activity": "Documentação final", "Responsible": "All Team", "Priority": "MUST", "Urgency": "High", "Complexity": "Medium", "Estimated_Hours": 8},
    {"Date": "2025-06-17", "Day": 16, "Phase": "Entrega", "Activity": "Entrega Final", "Responsible": "All Team", "Priority": "MUST", "Urgency": "High", "Complexity": "Low", "Estimated_Hours": 4}
  ],
  teamMembers: {
    "Leonardo": {
      "role": "Tech Lead e Mentor Principal",
      "experience": "Senior",
      "specialization": "Arquitetura de ML, Mentoria",
      "responsibilities": ["Definição da arquitetura geral", "Revisão de código", "Mentoria técnica"]
    },
    "Letícia": {
      "role": "Product Owner Técnico",
      "experience": "Intermediário",
      "specialization": "Experimentação de modelos",
      "responsibilities": ["Priorização de experimentos", "Critérios de aceitação", "Gestão de backlog"]
    },
    "Nathan": {
      "role": "Data Steward",
      "experience": "Intermediário",
      "specialization": "Análise de dados, Engenharia de features",
      "responsibilities": ["Exploração de dados", "Pipeline de processamento", "Qualidade de dados"]
    },
    "Luan": {
      "role": "Desenvolvedor Júnior",
      "experience": "Júnior",
      "specialization": "Implementação",
      "responsibilities": ["Componentes de ML", "Scripts de treinamento", "Pair programming"]
    },
    "Carlos": {
      "role": "Desenvolvedor Júnior",
      "experience": "Júnior", 
      "specialization": "Testes e Validação",
      "responsibilities": ["Testes de componentes", "Validação de modelos", "Análise de resultados"]
    }
  }
};

// State management
let completedActivities = new Set();
let currentFilters = {
  responsible: '',
  priority: ''
};

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
  initializeNavigation();
  updateCountdown();
  populateTimeline();
  populateTeamMembers();
  initializeCharts();
  initializeFilters();
  updateProgress();
  
  // Update countdown every hour
  setInterval(updateCountdown, 3600000);
});

// Navigation functionality
function initializeNavigation() {
  const navTabs = document.querySelectorAll('.nav-tab');
  const sections = document.querySelectorAll('.dashboard-section');
  
  navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetSection = tab.dataset.section;
      
      // Update active tab
      navTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      
      // Update active section
      sections.forEach(s => s.classList.remove('active'));
      document.getElementById(targetSection).classList.add('active');
    });
  });
}

// Countdown functionality
function updateCountdown() {
  const deadline = new Date('2025-06-17T23:59:59');
  const now = new Date();
  const timeDiff = deadline - now;
  const daysLeft = Math.max(0, Math.ceil(timeDiff / (1000 * 60 * 60 * 24)));
  
  document.getElementById('daysLeft').textContent = daysLeft;
  
  // Update urgency status
  const statusIndicator = document.querySelector('.status--warning');
  if (daysLeft <= 5) {
    statusIndicator.className = 'status status--error';
    statusIndicator.textContent = `Crítico - ${daysLeft} dias restantes`;
  } else if (daysLeft <= 10) {
    statusIndicator.textContent = `Urgente - ${daysLeft} dias restantes`;
  }
}

// Timeline functionality
function populateTimeline() {
  const container = document.getElementById('timelineActivities');
  container.innerHTML = '';
  
  const filteredActivities = filterActivities();
  
  filteredActivities.forEach((activity, index) => {
    const activityElement = createActivityElement(activity, index);
    container.appendChild(activityElement);
  });
}

function createActivityElement(activity, index) {
  const div = document.createElement('div');
  div.className = `activity-item ${completedActivities.has(index) ? 'completed' : ''}`;
  
  const phaseClass = getPhaseClass(activity.Phase);
  
  div.innerHTML = `
    <input type="checkbox" class="activity-checkbox" 
           ${completedActivities.has(index) ? 'checked' : ''} 
           onchange="toggleActivity(${index})">
    <div class="activity-phase ${phaseClass}"></div>
    <div class="activity-content">
      <div class="activity-info">
        <h4>Dia ${activity.Day}: ${activity.Activity}</h4>
        <div class="activity-meta">${activity.Date} • ${activity.Phase}</div>
      </div>
      <div class="activity-responsible">${activity.Responsible}</div>
      <div class="activity-priority priority-${activity.Priority.toLowerCase()}">${activity.Priority}</div>
      <div class="activity-hours">${activity.Estimated_Hours}h</div>
    </div>
  `;
  
  return div;
}

function getPhaseClass(phase) {
  const phaseMap = {
    'Setup e Planejamento': 'setup',
    'Coleta e Processamento': 'collection',
    'Modelo Básico': 'model',
    'Multi-Label e Interface': 'interface',
    'Refinamento e Testes': 'refinement',
    'Finalização': 'delivery',
    'Entrega': 'delivery'
  };
  return phaseMap[phase] || 'setup';
}

function toggleActivity(index) {
  if (completedActivities.has(index)) {
    completedActivities.delete(index);
  } else {
    completedActivities.add(index);
  }
  
  populateTimeline();
  updateProgress();
}

function filterActivities() {
  return projectData.timeline.filter(activity => {
    const responsibleMatch = !currentFilters.responsible || 
                           activity.Responsible.includes(currentFilters.responsible);
    const priorityMatch = !currentFilters.priority || 
                         activity.Priority === currentFilters.priority;
    
    return responsibleMatch && priorityMatch;
  });
}

function initializeFilters() {
  const responsibleFilter = document.getElementById('responsibleFilter');
  const priorityFilter = document.getElementById('priorityFilter');
  
  responsibleFilter.addEventListener('change', (e) => {
    currentFilters.responsible = e.target.value;
    populateTimeline();
  });
  
  priorityFilter.addEventListener('change', (e) => {
    currentFilters.priority = e.target.value;
    populateTimeline();
  });
}

// Team functionality
function populateTeamMembers() {
  const container = document.getElementById('teamList');
  container.innerHTML = '';
  
  Object.entries(projectData.teamMembers).forEach(([name, member]) => {
    const workload = calculateWorkload(name);
    const memberElement = createTeamMemberElement(name, member, workload);
    container.appendChild(memberElement);
  });
}

function createTeamMemberElement(name, member, workload) {
  const div = document.createElement('div');
  div.className = 'team-member';
  
  div.innerHTML = `
    <div class="member-name">${name}</div>
    <div class="member-role">${member.role}</div>
    <div class="member-specialization">${member.specialization}</div>
    <div class="member-workload">
      <span>Carga de trabalho:</span>
      <span class="workload-hours">${workload}h</span>
    </div>
  `;
  
  return div;
}

function calculateWorkload(memberName) {
  return projectData.timeline
    .filter(activity => activity.Responsible.includes(memberName))
    .reduce((total, activity) => {
      // Split hours for shared responsibilities
      const responsibleCount = activity.Responsible.split(', ').length;
      return total + (activity.Estimated_Hours / responsibleCount);
    }, 0);
}

// Progress functionality
function updateProgress() {
  const totalActivities = projectData.timeline.length;
  const completedCount = completedActivities.size;
  const progressPercentage = Math.round((completedCount / totalActivities) * 100);
  
  // Update overall progress
  document.getElementById('overallProgress').style.width = `${progressPercentage}%`;
  document.getElementById('progressText').textContent = `${progressPercentage}% concluído`;
  
  // Update completed activities count
  const metricNumber = document.querySelector('.metric-number');
  if (metricNumber) {
    metricNumber.textContent = completedCount;
  }
  
  // Update phase progress
  updatePhaseProgress();
}

function updatePhaseProgress() {
  const phases = ['Setup e Planejamento', 'Coleta e Processamento', 'Modelo Básico'];
  const phaseElements = document.querySelectorAll('.phase-item');
  
  phases.forEach((phase, index) => {
    const phaseActivities = projectData.timeline.filter(a => a.Phase === phase);
    const completedInPhase = phaseActivities.filter((_, activityIndex) => {
      const globalIndex = projectData.timeline.findIndex(a => a === phaseActivities[activityIndex]);
      return completedActivities.has(globalIndex);
    }).length;
    
    const phaseProgress = phaseActivities.length > 0 ? 
                         Math.round((completedInPhase / phaseActivities.length) * 100) : 0;
    
    if (phaseElements[index]) {
      const progressBar = phaseElements[index].querySelector('.progress-fill');
      const progressText = phaseElements[index].querySelector('.progress-percentage');
      
      if (progressBar) progressBar.style.width = `${phaseProgress}%`;
      if (progressText) progressText.textContent = `${phaseProgress}%`;
    }
  });
}

// Charts initialization
function initializeCharts() {
  createWorkloadChart();
  createMoscowChart();
}

function createWorkloadChart() {
  const ctx = document.getElementById('workloadChart');
  if (!ctx) return;
  
  const workloadData = Object.keys(projectData.teamMembers).map(name => ({
    name,
    hours: calculateWorkload(name)
  }));
  
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: workloadData.map(d => d.name),
      datasets: [{
        label: 'Horas de Trabalho',
        data: workloadData.map(d => d.hours),
        backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#5D878F', '#D2BA4C'],
        borderWidth: 0,
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Horas'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Membros da Equipe'
          }
        }
      }
    }
  });
}

function createMoscowChart() {
  const ctx = document.getElementById('moscowChart');
  if (!ctx) return;
  
  const moscowCounts = {
    'MUST': projectData.timeline.filter(a => a.Priority === 'MUST').length,
    'SHOULD': projectData.timeline.filter(a => a.Priority === 'SHOULD').length,
    'COULD': projectData.timeline.filter(a => a.Priority === 'COULD').length,
    'WONT': projectData.timeline.filter(a => a.Priority === 'WONT').length
  };
  
  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['MUST', 'SHOULD', 'COULD', 'WON\'T'],
      datasets: [{
        data: Object.values(moscowCounts),
        backgroundColor: ['#B4413C', '#FFC185', '#5D878F', '#ECEBD5'],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            padding: 20,
            usePointStyle: true
          }
        }
      }
    }
  });
}

// Checklist functionality
document.addEventListener('change', function(e) {
  if (e.target.matches('.checklist-item input[type="checkbox"]')) {
    const item = e.target.closest('.checklist-item');
    if (e.target.checked) {
      item.style.opacity = '0.7';
      item.style.textDecoration = 'line-through';
    } else {
      item.style.opacity = '1';
      item.style.textDecoration = 'none';
    }
  }
});

// Utility functions
function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('pt-BR');
}

function getPriorityColor(priority) {
  const colors = {
    'MUST': '#B4413C',
    'SHOULD': '#FFC185',
    'COULD': '#5D878F',
    'WONT': '#ECEBD5'
  };
  return colors[priority] || '#ECEBD5';
}

// Export functions for global access
window.toggleActivity = toggleActivity;