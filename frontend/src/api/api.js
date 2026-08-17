const API_BASE_URL = "http://127.0.0.1:8000"

export async function uploadDocument(file) {
  const formData = new FormData()
  formData.append("file", file)

  const response = await fetch(
    `${API_BASE_URL}/documents/upload`,
    {
      method: "POST",
      body: formData,
    }
  )

  if (!response.ok) {
    let message = "Failed to upload document."

    try {
      const errorData = await response.json()
      message = errorData.detail || message
    } catch {
      // Keep the default error message.
    }

    throw new Error(message)
  }

  return response.json()
}


export async function askQuestion(question, limit = 6) {
  const response = await fetch(
    `${API_BASE_URL}/rag/ask`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
        limit,
      }),
    }
  )

  if (!response.ok) {
    let message = "Failed to get an answer."

    try {
      const errorData = await response.json()
      message = errorData.detail || message
    } catch {
      // Keep the default error message.
    }

    throw new Error(message)
  }

  return response.json()
}