# Reuse before you create

Before writing a new component, function, hook, class, util or style, check the codebase already has one. Duplicates
drift apart, break the design system and double the bug surface.

## 1. Search first

Search by what the thing **does**, not only by the name you'd give it (a dropdown may be `Select`, `Combobox`,
`Picker` or `Menu`). Look in the usual places:

- **UI components:** `components/`, `components/ui/`, `ui/`, `shared/`, `common/`, a `packages/ui` or design-system
  package in a monorepo, and installed kits (shadcn/ui, MUI, Chakra, Radix, Mantine, NativeWind ...) in `package.json`.
- **Functions and hooks:** `lib/`, `utils/`, `helpers/`, `hooks/`, `services/`, `api/`, and the module next to the
  file you're editing.
- **Classes and types:** existing services, repositories, clients, base classes, schemas (zod, Prisma, DTOs) and
  shared types.
- Use Grep/Glob (or the LSP) for likely names and for the behaviour (`onSelect`, `formatCurrency`, `fetch(`), and look
  at how sibling screens solved the same thing.

## 2. Use what exists, in this order

1. **Use it as is.**
2. **Use it with its props, variants or slots** (`<Select size="sm" />`, `variant="ghost"`).
3. **Extend it** with a small, backward-compatible prop or variant, or compose/wrap it. Don't fork or copy-paste it.
4. **Create a new one** only when none of the above fits. Say in one line why the existing one didn't.

## 3. Respect the design system

If the repo has one (a `DESIGN.md`, a theme file, Tailwind config, CSS variables, tokens, a Storybook, a `ui` package):

- Build new UI from its components and tokens: colours, spacing, radius, type scale, shadows, motion.
- No hard-coded hex values, one-off font sizes or magic spacing when a token exists.
- No second library for something the system already covers (no new date picker, icon set or modal lib alongside the
  existing one).
- A new component goes where its siblings live and follows their file, naming, props and styling conventions.

## 4. Report it

In the end-of-task summary, name what you reused (`used <Select> from components/ui/select.tsx`) and anything new you
had to create, with the reason.
