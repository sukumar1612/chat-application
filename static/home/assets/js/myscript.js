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


async function handleFormSubmit(event) {
	event.preventDefault();

	const url = window.location.href;
	var x=url.split("/");
	//console.log(x[x.length-1])

	try {
		const responseData = await postFormDataAsJson({ url });

		//console.log({ responseData });
		if("names" in responseData)                                                                                     //inserts usernames into the table
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
}


window.addEventListener("load", handleFormSubmit);

function logout() {
    const url = window.location.href;
    var x=url.split("/");
    //console.log(x[x.length-1])
    window.location.href="/logout/"+x[x.length-1];
}

