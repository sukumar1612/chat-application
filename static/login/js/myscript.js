var uid=0;
var success=0;

// sends POST request along with appropriate headers to the end user
async function postFormDataAsJson({ url, formData }) {
	const plainFormData = Object.fromEntries(formData.entries());
	plainFormData['password']=CryptoJS.SHA256(plainFormData['password']).toString(CryptoJS.enc.Hex);					//does SHA 256 hash on password
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

	//console.log(url)
	//console.log(response)
	if (!response.ok) {
		const errorMessage = await response.text();
		alert("invaid username or password")
		throw new Error(errorMessage);
		window.location.href;																							//reloads page if error is found
	}


	return response.json();
}


//prevents default submit event and supplies data to this function
async function handleFormSubmit(event) {
	event.preventDefault();

	const form = event.currentTarget;
	var url = window.location.origin + "/auth";
	//const url1 = window.location.href;

	try {
		const formData = new FormData(form);
		const responseData = await postFormDataAsJson({ url, formData });									//submitting formdata to /auth

		url=window.location.href;

		const responseData1 = await postFormDataAsJson({ url, formData });									//submitting formdata to /login
		const plainFormData1 = Object.fromEntries(formData.entries());

		//console.log( {responseData} );
		if("access_token" in responseData)																				//checks if jwt token is present and stores it in the cookie
		{
			success=1;
			//alert("login successful "+responseData["access_token"]);
			//var plainFormData = Object.fromEntries(formData.entries());
			document.cookie="JWT "+responseData["access_token"]

		}
		if ("already_logged_in" in responseData1)																		//checks if user already logged in
		{
			alert("this user is already logged in");
		} else if(success==1) {
			uid=responseData1['user_id']
			plainFormData1['password']=CryptoJS.AES.encrypt(plainFormData1['password'], responseData1['key']).toString()	//stores password in AES encrypted form is successful authentication

			window.localStorage.setItem("pass"+String(uid),plainFormData1['password'])
			//console.log(window.localStorage.getItem("pass"+String(uid)))

			alert("login successful");
			window.location.href="/homepage/"+String(uid), true;														//redirects user to homepage
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

function newLocation() {
	window.location.href="/register";
}
