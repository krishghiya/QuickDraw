import CanvasDraw from 'react-canvas-draw'
import {useState} from 'react'
import axios from 'axios'

function sendData(data) {
  axios.post('http://localhost:8000/data/', {
    lines: data
  }, {
    headers: {
      'Content-Type': 'application/json',
    },
  }).then(res => {
    console.log(res);
    return res;
  })
}

function App() {

  const [color, setColor] = useState('black')
  const [saveableCanvas, setsaveableCanvas] = useState(null)

  return (
    <div className="container">
        <h1>
          Welcome to Quick Draw!
        </h1>
        <CanvasDraw 
          className='canvas'
          ref={canvasDraw => setsaveableCanvas(canvasDraw)}
          onChange={() => setColor("#" + Math.floor(Math.random() * 16777215).toString(16))}
          brushColor={color}
          hideGrid={true}
          brushRadius={2}
          lazyRadius={0}
        />
        <div className='button'>
          <button onClick={() => sendData(saveableCanvas.getSaveData())}>Predict Doodle</button>
          <button onClick={() => saveableCanvas.clear()}>Clear Screen</button>
        </div>
    </div>
  );
}

export default App;
