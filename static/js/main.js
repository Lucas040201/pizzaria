$(function(){

    const states = [
        { uf: 'AC', name: 'Acre' },
        { uf: 'AL', name: 'Alagoas' },
        { uf: 'AP', name: 'Amapá' },
        { uf: 'AM', name: 'Amazonas' },
        { uf: 'BA', name: 'Bahia' },
        { uf: 'CE', name: 'Ceará' },
        { uf: 'DF', name: 'Distrito Federal' },
        { uf: 'ES', name: 'Espirito Santo' },
        { uf: 'GO', name: 'Goiás' },
        { uf: 'MA', name: 'Maranhão' },
        { uf: 'MS', name: 'Mato Grosso do Sul' },
        { uf: 'MT', name: 'Mato Grosso' },
        { uf: 'MG', name: 'Minas Gerais' },
        { uf: 'PA', name: 'Pará' },
        { uf: 'PB', name: 'Paraíba' },
        { uf: 'PR', name: 'Paraná' },
        { uf: 'PE', name: 'Pernambuco' },
        { uf: 'PI', name: 'Piauí' },
        { uf: 'RJ', name: 'Rio de Janeiro' },
        { uf: 'RN', name: 'Rio Grande do Norte' },
        { uf: 'RS', name: 'Rio Grande do Sul' },
        { uf: 'RO', name: 'Rondônia' },
        { uf: 'RR', name: 'Roraima' },
        { uf: 'SC', name: 'Santa Catarina' },
        { uf: 'SP', name: 'São Paulo' },
        { uf: 'SE', name: 'Sergipe' },
        { uf: 'TO', name: 'Tocantins' }
    ];


    function userForm() {
        const $uf = $("#uf");
        createOptionsForState($uf);
        const $cep = $("#cep");
        $cep.mask("99999-999");
        $("#phone").mask("(99) 99999-9999");

        $cep.on('focusout', e => {
            const formatedCep = e.target.value.split('-').join('');
            const viacep = `https://viacep.com.br/ws/${formatedCep}/json/`;
            $.ajax({
                url: viacep
            }).done(e => {
                $('#district').attr('value', e.bairro);
                $('#street').attr('value', e.logradouro);
                $uf.val(e.uf);
            });
        }) ;
    }

    function createOptionsForState(field) {
        states.forEach((item, index) => {
            const option = document.createElement('option');
            option.setAttribute('value', item.uf.toUpperCase());
            option.innerText = item.name;
            field.append(option);
        })
    }


    if($('.form__page')) {
        userForm();
    }
});