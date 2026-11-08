# Sangjun Pyo

<img src="koi/koi.gif" width="256" alt="My koi" />

데이터·금융·AI 문제를 직접 구조화하고, 실제로 돌아가는 서비스로 만듭니다.

---

## Projects

| Project | Area | Description | Links |
| --- | --- | --- | --- |
| **PocketMeta** | Data / Web Service | 포켓몬 TCG Pocket 메타·티어 통계 사이트 (운영 중) | [Site](https://pocketmeta.app) |
| **EarlySignal** | AI / Safety Analytics | NHTSA 소비자 신고를 LLM으로 분류하고, 통계 경보와 원문 근거로 조사 준비를 돕는 도구 | [GitHub](https://github.com/SangJun-Pyo/EarlySignal) |
| **Markov-Trade** | Financial Data / Trading Analytics | 기대값·리스크·시나리오·복기 구조를 통합한 트레이딩 분석 시스템 | [GitHub](https://github.com/SangJun-Pyo/Markov-Trade) |
| **KOSIS_V2** | Public Data / Automation | KOSIS API 기반 통계 데이터 수집·실행·결과 관리 Streamlit 콘솔 | [GitHub](https://github.com/SangJun-Pyo/KOSIS_V2) |
| **TRUVE** | Web3 / Crypto Donation | XRPL 기반 가상자산 기부 및 증빙 인프라 프로토타입 | [GitHub](https://github.com/SangJun-Pyo/Truve_prototype) · [Demo](https://truve.pages.dev/) |
| **MyAiScore** | AI / Web | AI 활용 역량을 점수로 평가하는 웹 서비스 | [GitHub](https://github.com/SangJun-Pyo/MyAiScore) |
| **VeriYeon** | Digital ID / Web3 | DID/VC 기반 선택적 공개 신원 인증 매칭 컨셉 | [GitHub](https://github.com/SangJun-Pyo/VeriYeon) |

<details>
<summary><b>Markov-Trade 상세</b></summary>

금융 의사결정의 일관성을 높이기 위한 데이터 기반 트레이딩 분석 시스템입니다. 트레이딩 판단을 감정이나 직관이 아니라 기대값·리스크·시나리오·사후 복기 구조로 재설계하는 것을 목표로 했습니다.

- 기대값, 손익비, R-Multiple 기반 트레이딩 판단 구조 설계
- Win Rate, Profit Factor, Expectancy, Avg R:R, Max Drawdown, Equity Curve 분석
- Z-score, RSI, Bollinger Band 등 기술 지표 기반 차트 분석
- 진입 전 리스크, 최악 시나리오, 파산 확률, 신뢰도 지표 확인
- 5분 / 1시간 / 일봉 기준 다중 타임프레임 분석
- 자본·손절폭 기반 트레이드 플래너 시뮬레이션
- 매매 일지를 전략별·종목별·패턴별로 정량화하는 복기 시스템

**Stack:** Python, JavaScript
</details>

<details>
<summary><b>KOSIS_V2 상세</b></summary>

기존 `runner.py` 기반 배치 프로젝트를 지역/항목 선택, 실행 상태 확인, 결과 파일 관리가 가능한 Streamlit 대시보드로 리뉴얼했습니다.

- KOSIS API 기반 공공 통계 데이터 수집 자동화
- 작업 상태, KPI, 로그, 결과 파일을 한 화면에서 확인
- 실패 작업 재실행 및 실행 중지
- `.xlsx` 결과 파일 탐색 및 다운로드
- `jobs/**/*.json` 작업 정의 + `output/**/*.xlsx` 결과 관리 구조

**Stack:** Python, Streamlit, pandas, requests, openpyxl
</details>

<details>
<summary><b>TRUVE 상세</b></summary>

기부자가 XRP/XRPL 기반 자산으로 기부를 실행하고, 재단은 기부 내역을 Evidence Package와 Donation Credential로 관리하는 구조를 실험한 프로토타입입니다.

- Xaman Wallet 연동을 통한 지갑 연결 및 기부 실행
- 거래 해시, 기부 시점, 원화 환산 참고값, 캠페인 정보를 담은 Evidence Package
- XLS-70 Donation Credential 기반 기부 증빙 구조 실험
- 재단·캠페인 탐색, 기부 실행, 내 기부 현황, 검증 페이지, 관리자 페이지

**Stack:** Vite, TypeScript, Express, Prisma, XRPL, Xaman Wallet, Cloudflare Pages
</details>

<details>
<summary><b>Previous Experiments</b></summary>

- **FANFI** — 음악 감상·팬 활동·토큰·NFT를 연결한 Web3 팬 이코노미 플랫폼 실험 (MetaMask, ERC-20/721/1155) · [Demo](https://fanfi-v1.pages.dev/)
- **Robprofile** — Roblox API 기반 유저·게임 정보 시각화 웹 서비스 (Node.js, Firebase Functions) · [Web](https://Robprofile.com/)
</details>

---

## Tech Stack

- **Data:** Python · pandas · Streamlit
- **Web:** TypeScript · JavaScript · Vite · Node.js · Express · Firebase Functions · Prisma
- **Web3:** XRPL · Xaman Wallet · MetaMask · ERC-20/721/1155
- **Infra & Tools:** Cloudflare Pages/Workers · Wrangler · GitHub Actions · AI-assisted development

---

## Contribution Arcade

<img src="arcade/arcade.svg" width="100%" alt="Pac-Man eating my contribution graph" />
