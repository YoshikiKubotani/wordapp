import { atom } from 'jotai'
import { atomWithStorage, createJSONStorage } from 'jotai/utils'
import { seedWords } from './seed-words'
import type { Word } from '@/entities/word'

export type WordDraft = {
  term: string
  meaning: string
  note?: string
}

const generateWordId = () => {
  const cryptoObj = typeof globalThis !== 'undefined' ? globalThis.crypto : undefined
  if (cryptoObj?.randomUUID) return cryptoObj.randomUUID()
  if (cryptoObj?.getRandomValues) {
    const parts = cryptoObj.getRandomValues(new Uint32Array(4))
    return (
      'word-' +
      Array.from(parts)
        .map((value) => value.toString(16).padStart(8, '0'))
        .join('')
    )
  }
  return `word-${Date.now()}-${Math.random().toString(16).slice(2)}`
}

const storage = createJSONStorage<Word[]>(() =>
  typeof window === 'undefined' ? undefined : localStorage,
)

export const wordsAtom = atomWithStorage<Word[]>('wordapp.words', seedWords, storage)

export const sortedWordsAtom = atom((get) =>
  [...get(wordsAtom)].sort(
    (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime(),
  ),
)

export const wordStatsAtom = atom((get) => {
  const words = get(wordsAtom)
  const newest = words.at(-1)
  return {
    total: words.length,
    newestTerm: newest?.term ?? null,
  }
})

export const registerWordAtom = atom(null, (get, set, draft: WordDraft) => {
  const term = draft.term.trim()
  const meaning = draft.meaning.trim()
  if (!term || !meaning) return

  const normalizedTerm = term.toLowerCase()
  const words = get(wordsAtom)
  const existingIndex = words.findIndex((word) => word.term.toLowerCase() === normalizedTerm)

  const nextWord: Word = {
    id: existingIndex >= 0 ? words[existingIndex].id : generateWordId(),
    term,
    meaning,
    note: draft.note?.trim() || undefined,
    createdAt: existingIndex >= 0 ? words[existingIndex].createdAt : new Date().toISOString(),
  }

  if (existingIndex >= 0) {
    const nextWords = [...words]
    nextWords[existingIndex] = nextWord
    set(wordsAtom, nextWords)
    return
  }

  set(wordsAtom, [...words, nextWord])
})

export const removeWordAtom = atom(null, (get, set, id: string) => {
  const nextWords = get(wordsAtom).filter((word) => word.id !== id)
  set(wordsAtom, nextWords)
})
