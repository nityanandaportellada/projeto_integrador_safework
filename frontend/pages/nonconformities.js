import { request } from '../api.js';

export async function renderNC(root) {

    const ncs = await request('/nc');

    root.innerHTML = `
    <div class="page">
        <h1 class="page-title">Não Conformidades</h1>

        <form id="nc-form" class="form-card">

            <input name="origem" placeholder="Origem">

            <input name="descricao" placeholder="Descrição">

            <select name="severidade">
                <option>Baixa</option>
                <option>Média</option>
                <option>Alta</option>
                <option>Crítica</option>
            </select>

            <input name="responsavel" placeholder="Responsável">

            <button type="submit" class="btn-primary">
                Criar NC
            </button>

        </form>

        <div class="table-card">

            <table class="modern-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Descrição</th>
                        <th>Severidade</th>
                        <th>Status</th>
                    </tr>
                </thead>

                <tbody>
                    ${ncs.map(nc => `
                        <tr>
                            <td>${nc.id}</td>
                            <td>${nc.descricao}</td>

                            <td>
                                <span class="severity ${nc.severidade.toLowerCase()}">
                                    ${nc.severidade}
                                </span>
                            </td>

                            <td>
                                <span class="status-badge ativo">
                                    ${nc.status}
                                </span>
                            </td>

                        </tr>
                    `).join('')}
                </tbody>

            </table>

        </div>
    </div>
`;


    document.getElementById('nc-form').onsubmit = async (e) => {

        e.preventDefault();

        const form = new FormData(e.target);

        await request('/nc/', {
            method: 'POST',

            body: JSON.stringify({
                origem: form.get('origem'),
                descricao: form.get('descricao'),
                severidade: form.get('severidade'),
                responsavel: form.get('responsavel'),
                status: 'aberta',
                actions: []
            })
        });

        renderNC(root);
    };
}