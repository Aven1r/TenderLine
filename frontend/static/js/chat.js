const form = document.getElementById('messages__form');
const messages = document.querySelector('.messages');
const startForm = document.querySelector('.modal__wrapper');
const inputList = document.getElementById('main-form__form');
// let userIdNow = 0;
let socket;
let recipientId;

// Крестик закрывает вкладку
document.querySelector('.close').addEventListener('click', (e) => {
    startForm.classList.add('hidden');

})

// логика отправки сообщений
document.getElementById('main-form__form').addEventListener('submit', (e) => {
    e.preventDefault();
    socket.send(JSON.stringify(collect_message_json(startForm.getAttribute('data-action'))));
    startForm.classList.add('hidden');

})

// наполнение формы данными
function setup_data(data){

    // startForm.classList.remove('hidden');
    
    fetch(`http://192.168.8.130:8000/chats/message/${data.id}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        for (key in data['document']){
            document.getElementById(`main-form__${key}`).value = data['document'][key];
        }
        // startForm.classList.remove('hidden');
    })
       

}

// сбор полей с формы в json
function collect_message_json(message_status){
    return {
        "text": "Какой-то договор",
        "document": {
          "status": document.getElementById('main-form__status').value,
          "reestr_number": document.getElementById('main-form__reestr_number').value,
          "purchase_number": document.getElementById('main-form__purchase_number').value,
          "law_number": document.getElementById('main-form__law_number').value,
          "contract_method": document.getElementById('main-form__contract_method').value,
          "contract_basis": document.getElementById('main-form__contract_basis').value,
          "contract_number": document.getElementById('main-form__contract_number').value,
          "contract_lifetime": document.getElementById('main-form__contract_lifetime').value,
          "contract_subject": document.getElementById('main-form__contract_subject').value,
          "contract_place": document.getElementById('main-form__contract_place').value,
          "IKZ": document.getElementById('main-form__IKZ').value,
          "budget": "Бюджетные средства",
          "contract_price": document.getElementById('main-form__сontract_price').value,
          "prepayment": document.getElementById('main-form__prepayment').value,
          "previous_document_id": null,
          "document_status": message_status
        }
    };
}


function createElement(data, path){
    let div = document.createElement('div');
    if (data.document == null){
        // создание текстового сообщения без документа
        div.innerHTML = data.text;
        div.className = `message__${path}`;
        messages.appendChild(div);
    } else {
        switch (data.document.document_status){
            case 'Создано':
                div.innerHTML = '<p>Договор №52</p><img src="images/icons/file.svg"></img>';
                div.className = 'message__to';
                div.classList.add('open-file');
                div.setAttribute('data-message_id', data.id)
                messages.appendChild(div);

                // логика открытия и настройки формы

                div.addEventListener('click', () => {
                    startForm.classList.remove('hidden');
                    startForm.setAttribute('data-action', "Отредактировано")
                    setup_data(data)
                })
                
                return

            case 'Отредактировано':
                let str = `
                <div>
                    <h1>Договор №52</h1>
                    <img src="{{ url_for('static', path='images/icons/download.svg') }}"></img>
                </div>;
                <p>Сводка изменений:</p>
                <div>
                    <table>
                        <tr>
                            <td>значение</td>
                            <td>старое</td>
                        </tr>
                        <tr>
                            <td>значение</td>
                            <td>старое</td>
                        </tr>
                        <tr>
                            <td>значение</td>
                            <td>старое</td>
                        </tr>
                    </table>
                    <img src="{{ url_for('static', path='images/icons/change.svg') }}"></img>
                    <form id="changes__shortForm">
                        <div><label for="">новое</label><input type="checkbox" name="" id=""></div>
                        <div><label for="">новое</label><input type="checkbox" name="" id=""></div>
                        <div><label for="">новое</label><input type="checkbox" name="" id=""></div>
                        <br />
                        <input type="submit" value="редактировать">
                    </form>
                </div>`;

                // логика открытия и настройки формы
                div.addEventListener('click', () => {
                    startForm.classList.remove('hidden');
                    startForm.setAttribute('data-action', "Отредактировано")
                    setup_data(data)
                })
                
                div.insertAdjacentHTML('beforeend', str);
                div.className = 'message__from';
                messages.appendChild(div);
                return
            case 'Подтверждено':
                alert('3');
                return
        }
    }
    
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
        recipientId = e.target.getAttribute('data-user_id');

        e.preventDefault();
        messages.innerHTML = '';
        fetch(`http://192.168.8.130:8000/chats/messages?recipient_id=${e.target.getAttribute('data-user_id')}&limit=10&skip=0`)
        .then(response => response.json())
        .then(data => {
            //----check length of messages
            if (data.length != 0){
                data.forEach(userMess => {
                    console.log(userMess);
                    let div = document.createElement('div');
                    let direction;

                    if (userMess.author_id == recipientId){
                        direction = "from"
                    } else{
                        direction = 'to'
                    }
                    createElement(userMess, direction)
                })
            } else {
                // let doc = document.createElement('div');
                // doc.innerHTML += '<p>Заполните форму договора, чтобы начать диалог с исполнителем </p>';
                // doc.innerHTML += '<button>заполнить</button>';
                // doc.className = 'message__doc';
                // messages.appendChild(doc);

                // doc.addEventListener('click', () => {
                //     doc.classList.add('hidden');
                //     startForm.classList.remove('hidden');

                //     //----Close form-------
                //     document.getElementById('main-form__form').addEventListener('submit', (e) => {
                //         e.preventDefault();
                        

                //         // console.log(form);
                //         socket.send(JSON.stringify(collect_message_json("Создано")));

                //         startForm.classList.add('hidden');
                //         inputList.querySelectorAll('input').forEach(item => item.value = '')
                //         document.getElementById('submit__btn').value = 'отправить';
                //         // createElement('Здравствуйте!', 'to');
                //         // createElement(form, 'to');
                //         return false;
                //     })
                //     document.querySelector('.close-img').addEventListener('click', () => {
                //         startForm.classList.add('hidden')
                //     })
                // })
            }
        }
    )

    // userIdNow = e.target.getAttribute('data-user_id');

    if (socket !== undefined){
        socket.close();
    }

    socket = new WebSocket(`ws://192.168.8.130:8000/chats/ws/${e.target.getAttribute('data-user_id')}`);
    socket.onmessage = (message) => {
        let data = JSON.parse(JSON.parse(message.data));
        let messageDirection;
        if (recipientId == data.author_id){
            messageDirection = "from"
        } else {
            messageDirection = "to"
        }
        console.log(data)
        createElement(data, messageDirection)
    }
     form.addEventListener('submit', send);

    })
})
 
//------------Add classes for messages
//form.addEventListener('submit', (e) => {
//    e.preventDefault();
//    if(document.getElementById('messages__input').value != ''){
//        createElement(document.getElementById('messages__input').value, 'to');
//    }
//
//})