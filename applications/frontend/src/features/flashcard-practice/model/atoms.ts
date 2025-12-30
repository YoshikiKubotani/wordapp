import { atom } from 'jotai'
import type { Word } from '@/entities/word'

export type FlashcardSession = {
  queue: Word[]
  currentIndex: number
  revealed: boolean
  correctCount: number
  incorrectCount: number
  startedAt: string | null
}

const emptySession: FlashcardSession = {
  queue: [],
  currentIndex: 0,
  revealed: false,
  correctCount: 0,
  incorrectCount: 0,
  startedAt: null,
}

const flashcardSessionAtom = atom<FlashcardSession>(emptySession)

export const startSessionAtom = atom(null, (_get, set, words: Word[]) => {
  if (!words.length) {
    set(flashcardSessionAtom, emptySession)
    return
  }

  set(flashcardSessionAtom, {
    queue: shuffleWords(words),
    currentIndex: 0,
    revealed: false,
    correctCount: 0,
    incorrectCount: 0,
    startedAt: new Date().toISOString(),
  })
})

export const revealCardAtom = atom(null, (get, set) => {
  const session = get(flashcardSessionAtom)
  if (!session.queue.length || session.revealed) return
  set(flashcardSessionAtom, { ...session, revealed: true })
})

type Grade = 'correct' | 'incorrect'

export const gradeCardAtom = atom(null, (get, set, grade: Grade) => {
  const session = get(flashcardSessionAtom)
  if (!session.queue.length || session.currentIndex >= session.queue.length) return

  const nextIndex = session.currentIndex + 1
  set(flashcardSessionAtom, {
    ...session,
    currentIndex: Math.min(nextIndex, session.queue.length),
    revealed: false,
    correctCount: session.correctCount + (grade === 'correct' ? 1 : 0),
    incorrectCount: session.incorrectCount + (grade === 'incorrect' ? 1 : 0),
  })
})

export const resetSessionAtom = atom(null, (_get, set) => {
  set(flashcardSessionAtom, emptySession)
})

export const activeCardAtom = atom((get) => {
  const session = get(flashcardSessionAtom)
  if (!session.queue.length || session.currentIndex >= session.queue.length) return null
  return session.queue[session.currentIndex]
})

export const practiceProgressAtom = atom((get) => {
  const session = get(flashcardSessionAtom)
  const total = session.queue.length
  const completed = Math.min(session.currentIndex, total)
  const isFinished = completed >= total && total > 0

  return {
    total,
    completed,
    correct: session.correctCount,
    incorrect: session.incorrectCount,
    revealed: session.revealed,
    startedAt: session.startedAt,
    isFinished,
  }
})

function shuffleWords(list: Word[]) {
  const array = [...list]
  for (let index = array.length - 1; index > 0; index -= 1) {
    const randomIndex = Math.floor(Math.random() * (index + 1))
    ;[array[index], array[randomIndex]] = [array[randomIndex], array[index]]
  }
  return array
}
