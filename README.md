# Roblox Game & Web

## 1. 프로젝트 개요
Roblox 기반 게임 개발 및 관련 웹 서비스를 개인 프로젝트로 진행하며,
라이브 서비스 게임 환경에서 유저 행동과 시스템 구조를 이해하기 위한 목적의 프로젝트입니다.

## 2. 주요 프로젝트
### 2-1. Roblox 게임 개발
- 장르: 수집/성장형 게임
- 핵심 루프: 탐험 → 수집 → 업그레이드 → 반복 플레이
- 목적: 유저 진행도, 이탈 지점, 반복 플레이 동기 구조 설계

### 2-2. 웹사이트 개발 (robprofile)
- Roblox 게임/유저 정보를 시각화하고 제공하는 웹 서비스
- Node.js 기반 백엔드 + 프론트엔드 구성
- Roblox API Proxy 서버 구현

## 3. 데이터 분석 관점에서의 설계
게임 및 웹 서비스 설계 시 다음과 같은 데이터 활용을 고려했습니다.
- 유저 접속/플레이 이벤트 추적
- 진행 구간별 이탈 가능 지점 가설
- 유저 세그먼트(신규/헤비/수집형 플레이어) 분류 아이디어
- 향후 코호트/퍼널 분석을 고려한 이벤트 구조 설계

## 4. 기술 스택
- Frontend: HTML, CSS, JavaScript
- Backend: Node.js, Firebase Functions
- Data/Infra: Roblox API, Custom API Proxy
- Tools: GitHub, VS Code
