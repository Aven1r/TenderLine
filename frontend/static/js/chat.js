const form = document.getElementById('messages__form');
const messages = document.querySelector('.messages');
const startForm = document.querySelector('.modal__wrapper');
const inputList = document.getElementById('main-form__form');
// let userIdNow = 0;
let socket;
let recipientId;

const ip = "http://192.168.8.129:8000"

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
    
    fetch(ip+`/chats/message/${data.id}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        for (key in data['document']){
            document.getElementById(`main-form__${key}`).value = data['document'][key];
        }
        // startForm.classList.remove('hidden');
    })
       

}


// получение json с изменениями
fetch('')
.then(response => response.json())
.then(data => {
    //цикл по ключам, значениям. Заполнение формы
})


function get_from_string_id(value){
    if (value == 'null') return null
    else return parseInt(value)
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
          "previous_document_id": get_from_string_id(startForm.getAttribute('data-previous_id')),
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
                div.innerHTML = '<p>Договор №52</p><p>📂</p>'
                div.className = 'message__to';
                div.classList.add('open-file');
                div.setAttribute('data-message_id', data.id)

                messages.appendChild(div);

                // логика открытия и настройки формы
                div.addEventListener('click', () => {
                    startForm.classList.remove('hidden');
                    startForm.setAttribute('data-action', "Отредактировано")
                    startForm.setAttribute('data-previous_id', data.document.id)
                    setup_data(data)
                })
                
                return

            case 'Отредактировано':
                // fetch(`http://192.168.8.130:8000/chats/message/${data.id}`)
                // .then(response => response.json())
                // .then(data => console.log())
                let str = `
                <div class = message__${path}>
                    <div class="message__changed-head">
                        <h1>Договор №52</h1>
                        <a class='download-file-icon' downloads href='#'>📥</a>
                    </div>
                    <p>Сводка изменений:</p>
                    <div class="table__block">
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
                    
                        <form id="changes__shortForm">
                            <div>новое<input type="checkbox" name="" id=""></div>
                            <div>новое<input type="checkbox" name="" id=""></div>
                            <div>новое<input type="checkbox" name="" id=""></div>
                            <br />
                            <input id="change_${data.id}" type="button" value="редактировать">
                        </form>
                    </div>
                </div>
                <div class="btns" id="btns_${data.id}">
                    <button id="btn-ok_${data.id}" class="btn-ok" >согласиться</button>
                    <button id="btn-not_${data.id}" class="btn-not" >отказаться</button>
                </div>`;

                // логика открытия и настройки формы
                div.insertAdjacentHTML('beforeend', str);
                div.classList.add('messsage__changed');
                path == 'to' ? div.style.marginLeft = 'auto' : div.style.marginLeft = 0;
                messages.appendChild(div);

                // обработчик редактирования
                document.getElementById(`change_${data.id}`).addEventListener('click', () => {
                    startForm.classList.remove('hidden');
                    startForm.setAttribute('data-action', "Отредактировано")
                    startForm.setAttribute('data-previous_id', data.document.id)
                    setup_data(data)
                })

                //обработчик кнопок
                document.getElementById(`btns_${data.id}`).addEventListener('click', (e) => {
                    switch (e.target) {
                        // соглашение на заключение контракта
                        case document.getElementById(`btn-ok_${data.id}`):
                            console.log(200);
                            break;

                        // отказ от заключения контракта
                        case document.getElementById(`btn-not_${data.id}`):
                            messages.innerHTML = "<p>Спасибо, что воспользовались услугами нашего сервиса!</p>";
                            console.log(404);
                            document.getElementById('messages__input').setAttribute("disabled", "disabled");
                            document.getElementById(`btn-ok_${data.id}`).setAttribute("disabled", "disabled");
                            document.getElementById(`btn-not_${data.id}`).setAttribute("disabled", "disabled");
                            break;
                    }
                })

                

                return;

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
        fetch(ip+`/auth/user/${recipientId}`)
        .then(response => response.json())
        .then(data => {
            console.log(document.querySelector('.recipient__name'))
            document.querySelector('.recipient__name').innerText = data.email
        })

        e.preventDefault();
        messages.innerHTML = '';
        fetch(ip+`/chats/messages?recipient_id=${e.target.getAttribute('data-user_id')}&limit=10&skip=0`)
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

    socket = new WebSocket(`ws://192.168.8.129:8000/chats/ws/${e.target.getAttribute('data-user_id')}`);
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