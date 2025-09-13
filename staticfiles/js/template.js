document.addEventListener('DOMContentLoaded', function() {

    const url_service_details = '/get_service_details/';

    // Função principal para atualizar a linha
    function updateRow(row, serviceId) {

        if (!serviceId) {
            const cells = row.querySelectorAll('.field-display_max_quantity, .field-display_unit_price, .field-display_total');
            cells.forEach(cell => cell.textContent = '-');
            return;
        }

        // Requisição AJAX para o Django
        fetch(`${url_service_details}${serviceId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Falha na requisição: ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                
                const maxQuantityCell = row.querySelector('.field-display_max_quantity');
                const unitPriceCell = row.querySelector('.field-display_unit_price');
                const totalCell = row.querySelector('.field-display_total');
                const quantityInput = row.querySelector('.field-quantity input');
                const totalFieldWrapper = document.querySelector('.form-group .field-total_price_summary .readonly');
                if (maxQuantityCell) {
                    maxQuantityCell.textContent = data.max_quantity.toLocaleString('pt-BR');
                }
                if (unitPriceCell) {
                    unitPriceCell.textContent = data.unit_price.toLocaleString('pt-BR', { minimumFractionDigits: 2 });
                }

                
                const quantity = parseFloat(quantityInput.value.replace(',', '.'));
                if (!isNaN(quantity) && quantityInput) {
                    const total = quantity * data.unit_price;
                    if (totalCell) {
                        totalCell.textContent = total.toFixed(2).replace('.', ',')
                        const value = parseFloat(totalFieldWrapper.innerText.replace(',', '.'));
                        totalFieldWrapper.innerText = (value + total).toFixed(2).replace('.', ',')
                    }
                } else {
                    if (totalCell) {
                        totalCell.textContent = '-';
                    }
                }
            })
            .catch(error => {
                console.error('Erro geral:', error);
            });
    }

    // Função para adicionar listeners a uma linha específica
    function addListenersToRow(row) {
        const serviceSelect = row.querySelector('.field-service_price');
        const quantityInput = row.querySelector('.field-quantity');
        if (serviceSelect) {
            $(serviceSelect).on("select2:select", function (e) {
                const serviceId = e.params.data.id
                updateRow(row, serviceId);
            });
        }
        
        if (quantityInput) {
            quantityInput.addEventListener('input', function() {
                const serviceSelectValue = row.querySelector('.field-service_price select').value;
                updateRow(row, serviceSelectValue);
            });
        }
    }

    
    // Adiciona listeners para as linhas existentes ao carregar a página
    const existingRows = document.querySelectorAll('.dynamic-templatebuildingservice');
    const existingRowsBuildings = document.querySelectorAll('#buildingservice_building-0')
    existingRows.forEach(addListenersToRow);
    existingRowsBuildings.forEach(addListenersToRow);

    
    // Usa o evento nativo do Django para lidar com novas linhas
    document.addEventListener('formset:added', function(event) {
        const newRow = event.target;
        addListenersToRow(newRow);
    });

});