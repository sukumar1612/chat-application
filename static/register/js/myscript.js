//generating ECDH keys
//reference https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto
//see examples section for more info

function ab2str(buf) {
  return String.fromCharCode.apply(null, new Uint8Array(buf));
}
// all of this is done to export the keys in PEM format
//this function exports public key in spki format(standard format to store public key)
async function exportpublicKey(key) {
  const exported = await window.crypto.subtle.exportKey(
      "spki",
      key
  );
  const exportedAsString = ab2str(exported);
  const exportedAsBase64 = window.btoa(exportedAsString);
  const pemExported = `-----BEGIN PUBLIC KEY-----\n${exportedAsBase64}\n-----END PUBLIC KEY-----`;
  return pemExported;
}

//this function exports the private key in pksc8 format(standard format to store private key) i
async function exportprivateKey(key) {
  const exported = await window.crypto.subtle.exportKey(
    "pkcs8",
    key
  );
  const exportedAsString = ab2str(exported);
  const exportedAsBase64 = window.btoa(exportedAsString);
  const pemExported = `-----BEGIN PRIVATE KEY-----\n${exportedAsBase64}\n-----END PRIVATE KEY-----`;
  return pemExported;
}

//it generates the public private key pair
async function getkey(){
    const keyPair = await window.crypto.subtle.generateKey({name: "ECDH", namedCurve: "P-256",}, true, ["deriveKey", "deriveBits"]);
    const publicKeyJwk = await exportpublicKey(keyPair.publicKey);
    const privateKeyJwk = await exportprivateKey(keyPair.privateKey);
    return [publicKeyJwk, privateKeyJwk];
};




//sending and receiving data
//sends data over to the server to be stored in the database it includes username, email, password(hashed with sha256), public key and privatekey(encrypted with AES)
async function postFormDataAsJson({ url, formData ,x1}) {
	const plainFormData = Object.fromEntries(formData.entries());

	plainFormData['publickey']=x1[0];
	plainFormData['privatekey']=CryptoJS.AES.encrypt(x1[1], plainFormData['password']).toString();
    plainFormData['password']=CryptoJS.SHA256(plainFormData['password']).toString(CryptoJS.enc.Hex);

	//console.log(plainFormData, typeof (plainFormData))

	const formDataJsonString = JSON.stringify(plainFormData);

	const fetchOptions = {
		method: "POST",
		headers: {
		    	"Content-Type": "application/json",
		    	Accept: "application/json",
	    	},
		    body: formDataJsonString,
	    };

	const response = await fetch(url, fetchOptions);

	if (!response.ok) {
	    const errorMessage = await response.text();
	    throw new Error(errorMessage);
	}
	return response.json();
}


//prevents the submission of the form from doing the default and instead takes over
// waits for response from the server and then redirects user to login page
async function handleFormSubmit(event) {
	event.preventDefault();

	const form = event.currentTarget;
	const url = window.location.href;
	//console.log(url)

	try {
		const formData = new FormData(form);
		var x1= await getkey();
		//console.log(x1[0],x1[1]);
		const responseData = await postFormDataAsJson({ url, formData ,x1});

		//console.log({responseData});
		if(responseData["messege"]=="success")
		{
			alert("user "+responseData["username"]+" successfully registered")
			window.location.href="/login";
		}else if(responseData["messege"]=="username already exists"){
			alert ("Username already exists")
		}
	} catch (error) {
		console.error(error);
	}
}

// this is if the user has already registered he can manually go back to the login page
function newLoc(){
	window.location.href="/login";
}
const exampleForm = document.getElementById("register-form");
exampleForm.addEventListener("submit", handleFormSubmit);