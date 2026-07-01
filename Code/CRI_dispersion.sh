root="/home/b11209013/KW_CRI"

# ====================================================================
# SENSITIVITY SWEEP TARGETING VARIABLES
EXPERIMENT_DESC=${1:-"Routine sensitivity sweep"}
SCHEME=${2:-"full"}
TARGET=${3:-"all"}
EXTRA_ARGS=${4:-""}

# Parameter setup
VARIABLES=("f" "m1" "scaling_factor" "b1" "m2" "gamma_q")

get_sequence() {
    case $1 in
        f) echo $(seq -f "%.3f" -s " " 0.0 0.05 1.0) ;;
        m1) echo $(seq -f "%.3f" -s " " 0.0 0.1 2.0) ;;
        # c1) echo $(seq -f "%.3f" -s " " 0.8 0.02 1.2) ;;
        # c2) echo $(seq -f "%.3f" -s " " 0.4 0.01 0.6) ;;
        scaling_factor) echo $(seq -f "%.3f" -s " " 0.0 0.1 2.0) ;;
        b1) echo $(seq -f "%.3f" -s " " 0.0 0.2 4.0) ;;
        m2) echo $(seq -f "%.3f" -s " " -2.0 0.2 2.0) ;;
        gamma_q) echo $(seq -f "%.3f" -s " " 0.0 0.05 1.0) ;;
        *) echo "" ;;
    esac
}

# ====================================================================
# LOGGING SETUP
# ====================================================================
LOG_FILE="$root/docs/logging.md"
GIT_HASH=$(git -C "$root" rev-parse --short HEAD 2>/dev/null || echo "Not a git repository")

run_sweep() {
    local VAR_NAME=$1
    local VAR_LIST=$(get_sequence "$VAR_NAME")
    
    if [ -z "$VAR_LIST" ]; then
        echo "Error: Unknown parameter target $VAR_NAME"
        return
    fi

    echo "======================================================================"
    echo "Executing sweep for: $VAR_NAME"
    echo "======================================================================"

    local TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

    # Append formatted run metadata to the markdown log
    echo -e "\n### 🧪 Experiment Run: \`$TIMESTAMP\`" >> "$LOG_FILE"
    echo "| Property | Value |" >> "$LOG_FILE"
    echo "| :--- | :--- |" >> "$LOG_FILE"
    echo "| **Description** | $EXPERIMENT_DESC (Target: $VAR_NAME) |" >> "$LOG_FILE"
    echo "| **Scheme** | \`$SCHEME\` |" >> "$LOG_FILE"
    echo "| **Commit** | \`$GIT_HASH\` |" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
    echo "<details>" >> "$LOG_FILE"
    echo "<summary><b>View Swept Parameters</b></summary>" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
    echo "\`\`\`text" >> "$LOG_FILE"
    echo "${VAR_NAME}_LIST = [${VAR_LIST// /, }]" >> "$LOG_FILE"
    echo "\`\`\`" >> "$LOG_FILE"
    echo "</details>" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
    echo "---" >> "$LOG_FILE"

    echo "Starting dispersion sensitivity sweep ($EXPERIMENT_DESC) with scheme $SCHEME..."

    python3 "$root/Code/CRI_dispersion.py" \
        --scheme "$SCHEME" \
        $EXTRA_ARGS \
        --$VAR_NAME $VAR_LIST

    echo "Generating contours..."
    python3 "$root/Code/sensitivity_contour.py" \
        --scheme "$SCHEME" \
        --$VAR_NAME $VAR_LIST

    echo "Generating heatmaps (5-grid subset)..."
    python3 "$root/Code/sensitivity_heatmap.py" \
        --scheme "$SCHEME" \
        --$VAR_NAME $VAR_LIST
}

# ====================================================================
# EXECUTE SCRIPT
# ====================================================================
if [ "$TARGET" == "all" ]; then
    echo "Running all experiments continuously..."
    for VAR in "${VARIABLES[@]}"; do
        run_sweep "$VAR"
    done
else
    run_sweep "$TARGET"
fi

echo "Sweep and visualization finished successfully. Setup logged to $LOG_FILE."

# ====================================================================
# SYNC WITH GITHUB
# ====================================================================
echo "Automatically committing and pushing changes to GitHub..."

git -C "$root" add .
git -C "$root" commit -m "Update dispersion sensitivity sweep ($EXPERIMENT_DESC)" || true
git -C "$root" push || true
