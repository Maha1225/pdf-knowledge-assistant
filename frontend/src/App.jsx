import { useState } from "react"
import { askQuestion, uploadDocument } from "./api/api"


function App() {
  const [file, setFile] = useState(null)
  const [document, setDocument] = useState(null)
  const [question, setQuestion] = useState("")
  const [messages, setMessages] = useState([])
  const [uploading, setUploading] = useState(false)
  const [asking, setAsking] = useState(false)
  const [error, setError] = useState("")


  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0]

    if (!selectedFile) {
      return
    }

    if (!selectedFile.name.toLowerCase().endsWith(".pdf")) {
      setError("Please select a PDF file.")
      setFile(null)
      return
    }

    setError("")
    setFile(selectedFile)
  }


  const handleUpload = async () => {
    if (!file) {
      setError("Please select a PDF file first.")
      return
    }

    setUploading(true)
    setError("")

    try {
      const result = await uploadDocument(file)

      setDocument(result)

      setMessages([
        {
          role: "assistant",
          content: `I've loaded "${result.filename}". You can now ask questions about the document.`,
        },
      ])
    } catch (err) {
      setError(err.message || "Upload failed.")
    } finally {
      setUploading(false)
    }
  }


  const handleAsk = async (event) => {
    event.preventDefault()

    const trimmedQuestion = question.trim()

    if (!trimmedQuestion) {
      return
    }

    if (!document) {
      setError("Please upload a PDF before asking a question.")
      return
    }

    setError("")

    const userMessage = {
      role: "user",
      content: trimmedQuestion,
    }

    setMessages((current) => [
      ...current,
      userMessage,
    ])

    setQuestion("")
    setAsking(true)

    try {
      const result = await askQuestion(trimmedQuestion)

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: result.answer,
          sources: result.sources || [],
        },
      ])
    } catch (err) {
      setError(err.message || "Failed to get an answer.")
    } finally {
      setAsking(false)
    }
  }


  return (
    <div className="min-h-screen bg-slate-950 text-white">

      <header className="border-b border-slate-800 bg-slate-950/95">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">

          <div>
            <h1 className="text-2xl font-bold tracking-tight">
              PDF Knowledge Assistant
            </h1>

            <p className="mt-1 text-sm text-slate-400">
              Ask questions and get answers from your documents
            </p>
          </div>

          <div className="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-4 py-2 text-sm text-emerald-400">
            Local AI
          </div>

        </div>
      </header>


      <main className="mx-auto grid max-w-6xl gap-6 px-6 py-8 lg:grid-cols-[340px_1fr]">

        {/* Upload Section */}

        <section className="h-fit rounded-2xl border border-slate-800 bg-slate-900 p-6">

          <h2 className="text-lg font-semibold">
            Upload Document
          </h2>

          <p className="mt-2 text-sm leading-6 text-slate-400">
            Upload a PDF and ask questions about its contents.
          </p>


          <label className="mt-6 flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-slate-700 bg-slate-950 p-8 text-center transition hover:border-blue-500">

            <div className="text-4xl">
              📄
            </div>

            <span className="mt-3 text-sm font-medium">
              Choose PDF
            </span>

            <span className="mt-1 text-xs text-slate-500">
              PDF files only
            </span>

            <input
              type="file"
              accept=".pdf,application/pdf"
              onChange={handleFileChange}
              className="hidden"
            />

          </label>


          {file && (
            <div className="mt-4 rounded-lg bg-slate-800 p-3">

              <p className="truncate text-sm font-medium">
                {file.name}
              </p>

              <p className="mt-1 text-xs text-slate-400">
                {(file.size / 1024 / 1024).toFixed(2)} MB
              </p>

            </div>
          )}


          <button
            type="button"
            onClick={handleUpload}
            disabled={!file || uploading}
            className="mt-4 w-full rounded-lg bg-blue-600 px-4 py-3 font-medium transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {uploading ? "Uploading..." : "Upload PDF"}
          </button>


          {document && (
            <div className="mt-5 rounded-xl border border-emerald-500/20 bg-emerald-500/10 p-4">

              <p className="text-sm font-medium text-emerald-400">
                Document ready
              </p>

              <p className="mt-2 break-words text-sm text-slate-300">
                {document.filename}
              </p>

              <p className="mt-1 text-xs text-slate-400">
                {document.page_count} page(s)
              </p>

            </div>
          )}


          {error && (
            <div className="mt-5 rounded-lg border border-red-500/20 bg-red-500/10 p-3 text-sm text-red-400">
              {error}
            </div>
          )}

        </section>


        {/* Chat Section */}

        <section className="flex min-h-[650px] flex-col overflow-hidden rounded-2xl border border-slate-800 bg-slate-900">

          <div className="border-b border-slate-800 px-6 py-5">

            <h2 className="text-lg font-semibold">
              Document Chat
            </h2>

            <p className="mt-1 text-sm text-slate-400">
              Powered by RAG + Ollama
            </p>

          </div>


          <div className="flex-1 space-y-5 overflow-y-auto p-6">

            {messages.length === 0 && (
              <div className="flex h-full min-h-[500px] items-center justify-center text-center">

                <div>

                  <div className="text-5xl">
                    💬
                  </div>

                  <h3 className="mt-4 text-xl font-semibold">
                    Start a conversation
                  </h3>

                  <p className="mt-2 max-w-md text-sm leading-6 text-slate-400">
                    Upload a PDF on the left, then ask questions about
                    the document.
                  </p>

                </div>

              </div>
            )}


            {messages.map((message, index) => (
              <div
                key={index}
                className={
                  message.role === "user"
                    ? "flex justify-end"
                    : "flex justify-start"
                }
              >

                <div
                  className={
                    message.role === "user"
                      ? "max-w-[80%] rounded-2xl rounded-br-md bg-blue-600 px-5 py-3 text-sm leading-6"
                      : "max-w-[85%] rounded-2xl rounded-bl-md bg-slate-800 px-5 py-3 text-sm leading-6 text-slate-200"
                  }
                >

                  <p className="whitespace-pre-wrap">
                    {message.content}
                  </p>


                  {message.sources?.length > 0 && (
                    <div className="mt-4 border-t border-slate-700 pt-3">

                      <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
                        Sources
                      </p>

                      <div className="space-y-1">

                        {message.sources.map((source, sourceIndex) => (
                          <div
                            key={sourceIndex}
                            className="text-xs text-slate-400"
                          >
                            Page {source.page_number}
                            {" · "}
                            Chunk {source.chunk_index}
                            {" · "}
                            Distance {Number(source.distance).toFixed(4)}
                          </div>
                        ))}

                      </div>

                    </div>
                  )}

                </div>

              </div>
            ))}


            {asking && (
              <div className="flex justify-start">

                <div className="rounded-2xl rounded-bl-md bg-slate-800 px-5 py-3 text-sm text-slate-400">
                  Thinking...
                </div>

              </div>
            )}

          </div>


          <form
            onSubmit={handleAsk}
            className="border-t border-slate-800 p-4"
          >

            <div className="flex gap-3">

              <input
                type="text"
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                placeholder={
                  document
                    ? "Ask something about your PDF..."
                    : "Upload a PDF first..."
                }
                disabled={!document || asking}
                className="min-w-0 flex-1 rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm outline-none transition placeholder:text-slate-600 focus:border-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
              />

              <button
                type="submit"
                disabled={!document || !question.trim() || asking}
                className="rounded-xl bg-blue-600 px-6 py-3 text-sm font-medium transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {asking ? "..." : "Ask"}
              </button>

            </div>

          </form>

        </section>

      </main>

    </div>
  )
}


export default App