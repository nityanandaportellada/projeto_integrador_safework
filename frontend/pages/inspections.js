import { request } from '../api.js';

export async function renderInspections(root) {
    const clients = await request('/clients');
    const projects = await request('/projects');
    const checklists = [];

    root.innerHTML = `
        <div class="page">
            <h1 class="page-title">Nova Inspeção</h1>

            <form id="inspection-form" class="form-card">

                <select name="client_id" required>
                    <option value="">Selecione o Cliente</option>
                    ${clients.map(c => `
                        <option value="${c.id}">
                            ${c.nome}
                        </option>
                    `).join('')}
                </select>

                <select name="project_id" required>
                    <option value="">Selecione o Projeto</option>
                    ${projects.map(p => `
                        <option value="${p.id}">
                            ${p.nome}
                        </option>
                    `).join('')}
                </select>

                <select name="checklist_id" required>
                    <option value="">Selecione o Checklist</option>
                    ${checklists.map(c => `
                        <option value="${c.id}">
                            ${c.nome}
                        </option>
                    `).join('')}
                </select>

                <input 
                    name="localizacao" 
                    placeholder="Local da inspeção"
                    required
                >

                <button type="submit" class="btn-primary">
                    Finalizar inspeção
                </button>

            </form>
        </div>
    `;

    // 🔥 SUBMIT FUNCIONANDO
    document.getElementById('inspection-form').onsubmit = async (e) => {
        e.preventDefault();

        const form = new FormData(e.target);

        try {
            await request('/inspections/', {
                method: 'POST',
                body: JSON.stringify({
                    client_id: Number(form.get('client_id')),
                    project_id: Number(form.get('project_id')),
                    checklist_id: Number(form.get('checklist_id')),
                    localizacao: form.get('localizacao'),
                    answers: []
                })
            });

            alert('✅ Inspeção criada com sucesso!');

            // recarrega a tela
            renderInspections(root);

        } catch (err) {
            console.error(err);
            alert('❌ Erro ao criar inspeção');
        }
    };
}