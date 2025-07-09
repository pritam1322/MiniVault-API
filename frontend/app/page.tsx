import PromptForm from "@/components/PromptForm";
import Image from "next/image";

export default function Home() {
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-2xl font-bold mb-4">MiniVault Text Generator</h1>
      <PromptForm />
    </main>
  );
}
