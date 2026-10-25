/**
 * useThinkingSound.ts
 *
 * Thinking sound hook — completely silenced to prevent unnecessary buzzing / beeping
 * during AI reasoning and voice turns.
 */
import { useCallback } from 'react';

export type ThinkingSoundStyle = 'ping' | 'typing' | 'breath';

interface UseThinkingSoundOptions {
  volume?: number;
  pingIntervalMs?: number;
}

export function useThinkingSound(
  _style: ThinkingSoundStyle = 'ping',
  _options: UseThinkingSoundOptions = {},
) {
  const startThinking = useCallback(() => {
    // Sound generation disabled to eliminate unnecessary buzzing / beeping
  }, []);

  const stopThinking = useCallback(() => {
    // No-op
  }, []);

  return { startThinking, stopThinking };
}
