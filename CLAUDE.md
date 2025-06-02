# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **project management dashboard** for a Machine Learning initiative to develop a sensitive content classification system for music lyrics. The project has a tight 15-day deadline (ending June 17, 2025) and uses a web-based dashboard to track progress, team workload, and priorities.

**Note**: This repository currently contains only the **project planning and management dashboard**. The actual ML implementation (data processing, model training, Streamlit app) will be developed in a separate repository as outlined in the planning document.

## Architecture

The dashboard is a **client-side web application** with:

- **Frontend**: Vanilla JavaScript (`app.js`) with Chart.js for visualizations
- **Styling**: Custom CSS design system (`style.css`) with comprehensive theming
- **Data**: Hardcoded project timeline and team data in JavaScript objects
- **UI**: Tabbed interface with sections for overview, timeline, team, priorities, guide, and monitoring

### Key Components

- **Project Timeline**: 16 activities across 6 phases (Setup → Delivery) with MoSCoW prioritization
- **Team Management**: 5 team members with specialized roles and workload tracking
- **Progress Tracking**: Interactive checkboxes for activity completion with real-time progress updates
- **Charts**: Bar chart for workload distribution, doughnut chart for priority analysis
- **Filtering**: Timeline activities can be filtered by responsible person and priority level

## Development Commands

Since this is a static web application, no build tools or package managers are required:

```bash
# Serve the dashboard locally
python -m http.server 8000  # Then visit http://localhost:8000

# Alternative with Node.js
npx serve .
```

## File Structure

- `index.html` - Main dashboard interface with tabbed navigation
- `app.js` - Core dashboard functionality, state management, and chart initialization  
- `style.css` - Comprehensive design system with light/dark mode support
- `claude-md-plan.md` - Detailed 15-day implementation plan for the actual ML project
- `projeto_ml_timeline_15_dias.csv` - Timeline data export
- `gantt_chart.png` - Visual project timeline

## Code Patterns

### State Management
- Global state in `completedActivities` Set and `currentFilters` object
- Real-time UI updates triggered by user interactions
- Progress calculations based on completion state

### Chart Integration
- Chart.js integration for workload and priority visualizations
- Responsive chart containers with proper aspect ratio handling
- Data derived from the main project data structures

### Responsive Design
- Mobile-first CSS with progressive enhancement
- Flexible grid layouts that collapse to single column on mobile
- Touch-friendly interface elements

## Team Structure (from planning data)

- **Leonardo**: Tech Lead and Mentor (Architecture, Code Review)
- **Letícia**: Product Owner (Model Experimentation, Acceptance Criteria)  
- **Nathan**: Data Steward (Data Analysis, Feature Engineering)
- **Luan**: Junior Developer (ML Components, Implementation)
- **Carlos**: Junior Developer (Testing, Validation)

## Project Phases

1. **Setup e Planejamento** (Days 1-2)
2. **Coleta e Processamento** (Days 3-5) 
3. **Modelo Básico** (Days 6-8)
4. **Multi-Label e Interface** (Days 9-11)
5. **Refinamento e Testes** (Days 12-13)
6. **Finalização** (Days 14-15)
7. **Entrega** (Day 16)

## Making Changes

When modifying the dashboard:

- Update project data in `app.js` projectData object for timeline/team changes
- Modify CSS custom properties in `:root` for design system changes
- Add new chart types by extending the `initializeCharts()` function
- New dashboard sections require updates to navigation, HTML structure, and section management in `app.js`