import { request } from '../api.js';

export async function renderClients(root) {
    const clients = await request('/clients');

    root.innerHTML = `
    <div class="page">
        <h1 class="page-title">Clientes</h1>

        <form id="client-form" class="form-card">
            <input name="nome" placeholder="Nome">
            <input name="cnpj" placeholder="CNPJ">
            <input name="email" placeholder="Email">

            <button type="submit" class="btn-primary">
                Salvar
            </button>
        </form>

        <div class="table-card">
            <table class="modern-table">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>CNPJ</th>
                        <th>Email</th>
                    </tr>
                </thead>

                <tbody>
                    ${clients.map(client => `
                        <tr>
                            <td>${client.nome}</td>
                            <td>${client.cnpj}</td>
                            <td>${client.email}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    </div>
`;

    document.getElementById('client-form').onsubmit = async (e) => {
        e.preventDefault();

        const form = new FormData(e.target);

        await request('/clients/', {
            method: 'POST',
            body: JSON.stringify({
                nome: form.get('nome'),
                cnpj: form.get('cnpj'),
                email: form.get('email')
            })
        });

        renderClients(root);
    };
}