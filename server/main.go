package main

import (
	"flag"
	"net/http"
)

var (
	port = flag.String("ports", ":10914", "port to use")
)


func main() {
	flag.Parse()
	// http.HandleFunc("/", homeHandler)
	// http.HandleFunc("/", viewHandler)

	if err := http.ListenAndServe(*addr, nil); err != nil {
		log.Fatal("Listen'nServe: ", err)
	}
}

