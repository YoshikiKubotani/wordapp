import { useEffect } from 'react'
import { useAtomValue, useSetAtom } from 'jotai'
import type { Word } from '@/entities/word'
import {
  activeCardAtom,
  gradeCardAtom,
  practiceProgressAtom,
  resetSessionAtom,
  revealCardAtom,
  startSessionAtom,
} from '@/features/flashcard-practice'
import { Badge } from '@/shared/ui/badge'
import { Button } from '@/shared/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/ui/card'

type FlashcardPanelProps = {
  words: Word[]
}

export function FlashcardPanel({ words }: FlashcardPanelProps) {
  const startSession = useSetAtom(startSessionAtom)
  const revealCard = useSetAtom(revealCardAtom)
  const gradeCard = useSetAtom(gradeCardAtom)
  const resetSession = useSetAtom(resetSessionAtom)
  const activeCard = useAtomValue(activeCardAtom)
  const progress = useAtomValue(practiceProgressAtom)

  useEffect(() => {
    if (words.length > 0 && progress.total === 0) {
      startSession(words)
    }
  }, [progress.total, startSession, words])

  const hasWords = words.length > 0

  const renderEmpty = () => (
    <div className="flex flex-col items-start gap-3 rounded-xl border border-dashed border-border bg-muted/40 p-6">
      <p className="text-base font-semibold text-foreground">No cards yet</p>
      <p className="text-sm text-muted-foreground">
        Add a few words on the left. We will shuffle them into a practice round automatically.
      </p>
    </div>
  )

  const renderFinished = () => (
    <div className="flex flex-col gap-4 rounded-xl border border-border bg-accent/30 p-6">
      <p className="text-base font-semibold text-foreground">Round complete</p>
      <div className="flex flex-wrap gap-2">
        <Badge variant="solid">Correct {progress.correct}</Badge>
        <Badge variant="outline">Review again {progress.incorrect}</Badge>
      </div>
      <div className="flex flex-wrap gap-2">
        <Button onClick={() => startSession(words)}>Shuffle a new round</Button>
        <Button variant="ghost" onClick={() => resetSession()}>
          Reset session
        </Button>
      </div>
    </div>
  )

  const renderActiveCard = () => {
    if (!activeCard) return renderEmpty()

    return (
      <div className="flex flex-col gap-4">
        <div className="rounded-xl border border-border bg-gradient-to-br from-card via-card to-accent/30 p-6 shadow-lg">
          <div className="flex items-center justify-between gap-2">
            <p className="text-xs font-semibold uppercase text-muted-foreground">Prompt</p>
            <Badge variant="outline">
              Card {Math.min(progress.completed + 1, progress.total)} / {progress.total}
            </Badge>
          </div>
          <p className="mt-2 text-3xl font-bold tracking-tight text-foreground">
            {activeCard.term}
          </p>
          {activeCard.note ? (
            <p className="mt-1 text-sm text-muted-foreground">Hint: {activeCard.note}</p>
          ) : null}
          {progress.revealed ? (
            <div className="mt-6 space-y-1 rounded-lg border border-border/70 bg-card/70 p-4">
              <p className="text-xs font-semibold uppercase text-muted-foreground">Meaning</p>
              <p className="text-lg font-semibold text-foreground">{activeCard.meaning}</p>
            </div>
          ) : (
            <p className="mt-6 text-sm text-muted-foreground">
              Think of the meaning, then reveal to self-check.
            </p>
          )}
        </div>
        <div className="flex flex-wrap gap-2">
          {!progress.revealed ? (
            <>
              <Button onClick={() => revealCard()}>Reveal meaning</Button>
              <Button variant="ghost" onClick={() => startSession(words)}>
                Reshuffle
              </Button>
            </>
          ) : (
            <>
              <Button variant="secondary" onClick={() => gradeCard('incorrect')}>
                Need to review
              </Button>
              <Button onClick={() => gradeCard('correct')}>I remembered it</Button>
            </>
          )}
        </div>
      </div>
    )
  }

  return (
    <Card className="h-full backdrop-blur">
      <CardHeader className="flex flex-row items-start justify-between gap-4">
        <div className="space-y-1">
          <CardTitle>Flashcards</CardTitle>
          <CardDescription>Shuffle the deck, reveal answers, and track your round.</CardDescription>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <Badge variant="solid">Round size {progress.total}</Badge>
          <Badge variant="outline">Correct {progress.correct}</Badge>
          <Badge variant="outline">Missed {progress.incorrect}</Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {!hasWords ? renderEmpty() : progress.isFinished ? renderFinished() : renderActiveCard()}
      </CardContent>
    </Card>
  )
}
