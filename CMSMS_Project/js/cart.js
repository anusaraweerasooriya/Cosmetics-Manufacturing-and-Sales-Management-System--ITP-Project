
var updateButtons = document.getElementsByClassName('update-cart')

for(var i=0; i<updateButtons.length; i++){
    updateButtons[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action

        console.log('productID:', productId, 'action:', action)
        console.log('USER:' , user)

        if (user === 'AnonymousUser'){
            console.log('Not logged in')
        }else{
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){
    console.log('User is logged in, sending data..')

    var url = '/customer_sales/update_cart/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId,'action': action})
    })

    .then((response) =>{
            return response.json();
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()
    });
}
