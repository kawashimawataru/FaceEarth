const API_URL = "http://127.0.0.1:8000/items";

export async function getItems() {
  const response = await fetch(API_URL);
  return response.json();
}

export async function createItem(name: string) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  return response.json();
}
