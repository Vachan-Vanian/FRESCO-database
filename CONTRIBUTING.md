# FRESCO Contribution Guidelines

## Overview
Thank you for your interest in contributing to the FRESCO database! These guidelines will help you maintain consistency and quality when adding new entries or making improvements to our open-source database.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/FRESCO-database.git`
3. Create a new branch: `git checkout -b feature/name-your-contribution`
4. Make your changes
5. Test your changes
6. Push and submit a Pull Request

## Branch Naming

Format: `<type>/<issue-number>-brief-description`

**Types:** `feature`, `bugfix`, `docs`, `refactor`, `test`, `chore`

**Examples:**
```
feature/123-add-new-specimen-data
bugfix/456-fix-unit-conversion-issue
docs/789-update-database-schema
```

## Commit Messages

Format: `<type>(<scope>): <subject>`

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples:**
```
feat(database): add new specimen entry for FRP strengthening
fix(validation): correct infill geometry validation logic
docs(readme): update contribution guidelines
test(database): add unit tests for reinforcement parsing
```

Keep it short and use imperative mood ("add" not "added").

## Database Entry Guidelines

### Required Fields
The FRESCO database organizes data into 13 logical sections:

| Section | Purpose | Key Fields |
|---------|---------|------------|
| 1. Reference | Basic identification | specimen_id, year, authors, source |
| 2. Frame Geometry | RC frame dimensions | frm_h, frm_l, col_h, bm_h, etc. |
| 3. Infill Geometry | Masonry infill details | inf_type, inf_ul, inf_uh, openings |
| 4. Reinforcement Details | Steel reinforcement | Longitudinal & transverse rebars |
| 5. Concrete Properties | Concrete materials | fc, Ec, density |
| 6. Steel Properties | Steel materials | fy, fu, Ey |
| 7. Infill Mechanical Properties | Masonry materials | Brick and mortar properties |
| 8. Loading (In-Plane) | In-plane loading | Protocol, loads |
| 9. Loading (Out-of-Plane) | Out-of-plane loading | Protocol, loads |
| 10. Response (Global) | System-level response | Stiffness, peak load, failure mode |
| 11. Response (Local) | Component response | Crack patterns, damage |
| 12. Retrofit Techniques | Strengthening methods | Intervention description |
| 13. General Comments | Additional notes | User comments |

### Data Format Standards
- Use consistent units throughout (prefer metric system)
- Follow the existing template structure exactly
- All values should be numerical or strings with proper formatting
- When using measurements, specify units explicitly in brackets: `[value, "unit"]`
- For reinforcement specifications, follow established notation conventions

### Demo Example Structure
```python
{
    "specimen_id": "EXAMPLE_SPECIMEN",
    "specimen_scale": 1.0
    "source": "https://doi.org/xxxxx",
    "title": "Title of the Reference Source",
    "authors": "Author1, Author2, ...",
    "year": 2025,
    
    # Frame Geometry Group
    "frm_h": [1500, "mm"],
    "frm_l": [2100, "mm"],
    "col_h": [200, "mm"],
    "col_d": [140, "mm"],
    # ... other frame geometry fields ...
    
    # Infill Geometry Group
    "inf_type": "one_wythe",
    "inf_opn_type": "none",
    # ... other infill geometry fields ...
    
    # Reinforcement Details Group
    "col_long_reinf_corner": ["4#10", "mm"],
    # ... other reinforcement fields ...
}
```

## Code Style for Database Scripts

### Python Guidelines
- Follow [PEP 8](https://pep8.org/)
- Max line length: 88 characters
- Use type hints for functions
- Add docstrings for all functions and classes

### Naming Conventions
- Classes: `PascalCase`
- Functions: `snake_case` 
- Constants: `UPPER_CASE`
- Private methods: `_leading_underscore`

### Example Function
```python
from typing import Dict, List

def validate_database_entry(entry_data: Dict[str, any]) -> bool:
    """Validate that a database entry contains all required fields and values.
    
    Args:
        entry_data: Dictionary containing the complete specimen data
        
    Returns:
        True if validation passes, False otherwise
        
    Raises:
        ValueError: When critical validation fails
    """
    # Implementation here
    pass
```

## Testing

- Add tests for new database structures or validation logic
- Ensure all existing test cases still pass after changes
- Test both CSV and JSON export functionality

**Example test structure:**
```python
def test_new_specimen_entry():
    """Test that a new specimen entry can be properly added to the database."""
    # Arrange - create test data following FRESCO conventions
    test_entry = {
        "specimen_id": "TEST_001",
        # ... other required fields ...
    }
    
    # Act - add to database
    db.add_entry(entry_id=1, entry_data=test_entry)
    
    # Assert - verify the entry was stored correctly
    retrieved = db.data[1]
    assert retrieved["specimen_id"] == "TEST_001"
```

## Pull Requests

### Title
`<type>: Brief description`

Example: `feat(database): Add support for new FRP strengthening methods`

### Description Template
```markdown
## Summary
What this PR does and why.

## Changes
- Added new specimen entries for FRP strengthened systems
- Updated database schema to include additional material properties
- Enhanced validation logic for infill configurations

## Testing
How you tested: unit tests, manual verification of data entry structure, etc.

## Related Issues
Closes #123
```

### Checklist
- [ ] Database entries follow required field structure exactly
- [ ] All existing database functionality preserved
- [ ] New data formats consistent with existing conventions  
- [ ] Code follows style guidelines
- [ ] Tests added and passing
- [ ] Documentation updated (if applicable)
- [ ] No linting errors

## Reporting Issues

### Bug Reports
Include:
- FRESCO version
- Python version and OS
- Steps to reproduce the issue
- Expected vs actual behavior
- Error messages or screenshots

### Feature Requests
Describe:
- The problem you're solving with this contribution
- Your proposed solution approach
- How it benefits existing database users
- Any relevant examples or mockups

## Review Process

1. Submit PR
2. Wait for review by database maintainers
3. Address feedback and make requested changes
4. Get approval and merge

---

## Questions?

- Check [documentation](docs/)
- Search [issues](https://github.com/Vachan-Vanian/FRESCO-database/issues)

Thanks for contributing! 🎉

*Last updated: October, 2025*