const input = document.querySelector('input')
const button = document.querySelector('svg')
const chatContainer = document.querySelector('.chat-container')
const inputContainer = document.querySelector('.input-container')

function send() {
    if (input.value == "") return;
    let newEl = document.createElement('div')
    newEl.className = 'chats'
    newEl.innerHTML = `
        <img src="/static/chatbot/images/user.png" alt="user-img">
        <div class="content">
            <span class="owner">You</span>
            <p>${input.value}</p>
        </div>
    `
    inputContainer.insertAdjacentElement('beforebegin', newEl)
    let temp = input.value
    input.value = ''
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });



    $.ajax({
        type: 'POST',
        url: '/chat/',
        data:{
            'query': temp,
        },
        success: (response)=>{
            let newBotEl = document.createElement('div')
            newBotEl.className = 'chats'
            let finalResponse = response.response
            // if(response.score < 0.72) 
            //     finalResponse = 'I can\'t able to understand your query, kindly contack our support team!'
            newBotEl.innerHTML = `
            <img src="/static/chatbot/images/bot.jpg" alt="bot-img">
            <div class="content">
                <span class="owner">Bot</span>
                <p>${ response.response  } <br> <br>Thanks!<br></p>
            </div>
            `
            inputContainer.insertAdjacentElement('beforebegin', newBotEl)
            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: 'smooth'
            });
            input.focus()

        },
        error: (error)=>{
            console.log(error)
        }
    })
}

button.addEventListener('click', send)

input.addEventListener('keydown', event => {
    if (event.keyCode === 13) {
        send()
    }
})
