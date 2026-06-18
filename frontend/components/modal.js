export function createModal({
    id,
    title,
    content
}) {

    return `
        <div
            class="modal-overlay"
            id="${id}"
        >

            <div class="modal">

                <div class="modal-header">

                    <h2>
                        ${title}
                    </h2>

                    <button
                        class="modal-close"
                        onclick="closeModal('${id}')"
                    >
                        ✕
                    </button>

                </div>

                <div class="modal-content">

                    ${content}

                </div>

            </div>

        </div>
    `;
}


export function openModal(id) {

    const modal = document.getElementById(id);

    if (!modal) return;

    modal.style.display = 'flex';
}


export function closeModal(id) {

    const modal = document.getElementById(id);

    if (!modal) return;

    modal.style.display = 'none';
}


window.openModal = openModal;
window.closeModal = closeModal;