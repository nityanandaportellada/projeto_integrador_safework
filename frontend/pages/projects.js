import { request } from '../api.js';

export async function renderProjects(root) {

    const projects = await request('/projects');
    const clients = await request('/clients');

    root.innerHTML = `
    <div class="page">
        <h1 class="page-title">Projetos</h1>

        <div class="form-card">

            <select name="client_id">
                <option value="">Selecione o cliente</option>
                ${clients.map(client => `
                    <option value="${client.id}">
                        ${client.nome}
                    </option>
                `).join('')}
            </select>

            <input name="nome" placeholder="Nome do projeto">

            <input name="descricao" placeholder="Descrição">

            <select name="status">
                <option>Planejado</option>
                <option>Ativo</option>
                <option>Concluído</option>
            </select>

            <input name="responsavel" placeholder="Responsável">

            <button id="project-form" class="btn-primary">
                Salvar Projeto
            </button>

        </div>

        <div class="table-card">

            <table class="modern-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Projeto</th>
                        <th>Cliente</th>
                        <th>Status</th>
                        <th>Responsável</th>
                    </tr>
                </thead>

                <tbody>
                    ${projects.map(project => {
                        const client = clients.find(c => c.id === project.client_id);

                        return `
                            <tr>
                                <td>${project.id}</td>
                                <td>${project.nome}</td>
                                <td>${client ? client.nome : '-'}</td>
                                <td>
                                    <span class="status-badge ${project.status.toLowerCase()}">
                                        ${project.status}
                                    </span>
                                </td>
                                <td>${project.responsavel || '-'}</td>
                            </tr>
                        `;
                    }).join('')}
                </tbody>
            </table>

        </div>
    </div>
`;

    document.getElementById('project-form').onsubmit = async (e) => {

        e.preventDefault();

        const form = new FormData(e.target);

        await request('/projects/', {
            method: 'POST',

            body: JSON.stringify({
                client_id: Number(form.get('client_id')),
                nome: form.get('nome'),
                descricao: form.get('descricao'),
                status: form.get('status'),
                responsavel: form.get('responsavel')
            })
        });

        renderProjects(root);
    };
}