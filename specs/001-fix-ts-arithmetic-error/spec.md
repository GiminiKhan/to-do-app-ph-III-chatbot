# Fix TypeScript Arithmetic Operation Error in Dashboard Sorting Logic

## Feature Description
Resolve the TypeScript 'arithmetic operation' error in frontend/src/app/dashboard/page.tsx by adding .getTime() to the sorting logic. The error occurs when attempting to perform arithmetic operations on Date objects without converting them to timestamps first. This is a simple bug fix to ensure proper compilation and deployment to Vercel.

## User Scenarios & Testing
### Primary Scenario
- User navigates to the dashboard page
- Tasks are displayed and sorted according to selected sorting criteria
- Sorting functionality works without errors
- Page compiles successfully for deployment

### Testing
- Verify tasks sort correctly by "Newest" (chronological order by creation date)
- Verify tasks sort correctly by "Priority" with secondary sort by date
- Confirm no TypeScript compilation errors occur
- Validate that sorting works correctly after the fix

## Functional Requirements
### FR1: Date Sorting Functionality
- The system SHALL properly sort tasks by creation date when "Newest" is selected
- The system SHALL convert Date objects to numeric timestamps before arithmetic operations
- The system SHALL maintain correct chronological ordering of tasks

### FR2: Priority Sorting with Date Fallback
- The system SHALL sort tasks by priority level when "Priority" is selected
- The system SHALL use date as a secondary sort criterion when priorities are equal
- The system SHALL properly convert Date objects to numeric timestamps for comparison

### FR3: Error Prevention
- The system SHALL eliminate TypeScript compilation errors related to arithmetic operations on Date objects
- The system SHALL properly compile for deployment to Vercel
- The system SHALL maintain all existing functionality after the fix

## Success Criteria
- Tasks are sorted correctly by date and priority without runtime errors
- TypeScript compilation succeeds without arithmetic operation errors
- Deployment to Vercel completes successfully
- All existing dashboard functionality remains intact
- Sorting performance is maintained (no degradation in speed)

## Key Entities
- Task objects with date fields (created_at, updated_at)
- Date objects used in sorting algorithms
- Sorting parameters (Newest, Priority)

## Constraints and Assumptions
### Constraints
- No changes to any other logic, data, or files beyond the specific sorting code
- Maintain all existing functionality and behavior
- Fix must be minimal and targeted to the specific issue

### Assumptions
- Date fields (created_at, updated_at) exist on task objects in ISO string format
- The current sorting algorithm logic is correct and only needs the .getTime() addition
- Task objects follow the expected data structure from the backend API
- Project is otherwise functional and only needs this specific fix for deployment