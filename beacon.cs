using System.Text;
using System.Net;
using System.Text.Json;

var url = "https://eoqqzdfuzmgq7gg.m.pipedream.net/";

var request = WebRequest.Create(url);
request.Method = "POST";

var user = new User("John Doe", "gardener");
var json = JsonSerializer.Serialize(user);
byte[] byteArray = Encoding.UTF8.GetBytes(json);

request.ContentType = "application/x-www-form-urlencoded";
request.ContentLength = byteArray.Length;
request.UserAgent = "my user agent";

using var reqStream = request.GetRequestStream();
reqStream.Write(byteArray, 0, byteArray.Length);

using var response = request.GetResponse();
Console.WriteLine(((HttpWebResponse)response).StatusDescription);

using var respStream = response.GetResponseStream();

using var reader = new StreamReader(respStream);
string data = reader.ReadToEnd();
Console.WriteLine(data);

record User(string Name, string Occupation);