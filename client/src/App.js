import CanvasDraw from 'react-canvas-draw'
import {useState} from 'react'
import axios from 'axios'

const defaultList = [
  {
    name: 'No prediction', 
    confidence: '100',
  }]

function App() {

  async function sendData(data) {
    try {
      const res = await axios.post('http://localhost:8000/data/', {
        lines: data
        }, {
          headers: {
            'Content-Type': 'application/json',
          },
        }).then(res => setList(res['data']))
      return res;
    }catch (error) {
      setList(defaultList)  
    }
  }

  const [color, setColor] = useState('black')
  const [saveableCanvas, setsaveableCanvas] = useState(null)
  const [list, setList] = useState(defaultList)
  
  return (
    <div className="container">
        <h1>
          Welcome to Quick Draw!
        </h1>
          <CanvasDraw 
            className='canvas'
            ref={canvasDraw => setsaveableCanvas(canvasDraw)}
            onChange={() => {
              setColor("#" + Math.floor(Math.random() * 16777215).toString(16));
              sendData(saveableCanvas.getSaveData());
            }}
            brushColor={color}
            hideGrid={true}
            brushRadius={2}
            lazyRadius={0}
          />
          <ol className='results'>
            {list.map((item) => (
            <li key={item.name}>
              <p>Resembles <b>{item.name}</b> with confidence: {item.confidence}%</p>
            </li>
            ))}
          </ol>
        <button className='button' onClick={() => {saveableCanvas.clear();setList(defaultList);}}>
            Clear Screen
        </button>
    </div>
  );
}

export default App;
