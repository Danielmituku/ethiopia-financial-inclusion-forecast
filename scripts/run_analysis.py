#!/usr/bin/env python3
"""
Run All Analysis and Generate Final Report

This script runs all notebooks to generate figures and then creates the final PDF report.
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def run_notebook(notebook_path: str, timeout: int = 600):
    """Execute a Jupyter notebook."""
    print(f"\n📓 Running {notebook_path}...")
    
    cmd = [
        sys.executable, '-m', 'nbconvert',
        '--to', 'notebook',
        '--execute',
        '--inplace',
        '--ExecutePreprocessor.timeout=' + str(timeout),
        str(notebook_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode == 0:
            print(f"   ✓ {notebook_path} completed successfully")
            return True
        else:
            print(f"   ⚠️ {notebook_path} failed:")
            print(f"   {result.stderr[:500]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"   ⚠️ {notebook_path} timed out after {timeout}s")
        return False
    except FileNotFoundError:
        print(f"   ⚠️ nbconvert not found. Install with: pip install nbconvert")
        return False


def generate_report():
    """Generate the final PDF report."""
    print("\n📄 Generating final report...")
    
    report_script = PROJECT_ROOT / 'src' / 'generate_report.py'
    
    result = subprocess.run([sys.executable, str(report_script)], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(result.stdout)
        return True
    else:
        print(f"⚠️ Report generation failed: {result.stderr}")
        return False


def main():
    """Main execution function."""
    print("=" * 60)
    print("Ethiopia Financial Inclusion Analysis Pipeline")
    print("=" * 60)
    
    notebooks_dir = PROJECT_ROOT / 'notebooks'
    
    notebooks = [
        '01_data_exploration.ipynb',
        '02_eda.ipynb',
        '03_impact_modeling.ipynb',
        '04_forecasting.ipynb',
    ]
    
    results = {}
    for nb in notebooks:
        nb_path = notebooks_dir / nb
        if nb_path.exists():
            results[nb] = run_notebook(nb_path)
        else:
            print(f"⚠️ Notebook not found: {nb_path}")
            results[nb] = False
    
    report_success = generate_report()
    
    print("\n" + "=" * 60)
    print("Execution Summary")
    print("=" * 60)
    
    for nb, success in results.items():
        status = "✓" if success else "✗"
        print(f"  {status} {nb}")
    
    print(f"  {'✓' if report_success else '✗'} Final Report Generation")
    
    if all(results.values()) and report_success:
        print("\n✅ All tasks completed successfully!")
        print(f"\n📊 Reports available at:")
        print(f"   HTML: {PROJECT_ROOT / 'reports' / 'final_report.html'}")
        print(f"   PDF:  {PROJECT_ROOT / 'reports' / 'final_report.pdf'}")
    else:
        print("\n⚠️ Some tasks failed. Check output above for details.")
    
    return all(results.values()) and report_success


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
