import { type FormEvent, useState } from 'react'
import { useAtomValue } from 'jotai'
import { registerWordMutationAtom, type WordDraft } from '@/features/word-book'
import { Button } from '@/shared/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/ui/card'
import { Input } from '@/shared/ui/input'
import { Label } from '@/shared/ui/label'
import { Textarea } from '@/shared/ui/textarea'

type FormState = WordDraft

export function WordForm() {
  const registerWord = useAtomValue(registerWordMutationAtom)
  const [form, setForm] = useState<FormState>({
    term: '',
    meaning: '',
    note: '',
  })
  const [feedback, setFeedback] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const updateField = (field: keyof FormState) => (value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }))
    setFeedback(null)
    setError(null)
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setFeedback(null)
    setError(null)
    if (!form.term.trim() || !form.meaning.trim()) {
      setError('単語と意味の両方を記入して追加してね')
      return
    }

    try {
      await registerWord.mutateAsync(form)
      setForm({ term: '', meaning: '', note: '' })
      setFeedback('保存しました。この調子でどんどん追加しちゃおう！')
    } catch (submitError) {
      setError(
        submitError instanceof Error ? submitError.message : '保存に失敗しました。もう一度試してね',
      )
    }
  }

  return (
    <Card className="h-full backdrop-blur">
      <CardHeader>
        <CardTitle>単語を追加する</CardTitle>
        <CardDescription>
          表面に覚えたい単語を、裏面にその意味を記入して「追加」ボタンを押そう！
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form className="space-y-4" onSubmit={handleSubmit}>
          <div className="space-y-2">
            <Label htmlFor="term">単語/表面</Label>
            <Input
              id="term"
              placeholder="apple"
              value={form.term}
              onChange={(event) => updateField('term')(event.target.value)}
              autoComplete="off"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="meaning">意味/裏面</Label>
            <Input
              id="meaning"
              placeholder="りんご"
              value={form.meaning}
              onChange={(event) => updateField('meaning')(event.target.value)}
              autoComplete="off"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="note">ヒント（任意）</Label>
            <Textarea
              id="note"
              placeholder="例：赤くて美味しい手のひらサイズの果物"
              value={form.note}
              onChange={(event) => updateField('note')(event.target.value)}
            />
          </div>
          {error ? <p className="text-sm font-medium text-destructive">{error}</p> : null}
          {feedback ? <p className="text-sm text-foreground">{feedback}</p> : null}
          <div className="flex items-center gap-2">
            <Button type="submit" className="flex-1" disabled={registerWord.isPending}>
              {registerWord.isPending ? '送信中...' : '追加'}
            </Button>
            <Button
              type="button"
              variant="ghost"
              onClick={() => setForm({ term: '', meaning: '', note: '' })}
            >
              クリア
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}
