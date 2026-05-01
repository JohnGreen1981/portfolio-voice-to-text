# Cleanup Plan

- [x] Copy tracked source files from `VoiceToText`.
- [x] Replace personal owner ID with placeholder.
- [x] Exclude `.env`, `user_state.db`, `server.rtf`, caches and local agent files.
- [x] Run syntax check with `python -m py_compile`.
- [x] Run secret scan before first GitHub push.
