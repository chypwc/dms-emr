#!/bin/bash
set -e

# Usage: ./run-dms-task.sh <ExportName>
EXPORT_NAME="$1"

if [ -z "$EXPORT_NAME" ]; then
  echo "Usage: $0 <CloudFormationExportName>"
  exit 1
fi

# Lookup the task ARN from the exported value
TASK_ARN=$(aws cloudformation list-exports \
  --query "Exports[?Name=='$EXPORT_NAME'].Value" \
  --output text)

if [ -z "$TASK_ARN" ]; then
  echo "Error: Could not find export with name $EXPORT_NAME"
  exit 1
fi

echo "Starting DMS Task: $TASK_ARN"

# Check current task status
STATUS=$(aws dms describe-replication-tasks \
  --filters "Name=replication-task-arn,Values=$TASK_ARN" \
  --query "ReplicationTasks[0].Status" \
  --output text)

echo "Current task status: $STATUS"

# Start or resume task based on status
if [ "$STATUS" = "stopped" ]; then
  echo "Resuming task..."
  aws dms start-replication-task \
    --replication-task-arn "$TASK_ARN" \
    --start-replication-task-type resume-processing
elif [ "$STATUS" = "ready" ] || [ "$STATUS" = "failed" ]; then
  echo "Starting task from beginning..."
  aws dms start-replication-task \
    --replication-task-arn "$TASK_ARN" \
    --start-replication-task-type start-replication
else
  echo "Task is in state '$STATUS'; skipping start."
fi