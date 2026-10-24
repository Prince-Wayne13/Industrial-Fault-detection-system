#!/usr/bin/env bash
# Makes a plain-text copy of the Word document so changes can be read in git.
# Run this after every edit to the .docx, then commit both files together.
set -euo pipefail
cd "$(dirname "$0")/.."
pandoc srs/SRS_Industrial_Fault_Detection.docx -t gfm --wrap=none -o srs/SRS_Industrial_Fault_Detection.md
echo "Updated srs/SRS_Industrial_Fault_Detection.md"
