const form = document.getElementById('messages__form');
let socket;
current_id = fets

document.querySelectorAll('.chats__user').forEach(user => {
    user.addEventListener('click', (e) => {
        console.log(1);
        e.preventDefault();
        fetch(`http://192.168.8.130:8000/chats/messages?recipient_id=${e.target.getAttribute('data-user_id')}&limit=10&skip=0`)
        .then(response => response.json())
        .then(data => console.log(data))
        console.log(e.target.getAttribute('data-user_id'));

        if (socket !== undefined){
            socket.close();
        }

        socket = new WebSocket(`ws://192.168.8.130:8000/chats/ws/${e.target.getAttribute('data-user_id')}`);
        socket.onmessage = (message) => {
            console.log(message.data)
            let data = JSON.parse(JSON.parse(message.data));
            console.log(data);
            console.log(data.text);
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