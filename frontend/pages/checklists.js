export function renderChecklists(root) {

    // 🔥 DADOS FAKE (simulando backend)
    const checklists = [
        {
            id: 1,
            nome: "Segurança do Trabalho",
            versao: "1.0",
            bloqueado: false
        },
        {
            id: 2,
            nome: "Inspeção de Equipamentos",
            versao: "2.1",
            bloqueado: true
        }
    ];

    root.innerHTML = `
        <div class="page">
            <h1 class="page-title">Checklists</h1>

            <div class="table-card">

                ${checklists.map(checklist => `
                    <div class="card mt">
                        <h3>${checklist.nome}</h3>
                        <p><strong>Versão:</strong> ${checklist.versao}</p>
                        <p>
                            ${checklist.bloqueado 
                                ? '<span class="status-badge concluído">🔒 Bloqueado</span>' 
                                : '<span class="status-badge ativo">✅ Editável</span>'}
                        </p>
                    </div>
                `).join('')}

            </div>
        </div>
    `;
}