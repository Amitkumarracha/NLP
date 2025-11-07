"""
NLP Rubrics Evaluation Package

Comprehensive evaluation suite for NLP project rubrics:
- Data preprocessing experiments and comparisons
- Model evaluation with complete metrics
- Literature baseline comparisons

Usage:
    from nlp_rubrics import run_all_evaluations
    run_all_evaluations()

Or run directly:
    python -m nlp_rubrics.run_all_rubrics
"""

__version__ = '1.0.0'
__author__ = 'Beyond Words Team'

from pathlib import Path

# Package paths
PACKAGE_DIR = Path(__file__).parent
RESULTS_DIR = PACKAGE_DIR / 'results'

# Ensure results directory exists
RESULTS_DIR.mkdir(exist_ok=True)

def run_all_evaluations():
    """Execute all NLP rubric evaluations"""
    from .run_all_rubrics import main
    main()

__all__ = ['run_all_evaluations', 'RESULTS_DIR']
