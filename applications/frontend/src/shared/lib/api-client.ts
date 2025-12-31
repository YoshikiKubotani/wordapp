const DEFAULT_API_BASE_URL = 'https://api.example.com'

type RequestOptions = {
  path: string
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'
  body?: unknown
  signal?: AbortSignal
}

const buildUrl = (path: string) => {
  const baseUrl = import.meta.env.VITE_API_BASE_URL || DEFAULT_API_BASE_URL
  return new URL(path, baseUrl).toString()
}

export async function apiRequest<T>(options: RequestOptions): Promise<T> {
  const { path, method = 'GET', body, signal } = options
  const response = await fetch(buildUrl(path), {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
    body: body ? JSON.stringify(body) : undefined,
    signal,
  })

  if (!response.ok) {
    const message = await safeReadErrorMessage(response)
    throw new Error(message)
  }

  const contentType = response.headers.get('content-type')
  if (contentType && contentType.includes('application/json')) {
    return (await response.json()) as T
  }

  return undefined as T
}

async function safeReadErrorMessage(response: Response) {
  try {
    const data = await response.json()
    if (typeof data?.message === 'string') {
      return data.message
    }
  } catch {
    // ignore JSON parse errors
  }
  return `API request failed with status ${response.status}`
}
