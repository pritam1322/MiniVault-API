'use client';

import { useState } from "react";

export default function PromptForm() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [model, setModel] = useState("phi"); 

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setResponse("");

    const res = await fetch("http://localhost:8000/generate/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, model }), 
    });

    
    const reader = res.body?.getReader();
    let final = "";
    while (reader) {
        const { value, done } = await reader.read();
        if (done) break;
        final += new TextDecoder().decode(value);
        setResponse(final || "No response.");
        setLoading(false);
    }
  }

  return (
    <section className="max-w-xl mx-auto mt-16">
      <form onSubmit={handleSubmit} className="space-y-4">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter your prompt..."
          className="w-full p-2 border rounded bg-neutral-900"
          rows={4}
        />

        <select
          value={model}
          onChange={(e) => setModel(e.target.value)}
          className="w-full p-2 border rounded bg-neutral-900"
        >
          <option className="bg-blue-200 text-blue-900" value="phi">phi-2 (lightweight)</option>
        </select>

        <div className="flex gap-4">

            <button
            type="submit"
            className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 w-full"
            >
            {loading ? "Generating..." : "Generate"}
            </button>

            <button
            type="submit"
            className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 w-full"
            >               
            {loading ? "Streaming......" : "Stream"}
            </button>

        </div>
        {  loading && (
            <h1>Hold on model is working at backend :/</h1>
        )}
      </form>

      {response && (
        <div className="mt-6 p-4 border rounded bg-gray-100 text-black">
          <h3 className="font-bold mb-2">Response:</h3>
          <pre className="whitespace-pre-wrap">{response}</pre>
        </div>
      )}
    </section>
  );
}
