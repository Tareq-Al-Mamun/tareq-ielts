#!/bin/bash
# Persistent server start script — detaches the Node server from the bash session
# so it survives after the bash tool call ends.
cd /home/z/my-project/server

# Kill any existing server on port 3001
pkill -f "node.*server.js" 2>/dev/null
sleep 1

# Start the server in a fully detached way
# Use setsid to create a new session, redirect all I/O, and run in background
setsid bash -c 'node server.js > /tmp/server.log 2>&1' < /dev/null > /dev/null 2>&1 &

# Save PID for later cleanup
SERVER_PID=$!
echo $SERVER_PID > /tmp/tareq_server.pid

# Wait for it to be ready
for i in 1 2 3 4 5 6 7 8 9 10; do
  sleep 1
  if curl -s --max-time 1 http://localhost:3001/api/health > /tmp/health.json 2>&1; then
    cat /tmp/health.json
    echo ""
    echo "✓ Server is up (PID was $SERVER_PID, but it's in a new session)"
    exit 0
  fi
done

echo "✗ Server did not start within 10s"
echo "--- log ---"
cat /tmp/server.log
exit 1
