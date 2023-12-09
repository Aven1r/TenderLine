const form = document.getElementById('messages__form');
const messages = document.querySelector('.messages');
let userIdNow = 0;
let socket;

document.querySelectorAll('.chats__user').forEach(user => {
    user.addEventListener('click', (e) => {
        e.preventDefault();
        messages.innerHTML = '';
        fetch(`http://192.168.8.129:8000/chats/messages?recipient_id=${e.target.getAttribute('data-user_id')}&limit=10&skip=0`)
        .then(response => response.json())
        .then(data => console.log(data.forEach(userMess => {
            let div = document.createElement('div');
            if (userMess.author_id == e.target.getAttribute('data-user_id')){
                div.innerHTML = userMess.text;
                div.className = 'message__to';
                messages.appendChild(div);
            } else{
                div.innerHTML = userMess.text;
                div.className = 'message__from';
                messages.appendChild(div);
            }
        })))
        userIdNow = e.target.getAttribute('data-user_id');
        console.log(e.target.getAttribute('data-user_id'));

        if (socket !== undefined){
            socket.close();
        }

        socket = new WebSocket(`ws://192.168.8.129:8000/chats/ws/${e.target.getAttribute('data-user_id')}`);
        socket.onmessage = (message) => {
            // alert(message);
            let data = JSON.parse(JSON.parse(message.data));
            console.log(data);
            let div = document.createElement('div');
            div.innerHTML = data.text;
            div.className = 'message__from';
            messages.appendChild(div);
        }

     const send = (event) => {
         event.preventDefault();
         const text = document.getElementById('messages__input').value;
         socket.send(JSON.stringify({text}))
         return false;
     }

     form.addEventListener('submit', send);


    })
})
 
//------------Add classes for messages----
form.addEventListener('submit', (e) => {
    e.preventDefault();
    if(document.getElementById('messages__input').value != ''){
        let div = document.createElement('div');
        div.innerHTML = document.getElementById('messages__input').value;
        div.className = 'message__to';
        messages.appendChild(div);
    } 
    document.getElementById('messages__input').value = '';
}) 

//----Close form-------
document.getElementById('main-form__form').addEventListener('submit', (e) => {
    e.preventDefault();
    document.querySelector('.modal__wrapper').classList.add('hidden');
})
document.querySelector('.close-img').addEventListener('click', () => {
    document.querySelector('.modal__wrapper').classList.add('hidden')
})

