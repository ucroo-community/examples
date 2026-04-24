function(payload){
let user = JSON.stringify(fromJValue(payload.get('campusCookieValidatorUserJValue').get()))
//let user = fromJValue(payload.get('campusCookieValidatorUserJValue').get())

debug('userDebug',user)
warn('userWarn',user)

return [code_data_SimpleStringData(user)];
}