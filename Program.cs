using System;
using System.Net;
using System.Net.Http;
// https://qawithexperts.com/article/c-sharp/run-cmd-commands-using-c/520
// https://stackoverflow.com/a/27326758/9329272

namespace Testing
{
    public class Program
    {
        static readonly HttpClient client = new HttpClient();
        static void Main()
        {
            string command = "whoami";
			
            string whoami = ExecuteMe(command);

            Console.WriteLine(whoami);

            Task<string> post = PostMe("https://eoqqzdfuzmgq7gg.m.pipedream.net/");

            Console.WriteLine(post);

            Task<string> stat = GetMe("https://eoqqzdfuzmgq7gg.m.pipedream.net/");

            Console.WriteLine(stat);
        }
        static async Task<string> GetMe(string place, string subdir = "/"){
                client.BaseAddress = new Uri(place);
                HttpResponseMessage response = client.GetAsync(subdir).Result;
                response.EnsureSuccessStatusCode();
                string result = response.Content.ReadAsStringAsync().Result;
                return result;
        }
        public static async Task<string> PostMe(string url)
        {
            var values = new Dictionary<string, string>
            {  
                { "accountidentifier", "Data you want to send at account field" },
                { "type", "Data you want to send at type field"},
                { "seriesid", "The data you went to send at seriesid field"
                }
            };
            //form "postable object" if that makes any sense
            var content = new FormUrlEncodedContent(values);
            //POST the object to the specified URI 
            var response = await client.PostAsync(url, content);
            //Read back the answer from server
            var responseString = await response.Content.ReadAsStringAsync();
            return responseString;
        }
        static string ExecuteMe(string command){
            System.Diagnostics.ProcessStartInfo procStartInfo = new System.Diagnostics.ProcessStartInfo("cmd", "/c " + command);
			procStartInfo.RedirectStandardOutput = true;
            procStartInfo.UseShellExecute = false;
            // Do not create the black window.
            procStartInfo.CreateNoWindow = true;
            // Now we create a process, assign its ProcessStartInfo and start it
            System.Diagnostics.Process proc = new System.Diagnostics.Process();
            proc.StartInfo = procStartInfo;
            proc.Start();

            // Get the output into a string
            string ressy = proc.StandardOutput.ReadToEnd();
            return ressy;
        }
    }
}