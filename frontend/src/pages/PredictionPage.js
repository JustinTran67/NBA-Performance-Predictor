import PlayerPredict from '../components/PlayerPredict';
import { Link } from 'react-router-dom';

export default function PredictionPage() {
    return (
        <div>
            <Link to="/">Home</Link>
            <PlayerPredict />
        </div>
    )
}