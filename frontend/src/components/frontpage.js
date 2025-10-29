
export default function Frontpage() {

    //fetch player data from backend

    return (
        <div>
            <h1>NextPlay AI</h1>
            <SearchBar />
            <PlayerList playerData/>
        </div>
    )
}

function SearchBar() {
    return (
        <div>
            <input type="text" placeholder="Search players to get projections..." />
        </div>
    )
}

function PlayerList(playerData) { //use playerData to generate list of players from backend.
    return (
        <div>
            <h2>Players</h2>
            <ul>
                <li>{<PlayerCard name="Stephen Curry" position="PG" team="GSW"/>}</li>
                <li>{<PlayerCard name="Lebron James" position="SF" team="LAL"/>}</li>
                <li>{<PlayerCard name="Kevin Durant" position="PF" team="HOU"/>}</li>
            </ul>
        </div>
    )
}

function PlayerCard({ name, position, team }) {
    return (
        <div>
            <h3>{name}</h3>
            <p>{position}</p>
            <p>{team}</p>
        </div>
    )
}