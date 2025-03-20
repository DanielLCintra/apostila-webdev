/**
 * Gerenciador de abas para os tutoriais de instalação
 * 
 * Este script permite alternar entre as diferentes abas de sistemas operacionais
 * nos tutoriais de instalação do Node.js e Git.
 */

// Executar quando a página estiver totalmente carregada
document.addEventListener('DOMContentLoaded', function () {
    // Seleção de todos os grupos de tabs (node e git)
    const tabGroups = ['node', 'git'];

    // Para cada grupo, configurar eventos e estado inicial
    tabGroups.forEach(group => {
        // Selecionar o primeiro botão de tab do grupo como padrão
        const defaultTab = document.querySelector(`.tab-btn[data-tab^="${group}-"]:first-child`);
        if (defaultTab) {
            defaultTab.classList.add('active');
        }

        // Selecionar o primeiro conteúdo de tab do grupo como padrão
        const defaultContent = document.querySelector(`.tab-content[id^="${group}-"]:first-child`);
        if (defaultContent) {
            defaultContent.classList.add('active');
        }

        // Adicionar eventos de clique aos botões de tab
        const tabButtons = document.querySelectorAll(`.tab-btn[data-tab^="${group}-"]`);
        tabButtons.forEach(button => {
            button.addEventListener('click', function () {
                const tabId = this.getAttribute('data-tab');
                switchTab(group, tabId);
            });
        });
    });
});

/**
 * Função para alternar entre abas de um determinado grupo
 * @param {string} group - Grupo de abas (node ou git)
 * @param {string} tabId - ID da aba a ser mostrada
 */
function switchTab(group, tabId) {
    // Desativar todos os botões do grupo
    const allButtons = document.querySelectorAll(`.tab-btn[data-tab^="${group}-"]`);
    allButtons.forEach(button => {
        button.classList.remove('active');
    });

    // Esconder todos os conteúdos do grupo
    const allContents = document.querySelectorAll(`.tab-content[id^="${group}-"]`);
    allContents.forEach(content => {
        content.classList.remove('active');
    });

    // Ativar o botão selecionado
    const selectedButton = document.querySelector(`.tab-btn[data-tab="${tabId}"]`);
    if (selectedButton) {
        selectedButton.classList.add('active');
    }

    // Mostrar o conteúdo selecionado
    const selectedContent = document.getElementById(tabId);
    if (selectedContent) {
        selectedContent.classList.add('active');
    }
}