Go server for competition talks to python clients and web clients

Each python client can be involved with only one game at a time

Before connecting to the server, the client boilerplate code prompts the user for a name.  Then the client generates a random passcode and transmits that passcode to the server.

After connecting the server, client connections are placed in a pool of available opponents.

Students can connect to the web client with the name and computer generated passcode.

Web clients can challenge opponents if their bot is not currently in action - check with the server after submitting a challenge request

Challenges cannot be denied (fix later if time); tell students to spin up a new bot if their current one is running

In a game, bots are given n+0.5 seconds per move.  We tell students n seconds, but add 0.5 seconds because network latencies and stuff.

During a game, moves are broadcast from the bot to 1) the other bot and 2) the web clients listening.

Games are assigned IDs.  Clients can connect to a game by going to /view/<game_id>

