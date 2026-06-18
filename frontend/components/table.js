export function createTable({
    columns,
    data,
    actions = []
}) {

    const headers = columns.map(column => `
        <th>${column.label}</th>
    `).join('');

    const rows = data.map(item => {

        const cells = columns.map(column => `
            <td>${item[column.key] ?? '-'}</td>
        `).join('');

        const actionButtons = actions.map(action => `
            <button
                class="${action.className || ''}"
                data-id="${item.id}"
                data-action="${action.name}"
            >
                ${action.label}
            </button>
        `).join('');

        return `
            <tr>

                ${cells}

                ${actions.length > 0
                    ? `<td>${actionButtons}</td>`
                    : ''
                }

            </tr>
        `;
    }).join('');

    return `
        <table class="data-table">

            <thead>

                <tr>

                    ${headers}

                    ${actions.length > 0
                        ? '<th>Ações</th>'
                        : ''
                    }

                </tr>

            </thead>

            <tbody>

                ${rows}

            </tbody>

        </table>
    `;
}