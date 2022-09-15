$(function(){

    function userForm() {
        const $uf = $("#uf");
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


    function addToCart() {
        $('.product__add').on('click', e => {
           const currentProduct = {};
           const cardBox = $(e.target).parent();
           currentProduct.img = cardBox.find('.product__image').attr('src');
           currentProduct.name = cardBox.find('.product__name').text();
           currentProduct.price = parseFloat(cardBox.find('.product__price').text().split('$')[1]);
           currentProduct.id = $(e.target).data('product');
           currentProduct.quantity = 1;

           if (!localStorage.getItem('products')) {
               localStorage.setItem('products', JSON.stringify([currentProduct]));
           } else {
               const products =  JSON.parse(localStorage.getItem('products'));
               const hasProduct = products.find(prod => {
                   return prod.id === currentProduct.id;
               });
               if(hasProduct) {
                   let productsNew = products.map(item => {
                       if(item.id === currentProduct.id){
                           item.quantity +=1;
                       }
                       return item
                   });
                    localStorage.setItem('products', JSON.stringify(productsNew));
               } else {
                    products.push(currentProduct);
                    localStorage.setItem('products', JSON.stringify(products));
               }
               checkCartQuantity();
           }
        });
    }



    function checkCartQuantity() {
        const cart = $('.cart').find('span');
        const items = JSON.parse(localStorage.getItem('products'));
        let quantity = 0;
        if(items.length === 1) {
           quantity = items[0].quantity;
        } else {
            quantity = items.reduce((prevValue, prod) => {
               return prevValue + prod.quantity;
           }, 0);
        }
        cart.text(quantity);
    }








    addToCart();

    checkCartQuantity();

    if($('.form__page')) {
        userForm();
    }
});