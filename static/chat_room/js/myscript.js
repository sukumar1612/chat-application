const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");
const msger=get(".msger-header");



// Icons made by Freepik from www.flaticon.com
const BOT_IMG = "https://image.flaticon.com/icons/svg/327/327779.svg";
const PERSON_IMG = "https://image.flaticon.com/icons/svg/145/145867.svg";
const BOT_NAME = "BOT";
const PERSON_NAME = "Sajad";

function appenduser(usern)
{
    const msgg=`<div class="msger-header-options">
      Username : ${usern}
    </div>`;

    msger.insertAdjacentHTML("beforeend", msgg);
}

function appendMessage(name, img, side, text) {
  //   Simple solution for small apps
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}

// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}




var recipient_publickey;
var user_privatekey;
var user_publickey;
var user_password;
var derived_key;
var you;

//jwt auth
async function postFormDataAsJson({ url }) {
    var jwt;
	var x=document.cookie.split(";");

    for (i of x){
        if(i.includes("JWT ")){
            jwt=i;
            break;
        }
    }

    //console.log(jwt)

	const fetchOptions = {
		method: "POST",
		headers: {
			"Authorization": jwt,
			Accept: "application/json",
		}
	};

	const response = await fetch(url, fetchOptions);

	if (!response.ok) {
		const errorMessage = await response.text();
		//console.log("invalid token");
		alert("Invalid JWT........redirecting to login");
        window.location.href="/login";
        throw new Error(errorMessage);

	}

	return response.json();
}


$(window).load(async function (){
	//event.preventDefault();

	const url = window.location.href;
	var x=url.split("/");
	//console.log(x[x.length-2])

	try {
		const responseData = await postFormDataAsJson({ url });

		//console.log({ responseData });
		if("names" in responseData)
        {
          for (i of responseData["names"])
          {
            if(i[0]!=x[x.length-1])
            {
                var table = document.getElementById("myTable");
                var row = table.insertRow(1);
                var cell = row.insertCell(0);
                var url1= url+ '/' +String(i[0]);
                cell.innerHTML='<a href="'+url1+'">'+i[1]+'</a>';
            }
          }
        }
	} catch (error) {
		console.error(error);
	}
})


//e2ee encryption functions

//generating ECDH keys
//reference https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto
//see examples section for more info
// summary of the functions : it takes in keys in PEM format and converts them into a format of type Crypto

function str2ab(str) {
  const buf = new ArrayBuffer(str.length);
  const bufView = new Uint8Array(buf);
  for (let i = 0, strLen = str.length; i < strLen; i++) {
    bufView[i] = str.charCodeAt(i);
  }
  return buf;
}

function importPrivateKey(pem) {
  // fetch the part of the PEM string between header and footer
  const pemHeader = "-----BEGIN PRIVATE KEY-----";
  const pemFooter = "-----END PRIVATE KEY-----";
  const pemContents = pem.substring(pemHeader.length, pem.length - pemFooter.length);
  // base64 decode the string to get the binary data
  const binaryDerString = window.atob(pemContents);
  // convert from a binary string to an ArrayBuffer
  const binaryDer = str2ab(binaryDerString);

  return window.crypto.subtle.importKey(
    "pkcs8",
    binaryDer,
     {
      name: "ECDH",
      namedCurve: "P-256",
    },
    true,
    ["deriveKey", "deriveBits"]
  );
}

function importPublicKey(pem) {
    // fetch the part of the PEM string between header and footer
    const pemHeader = "-----BEGIN PUBLIC KEY-----";
    const pemFooter = "-----END PUBLIC KEY-----";
    const pemContents = pem.substring(pemHeader.length, pem.length - pemFooter.length);
    // base64 decode the string to get the binary data
    const binaryDerString = window.atob(pemContents);
    // convert from a binary string to an ArrayBuffer
    const binaryDer = str2ab(binaryDerString);

    return window.crypto.subtle.importKey(
        "spki",
        binaryDer,
        {
        name: "ECDH",
        namedCurve: "P-256",
        },
        true,
        []
    );
}


//takes recipient public key and user private key and generates shared key
async function derive_key(publicKeyJwk, privateKeyJwk){
  const publicKey = await importPublicKey(publicKeyJwk)

  const privateKey = await importPrivateKey(privateKeyJwk)

  return await window.crypto.subtle.deriveKey(
    { name: "ECDH", public: publicKey },
    privateKey,
    { name: "AES-GCM", length: 256 },
    true,
    ["encrypt", "decrypt"]
  );
};

//encrypts data using AES encryption and accepts shared key as password
async function encrypt_data(text, derivedKey){
  const encodedText = new TextEncoder().encode(text);

  const encryptedData = await window.crypto.subtle.encrypt(
    { name: "AES-GCM", iv: new TextEncoder().encode("Initialization Vector") },
    derivedKey,
    encodedText
  );

  const uintArray = new Uint8Array(encryptedData);

  const string = String.fromCharCode.apply(null, uintArray);

  const base64Data = btoa(string);

  return base64Data;
};

//decrypts AES encrypted data
async function decrypt_data(text, derivedKey) {
  try {

    const string = atob(text);
    const uintArray = new Uint8Array(
      [...string].map((char) => char.charCodeAt(0))
    );
    const algorithm = {
      name: "AES-GCM",
      iv: new TextEncoder().encode("Initialization Vector"),
    };
    const decryptedData = await window.crypto.subtle.decrypt(
      algorithm,
      derivedKey,
      uintArray
    );

    return new TextDecoder().decode(decryptedData);
  } catch (e) {
    return `error decrypting message: ${e}`;
  }
};

//websockets(socketio) part
$(document).ready(function(){

    const url1 = window.location.href;
    var socket = io.connect(window.location.origin);
    //console.log(window.location.origin);
    var uid=url1.split("/");

    user_password = window.localStorage.getItem("pass"+uid[uid.length-2])                                           //retrives password from local storage (encrypted)
    if(user_password=="logged out")
    {
        alert("unauthorised access")
        window.location.href="/login";
    }
   // console.log("password is :"+user_password)
                                                                                                                        //establishes socket connection and sends userid and recipient id
    socket.on( 'connect', function() {
        const url = window.location.href;
        var x=url.split("/");

        socket.emit( 'connect_user', {
            userid : String(x[x.length-2]),
            recipientid : String(x[x.length-1])
        });

    })
                                                                                                                        //receives info such as username,recipientid, 16byte hex token,
    socket.on( 'connect_return', async function(msg) {                                                                  //chat history and the required ECDH keys
        //console.log(msg['publicKey'])
        recipient_publickey=msg['recipient_publickey']
        user_publickey=msg['user_publickey']

       // console.log(user_password+"   ",msg['key'])
        if(msg['key']=="None")
        {
            alert("unauthorised access")
            window.location.href="/login";
        }

        user_password=CryptoJS.AES.decrypt(user_password, msg['key']).toString(CryptoJS.enc.Utf8);
        console.log(user_password)

        user_privatekey=CryptoJS.AES.decrypt(msg['user_privatekey'], String(user_password)).toString(CryptoJS.enc.Utf8);

       // console.log(recipient_publickey,user_publickey,user_privatekey)

        derived_key= await derive_key(recipient_publickey, user_privatekey)
        you = msg['you']

       // console.log("-----------------connect-------------------")
       // console.log(derived_key)
       // console.log("-----------------connect-------------------")
        console.log(msg['text_hist'])
        //console.log("-----------------connect-------------------")
        //console.log(msg['mapping'])
        //console.log(you)

        appenduser(you);
        var txt;
        if (msg['text_hist']!=null){
            msg['text_hist']=msg['text_hist'].reverse();
            for (txt of msg['text_hist']){
                var mess=await decrypt_data(String(txt[1]), derived_key);
                if(msg['mapping'][txt[0]]==you)
                {
                    appendMessage("you", PERSON_IMG, "right", mess);
                }
                else
                {
                    appendMessage(msg['mapping'][txt[0]], PERSON_IMG, "left", mess);
                }
            }}

    })
    var form = $( 'form' ).on( 'submit', async function( e ) {                                                          //on submission of form it extracts message and
        e.preventDefault()                                                                                              //performs encryption then sends along with info like userid and
                                                                                                                        //recipient id
        const url = window.location.href;
        var x=url.split("/");

        let userid =  String(x[x.length-2])
        let recipientid =  String(x[x.length-1])
        //console.log(userid, recipientid)

        let user_input = await encrypt_data($( 'input.msger-input' ).val(), derived_key)
        //console.log("messege sent"+await decrypt_data(String(user_input), derived_key)+" "+typeof(user_input))

        socket.emit( 'sending_text', {
            userid : userid,
            recipientid : recipientid,
            message : user_input
        })
        $( 'input.msger-input' ).val( '' ).focus()
    })

socket.on( 'text_response', async function( msg ) {                                                                     //receives message and decrypts it
        //console.log( msg )
        if( typeof msg.username !== 'undefined' ) {
            var mess=await decrypt_data(String(msg['message']), derived_key);
            if(msg['username']==you)
            {
                appendMessage("you", PERSON_IMG, "right", mess);
            }
            else
            {
                appendMessage(msg['username'], PERSON_IMG, "left", mess);
            }
        }
    })
})


function newLoc(){
    const url1 = window.location.href;
    var uid=url1.split("/");

	window.location.href="/homepage/"+uid[uid.length-2];
}