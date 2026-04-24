function(payload){
let apiKey = getConfig('[CONFIG_NAME]')

return [
  new HttpRequest(
    'https', //scheme, //java.lang.String
    'api.nasa.gov', //host, //java.lang.String
    443, //port, // int
    newList(['planetary', 'apod']), //path, // scala.collection.immutable.List[java.lang.String]
    'GET', //verb, // java.lang.String
    toKVList([
      ['api_key', apiKey]
    ]) //params, // scala.collection.immutable.Map[java.lang.Stringjava.lang.String]
  )
];
}