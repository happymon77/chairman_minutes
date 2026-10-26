---
description: 실시간 로그 1줄 적재 (작업 중, handoff/{오늘}.md)
argument-hint: <한 일 → 결과 · 근거>
allowed-tools: Bash(date*), Read, Edit, Write
disable-model-invocation: true
---

`handoff/{오늘 YYYY-MM-DD}.md`의 **`## 실시간 로그` 섹션 끝에 1줄 append**하라.

파일이 없으면 아래 뼈대로 먼저 생성한 뒤 append한다.

```markdown
# Handoff {오늘 YYYY-MM-DD}
> 그날 작업 상세(시도·결과·실패·기각·수정 사유). 작업현황.md 최상단은 이 파일을 요약한 것.

## 실시간 로그
```

로그 형식:

```markdown
- [HH:MM] {무엇을} → {✅ 성공 | ❌ 실패: 이유 | ⏸ 막힘: 이유 | ⛔ 기각: 이유} · 근거: {발언자·페이지·수치·파일:줄·명령}
```

- 시각(HH:MM)은 `date +%H:%M`으로 얻는다.
- 요약하거나 윤색하지 말고 사실만 적는다.
- 기각하거나 막힌 내용도 반드시 기록한다.
- 회의록 작업은 회장님 발언, 참석자 의견, 편집상 보완을 구분한다.
- 이 handoff 파일만 수정하고 다른 산출물은 건드리지 않는다.

기록할 내용: $ARGUMENTS
