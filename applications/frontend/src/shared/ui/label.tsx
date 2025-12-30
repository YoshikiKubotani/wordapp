import type { LabelHTMLAttributes } from 'react'
import { forwardRef } from 'react'
import { cn } from '@/shared/lib/utils'

type LabelProps = LabelHTMLAttributes<HTMLLabelElement>

export const Label = forwardRef<HTMLLabelElement, LabelProps>(({ className, ...props }, ref) => (
  <label ref={ref} className={cn('text-sm font-medium text-foreground', className)} {...props} />
))

Label.displayName = 'Label'
