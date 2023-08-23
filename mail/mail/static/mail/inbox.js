document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector("#compose-form").addEventListener("submit", send_email);


  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(reciever, subject, body) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector("#message-view").style.display = "none";
  document.querySelector('#compose-view').style.display = 'block';

  //
  if (reciever !== undefined && subject !== undefined && body !== undefined) {
		document.querySelector("#compose-recipients").value = reciever;
		document.querySelector("#compose-subject").value = subject;
		document.querySelector("#compose-body").value = body;
	}
  else{

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }

}
function send_email(submit) {
  submit.preventDefault();
	fetch("/emails", {
		method: "POST",
		body: JSON.stringify({
			recipients: document.querySelector("#compose-recipients").value,
			subject: document.querySelector("#compose-subject").value,
			body: document.querySelector("#compose-body").value
		}),
	})
		.then(response=>response.json()).then(setTimeout(() => {
      load_mailbox('sent');//delay the redirect so the api has enough time to fetch new info
    }, 100)).catch(error => console.log(error))


}
function open_email(id,fromMailbox){
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(data=>{
    
    document.querySelector("#emails-view").style.display = "none";
    document.querySelector("#message-view").style.display = "block";
		document.querySelector("#compose-view").style.display = "none";
    const element = document.createElement('div');
    
    element.innerHTML = `
    <h3>${data["subject"]}</h3>
    <div class = "email-detail-container">
    <p class="email-timestamp">${data["timestamp"]}</p>
    <p class="email-sender-view"><span class="bold-label">From:</span> ${data["sender"]}</p>
    <p class="email-recipients"><span class="bold-label">To:</span> ${data["recipients"]}</p>
    <div>
    <button class="btn btn-sm btn-outline-primary" id='read-button'>Mark as Unread</button>
    <button class="btn btn-sm btn-outline-primary" id ='reply-button'>Reply</button>
    <button class="btn btn-sm btn-outline-primary" id ='archive-button'>Archive</button>
    </div>  
    </div> 
      <p class="email-body">${data["body"]}</p>
      `;
    document.querySelector("#message-view").innerHTML = "";
    document.querySelector("#message-view").appendChild(element);
    readStatus(true, data["id"]);

    const readButton = document.querySelector("#read-button");
    fromMailbox === "inbox" || fromMailbox === "archive"
			? (readButton.style.visibility = "visible")
			: (readButton.style.visibility = "hidden");
		readButton.addEventListener("click", () => {
				readStatus(false, data["id"]);
		});
    const archiveButton= document.querySelector("#archive-button");
    fromMailbox === "inbox" 
			? (archiveButton.style.visibility = "visible")
			: (archiveButton.style.visibility = "hidden");
    archiveButton.addEventListener("click", () =>{
      archiveEmail(true,data['id']);
    });

    if(fromMailbox=== 'archive'){
      archiveButton.style.visibility = "visible";
      archiveButton.textContent = "Un Archive"
      archiveButton.addEventListener("click", () => {
				archiveEmail(false, data["id"]);
			});
    }

    const replyButton = document.querySelector("#reply-button");
    fromMailbox === "inbox" || fromMailbox === "archive"
			? (replyButton.style.visibility = "visible")
			: (replyButton.style.visibility = "hidden");
		replyButton.addEventListener("click", () => {
			reciever = data["sender"];
      subject = data["subject"].includes("Re:")
				? data["subject"]
				: `Re: ${data["subject"]}`;
      body = `On ${data['timestamp']} ${data['sender']} wrote: ${data['body']}\n\n\n\n`;
      compose_email(reciever,subject,body);
			
		});
    
  })
}

function readStatus(boolean, emailID){
  fetch(`emails/${emailID}`,{
    method: 'PUT',
    body: JSON.stringify({
      read: boolean
    })
  })
}
function archiveEmail(boolean, emailID){
  fetch(`/emails/${emailID}`, {
		method: "PUT",
		body: JSON.stringify({
			archived: boolean,
		}),
	});
}
 

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector("#message-view").style.display = "none";
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`).then(response => response.json()).then(emails =>{
		// Inside the fetch block of load_mailbox function
		emails.forEach((email) => {
      if(mailbox==="archive" && email['archived']){
        let element = document.createElement("div");
				element.className = "email-item";
				element.className += email["read"] ? " read" : " unread";

				element.innerHTML = `
        <p class="email-sender">${email["sender"]}</p> 
        <p class="email-subject">${email["subject"]}</p> 
        <p class="email-subject">${email["timestamp"]}</p>`;
				document.querySelector("#emails-view").appendChild(element);

				element.addEventListener("click", () =>
					open_email(email["id"], mailbox)
				);

      }
      else if (mailbox!== "archive"){
			let element = document.createElement("div");
			element.className = "email-item";
			element.className += email["read"] ? " read" : " unread";

			element.innerHTML = `<p class="email-sender">${email["sender"]}</p> <p class="email-subject">${email["subject"]}</p> <p class="email-subject">${email["timestamp"]}</p>`;
			document.querySelector("#emails-view").appendChild(element);
		

      element.addEventListener("click", () => open_email(email["id"],mailbox));
      }
		});

	})

}



