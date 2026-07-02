// SessionStart 훅이 호출 — 프로젝트 STATE 파일을 stdout으로 출력해 세션 컨텍스트에 자동 주입한다.
// __dirname 기준으로 경로를 잡으므로 훅 실행 CWD와 무관하게 동작한다.
const fs = require('fs');
const path = require('path');

const stateFile = path.join(__dirname, '..', '작업현황.md');

try {
  process.stdout.write('=== 이전 작업 현황 (자동 로드) ===\n' + fs.readFileSync(stateFile, 'utf8'));
} catch (e) {
  process.stdout.write('작업현황.md 아직 없음 — /handoff 로 먼저 생성하세요');
}
