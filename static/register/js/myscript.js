//generating ECDH keys
function ab2str(buf) {
  return String.fromCharCode.apply(null, new Uint8Array(buf));
}

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


async function getkey(){
    const keyPair = await window.crypto.subtle.generateKey({name: "ECDH", namedCurve: "P-256",}, true, ["deriveKey", "deriveBits"]);
    const publicKeyJwk = await exportpublicKey(keyPair.publicKey);
    const privateKeyJwk = await exportprivateKey(keyPair.privateKey);
    return [publicKeyJwk, privateKeyJwk];
};




//sending and receiving data
async function postFormDataAsJson({ url, formData ,x1}) {
	const plainFormData = Object.fromEntries(formData.entries());

	plainFormData['publickey']=x1[0];
	plainFormData['privatekey']=CryptoJS.AES.encrypt(x1[1], plainFormData['password']).toString();
    plainFormData['password']=CryptoJS.SHA256(plainFormData['password']).toString(CryptoJS.enc.Hex);

	console.log(plainFormData, typeof (plainFormData))

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




async function handleFormSubmit(event) {
	event.preventDefault();

	const form = event.currentTarget;
	const url = window.location.href;
	console.log(url)

	try {
		const formData = new FormData(form);
		var x1= await getkey();
		console.log(x1[0],x1[1]);
		const responseData = await postFormDataAsJson({ url, formData ,x1});

		console.log({responseData});
		if(responseData["messege"]=="success")
		{
			alert("user "+responseData["username"]+" successfully registered")
			window.location.href="/login";
		}
	} catch (error) {
		console.error(error);
	}
}

function newLoc(){
	window.location.href="/login";
}
const exampleForm = document.getElementById("register-form");
exampleForm.addEventListener("submit", handleFormSubmit);