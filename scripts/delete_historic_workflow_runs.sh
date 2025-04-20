#!/bin/bash

username="AntonioMrtz"
reponame="SpotifyElectron"

if [[ -z "$username" || -z "$reponame" ]]; then
    echo "Usage: delete_workflow_runs <username> <reponame>"
    return 1
fi

echo "Fetching workflow runs for $username/$reponame..."

# Fetch all workflow runs with pagination
runs=$(gh api --paginate /repos/$username/$reponame/actions/runs | jq -r '.workflow_runs[].id')

if [[ -z "$runs" ]]; then
    echo "No workflow runs found."
    exit 0
fi

for run_id in $runs; do
    echo "Deleting workflow run ID $run_id"
    gh api -X DELETE /repos/$username/$reponame/actions/runs/$run_id
done

echo "All workflow runs deleted."

# Example usage:
# ./delete_workflow_runs.sh
