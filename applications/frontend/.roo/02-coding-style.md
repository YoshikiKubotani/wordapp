# Coding Style Guidelines

This document outlines the coding style and quality assurance practices for this project.

## Linting and Formatting

- **Linter**: ESLint
- **Formatter**: Prettier

ESLint and Prettier are configured in `package.json` scripts. After making code changes or additions, ensure no errors are present by running `yarn lint` and `yarn format`.

## Code Quality and Refactoring

### Continuous Refactoring Practice

**IMPORTANT**: After every code change, you MUST actively check for refactoring opportunities:

1. **Remove Dead Code**: Identify and remove any code that has become obsolete due to your changes
   - Unused imports, functions, types, or components
   - Commented-out code that is no longer needed
   - Deprecated implementations replaced by new code

2. **Check Architecture Alignment**: Ensure changes align with the overall system design
   - Verify adherence to the layer structure defined in [`.roo/03-architecture-principles.md`](.roo/03-architecture-principles.md:1)
   - Confirm dependencies flow in the correct direction (top-down only)
   - Check that new code is placed in the appropriate layer

3. **Identify Refactoring Needs**: Look for code that should be refactored based on the changes
   - Similar code patterns that could be abstracted
   - Functions or components that have grown too large
   - Violations of single responsibility principle
   - Opportunities to improve type safety or error handling

4. **Update Related Code**: Consider the broader impact of your changes
   - Update documentation if behavior has changed
   - Refactor tests affected by the changes
   - Update related components or features that might benefit from the improvements

**Example Checklist**:
- [ ] Removed unused imports and dead code
- [ ] Verified layer boundaries are respected
- [ ] Checked for code duplication or abstraction opportunities
- [ ] Ensured naming conventions are consistent
- [ ] Updated related documentation or comments