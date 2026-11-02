#!/bin/sh
set -eu
echo 'Hello, 05Shaibaan! Your independent Jenkins lab is running.'
printf 'Job: %s | Run: #%s\n' "$JOB_NAME" "$BUILD_NUMBER"
printf 'Build URL: %s\nWorkspace: %s\n' "$BUILD_URL" "$WORKSPACE"
printf 'Ubuntu user: '; whoami
date --iso-8601=seconds
