---
name: ingest-lecture
description: 강의 녹음·강의안을 소화해서 주차별 강의 노트(notes.md)와 예습 교재와의 delta(delta.md)를 생성한다. 학기 중 복습 단계의 핵심 스킬.
---

# ingest-lecture

인자: `<course-slug> <주차 번호>` (예: `system-programming 3`)

전제: 사용자가 `_private/<학기>/<course-slug>/week-NN/` 에 녹음 파일(m4a/mp3 등)과 강의안(pdf/pptx)을 넣어둔 상태.

## 절차

1. `_private/<학기>/<course-slug>/week-NN/` 의 파일 목록을 확인한다. 없으면 사용자에게 위치를 물어본다.
2. **전사(transcription)** — 녹음 파일이 있고 `transcript.txt` 가 아직 없으면:
   ```bash
   # 최초 1회 설치
   brew install whisper-cpp
   # 모델 다운로드 (최초 1회, large-v3-turbo 권장)
   # https://huggingface.co/ggerganov/whisper.cpp 의 ggml-large-v3-turbo.bin → _private/models/
   ffmpeg -i <녹음파일> -ar 16000 -ac 1 -c:a pcm_s16le /tmp/lecture.wav
   whisper-cli -m _private/models/ggml-large-v3-turbo.bin -l auto -f /tmp/lecture.wav \
     --output-txt --output-file _private/<학기>/<course-slug>/week-NN/transcript
   ```
   강의가 영어 진행이므로 `-l en` 이 기본, 한국어 혼용이면 `-l auto`.
3. 전사본 + 강의안을 읽고 `semester/week-NN/` 에 생성:
   - `notes.md` — 구조화 강의 노트. 강의 흐름 순서가 아니라 개념 구조 순서로 재조직. 교수의 예시·판서 포인트·질답 포함. 언어 규칙은 루트 CLAUDE.md 를 따른다.
   - `delta.md` — 예습 챕터(`weeks/NN-*/README.md`)와 대조해서 세 가지만 추린다:
     1. **Emphasized** — 교수가 강조했는데 예습 교재에서 비중이 작았던 것 (시험 신호 ★)
     2. **New** — 교재에 없던 내용 (교수 자체 자료·최신 내용)
     3. **Corrected** — 교재 서술과 다르거나 더 정확한 서술
4. delta 의 Emphasized/New 항목은 해당 주차 `quiz.md` 에 문항으로 추가한다 (섹션 `## From lecture` 아래).
5. **원본(녹음·전사본·강의안)은 절대 커밋하지 않는다** — `_private/` 확인 후 `semester/` 생성물만 커밋: `<course-slug>: digest week NN lecture`.
