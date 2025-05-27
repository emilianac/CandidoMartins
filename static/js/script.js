const generoSelect = document.getElementById('genero');
const estadoCivilSelect = document.getElementById('estado_civil');

    const opcoesEstadoCivil = {
        masculino: [
            { value: 'solteiro', text: 'Solteiro' },
            { value: 'casado', text: 'Casado' },
            { value: 'divorciado', text: 'Divorciado' },
            { value: 'viuvo', text: 'Viúvo' },
            { value: 'separado', text: 'Separado' }
        ],
        feminino: [
            { value: 'solteira', text: 'Solteira' },
            { value: 'casada', text: 'Casada' },
            { value: 'divorciada', text: 'Divorciada' },
            { value: 'viuva', text: 'Viúva' },
            { value: 'separada', text: 'Separada' }
        ]
    };

generoSelect.addEventListener('change', function () {
const generoSelecionado = generoSelect.value;
        // Limpa as opções antigas
    estadoCivilSelect.innerHTML = '<option value="" disabled selected>Selecione seu estado civil</option>';

    if (opcoesEstadoCivil[generoSelecionado]) {
        opcoesEstadoCivil[generoSelecionado].forEach(opcao => {
            const optionElement = document.createElement('option');
            optionElement.value = opcao.value;
            optionElement.textContent = opcao.text;
            estadoCivilSelect.appendChild(optionElement);
        });
    }
});

// Formatar CPF para 000.000.000-00
document.getElementById('cpf').addEventListener('input', function(e) {
    let valor = e.target.value.replace(/\D/g, ''); // Remove tudo que não for dígito
    valor = valor.slice(0, 11); // Limita para 11 dígitos

    let cpfFormatado = valor;

    if (valor.length > 9) {
        cpfFormatado = valor.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
    } else if (valor.length > 6) {
        cpfFormatado = valor.replace(/(\d{3})(\d{3})(\d{1,3})/, '$1.$2.$3');
    } else if (valor.length > 3) {
        cpfFormatado = valor.replace(/(\d{3})(\d{1,3})/, '$1.$2');
    }
    e.target.value = cpfFormatado;
});

// Buscar CEP e preencher campos
function buscarCep() {
    const cep = document.getElementById('cep').value.replace(/\D/g, '');

    if (cep.length !== 8) {
        alert('CEP inválido!');
        return;
    }
    if (!/^\d{8}$/.test(cep)) {
        alert('CEP deve conter apenas números!');
        return;
    }
    const cepLimpo = cep.replace(/\D/g, ''); // remove tudo que não é número
    const url = `https://viacep.com.br/ws/${cepLimpo}/json/`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.erro) {
                alert('CEP não encontrado!');
                return;
            }

            document.getElementById('logradouro').value = data.logradouro || '';
            document.getElementById('bairro').value = data.bairro || '';
            document.getElementById('cidade').value = data.localidade || '';
            document.getElementById('estado').value = data.uf || '';
        })
            .catch(error => console.error('Erro ao buscar CEP:', error));
    }

// Formatar RG
const rgInput = document.getElementById('rg');

  rgInput.addEventListener('input', () => {
    let rg = rgInput.value;

    // Remove tudo que não for número ou letra (alguns RGs têm letra no final)
    rg = rg.replace(/[^0-9a-zA-Z]/g, '');

    // Aplica máscara: 12.345.678-9
    if (rg.length > 2) rg = rg.slice(0, 2) + '.' + rg.slice(2);
    if (rg.length > 6) rg = rg.slice(0, 6) + '.' + rg.slice(6);
    if (rg.length > 10) rg = rg.slice(0, 10) + '-' + rg.slice(10, 11);

    rgInput.value = rg;
});