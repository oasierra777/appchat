$(function(){
    var url = 'ws://'+window.location.host+'/ws/room/'+room_id+'/'
    //console.log(url)
    var chatSocket = new WebSocket(url)

    chatSocket.onopen = function(e){
        console.log('Abierto')
    }

    chatSocket.onclose = function(e){
        console.log('cerrado')
    }

    chatSocket.onmessage = function(e){
        const data = JSON.parse(e.data)
        console.log(data.type)
        if (data.type === 'chat_message'){
            const msj = data.message
            const username = data.username
            const datetime = data.datetime

            document.querySelector('#boxMessages').innerHTML += 
            `
                <div class="alert alert-success" role="alert">
                    ${msj}
                    <div>
                        <small class="fst-italic fw-bold">${username}</small>.
                        <small class="float-end">${datetime}</small>
                    </div>
                </div>
            `
        }else if(data.type == 'user_list'){
            let userListHTML = ''
            for(const username of data.users){
                const userClass = (username === user) ? 'list-group-item-success' : ''
                userListHTML += `<li class="list-group-item ${userClass}">@${username}</li>`
            }
            document.querySelector('#userList').innerHTML = userListHTML
        }    
    }

    document.querySelector('#btnMessage').addEventListener('click', sendMessage)
    document.querySelector('#inputMessage').addEventListener('keypress', 
        function(e){
            if (e.keyCode == 13){
                sendMessage()
            }
        })

    function sendMessage(){
        var message = document.querySelector('#inputMessage')
        
        if(message.value.trim() !== ''){
            loadMessageHTML(message.value.trim())
            chatSocket.send(JSON.stringify({
                type: 'chat_message',
                message: message.value.trim(),
            }))
            console.log(message.value.trim())
            message.value = ''
        }else{
            console.log('Nooooo')
        }
    }

    function loadMessageHTML(m){
        var currentDatetime = new Date();
        var dateObject = new Date(currentDatetime)

        var year = dateObject.getFullYear();
        var month = ('0' + (dateObject.getMonth() + 1)).slice(-2);
        var day = ('0' + dateObject.getDate()).slice(-2);
        var hours = ('0' + dateObject.getHours()).slice(-2);
        var minutes = ('0' + dateObject.getMinutes()).slice(-2);
        var seconds = ('0' + dateObject.getSeconds()).slice(-2);

        const formattedDate = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
        document.querySelector('#boxMessages').innerHTML += 
        `
            <div class="alert alert-primary" role="alert">
                ${m}
                <div>
                    <small class="fst-italic fw-bold">${user}</small>.
                    <small class="float-end">${formattedDate}</small>
                </div>
            </div>
        `
    }
})


    
