import { useEffect, useState } from 'react'
import type { Word } from '@/entities/word'
import { Badge } from '@/shared/ui/badge'
import { Button } from '@/shared/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/ui/card'

type FlashcardPanelProps = {
  words: Word[]
}

export function FlashcardPanel({ words }: FlashcardPanelProps) {
  const [queue, setQueue] = useState<Word[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [revealed, setRevealed] = useState(false)
  const [correct, setCorrect] = useState(0)
  const [incorrect, setIncorrect] = useState(0)

  useEffect(() => {
    if (!words.length) {
      setQueue([])
      setCurrentIndex(0)
      setRevealed(false)
      setCorrect(0)
      setIncorrect(0)
      return
    }
    setQueue(shuffleWords(words))
    setCurrentIndex(0)
    setRevealed(false)
    setCorrect(0)
    setIncorrect(0)
  }, [words])

  const total = queue.length
  const completed = Math.min(currentIndex, total)
  const isFinished = total > 0 && completed >= total
  const displayIndex = total === 0 ? 0 : isFinished ? total : currentIndex + 1
  const activeCard = !isFinished ? queue[currentIndex] : null

  const hasWords = words.length > 0

  const handleCardReveal = () => {
    if (!revealed && activeCard) {
      setRevealed(true)
    }
  }

  const handleGrade = (grade: 'correct' | 'incorrect') => {
    if (!activeCard || !revealed) return
    if (grade === 'correct') {
      setCorrect((value) => value + 1)
    } else {
      setIncorrect((value) => value + 1)
    }
    setCurrentIndex((value) => value + 1)
    setRevealed(false)
  }

  const handleRetry = () => {
    if (!words.length) return
    setQueue(shuffleWords(words))
    setCurrentIndex(0)
    setRevealed(false)
    setCorrect(0)
    setIncorrect(0)
  }

  const renderEmpty = () => (
    <div className="flex flex-col items-start gap-3 rounded-xl border border-dashed border-border bg-muted/40 p-6">
      <p className="text-sm text-secondary-foreground">
        まだ単語が追加されていないよ！まずは学習したい単語を追加しよう
      </p>
    </div>
  )

  const renderFinished = () => (
    <div className="flex flex-col gap-4 rounded-xl border border-border bg-accent/30 p-6">
      <p className="text-base font-semibold text-foreground">🎉ラウンド完了</p>
      <div className="space-y-1 text-sm text-foreground">
        <p>正解: {correct} 件</p>
        <p>不正解: {incorrect} 件</p>
      </div>
      <div className="flex flex-wrap gap-2">
        <Button onClick={handleRetry}>もう一度学習する</Button>
      </div>
    </div>
  )

  const renderActiveCard = () => {
    if (!activeCard) return renderEmpty()

    return (
      <div className="flex flex-col gap-4">
        <div
          role={!revealed ? 'button' : undefined}
          tabIndex={!revealed ? 0 : -1}
          onClick={handleCardReveal}
          onKeyDown={(event) => {
            if ((event.key === 'Enter' || event.key === ' ') && !revealed) {
              event.preventDefault()
              handleCardReveal()
            }
          }}
          className="rounded-xl border border-border bg-gradient-to-br from-card via-card to-accent/30 p-6 shadow-lg outline-none transition hover:translate-y-0 hover:shadow-xl focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
          style={!revealed ? { cursor: 'pointer' } : undefined}
        >
          <div className="flex items-center justify-between gap-2">
            <p className="text-xs font-semibold uppercase text-secondary-foreground">単語</p>
            <Badge variant="outline">
              カード {displayIndex} / {total}
            </Badge>
          </div>
          <p className="mt-2 text-3xl font-bold tracking-tight text-foreground">
            {activeCard.term}
          </p>
          {activeCard.note ? (
            <p className="mt-1 text-sm text-secondary-foreground">ヒント: {activeCard.note}</p>
          ) : null}
          {revealed ? (
            <div className="mt-6 space-y-1 rounded-lg border border-border/70 bg-card/70 p-4">
              <p className="text-xs font-semibold uppercase text-secondary-foreground">意味</p>
              <p className="text-lg font-semibold text-foreground">{activeCard.meaning}</p>
            </div>
          ) : (
            <p className="mt-6 text-sm text-secondary-foreground">クリックして答えを表示</p>
          )}
        </div>
        {revealed ? (
          <div className="flex flex-wrap gap-2">
            <Button variant="secondary" onClick={() => handleGrade('incorrect')}>
              間違い
            </Button>
            <Button onClick={() => handleGrade('correct')}>正解</Button>
          </div>
        ) : null}
      </div>
    )
  }

  return (
    <Card className="h-full backdrop-blur">
      <CardHeader className="flex flex-row items-start justify-between gap-4">
        <div className="space-y-1">
          <CardTitle>学習</CardTitle>
          <CardDescription>追加された単語をシャッフルして1周学習しよう</CardDescription>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {!hasWords ? renderEmpty() : isFinished ? renderFinished() : renderActiveCard()}
      </CardContent>
    </Card>
  )
}

function shuffleWords(list: Word[]) {
  const array = [...list]
  for (let index = array.length - 1; index > 0; index -= 1) {
    const randomIndex = Math.floor(Math.random() * (index + 1))
    ;[array[index], array[randomIndex]] = [array[randomIndex], array[index]]
  }
  return array
}
