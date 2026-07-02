# Chairman Minutes — 프로젝트 개요

84세 회장님(김영대)의 클로바노트 음성인식 txt 파일을 정식 회의록(DOCX/PDF)으로 변환하는 프로젝트.
회장님 발음이 불명확하여 클로바노트 오인식이 많음. 변환은 Claude Code가 직접 수행 (외부 API 없음).

---

## 폴더 구조

```
D:\claude_project\Chairman_minutes\
├── recording/          # 클로바노트 원본 txt (35개)
├── minutes/            # 정리된 회의록 DOCX/PDF + _extracted.txt 캐시
├── spelling_correction/ # 맞춤법/표현 수정표 (별도 작업)
├── convert.py          # 유틸리티 (extract/pairs 명령)
└── patterns.md         # 교정 패턴 사전 ← 변환 시 반드시 참조
```

---

## convert.py 사용법

```bash
python convert.py extract   # minutes/ 의 DOCX/DOC/PDF → _extracted.txt 캐시 생성
python convert.py pairs     # recording ↔ minutes 매칭 현황 출력 (✔/✘)
```

- `.docx` → `python-docx`
- `.doc`  → `win32com.client` (Word COM 자동화)
- `.pdf`  → `pdfplumber`
- 같은 날짜 txt 여러 개 → `[N개 합산]`으로 표시

---

## 현재 쌍 현황 (2026-06-17 기준)

- recording: 35개 txt
- minutes: 33쌍 매칭 완료 (모두 ✔)
- `_extracted.txt` 캐시: 전체 생성 완료

---

## 새 txt 변환 워크플로우

1. `patterns.md` 읽기
2. 변환할 txt와 같은 회의 유형의 기존 _extracted.txt 1~2개 읽기 (few-shot 예시)
3. 아래 규칙 적용하여 회의록 작성:
   - 클로바노트 메타정보·타임스탬프 전부 제거
   - 오인식 교정 (patterns.md 섹션 1~3)
   - 구어체 → 문어체 변환 (섹션 6)
   - 회의 유형에 맞는 헤더·2컬럼 형식 적용 (섹션 5)
   - 회장님 지시사항 → `▶` 기호, 오른쪽 컬럼

---

## 회의 유형별 담당 파일 패턴

| 유형 | recording 파일 패턴 | minutes 파일 패턴 |
|---|---|---|
| VESTA (미국 온수기) | `VESTA*`, `*VESTA*` | `VESTA 회의 (YYYYMMDD)*` |
| 에너지기기 생산/원통형 | `*에너지기기*`, `*원통형*` | `에너기기기_쎌틱_원통형*`, `에너지기기-쎌틱 생산*` |
| 영업 회의 | `*영업*` | `쎌틱 영업 회장님 보고*` |
| 공장 회의 | `*공장*` | `에너지기기-쎌틱 생산*` |

---

## 핵심 참고 정보

- **회장님**: 김영대 (클로바노트 화자 레이블로 표시됨, 회의록에는 "담당 회장"으로만 기재)
- **회의록 작성자**: 김정민 부사장 (산업본사)
- **주요 계열사**: 대성쎌틱, 대성히트에너시스, 산업본사, VESTA (미국법인)
- **patterns.md**: 오인식 교정 패턴 사전. 변환 전 반드시 전체 읽을 것.
- **spelling_correction/**: 별도 맞춤법 수정 작업 결과물 (변환과 무관)

---

## 세션 연속성 (handoff)

- **자동 로드**: 세션 시작 시 `작업현황.md`가 SessionStart 훅으로 자동 로드된다(`.claude/settings.json` + `.claude/load-state.js`).
- **세션 종료**: `/handoff` 명령으로 `작업현황.md`를 갱신한다(상단 4섹션 덮어쓰기 + 진행 로그 append).
