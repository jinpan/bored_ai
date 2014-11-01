package main

var (
	Players = make(map[string] Player)
)


type Player struct {
	ws *websocket.Conn
	username string
	passcode string

	game Game
}

func handler(player *Player) {
	
}
