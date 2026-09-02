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
3. 전사본 + 강의안(있으면 슬라이드, 없으면 판서·캡처 사진)을 **끝까지 전부** 읽고
   `semester/week-NN/` 에 생성:
   - `notes.md` — 구조화 강의 노트. 강의 흐름 순서가 아니라 개념 구조 순서로 재조직하되,
     **원본 내용을 최대한 보존한다 — 요약문이 아니다.** 교수의 예시·수치·판서 내용·질답
     상호작용(질문→답변→교정)·잡담성 일화까지 실제로 나온 건 다 담는다. "핵심만 추려서"
     압축하지 말 것 — 나중에 이 노트만 보고 시험공부를 할 사람 입장에서, 강의에 있었는데
     노트에 없는 내용이 있으면 그게 실패다. 전사본을 죽 훑다가 "이 부분은 요약해도 되겠다"
     싶은 유혹이 들어도, 실제 예시·풀이 과정·교수가 던진 질문과 학생 반응은 생략하지 않는다.
     분량이 길어지는 건 괜찮다 — 짧게 쓰는 것보다 빠짐없이 쓰는 게 우선이다.
   - **추측 금지**: 강의에서 실제로 다루지 않은 내용을 예상하거나 대신 채워 넣지 않는다
     (예: "다음 시간에 다룰 것으로 보이는 정답은 아마 이럴 것이다" 같은 서술 금지). 교수가
     질문을 미완으로 남기거나 다음 시간으로 미뤘으면, 그 사실만 적는다 — 답을 대신
     추론해서 적지 않는다. 확실하지 않은 내용(오디오가 불분명하거나 STT가 깨진 부분)은
     추측해서 채우지 말고 "이 부분 불명확"이라고 표시한다.
   - 언어 규칙은 루트 CLAUDE.md 를 따르되(본문 한국어, 용어/코드/수식 영어 원어),
     **영어판도 같이 만든다**: 같은 디렉토리에 `notes.en.md` — 구조·절·문단 순서는
     `notes.md`와 1:1 대응, 본문을 영어로 쓴다(번역이 아니라 같은 사실관계를 영어로
     새로 서술하는 느낌으로). 위의 "원본 보존·추측 금지" 원칙은 두 언어판 모두 동일하게
     적용된다 — 한쪽에만 있는 내용이 없어야 한다.
   - `delta.md` — 예습 챕터(`weeks/NN-*/README.md`)와 대조해서 세 가지만 추린다:
     1. **Emphasized** — 교수가 강조했는데 예습 교재에서 비중이 작았던 것 (시험 신호 ★)
     2. **New** — 교재에 없던 내용 (교수 자체 자료·최신 내용)
     3. **Corrected** — 교재 서술과 다르거나 더 정확한 서술
4. delta 의 Emphasized/New 항목은 해당 주차 `quiz.md` 에 문항으로 추가한다 (섹션 `## From lecture` 아래).
5. **원본(녹음·전사본·강의안)은 절대 커밋하지 않는다** — `_private/` 확인 후 `semester/` 생성물만 커밋: `<course-slug>: digest week NN lecture`.
