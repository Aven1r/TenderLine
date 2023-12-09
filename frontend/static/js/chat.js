const form = document.getElementById('messages__form');
const messages = document.querySelector('.messages');
const startForm = document.querySelector('.modal__wrapper');
// let userIdNow = 0;
let socket;

function createElement(text, path){
    let div = document.createElement('div');
    div.innerHTML = text;
    div.className = `message__${path}`;
    messages.appendChild(div);
}

//----send message
const send = (event) => {
    event.preventDefault();
    const text = document.getElementById('messages__input').value;
    socket.send(JSON.stringify({text}))
    return false;
}
   
document.querySelectorAll('.chats__user').forEach(user => {
    user.addEventListener('click', (e) => {
        e.preventDefault();
        messages.innerHTML = '';
        fetch(`http://192.168.8.129:8000/chats/messages?recipient_id=${e.target.getAttribute('data-user_id')}&limit=10&skip=0`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            //----check length of messages
            if (data.length == 0){
                data.forEach(userMess => {
                    console.log(userMess);
                    let div = document.createElement('div');
                    if (userMess.author_id == e.target.getAttribute('data-user_id')){
                        div.innerHTML = userMess.text;
                        div.className = 'message__from';
                        messages.appendChild(div);
                    } else{
                        div.innerHTML = userMess.text;
                        div.className = 'message__to';
                        messages.appendChild(div);
                    }
                })
            } else {
                let doc = document.createElement('div');
                doc.innerHTML += '<p>Заполните форму договора, чтобы начать диалог с исполнителем </p>';
                doc.innerHTML += '<button>заполнить</button>';
                doc.className = 'message__doc';
                messages.appendChild(doc);

                doc.addEventListener('click', () => {
                    doc.classList.add('hidden');
                    startForm.classList.remove('hidden');

                    //----Close form-------
                    document.getElementById('main-form__form').addEventListener('submit', (e) => {
                        e.preventDefault();
                        const form = {
                            "text": "string",
                            "document": {
                              "status": document.getElementById('main-form__status').value,
                              "reestr_number": document.getElementById('main-form__registry-num').value,
                              "purchase_number": document.getElementById('main-form__purchase').value,
                              "law_number": document.getElementById('main-form__law').value,
                              "contract_method": document.getElementById('main-form__contract_method').value,
                              "contract_basis": document.getElementById('main-form__contract_basis').value,
                              "contract_number": document.getElementById('main-form__contract_number').value,
                              "contract_lifetime": document.getElementById('main-form__contract_lifetime').value,
                              "contract_subject": document.getElementById('main-form__contract_subject').value,
                              "contract_place": document.getElementById('main-form__contract_place').value,
                              "IKZ": document.getElementById('main-form__IKZ').value,
                              "budget": document.getElementById('main-form__budget').value,
                              "contract_price": document.getElementById('main-form__сontract_price').value,
                              "prepayment": document.getElementById('main-form__prepayment').value,
                              "previous_document_id": 0,
                              "document_status": "Создано"
                            }
                        };
                        console.log(form);
                        socket.send(JSON.stringify(form));
                        
                        createElement('Здравствуйте!', 'to');
                        createElement('тут будет файл', 'to');

                        startForm.classList.add('hidden');
                        return false;
                    })
                    document.querySelector('.close-img').addEventListener('click', () => {
                        startForm.classList.add('hidden')
                    })
                })
            }
        }
    )

    // userIdNow = e.target.getAttribute('data-user_id');

    // if (socket !== undefined){
    //     socket.close();
    // }

    socket = new WebSocket(`ws://192.168.8.129:8000/chats/ws/${e.target.getAttribute('data-user_id')}`);
    socket.onmessage = (message) => {
        let data = JSON.parse(JSON.parse(message.data));
        createElement(data.text, 'from');
    }
     form.addEventListener('submit', send);
    })
})
 
//------------Add classes for messages
form.addEventListener('submit', (e) => {
    e.preventDefault();
    if(document.getElementById('messages__input').value != ''){
        createElement(document.getElementById('messages__input').value, 'to');
        document.getElementById('messages__input').value = '';
    } 
}) 