import { request } from '../api.js';

export async function renderReports(root) {

    const inspections = await request('/inspections');

    root.innerHTML = `
        <div class="page">

            <h1>Relatórios</h1>

            <table class="data-table">

                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Localização</th>
                        <th>Data</th>
                        <th>Ações</th>
                    </tr>
                </thead>

                <tbody>

                    ${inspections.map(inspection => `
                        <tr>

                            <td>
                                ${inspection.id}
                            </td>

                            <td>
                                ${inspection.localizacao}
                            </td>

                            <td>
                                ${new Date(
                                    inspection.criado_em
                                ).toLocaleString()}
                            </td>

                            <td>

                                <button
                                    class="btn-report"
                                    data-id="${inspection.id}"
                                >
                                    Gerar PDF
                                </button>

                            </td>

                        </tr>
                    `).join('')}

                </tbody>

            </table>

        </div>
    `;

    document.querySelectorAll('.btn-report')
        .forEach(button => {

            button.onclick = () => {

                const id = button.dataset.id;

                window.open(
                    `http://localhost:8000/reports/inspection/${id}`,
                    '_blank'
                );
            };
        });
}