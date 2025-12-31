import { atom } from 'jotai'
import { atomWithMutation, atomWithQuery, queryClientAtom } from 'jotai-tanstack-query'
import { seedWords } from './seed-words'
import { apiRequest } from '@/shared/lib/api-client'
import type { Word } from '@/entities/word'

export type WordDraft = {
  term: string
  meaning: string
  note?: string
}

const WORDS_QUERY_KEY = ['words']

export const wordsQueryAtom = atomWithQuery<Word[]>((_get) => ({
  queryKey: WORDS_QUERY_KEY,
  queryFn: async ({ signal }) => apiRequest<Word[]>({ path: 'words', signal }),
  initialData: seedWords,
  staleTime: 5 * 60 * 1000,
}))

export const sortedWordsAtom = atom((get) => {
  const result = get(wordsQueryAtom)
  const words = result.data ?? []
  return [...words].sort(
    (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime(),
  )
})

export const wordStatsAtom = atom((get) => {
  const result = get(wordsQueryAtom)
  const words = result.data ?? []
  const newest = words.at(-1)
  return {
    total: words.length,
    newestTerm: newest?.term ?? null,
  }
})

export const registerWordMutationAtom = atomWithMutation<Word, WordDraft, Error>((get) => ({
  mutationKey: ['registerWord'],
  mutationFn: async (draft) => {
    const term = draft.term.trim()
    const meaning = draft.meaning.trim()
    const note = draft.note?.trim() || undefined

    if (!term || !meaning) {
      throw new Error('単語と意味の両方を入力してください')
    }

    const existing = get(sortedWordsAtom).find(
      (word) => word.term.trim().toLowerCase() === term.toLowerCase(),
    )

    const payload: WordDraft = { term, meaning, note }

    if (existing) {
      return apiRequest<Word>({
        path: `words/${encodeURIComponent(existing.id)}`,
        method: 'PUT',
        body: payload,
      })
    }

    return apiRequest<Word>({
      path: 'words',
      method: 'POST',
      body: payload,
    })
  },
  onSuccess: async (_data, _variables, _context) => {
    const queryClient = get(queryClientAtom)
    await queryClient.invalidateQueries({ queryKey: WORDS_QUERY_KEY })
  },
}))

export const removeWordMutationAtom = atomWithMutation<undefined, string, Error>((get) => ({
  mutationKey: ['removeWord'],
  mutationFn: async (id) =>
    apiRequest({
      path: `words/${encodeURIComponent(id)}`,
      method: 'DELETE',
    }),
  onSuccess: async () => {
    const queryClient = get(queryClientAtom)
    await queryClient.invalidateQueries({ queryKey: WORDS_QUERY_KEY })
  },
}))
