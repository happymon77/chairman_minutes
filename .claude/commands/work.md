---
description: 현재 진행현황 파악 — CLAUDE.md·작업현황.md·git 상태를 읽고 무엇이 됐고/남았는지 요약 (착수 전 맥락 복원)
argument-hint: [특정 영역(선택): VESTA / DS파워 / 영업 / 요약본 …]
allowed-tools: Read, Grep, Glob, Bash(git status:*), Bash(git branch:*), Bash(git log:*), Bash(git rev-parse:*), Bash(grep:*)
disable-model-invocation: true
---

프로젝트의 **현재 진행현황을 파악해 보고**하라. (작업 착수 전 맥락 복원용 — 파일 수정 금지, 읽기·요약 전용)

## 읽을 것
1. `CLAUDE.md` — 프로젝트 개요·폴더구조·작업규칙. 이미 컨텍스트에 로드돼 있으면 재읽기 불필요.
2. 프로젝트 루트 `작업현황.md` — 상단 4섹션(현재상태 / 결과물 / 과정·결정 / 다음단계) + **맨 아래 진행 로그 최신 1~2개**. SessionStart 훅으로 이미 로드됐으면 중복 읽지 말고 그대로 활용.
3. 필요 시 최신 날짜 핸드오프 스냅샷(권위본)만 확인.

## git 실제 상태 (작업현황.md와 대조)
- 현재 브랜치: !`git branch --show-current 2>/dev/null`
- HEAD·동기화: !`git status -sb 2>/dev/null | head -1`
- 최근 커밋: !`git log --oneline -6 2>/dev/null`
- 미커밋/미추적: !`git status --short 2>/dev/null`
- 사용자 지정 영역(선택): $ARGUMENTS

## 보고 형식 (간결하게, 불릿 위주)
1. **현재 상태 한 줄** — 무엇이 완료/라이브인지 + 마지막 작업 요지
2. **최근 완료** — 마지막 세션(들)에서 확정·제출한 것 (핵심 커밋 해시 포함)
3. **확인/회신 대기** — 사용자 액션·회신이 필요한 항목
4. **남은 큰 과제** — 미착수 블로커·다음 단계 (작업현황.md §4 기준, ★ 우선)
5. **워킹트리 주의** — 미커밋/미추적/동기화 이슈

## 규칙
- **작업현황.md와 git 실제 상태가 어긋나면 반드시 지적**한다 (예: HEAD가 핸드오프 기록보다 앞섬 = 다른 세션이 선행 커밋, 미커밋 잔존, origin과 ahead/behind).
- `$ARGUMENTS`로 특정 영역(VESTA/DS파워/영업/요약본 등)이 지정되면 **그 부분만 깊게**, 없으면 전체 요약.
- 파일을 수정하지 말 것. 마지막에 **"다음 무엇부터 진행할지" 한 줄로 물어라.**
