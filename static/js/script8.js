const dropdownOptions=document.querySelector(".dropdown-options")
const dropdownButton=document.querySelector(".dropdown-button")
dropdownButton.addEventListener('click',(event)=>{
  dropdownOptions.classList.toggle('show')
})

let url = `ws://${window.location.host}/ws/socket-server/`

const chatSocket = new WebSocket(url)//It creates a new websocket connection

chatSocket.onmessage = (e)=>{//It receives message from websocket
    let data=JSON.parse(e.data)//Convert the text JSON in a object JSON
    if(data.type === 'chat_message'){
      console.log('Data received')
  }
}

let form=document.getElementById("formWriteMessage")
form.addEventListener('submit',(e)=>{//It sends the information to backend
  const message=e.target.body.value
  console.log("AAAAAAAAAAA")
  console.log(message.replace(/\s/g,'').length)
  if(message.replace(/\s/g,'').length<=0){//Test if the string is empty
    return alert("You cannot send empty messages")
  }
  const messageUsername=document.getElementById("messageUsername").value
  const messageAvatar=document.getElementById("messageAvatar").value
  const roomPK=document.getElementById("roomPK").value
  const avatarUser=document.getElementById("avatarUser").value
  chatSocket.send(JSON.stringify({'type':'chat_message','messageAvatar':messageAvatar,'messageUsername':messageUsername,'message':message,'roomPK':roomPK}))
  form.reset()
  let messageField=document.getElementsByClassName('thread')
  let firstMessage=document.getElementById('thread')
  messageField=[...messageField]
  messageField.reverse()
  console.log(firstMessage)
  const stringHTML=`<div class="thread">
                  <div class="thread__top">
                    <div class="thread__author">
                      <a href="{% url 'user-profile' message.user.id %}" class="thread__authorInfo">
                        <div class="avatar">
                          <img src="/images/${avatarUser}">
                        </div>
                        <span>@${messageUsername}</span>
                      </a>
                      <div>
                        <span class="thread__date">Message sent</span>
                      </div>
                    </div>
                  </div>
                  <div class="thread__details">${message}</div>
                </div>`
  if (messageField.length>0){
    messageField[0].insertAdjacentHTML('afterend',stringHTML)
    e.preventDefault()//It cancel the page reloading after the submit
  }
})