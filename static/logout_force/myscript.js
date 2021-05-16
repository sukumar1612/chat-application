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
	var url = window.location.href;
	//const url1 = window.location.href;

	try {
		const formData = new FormData(form);
		const responseData = await postFormDataAsJson({ url, formData });									//submitting formdata to /auth
		//console.log( {responseData} );
		if("message" in responseData)																				//checks if jwt token is present and stores it in the cookie
		{
			if(responseData["message"]=="successful"){
				alert("successfully logged out")
				window.location.href="/login";
			}else{
				alert(responseData["message"])
				window.location.href;
			}

		}


	} catch (error) {
		console.error(error);
	}
}

const exampleForm = document.getElementById("login-form");
exampleForm.addEventListener("submit", handleFormSubmit);

function newLocation() {
	window.location.href="/login";
}
