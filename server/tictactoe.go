package main

import (
	"sync"
)

var (
	TTT_id = 0
	TTT_id_lock = sync.RWMutex{}
	TTTGames = make(map[int] *TTTGame)
)


type TTTMove struct {
	player *Player
	xloc int
	yloc int
}

type TTTPiece struct {
	xloc int
	yloc int
}

type TTTGame struct {
	game_id string
	player1 *Player
	player2 *Player

	history []Move
	finished bool

	state [
}

func TTTGameInit(player1, player2 *Player) {
	TTT_id_lock.Lock()
	defer func() {
		TTT_id_lock.Unlock()
	}

	TTTGame game {
		TTT_id,
		player1, player2,
		make([]TTTMove, 9),
		false
	}

	TTTGames[game.TTT_id] = &game
}

func TTTGameInit(move TTTMove) bool {
	if 
}

func broadcastGames() {
	game_ids = make([]int, 0)

	for game_id, game := range(TTTGames) {
		if !game.finished {
			game_ids = append(game_ids, game_id)
		}
	}

	// TODO: actually broadcast
}

