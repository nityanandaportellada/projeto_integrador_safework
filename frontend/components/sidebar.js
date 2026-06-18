export function renderSidebar() {

    return `
        <aside class="sidebar">

            <div class="sidebar-header">
                <h2>SafeWork</h2>

                <p>
                    Gestão de Segurança do Trabalho
                </p>
            </div>

            <nav class="sidebar-nav">

                <button onclick="navigate('dashboard')">
                    Dashboard
                </button>

                <button onclick="navigate('clients')">
                    Clientes
                </button>

                <button onclick="navigate('projects')">
                    Projetos
                </button>

                <button onclick="navigate('checklists')">
                    Checklists
                </button>

                <button onclick="navigate('inspections')">
                    Inspeções
                </button>

                <button onclick="navigate('nonconformities')">
                    Não Conformidades
                </button>

                <button onclick="navigate('reports')">
                    Relatórios
                </button>

            </nav>

        </aside>
    `;
}