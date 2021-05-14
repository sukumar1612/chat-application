var uid=0;
var success=0;


async function postFormDataAsJson({ url, formData }) {
	const plainFormData = Object.fromEntries(formData.entries());
	plainFormData['password']=CryptoJS.SHA256(plainFormData['password']).toString(CryptoJS.enc.Hex);
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
		alert("invaid username or password")
		throw new Error(errorMessage);

		window.location.href;
	}


	return response.json();
}



async function handleFormSubmit(event) {
	event.preventDefault();

	const form = event.currentTarget;
	const url = window.location.origin + "/auth";


	try {
		const formData = new FormData(form);
		const responseData = await postFormDataAsJson({ url, formData });

		//console.log( {responseData} );
		if("access_token" in responseData)
		{
			success=1;
			//alert("login successful "+responseData["access_token"]);
			var plainFormData = Object.fromEntries(formData.entries());
			document.cookie="JWT "+responseData["access_token"]

		}

	} catch (error) {
		console.error(error);
	}
}


async function handleFormSubmit1(event) {
	event.preventDefault();

	const form = event.currentTarget;
	const url = window.location.href;
	// console.log(url)

	try {
		const formData = new FormData(form);
		const responseData = await postFormDataAsJson({ url, formData });
		const plainFormData = Object.fromEntries(formData.entries());

		if ("already_logged_in" in responseData)
		{
			alert("this user is already logged in");
		} else if(success==1) {
			uid=responseData['user_id']
			plainFormData['password']=CryptoJS.AES.encrypt(plainFormData['password'], responseData['key']).toString()

			window.localStorage.setItem("pass"+String(uid),plainFormData['password'])
			//console.log(window.localStorage.getItem("pass"+String(uid)))

			alert("login successful");
			window.location.href="/homepage/"+String(uid), true;
		}
		else
		{
			window.location.href
		}

	} catch (error) {
		console.error(error);
	}
}



const exampleForm = document.getElementById("login-form");
exampleForm.addEventListener("submit", handleFormSubmit);
exampleForm.addEventListener("submit", handleFormSubmit1);

function newLocation() {
	window.location.href="/register";
}
