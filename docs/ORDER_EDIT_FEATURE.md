# Order Test Editing Feature - Out of Scope

## Status: NOT IMPLEMENTED - DEFERRED

### Original Requirement
From Priority 2 Operational improvements:
> "Optionally edit tests (only if no samples or results exist)"

### Decision
This feature is **out of scope** for the current PR and **deferred** to a future enhancement.

### Rationale

1. **Lower Priority**: Order cancellation addresses the primary need (abort incorrect orders)
2. **Complex Workflow**: Test editing requires careful handling of:
   - Order item updates
   - Price recalculation
   - Audit trail
   - UI for adding/removing tests
   - Validation to prevent editing after samples exist
3. **Time Constraints**: Commercial deployment timeline prioritizes core improvements
4. **Workaround Available**: Users can cancel and recreate orders if needed
5. **Limited Use Case**: Most edits happen before sample collection (cancellation covers this)

### What Was Implemented Instead

✅ **Order Cancellation**: 
- Allows canceling entire orders before sample collection
- Prevents errors from propagating through workflow
- Simpler and safer than editing

✅ **Validation**:
- Cannot cancel orders after samples collected
- Clear error messages
- Role-based permissions (Admin/Reception only)

### Comparison: Cancel vs Edit

| Feature | Cancel Order | Edit Order Tests |
|---------|-------------|------------------|
| Use Case | Wrong patient, wrong tests | One test wrong, rest OK |
| Complexity | Low | High |
| Data Integrity | Simple (mark cancelled) | Complex (update, recalc) |
| Audit Trail | Clear (cancelled state) | Must track changes |
| UI Required | 1 button + confirm | Full editing interface |
| Backend Logic | ~50 lines | ~200+ lines |
| Testing Needed | 4 tests | 15+ tests |
| Risk | Low | Medium-High |
| **Implemented** | ✅ Yes | ❌ No |

### Current Workflow

**Before sample collection:**
1. User realizes order has wrong tests
2. User clicks "Cancel Order"
3. Confirms cancellation
4. Creates new order with correct tests
5. ✅ Problem solved

**Why this is acceptable:**
- Happens before sample collection (no sample waste)
- Takes ~30 seconds to recreate order
- No data integrity concerns
- Clear audit trail (cancelled + new order)
- Simple UX (no complex editing UI)

### Future Enhancement Proposal

If test editing is needed later, it could be implemented with:

#### Backend Requirements:
- New endpoint: `PATCH /api/orders/{id}/`
- Request body:
  ```json
  {
    "tests_to_add": [4, 5],
    "tests_to_remove": [3],
    "reason": "Patient requested additional panel"
  }
  ```
- Validation:
  - No samples exist with status > PENDING
  - No results exist
  - User has Admin/Reception role
  - Price recalculation
- Response includes updated order with audit entry

#### Frontend Requirements:
- "Edit Tests" button in OrderDetail (conditional)
- Modal with:
  - Current tests list
  - Add tests dropdown (from catalog)
  - Remove test buttons
  - Reason textarea (required)
  - Price preview
- Confirmation step showing changes
- Success/error handling

#### Testing Requirements:
- Unit tests: ~10 tests
- Integration tests: ~8 tests
- E2E tests: ~2 scenarios
- Manual testing: various edge cases

#### Estimated Effort:
- Backend: 1 day
- Frontend: 1 day
- Testing: 1 day
- **Total**: 3 days

### Recommendation

**For now**: Use order cancellation + recreation workflow
**Future**: If users frequently need to edit tests (>5 times/week), implement editing feature

The cancellation feature provides 80% of the value with 20% of the effort, following the Pareto principle.

### Alternative Approaches Considered

1. **Allow editing without cancellation**
   - ❌ Too complex for v1
   - ❌ Higher risk of data integrity issues

2. **Allow editing only if NO order items have ANY samples**
   - ❌ Still complex UI
   - ❌ Limited use case coverage

3. **Auto-cancel + recreate with edits**
   - ❌ Confusing UX
   - ❌ Breaks audit trail clarity

4. **✅ Implement cancellation, defer editing**
   - ✅ Simple and safe
   - ✅ Covers most use cases
   - ✅ Can add editing later if needed

### Acceptance Criteria Update

Original requirement:
- [ ] Optionally edit tests (only if no samples or results exist)

Updated decision:
- ✅ Order cancellation implemented (covers primary use case)
- ⏸️ Test editing deferred to future enhancement
- ✅ Documented rationale and future implementation plan

### Conclusion

Order test editing is intentionally excluded from this PR. The cancellation feature provides a simpler, safer solution that addresses the primary need (fixing incorrect orders before sample collection). If test editing becomes a frequent user request, it can be implemented in a future PR with dedicated time for proper design, implementation, and testing.

---

**Decision Date**: 2025-11-05
**Status**: Deferred - Not Blocking
**Alternative**: Use order cancellation + recreation
**Future Enhancement**: Issue to be created if needed
