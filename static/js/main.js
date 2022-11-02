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
           }
            checkCartQuantity();
        });
    }

    function checkCartQuantity() {
        const cart = $('.cart').find('span');
        const items = JSON.parse(localStorage.getItem('products'));
        if (!items) return;
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

    function checkRecpatcha(form) {
        form.on('submit', event => {
            if(grecaptcha.getResponse()) {
                return true;
            }

            alert('Selecione o campo "Eu não sou um Robô"');
            event.preventDefault();
        })


    }

    function processPayment() {
        const products = JSON.parse(localStorage.getItem('products'));

        if(!products) {
            removeSectionProccessPayment();
        }
        const $currentProductItem = $('.payment__item');
        const $productClone = $currentProductItem.clone();
        $currentProductItem.remove();

        let totalPrice = 0;
        for(product of products) {
            const currentPrice = product.quantity * product.price;
            totalPrice += currentPrice;
            const $currentProduct = $productClone.clone();

            $currentProduct.find('.payment__product_image').attr('src', product.img);
            $currentProduct.find('.payment__product_title').text(product.name);
            $currentProduct.find('.payment__product_qtt_item').text(product.quantity);
            $currentProduct.find('.payment__product_money').text(currentPrice.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));

            $('.payment__items').append($currentProduct);
        }

        $('.payment__actions_price_total').text(totalPrice.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }));


    }


    function removeSectionProccessPayment() {
            $('.payment__columns').remove();
            const section = document.createElement('section');
            section.classList.add('payment__empty');
            section.classList.add('wrapper');
            const h2 = document.createElement('h2');
            h2.innerText = 'Não há produtos no seu carrinho.'
            h2.classList.add('payment__empty_title');
            section.append(h2);
            $('.payment__confirm').append(section);
    }

    if($('.payment__confirm').length) {
        processPayment();
    }




    addToCart();

    checkCartQuantity();

    if($('.submited__form')) {
        checkRecpatcha($('.submited__form'))
    }

    if($('.form__page')) {
        userForm();
    }
});




function initPayPalButton() {
    const products = JSON.parse(localStorage.getItem('products'));

    let totalPrice = 0;

    for(product of products) {
        totalPrice += product.quantity * product.price;
    }

  paypal.Buttons({
    style: {
      shape: 'pill',
      color: 'gold',
      layout: 'horizontal',
      label: 'checkout',
      tagline: true
    },

    createOrder: function(data, actions) {
      return actions.order.create({
        purchase_units: [{"amount":{"currency_code":"BRL","value":totalPrice}}]
      });
    },

    onApprove: function(data, actions) {
      return actions.order.capture().then(function(orderData) {
          fetch(`${window.location.origin}/pedido`, {
              method: 'POST',
              body: JSON.stringify({
                  products: JSON.parse(localStorage.getItem('products'))
              })
            }).then(response => {
                return JSON.parse(response)
            }).then(data => {
                localStorage.clear();
                if(data.error) {
                    alert("Erro ao criar o pedido");
                    window.location.href = window.location.origin;
                }
                alert("Pedido Criado com sucesso");
                window.location.href = `${window.location.origin}/pedido/${data.order_id}`;
          }).catch(err => {
              localStorage.clear();
              alert("Houve um erro ao tentar criar o pedido, tente novamente mais tarde");
              console.log(err);
            })

      });
    },

    onError: function(err) {
      console.log(err);
    }
  }).render('#paypal-button-container');
}
if(document.querySelector('#paypal-button-container')) {
    initPayPalButton();
}
