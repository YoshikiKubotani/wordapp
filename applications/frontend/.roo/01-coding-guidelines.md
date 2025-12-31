# Framework and Styling Guidelines

This document outlines the preferred technologies and practices for development within this project.

## Language and Framework

- **Language**: TypeScript v5.7
- **Framework**: React v19

Please ensure all code adheres to the syntax and best practices compatible with these versions.

## Styling

- **Styling Framework**: Tailwind CSS v4

Utilize Tailwind CSS v4 utility classes for all styling. Refer to the official Tailwind CSS documentation for the most up-to-date utility classes and features.

### Theme Color Guidelines

**IMPORTANT**: Do NOT use direct color specifications (e.g., `bg-blue-500`, `text-red-600`) in your code. Instead, always use the theme utility classes defined in [`src/app/index.css`](src/app/index.css:1).

- Use semantic color tokens like `bg-primary`, `text-foreground`, `border-border`, etc.
- If a new semantic color is needed, define it as a CSS custom property in [`src/app/index.css`](src/app/index.css:1) first, then create a corresponding utility class
- This ensures consistency across light/dark themes and makes theme customization easier

**Example**:
- ❌ Bad: `className="bg-blue-500 text-white"`
- ✅ Good: `className="bg-primary text-primary-foreground"`

## UI Components

- **UI Component Library**: shadcn/ui

For UI components, use `shadcn/ui`. If a required component is not yet installed, please refer to the official documentation for installation and usage: [`https://ui.shadcn.com/docs/components`](https://ui.shadcn.com/docs/components).

The component will be added by `yarn shadcn@latest add <component>`.

### Loading States

**IMPORTANT**: Always use the [`Skeleton`](src/shared/ui/skeleton.tsx:1) component from shadcn/ui for loading states. This ensures consistent loading UX across the application.

- Use `<Skeleton />` for all loading placeholders
- Match the skeleton dimensions to the content being loaded
- Consider using multiple skeleton elements to mimic the structure of the loaded content

**Example**:
```tsx
{isLoading ? (
  <Skeleton className="h-10 w-full" />
) : (
  <div>{data}</div>
)}
```

## State Management and Fetching

- **State Management Library**: Jotai

Use jotai-effect extension for sideeffect management.

- **Fetching**: jotai-tanstack-query extension

## Running the Application

To run the development server, use the command: `yarn dev`.