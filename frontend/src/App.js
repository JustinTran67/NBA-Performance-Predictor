import './App.css';
import SeasonStat from './components/SeasonStat';
import Predict from './components/Predict';
import PlayerPredict from './components/PlayerPredict';

function App() {
  return (
    <div className="App">
      <SeasonStat />
      <PlayerPredict />
    </div>
  );
}

export default App;
