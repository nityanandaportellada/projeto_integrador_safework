import { request } from '../api.js';

export async function renderDashboard(root) {
    const data = await request('/dashboard');

    root.innerHTML = `
        <div class="page">
            <h1 class="page-title">Dashboard</h1>

            <div class="kpis">

                <div class="kpi-card">
                    <h3>Inspeções</h3>
                    <span class="kpi-value">
                        ${data.total_inspections}
                    </span>
                </div>

                <div class="kpi-card danger">
                    <h3>NC Abertas</h3>
                    <span class="kpi-value">
                        ${data.open_nc}
                    </span>
                </div>

            </div>

            <div class="table-card mt">
                <h2>NC Críticas</h2>

                <ul class="nc-list">
                    ${data.critical_nc.map(nc => `
                        <li>
                            <span class="nc-dot"></span>
                            ${nc.descricao}
                        </li>
                    `).join('')}
                </ul>
            </div>
        </div>
    `;
}