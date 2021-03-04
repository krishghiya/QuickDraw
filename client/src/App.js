import CanvasDraw from 'react-canvas-draw'

function App() {
  return (
    <div className="container">
        <h1>
          Welcome to Quick Draw!
        </h1>
        <CanvasDraw style={{
          position: 'absolute', left: '50%', top: '50%',
          transform: 'translate(-50%, -50%)'}}/>
    </div>
  );
}

export default App;
