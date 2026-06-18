import { renderDashboard } from './pages/dashboard.js';
import { renderClients } from './pages/clients.js';
import { renderProjects } from './pages/projects.js';
import { renderChecklists } from './pages/checklists.js';
import { renderInspections } from './pages/inspections.js';
import { renderNC } from './pages/nonconformities.js';
import { renderReports } from './pages/reports.js';

window.navigate = function(page) {
    const root = document.getElementById('content');

    switch(page) {
        case 'dashboard':
            renderDashboard(root);
            break;

        case 'clients':
            renderClients(root);
            break;

        case 'projects':
            renderProjects(root);
            break;

        case 'checklists':
            renderChecklists(root);
            break;

        case 'inspections':
            renderInspections(root);
            break;

        case 'nonconformities':
            renderNC(root);
            break;

        case 'reports':
            renderReports(root);
            break;
    }
}

navigate('dashboard');