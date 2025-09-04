#!/bin/sh
set -eu

if [ "${MODE:-quick}" = "quick" ]; then
  if [ -z "${ORIGIN_URL:-}" ]; then
    echo "ERROR: ORIGIN_URL is required for MODE=quick" >&2
    exit 1
  fi

  # Auto-resolve domain to IP and set Host/SNI
  HOST_PART=$(echo "$ORIGIN_URL" | sed -E 's|^https?://([^:/]+).*|\1|')
  if ! echo "$HOST_PART" | grep -qE '^[0-9.]+$'; then
    IP=$(getent hosts "$HOST_PART" 2>/dev/null | head -1 | awk '{print $1}')
    if [ -n "$IP" ]; then
      echo "Resolved $HOST_PART → $IP"
      ORIGIN_URL=$(echo "$ORIGIN_URL" | sed "s|$HOST_PART|$IP|")
      ORIGIN_HOST="${ORIGIN_HOST:-$HOST_PART}"
      ORIGIN_SNI="${ORIGIN_SNI:-$HOST_PART}"
    fi
  fi

  ARGS="--no-autoupdate --url ${ORIGIN_URL}"

  # add only if provided
  if [ -n "${ORIGIN_HOST:-}" ]; then
    ARGS="$ARGS --http-host-header ${ORIGIN_HOST}"
  fi
  if [ -n "${ORIGIN_SNI:-}" ]; then
    ARGS="$ARGS --origin-server-name ${ORIGIN_SNI}"
  fi

  echo "Starting Quick Tunnel → ${ORIGIN_URL}"
  echo "Configuration: Host=${ORIGIN_HOST:-<default>}, SNI=${ORIGIN_SNI:-<default>}"
  exec cloudflared tunnel $ARGS

else
  # MODE=named
  if [ -z "${TUNNEL_TOKEN:-}" ]; then
    echo "ERROR: TUNNEL_TOKEN is required for MODE=named" >&2
    exit 1
  fi

  echo "Starting Named Tunnel with token"
  exec cloudflared tunnel --no-autoupdate run --token "${TUNNEL_TOKEN}"
fi


