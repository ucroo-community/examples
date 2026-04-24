function(item,payload){
let apiCall = JSON.parse(new JavaString(item.body().get(),'UTF-8'))
let user = fromJValue(payload.get('campusCookieValidatorUserJValue').get())

let newResponseShape = {
	title: apiCall.title,
  	url: apiCall.url,
  	explanation: apiCall.explanation,
  	when: new Date().getTime(),
  	status: "short on coffee",
  	username: user.first_name
}

return new code_model_flows_processors_http_HttpResponse(
	200, //status code
  	toKVList([['content-type','application/json']]),//headers
  	Some(JSON.stringify(newResponseShape).getBytes('UTF-8'))//body
)
}