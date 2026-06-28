#!/bin/bash

root="/home/b11209013/KW_CRI"

# ====================================================================
# SENSITIVITY SWEEP TARGETING VARIABLES
# ====================================================================
# Optional: Add a description when running the script 
# e.g., ./CRI_dispersion_mode.sh "Testing moisture sensitivity" "simplified"
EXPERIMENT_DESC=${1:-"Routine sensitivity sweep"}
MODE=${2:-"full"}

# ====================================================================
# Parameter setup
# ====================================================================

# Original configurations:
# F_LIST="3.0 4.0 5.0"
# f_LIST="0.0 0.25 0.5 0.75 1.0"
# m1_LIST="-1.0 -0.5 0.0 0.5 1.0"
# c1_LIST="0.8 1.0 1.2"
# c2_LIST="0.4 0.5 0.6"
# scaling_factor_LIST="0.0 0.1 0.5 1.0 2.0"
# b1_LIST="0.0 1.0 2.0 3.0 4.0"
# m2_LIST="-2.0 -1.0 0.0 1.0 2.0"
# gamma_q_LIST="0.0 0.25 0.5 0.7 1.0"

# Dense grid configurations (~100 samples) across the same boundaries:
# F_LIST=$(seq -f "%.3f" -s " " 3.0 0.02 5.0)
# f_LIST=$(seq -f "%.3f" -s " " 0.0 0.05 1.0)
m1_LIST=$(seq -f "%.3f" -s " " 0.0 0.1 2.0)
# c1_LIST=$(seq -f "%.3f" -s " " 0.8 0.02 1.2)
# c2_LIST=$(seq -f "%.3f" -s " " 0.4 0.01 0.6)
# scaling_factor_LIST=$(seq -f "%.3f" -s " " 0.0 0.1 2.0)
# b1_LIST=$(seq -f "%.3f" -s " " 0.0 0.2 4.0)
# m2_LIST=$(seq -f "%.3f" -s " " -2.0 0.2 2.0)
# gamma_q_LIST=$(seq -f "%.3f" -s " " 0.0 0.05 1.0)

# ====================================================================
# LOGGING SETUP
# ====================================================================
LOG_FILE="/home/b11209013/KW_CRI/docs/logging.md"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
GIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "Not a git repository")

# Append formatted run metadata to the markdown log
echo -e "\n### Experiment Run: $TIMESTAMP" >> "$LOG_FILE"
echo "- **Description:** $EXPERIMENT_DESC" >> "$LOG_FILE"
echo "- **Git Commit:** \`$GIT_HASH\`" >> "$LOG_FILE"
echo "- **Swept Parameters:**" >> "$LOG_FILE"

# Dynamically log whichever parameters are active
[ -n "$F_LIST" ] && echo "- \`F_LIST\`: $F_LIST" >> "$LOG_FILE"
[ -n "$f_LIST" ] && echo "- \`f_LIST\`: $f_LIST" >> "$LOG_FILE"
[ -n "$m1_LIST" ] && echo "- \`m1_LIST\`: $m1_LIST" >> "$LOG_FILE"
[ -n "$c1_LIST" ] && echo "- \`c1_LIST\`: $c1_LIST" >> "$LOG_FILE"
[ -n "$c2_LIST" ] && echo "- \`c2_LIST\`: $c2_LIST" >> "$LOG_FILE"
[ -n "$scaling_factor_LIST" ] && echo "- \`scaling_factor_LIST\`: $scaling_factor_LIST" >> "$LOG_FILE"
[ -n "$b1_LIST" ] && echo "- \`b1_LIST\`: $b1_LIST" >> "$LOG_FILE"
[ -n "$m2_LIST" ] && echo "- \`m2_LIST\`: $m2_LIST" >> "$LOG_FILE"
[ -n "$gamma_q_LIST" ] && echo "- \`gamma_q_LIST\`: $gamma_q_LIST" >> "$LOG_FILE"

echo "****" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# ====================================================================
# EXECUTE SCRIPT
# ====================================================================
echo "Starting dispersion sensitivity sweep ($EXPERIMENT_DESC) with mode $MODE..."

# Using bash parameter expansion ${VAR:+...} to only include the flag 
# if the variable is defined and not empty. 
python3 $root/Code/CRI_dispersion_mode.py \
    --mode $MODE \
    ${F_LIST:+--F $F_LIST} \
    ${f_LIST:+--f $f_LIST} \
    ${m1_LIST:+--m1 $m1_LIST} \
    ${c1_LIST:+--c1 $c1_LIST} \
    ${c2_LIST:+--c2 $c2_LIST} \
    ${scaling_factor_LIST:+--scaling_factor $scaling_factor_LIST} \
    ${b1_LIST:+--b1 $b1_LIST} \
    ${m2_LIST:+--m2 $m2_LIST} \
    ${gamma_q_LIST:+--gamma_q $gamma_q_LIST}

echo "Generating contours..."

python3 $root/Code/sensitivity_contour_mode.py \
    --mode $MODE \
    ${F_LIST:+--F $F_LIST} \
    ${f_LIST:+--f $f_LIST} \
    ${m1_LIST:+--m1 $m1_LIST} \
    ${c1_LIST:+--c1 $c1_LIST} \
    ${c2_LIST:+--c2 $c2_LIST} \
    ${scaling_factor_LIST:+--scaling_factor $scaling_factor_LIST} \
    ${b1_LIST:+--b1 $b1_LIST} \
    ${m2_LIST:+--m2 $m2_LIST} \
    ${gamma_q_LIST:+--gamma_q $gamma_q_LIST}

echo "Generating heatmaps (5-grid subset)..."

python3 $root/Code/sensitivity_heatmap_mode.py \
    --mode $MODE \
    ${F_LIST:+--F $F_LIST} \
    ${f_LIST:+--f $f_LIST} \
    ${m1_LIST:+--m1 $m1_LIST} \
    ${c1_LIST:+--c1 $c1_LIST} \
    ${c2_LIST:+--c2 $c2_LIST} \
    ${scaling_factor_LIST:+--scaling_factor $scaling_factor_LIST} \
    ${b1_LIST:+--b1 $b1_LIST} \
    ${m2_LIST:+--m2 $m2_LIST} \
    ${gamma_q_LIST:+--gamma_q $gamma_q_LIST}

echo "Sweep and visualization finished successfully. Setup logged to $LOG_FILE."

# ====================================================================
# SYNC WITH GITHUB
# ====================================================================
echo "Automatically committing and pushing changes to GitHub..."

PROJECT_ROOT="/home/b11209013/KW_CRI"
bash -ic "gpush \"$PROJECT_ROOT\""
