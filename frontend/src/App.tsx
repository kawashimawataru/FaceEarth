import { useEffect, useState } from "react";
import { getItems, createItem } from "./api";

function App() {
  const [items, setItems] = useState<{ id: number; name: string }[]>([]);
  const [name, setName] = useState("");

  useEffect(() => {
    getItems().then(setItems);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const newItem = await createItem(name);
    setItems([...items, newItem]);
    setName("");
  };

  return (
    <div>
      <h1>FastAPI + React</h1>
      <ul>
        {items.map((item) => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
      <form onSubmit={handleSubmit}>
        <input value={name} onChange={(e) => setName(e.target.value)} />
        <button type="submit">追加</button>
      </form>
    </div>
  );
}

export default App;
