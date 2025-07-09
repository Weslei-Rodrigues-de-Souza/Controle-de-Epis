// Funções para controle de modais
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    
    const endpoints = {
        'departamentoModal': '/departamento',
        'funcaoModal': '/funcao',
        'funcionarioModal': '/funcionario',
        'fornecedorModal': '/fornecedor',
        'epiModal': '/epi',
        'entradaEpiModal': '/entrada_epi',
        'liberacaoEpiModal': '/liberacao_epi'
    };
    
    fetch(endpoints[modalId])
        .then(response => response.text())
        .then(html => {
            modal.innerHTML = html;
            modal.style.display = 'block';
            
            // Event listeners para fechar modal
            const closeBtn = modal.querySelector('.close');
            if (closeBtn) {
                closeBtn.onclick = () => closeModal(modalId);
            }
            
            modal.onclick = (event) => {
                if (event.target === modal) {
                    closeModal(modalId);
                }
            };
            
            // Configurar formulário
            const form = modal.querySelector('form');
            if (form) {
                form.onsubmit = (e) => handleFormSubmit(e, modalId);
            }
            
            // Executar scripts após carregar
            setTimeout(() => {
                executeModalScripts(modalId);
            }, 200);
        })
        .catch(error => {
            console.error('Erro ao carregar modal:', error);
            showAlert('Erro ao carregar formulário', 'danger');
        });
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'none';
}

// Executar scripts específicos de cada modal
function executeModalScripts(modalId) {
    console.log('Executando scripts para:', modalId);
    
    switch(modalId) {
        case 'departamentoModal':
            loadDepartamentosData();
            break;
        case 'funcaoModal':
            loadFuncoesData();
            break;
        case 'funcionarioModal':
            loadFuncionariosData();
            break;
        case 'fornecedorModal':
            loadFornecedoresData();
            break;
        case 'epiModal':
            loadEPIsData();
            break;
    }
}

// FUNÇÕES DE CARREGAMENTO DE DADOS
function loadDepartamentosData() {
    console.log('Iniciando carregamento de departamentos...');
    
    fetch('/departamentos')
        .then(response => {
            console.log('Status da resposta:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Departamentos recebidos:', data);
            
            const tbody = document.getElementById('departamentosTableBody');
            if (!tbody) {
                console.error('Elemento departamentosTableBody não encontrado!');
                return;
            }
            
            tbody.innerHTML = '';
            
            if (!data || data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="3" class="text-center text-muted">Nenhum departamento cadastrado</td></tr>';
                return;
            }
            
            // Ordenar por data de criação (mais recente primeiro)
            data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
            
            data.forEach((dept, index) => {
                const dataFormatada = dept.created_at ? 
                    new Date(dept.created_at).toLocaleDateString('pt-BR') : 
                    'N/A';
                
                const row = document.createElement('tr');
                
                // Destacar o primeiro item (mais recente)
                if (index === 0) {
                    row.classList.add('table-success');
                    setTimeout(() => {
                        row.classList.remove('table-success');
                    }, 3000);
                }
                
                row.innerHTML = `
                    <td>${dept.nome}</td>
                    <td>${dataFormatada}</td>
                    <td>
                        <button class="btn btn-sm btn-warning" onclick="editDepartamento(${dept.id}, '${dept.nome.replace(/'/g, "\\'")}')">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" onclick="deleteDepartamento(${dept.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(row);
            });
            
            console.log('Departamentos carregados com sucesso!');
        })
        .catch(error => {
            console.error('Erro ao carregar departamentos:', error);
            const tbody = document.getElementById('departamentosTableBody');
            if (tbody) {
                tbody.innerHTML = '<tr><td colspan="3" class="text-center text-danger">Erro ao carregar dados</td></tr>';
            }
            showAlert('Erro ao carregar lista de departamentos', 'danger');
        });
}


function loadFuncoesData() {
    console.log('Iniciando carregamento de funções...');
    
    fetch('/funcoes')
        .then(response => {
            console.log('Status da resposta:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Funções recebidas:', data);
            
            const tbody = document.getElementById('funcoesTableBody');
            if (!tbody) {
                console.error('Elemento funcoesTableBody não encontrado!');
                return;
            }
            
            tbody.innerHTML = '';
            
            if (!data || data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="3" class="text-center text-muted">Nenhuma função cadastrada</td></tr>';
                return;
            }
            
            data.forEach(func => {
                const dataFormatada = func.created_at ? 
                    new Date(func.created_at).toLocaleDateString('pt-BR') : 
                    'N/A';
                
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${func.nome}</td>
                    <td>${dataFormatada}</td>
                    <td>
                        <button class="btn btn-sm btn-warning" onclick="editFuncao(${func.id}, '${func.nome.replace(/'/g, "\\'")}')">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" onclick="deleteFuncao(${func.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(row);
            });
            
            console.log('Funções carregadas com sucesso!');
        })
        .catch(error => {
            console.error('Erro ao carregar funções:', error);
            const tbody = document.getElementById('funcoesTableBody');
            if (tbody) {
                tbody.innerHTML = '<tr><td colspan="3" class="text-center text-danger">Erro ao carregar dados</td></tr>';
            }
            showAlert('Erro ao carregar lista de funções', 'danger');
        });
}

function loadFuncionariosData() {
    console.log('Iniciando carregamento de funcionários...');
    
    fetch('/funcionarios')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Funcionários recebidos:', data);
            
            const tbody = document.getElementById('funcionariosTableBody');
            if (!tbody) {
                console.error('Elemento funcionariosTableBody não encontrado!');
                return;
            }
            
            tbody.innerHTML = '';
            
            if (!data || data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">Nenhum funcionário cadastrado</td></tr>';
                return;
            }
            
            data.forEach(func => {
                const dataAdmissao = func.data_admissao ? 
                    new Date(func.data_admissao).toLocaleDateString('pt-BR') : 
                    'N/A';
                
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${func.nome}</td>
                    <td>${func.cpf}</td>
                    <td>${func.departamento}</td>
                    <td>${func.funcao}</td>
                    <td>${dataAdmissao}</td>
                    <td>
                        <button class="btn btn-sm btn-warning" onclick="editFuncionario(${func.id})" title="Editar">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" onclick="deleteFuncionario(${func.id})" title="Excluir">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(row);
            });
            
            console.log('Funcionários carregados com sucesso!');
        })
        .catch(error => {
            console.error('Erro ao carregar funcionários:', error);
            const tbody = document.getElementById('funcionariosTableBody');
            if (tbody) {
                tbody.innerHTML = '<tr><td colspan="6" class="text-center text-danger">Erro ao carregar dados</td></tr>';
            }
            showAlert('Erro ao carregar lista de funcionários', 'danger');
        });
}

// FUNÇÕES DE EDIÇÃO E EXCLUSÃO
function editDepartamento(id, nome) {
    openEditModal('editDepartamentoModal', `/departamento/${id}/edit`);
}

function deleteDepartamento(id) {
    if (confirm('Tem certeza que deseja remover este departamento?')) {
        fetch(`/departamento/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert(data.message, 'success');
                loadDepartamentosData();
            }
        })
        .catch(error => {
            console.error('Erro ao excluir departamento:', error);
            showAlert('Erro ao excluir departamento', 'danger');
        });
    }
}

function editFuncao(id) {
    openEditModal('editFuncaoModal', `/funcao/${id}/edit`);
}

function deleteFuncao(id) {
    if (confirm('Tem certeza que deseja remover esta função?')) {
        fetch(`/funcao/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert(data.message, 'success');
                loadFuncoesData();
            }
        })
        .catch(error => {
            console.error('Erro ao excluir função:', error);
            showAlert('Erro ao excluir função', 'danger');
        });
    }
}

function editFuncionario(id) {
    openEditModal('editFuncionarioModal', `/funcionario/${id}/edit`);
}

function deleteFuncionario(id) {
    if (confirm('Tem certeza que deseja remover este funcionário?')) {
        fetch(`/funcionario/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert(data.message, 'success');
                loadFuncionariosData();
            }
        })
        .catch(error => {
            console.error('Erro ao excluir funcionário:', error);
            showAlert('Erro ao excluir funcionário', 'danger');
        });
    }
}

// OUTRAS FUNÇÕES
function handleFormSubmit(event, modalId) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    
    // Desabilitar botão de submit para evitar duplo clique
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Salvando...';
    
    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert(data.message, 'success');
            
            // Limpar apenas o formulário, mantendo o modal aberto
            form.reset();
            
            // Recarregar APENAS a lista do modal ativo
            setTimeout(() => {
                executeModalScripts(modalId);
            }, 500); // Pequeno delay para mostrar o alerta
            
            // Atualizar estatísticas do dashboard
            loadDashboardStats();
            
        } else {
            showAlert(data.message || 'Erro ao processar formulário', 'danger');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        showAlert('Erro ao enviar formulário', 'danger');
    })
    .finally(() => {
        // Reabilitar botão de submit
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    });
}


function showAlert(message, type) {
    // Verificar se existe um modal aberto
    const openModal = document.querySelector('.modal[style*="display: block"]');
    
    if (openModal) {
        // Mostrar alerta dentro do modal
        const modalBody = openModal.querySelector('.modal-body');
        const existingAlert = modalBody.querySelector('.alert');
        
        // Remover alerta anterior se existir
        if (existingAlert) {
            existingAlert.remove();
        }
        
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Inserir no topo do modal-body
        modalBody.insertBefore(alertDiv, modalBody.firstChild);
        
        // Remover automaticamente após 4 segundos
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 4000);
        
    } else {
        // Mostrar alerta na página principal (comportamento original)
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;
        
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

function highlightNewItem(tableBodyId) {
    const tbody = document.getElementById(tableBodyId);
    if (tbody && tbody.children.length > 0) {
        const firstRow = tbody.children[0];
        firstRow.classList.add('table-success');
        firstRow.style.animation = 'pulse 1s ease-in-out';
        
        // Remover destaque após 3 segundos
        setTimeout(() => {
            firstRow.classList.remove('table-success');
            firstRow.style.animation = '';
        }, 3000);
    }
}


function loadDashboardStats() {
    Promise.all([
        fetch('/funcionarios').then(r => r.json()),
        fetch('/epis').then(r => r.json()),
        fetch('/departamentos').then(r => r.json()),
        fetch('/fornecedores').then(r => r.json())
    ]).then(([funcionarios, epis, departamentos, fornecedores]) => {
        const totalFuncionarios = document.getElementById('totalFuncionarios');
        const totalEpis = document.getElementById('totalEpis');
        const totalDepartamentos = document.getElementById('totalDepartamentos');
        const totalFornecedores = document.getElementById('totalFornecedores');
        
        if (totalFuncionarios) totalFuncionarios.textContent = funcionarios.length;
        if (totalEpis) totalEpis.textContent = epis.length;
        if (totalDepartamentos) totalDepartamentos.textContent = departamentos.length;
        if (totalFornecedores) totalFornecedores.textContent = fornecedores.length;
    }).catch(error => {
        console.error('Erro ao carregar estatísticas:', error);
    });
}

// Carregar estatísticas quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    loadDashboardStats();
});

// Fechar modais com tecla ESC
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (modal.style.display === 'block') {
                modal.style.display = 'none';
            }
        });
    }
});

function loadFornecedoresData() {
    console.log('Iniciando carregamento de fornecedores...');
    
    fetch('/fornecedores')
        .then(response => {
            console.log('Status da resposta:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Fornecedores recebidos:', data);
            
            const tbody = document.getElementById('fornecedoresTableBody');
            if (!tbody) {
                console.error('Elemento fornecedoresTableBody não encontrado!');
                return;
            }
            
            tbody.innerHTML = '';
            
            if (!data || data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted">Nenhum fornecedor cadastrado</td></tr>';
                return;
            }
            
            data.forEach(forn => {
                const dataFormatada = forn.created_at ? 
                    new Date(forn.created_at).toLocaleDateString('pt-BR') : 
                    'N/A';
                
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${forn.cnpj}</td>
                    <td>${forn.nome}</td>
                    <td>${dataFormatada}</td>
                    <td>
                        <button class="btn btn-sm btn-warning" onclick="editFornecedor(${forn.id}, '${forn.nome.replace(/'/g, "\\'")}', '${forn.cnpj}')">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" onclick="deleteFornecedor(${forn.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(row);
            });
            
            console.log('Fornecedores carregados com sucesso!');
        })
        .catch(error => {
            console.error('Erro ao carregar fornecedores:', error);
            const tbody = document.getElementById('fornecedoresTableBody');
            if (tbody) {
                tbody.innerHTML = '<tr><td colspan="4" class="text-center text-danger">Erro ao carregar dados</td></tr>';
            }
            showAlert('Erro ao carregar lista de fornecedores', 'danger');
        });
}

function loadEPIsData() {
    console.log('Iniciando carregamento de EPIs...');
    
    fetch('/epis')
        .then(response => {
            console.log('Status da resposta:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('EPIs recebidos:', data);
            
            const tbody = document.getElementById('episTableBody');
            if (!tbody) {
                console.error('Elemento episTableBody não encontrado!');
                return;
            }
            
            tbody.innerHTML = '';
            
            if (!data || data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">Nenhum EPI cadastrado</td></tr>';
                return;
            }
            
            data.forEach(epi => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${epi.nome}</td>
                    <td>${epi.marca}</td>
                    <td>${epi.ca}</td>
                    <td>${epi.periodicidade_dias} dias</td>
                    <td>
                        <button class="btn btn-sm btn-warning" onclick="editEPI(${epi.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" onclick="deleteEPI(${epi.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(row);
            });
            
            console.log('EPIs carregados com sucesso!');
        })
        .catch(error => {
            console.error('Erro ao carregar EPIs:', error);
            const tbody = document.getElementById('episTableBody');
            if (tbody) {
                tbody.innerHTML = '<tr><td colspan="5" class="text-center text-danger">Erro ao carregar dados</td></tr>';
            }
            showAlert('Erro ao carregar lista de EPIs', 'danger');
        });
}

// Funções de edição e exclusão para fornecedores
function editFornecedor(id, nome, cnpj) {
    openEditModal('editFornecedorModal', `/fornecedor/${id}/edit`);
}

function deleteFornecedor(id) {
    if (confirm('Tem certeza que deseja remover este fornecedor?')) {
        fetch(`/fornecedor/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert(data.message, 'success');
                loadFornecedoresData();
            }
        })
        .catch(error => {
            console.error('Erro ao excluir fornecedor:', error);
            showAlert('Erro ao excluir fornecedor', 'danger');
        });
    }
}

// Funções de edição e exclusão para EPIs
function editEPI(id) {
    openEditModal('editEpiModal', `/epi/${id}/edit`);
}

function deleteEPI(id) {
    if (confirm('Tem certeza que deseja remover este EPI?')) {
        fetch(`/epi/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert(data.message, 'success');
                loadEPIsData();
            }
        })
        .catch(error => {
            console.error('Erro ao excluir EPI:', error);
            showAlert('Erro ao excluir EPI', 'danger');
        });
    }
}

// Função genérica para abrir modais de edição
function openEditModal(modalId, endpoint) {
    console.log('Abrindo modal de edição:', modalId, 'Endpoint:', endpoint);
    const modal = document.getElementById(modalId);
    
    if (!modal) {
        console.error('Modal não encontrado:', modalId);
        showAlert('Erro: Modal de edição não encontrado', 'danger');
        return;
    }
    
    fetch(endpoint)
        .then(response => {
            console.log('Status da resposta:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(html => {
            console.log('HTML recebido, carregando modal...');
            modal.innerHTML = html;
            modal.style.display = 'block';
            
            // Event listeners para fechar modal
            const closeBtn = modal.querySelector('.close');
            if (closeBtn) {
                closeBtn.onclick = () => closeModal(modalId);
            }
            
            modal.onclick = (event) => {
                if (event.target === modal) {
                    closeModal(modalId);
                }
            };
            
            // CONFIGURAR FORMULÁRIO DE EDIÇÃO CORRETAMENTE
            const form = modal.querySelector('form');
            if (form) {
                console.log('Configurando formulário de edição...');
                
                // Remover listeners anteriores
                form.onsubmit = null;
                
                // Adicionar novo listener
                form.addEventListener('submit', function(e) {
                    console.log('Submit do formulário de edição detectado');
                    handleEditFormSubmit(e, modalId);
                });
                
                console.log('Formulário configurado com sucesso');
            } else {
                console.error('Formulário não encontrado no modal');
            }
        })
        .catch(error => {
            console.error('Erro ao carregar modal de edição:', error);
            showAlert('Erro ao carregar formulário de edição', 'danger');
        });
}

// Função para lidar com submissão de formulários de edição
function handleEditFormSubmit(event, modalId) {
    event.preventDefault();
    console.log('Processando edição para modal:', modalId);
    
    const form = event.target;
    const formData = new FormData(form);
    
    // Debug: Verificar dados do formulário
    console.log('Dados do formulário:');
    for (let [key, value] of formData.entries()) {
        console.log(key, value);
    }
    
    // Desabilitar botão de submit
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Atualizando...';
    
    // Usar POST com _method=PUT
    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        console.log('Status da resposta:', response.status);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Resposta do servidor:', data);
        if (data.success) {
            showAlert(data.message, 'success');
            
            // Fechar modal de edição
            closeModal(modalId);
            
            // Recarregar lista do modal principal correspondente
            const mainModalId = getMainModalFromEdit(modalId);
            if (mainModalId) {
                setTimeout(() => {
                    executeModalScripts(mainModalId);
                }, 500);
            }
            
            // Atualizar estatísticas
            loadDashboardStats();
            
        } else {
            showAlert(data.message || 'Erro ao atualizar registro', 'danger');
        }
    })
    .catch(error => {
        console.error('Erro ao processar edição:', error);
        showAlert('Erro ao atualizar registro. Verifique os dados e tente novamente.', 'danger');
    })
    .finally(() => {
        // Reabilitar botão
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    });
}

// Função para mapear modal de edição para modal principal
function getMainModalFromEdit(editModalId) {
    const mapping = {
        'editDepartamentoModal': 'departamentoModal',
        'editFuncaoModal': 'funcaoModal',
        'editFuncionarioModal': 'funcionarioModal',
        'editFornecedorModal': 'fornecedorModal',
        'editEpiModal': 'epiModal'
    };
    return mapping[editModalId];
}
