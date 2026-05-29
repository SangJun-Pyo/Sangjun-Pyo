# Sangjun Pyo

데이터 분석, FinTech, Web3, 공공데이터, 팬 플랫폼 관련 개인 프로젝트를 정리한 공간입니다.  
서비스 아이디어를 직접 구조화하고, 웹 프로토타입과 데이터 기반 의사결정 시스템으로 구현해보는 것에 관심이 있습니다.

---

## Projects

| Project | Area | Description | Links |
| --- | --- | --- | --- |
| **Markov-Trade** | Financial Data / Trading Analytics | 기대값, 리스크, 시나리오, 복기 구조를 통합한 트레이딩 분석 시스템 | [GitHub](https://github.com/SangJun-Pyo/Markov-Trade) 
| **TRUVE** | Web3 / Crypto Donation | XRPL 기반 가상자산 기부 및 증빙 인프라 | [GitHub](https://github.com/SangJun-Pyo/Truve_prototype) · [Demo](https://truve.pages.dev/) |
| **KOSIS_V2** | Public Data / Automation | KOSIS API 기반 통계 데이터 수집·실행·결과 관리 콘솔 | [GitHub](https://github.com/SangJun-Pyo/KOSIS_V2) |
| **FANFI** | Web3 / Fan Economy | 팬 참여, 토큰, NFT, 음악 후원을 연결한 Web3 팬 플랫폼 실험 | [Demo](https://fanfi-v1.pages.dev/) |
| **Roblox Game & Web** | Previous Experiment | Roblox 게임 구조와 Roblox API 기반 웹 서비스 실험 | Archived Experiment |

---

## Markov-Trade

Markov-Trade는 금융 의사결정의 일관성을 높이기 위한 데이터 기반 트레이딩 분석 시스템입니다.  
트레이딩 판단을 감정이나 직관이 아니라, 기대값·리스크·시나리오·사후 복기 구조로 재설계하는 것을 목표로 했습니다.

### Key Features

- 기대값, 손익비, R-Multiple 기반 트레이딩 판단 구조 설계
- Win Rate, Profit Factor, Expectancy, Avg R:R, Max Drawdown, Equity Curve 분석
- Z-score, RSI, Bollinger Band 등 기술 지표 기반 차트 분석
- 진입 전 리스크, 최악 시나리오, 파산 확률, 신뢰도 지표 확인
- 5분 / 1시간 / 일봉 기준의 다중 타임프레임 분석 구조
- 트레이드 플래너를 통한 자본·손절폭 기반 시뮬레이션
- 매매 일지를 전략별·종목별·패턴별로 정량화하는 복기 시스템
- AI 어시스턴트를 활용한 진입 근거 해석 및 전략 개선 가이드 설계

**Keywords:** Financial Data Analysis, Trading Analytics, Risk Management, Expectancy, R-Multiple, Python, JavaScript, AI-assisted Workflow

---

## TRUVE

TRUVE는 XRPL 기반 가상자산 기부 인프라 프로토타입입니다.  
기부자가 XRP/XRPL 기반 자산으로 기부를 실행하고, 재단은 기부 내역을 Evidence Package와 Donation Credential로 관리할 수 있는 구조를 실험했습니다.

[GitHub](https://github.com/SangJun-Pyo/Truve_prototype) · [Live Demo](https://truve.pages.dev/)

### Project Focus

- XRP / XRPL 기반 가상자산 기부 플로우 설계
- Xaman Wallet 연동을 통한 Web3 지갑 연결 및 기부 실행
- 기부자 → 재단 직접 송금 구조 설계
- Evidence Package를 통한 거래 해시, 기부 시점, 원화 환산 참고값, 캠페인 정보 정리
- XLS-70 Donation Credential 기반 기부 증빙 구조 실험
- 굿네이버스와의 협업/활용 논의를 바탕으로 한 재단 운영 흐름 반영
- 재단·캠페인 탐색, 기부 실행, 내 기부 현황, 검증 페이지, 관리자 페이지 구조 설계
- 향후 재단 SaaS, 세무·감사 검증 콘솔, ESG/CSR 리포트로 확장 가능한 B2B 인프라 구상

### Implemented Pages

- Landing / Service Introduction
- Foundation & Campaign Information
- Donation Flow
- My Donation Status Dashboard
- Evidence & Credential Verification
- Community
- Admin Page

**Tech Stack:** Vite, TypeScript, HTML, CSS, Express, Prisma, XRPL, Xaman Wallet, Cloudflare Pages, Wrangler  
**Keywords:** XRPL, XRP, Xaman Wallet, Web3 Donation, Crypto Donation, Evidence Package, XLS-70 Credential, Good Neighbors, B2B Donation Infrastructure

---

## KOSIS_V2

KOSIS_V2는 KOSIS API 기반 통계 데이터 수집 작업을 관리하기 위한 Streamlit 운영 콘솔입니다.  
기존 `runner.py` 기반 배치 프로젝트를 지역/항목 선택, 실행 상태 확인, 결과 파일 관리가 가능한 대시보드 형태로 리뉴얼했습니다.

[GitHub](https://github.com/SangJun-Pyo/KOSIS_V2)

### Project Focus

- KOSIS API 기반 공공 통계 데이터 수집 자동화
- Streamlit 기반 운영 콘솔 구현
- 지역별 데이터 작업 분류 및 실행 관리
- 작업 상태, KPI, 로그, 결과 파일을 한 화면에서 확인
- 실패 작업 재실행 및 실행 중지 기능
- 생성된 `.xlsx` 결과 파일 탐색 및 다운로드
- `jobs/**/*.json` 기반 작업 정의와 `output/**/*.xlsx` 기반 결과 관리 구조

### Main Structure

- `app.py`: Streamlit 앱 진입점
- `runner.py`: 기존 데이터 수집 실행 로직
- `jobs/`: KOSIS 수집 작업 JSON 정의
- `services/job_runner_service.py`: 실행, 중지, 로그, 결과 파일 관리
- `services/job_catalog_service.py`: 작업 메타데이터 파싱 및 지역 분류
- `state/dashboard_state.py`: 실행 상태 및 세션 상태 관리
- `ui/dashboard_views.py`: 지역 선택, 작업 선택, 실시간 패널, 결과 테이블 렌더링

**Tech Stack:** Python, Streamlit, pandas, requests, openpyxl  
**Keywords:** KOSIS, Public Data, Data Collection, Streamlit Dashboard, Regional Statistics, Automation

---

## FANFI

FANFI는 팬과 아티스트를 연결하는 Web3 팬 이코노미 플랫폼 실험입니다.  
음악 감상, 팬 활동, 디지털 후원, 토큰 발행, NFT 성장을 연결해 팬 참여 기반의 새로운 보상 구조를 구상했습니다.

[Live Demo](https://fanfi-v1.pages.dev/)

> Repository is private.

### Project Focus

- MetaMask 지갑 연동을 통한 Web3 사용자 연결
- FANFI Token 발행 실험
- ERC-20 기반 팬 토큰 발행 실험
- ERC-721 기반 아티스트/NFT 발행 실험
- ERC-1155 기반 멀티 토큰 및 리워드 구조 실험
- Listen Point와 Song Coin을 활용한 팬 참여 보상 구조 설계
- 음악 재생 → 포인트 적립 → NFT 성장 → 팬 등급 상승 흐름 구상
- 팬 리더보드, 아티스트 페이지, 곡 탐색, 팬 대시보드 구조 설계

### Concept

FANFI는 팬이 단순히 음악을 소비하는 것을 넘어,  
음악 감상과 팬 활동을 통해 포인트와 토큰을 얻고, 아티스트 NFT를 성장시키는 구조를 실험한 프로젝트입니다.

**Tech Stack:** JavaScript, Web3, MetaMask, ERC-20, ERC-721, ERC-1155, NFT, Token Issuance  
**Keywords:** Fan Economy, Music Platform, MetaMask, FANFI Token, NFT, Listen Point, Song Coin, Web3 Rewards

---

## Roblox Game & Web

Roblox 기반 게임 개발과 관련 웹 서비스를 실험했던 프로젝트입니다.  
현재는 진행하지 않지만, 라이브 서비스 게임 구조와 Roblox API 기반 웹 서비스 설계를 이해하기 위해 진행했습니다.

### Roblox Game Development

- 수집 / 성장형 게임 구조 실험
- 탐험 → 수집 → 업그레이드 → 반복 플레이 루프 설계
- 유저 진행도, 아이템 구조, 보상 시스템 설계

### Robprofile

Roblox 유저 및 게임 정보를 시각화해서 보여주는 웹 서비스입니다.

- Roblox 유저/게임 정보 조회
- Roblox API 활용
- Node.js 기반 백엔드와 프론트엔드 구성
- API Proxy 서버 구현 실험

**Keywords:** Roblox, Roblox API, Node.js, Firebase Functions, Game System Design

---

## Tech Stack

### Data & Analytics

- Python
- pandas
- Streamlit
- Public Data Analysis
- Financial Data Analysis
- Trading Metrics
- Data Visualization

### Web Development

- HTML
- CSS
- JavaScript
- TypeScript
- Vite
- Node.js
- Express
- Firebase Functions

### Web3 & Blockchain

- XRPL / XRP
- Xaman Wallet
- MetaMask
- ERC-20
- ERC-721
- ERC-1155
- NFT Issuance
- Token Issuance
- Web3 Wallet Integration

### Tools

- GitHub
- VS Code
- Cloudflare Pages
- Cloudflare Workers
- Wrangler
- Prisma
- AI-assisted development workflow

---

## Interests

- Data Analytics
- FinTech
- Web3 Infrastructure
- Crypto Donation Platforms
- Fan Economy
- Public Data
- Financial Decision Systems
- API-based Services
