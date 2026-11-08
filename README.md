# Sangjun Pyo

<img src="pond/pond.svg" width="100%" alt="Koi pond drawn from my GitHub activity: one koi per top language, lily pads for months, my contribution year on the pond floor" />

데이터·금융·AI 문제를 직접 구조화하고, **실제로 돌아가는 서비스**로 만듭니다.
분석에서 끝내지 않고 배포·검증·기록까지 남기는 방식으로 일합니다.

---

## Featured Projects

<table>
<tr>
<td width="50%" valign="top">

### 🚗 EarlySignal
자동차 소비자 신고를 **LLM으로 증상 분류**하고, 차종별 **포아송 경보**와 원문 근거를 묶어 안전 담당자의 조사 요청서 작성을 돕는 도구.

NHTSA 신고 **93만 건** 적재 · **7,502건** LLM 분류 · 자동 검사 250개

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white) ![Cloudflare](https://img.shields.io/badge/Cloudflare-F38020?style=flat-square&logo=cloudflare&logoColor=white)

[Demo](https://earlysignal.pages.dev/) · [Repo](https://github.com/SangJun-Pyo/EarlySignal)

</td>
<td width="50%" valign="top">

### 🍷 비싼 와인은 진짜 맛있을까?
와인 리뷰 **약 11만 건**으로 가격·산지·품종이 평점을 얼마나 설명하는지 분석하고, 예산 안에서 모델로 고르는 게 "제일 비싼 것 고르기"보다 나은지 검증한 ML 팀 프로젝트.

XGBoost R² **0.50** · 90점 이상 분류 AUC **0.857** · $30 예산 시뮬레이션에서 90점+ 적중 **41% → 65%**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white) ![XGBoost](https://img.shields.io/badge/XGBoost-189FDD?style=flat-square) ![SHAP](https://img.shields.io/badge/SHAP-FF0D57?style=flat-square)

[Repo](https://github.com/SangJun-Pyo/SKKU_ML_Project) · [Colab](https://colab.research.google.com/github/SangJun-Pyo/SKKU_ML_Project/blob/main/notebooks/wine_stats_colab.ipynb)

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🧭 MyAiScore
공개 GitHub 저장소 URL 하나로 문서·검증·기록·자동화 신호를 읽어 **AI 개발 체계 점수**(100점)와 협업 유형을 보여주는 웹 서비스.

LLM 호출·코드 실행 없이 **결정론적 분석** · 근거 파일 경로 공개

![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white) ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white) ![Railway](https://img.shields.io/badge/Railway-0B0D0E?style=flat-square&logo=railway&logoColor=white)

[Demo](https://myaiscore-production.up.railway.app/) · [Repo](https://github.com/SangJun-Pyo/MyAiScore)

</td>
<td width="50%" valign="top">

### 🃏 PocketMeta
포켓몬 TCG Pocket의 **메타·티어 통계**를 보여주는 사이트. 기획부터 배포·운영까지 혼자 맡고 있는 라이브 서비스.

![Cloudflare Workers](https://img.shields.io/badge/Cloudflare_Workers-F38020?style=flat-square&logo=cloudflareworkers&logoColor=white) ![Status](https://img.shields.io/badge/status-live-2ea44f?style=flat-square)

[Site](https://pocketmeta.app)

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 📈 Markov-Trade
기대값·리스크·시나리오·복기 구조로 매매 판단을 재설계한 트레이딩 분석 시스템. **Claude Tool Use 차트 에이전트**, Monte Carlo 시뮬레이션, 매매 일지 분석 포함.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white) ![Claude](https://img.shields.io/badge/Claude_API-D97757?style=flat-square&logo=anthropic&logoColor=white)

[Repo](https://github.com/SangJun-Pyo/Markov-Trade)

</td>
<td width="50%" valign="top">

### 💎 TRUVE
XRPL 기반 가상자산 기부 인프라. **Xaman 결제 → Evidence Package → XLS-70 Donation Credential** 발급·검증까지 연결하고, 기부금은 재단으로 직접 이동.

![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white) ![XRPL](https://img.shields.io/badge/XRPL-23292F?style=flat-square&logo=xrp&logoColor=white) ![Prisma](https://img.shields.io/badge/Prisma-2D3748?style=flat-square&logo=prisma&logoColor=white)

[Demo](https://truve.pages.dev/) · [Repo](https://github.com/SangJun-Pyo/Truve_prototype)

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 📊 KOSIS_V2
KOSIS API 공공통계 수집 배치를 **Streamlit 운영 콘솔**로 리뉴얼. 지역·항목 선택 실행, 실패 작업 재실행, 실시간 로그·KPI, 결과 xlsx 관리.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white) ![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white)

[Repo](https://github.com/SangJun-Pyo/KOSIS_V2)

</td>
<td width="50%" valign="top">

### 🗂 More
- **VeriYeon** — DID/VC 기반 선택적 공개 신원 확인 매칭 프로토타입 · [Repo](https://github.com/SangJun-Pyo/VeriYeon)
- **FANFI** — 음악 감상·팬 활동·토큰·NFT를 연결한 Web3 팬 이코노미 실험 · [Demo](https://fanfi-v1.pages.dev/)
- **Robprofile** — Roblox API 기반 유저·게임 정보 시각화 웹 서비스 · [Web](https://Robprofile.com/)

</td>
</tr>
</table>

<details>
<summary><b>EarlySignal 더 보기</b></summary>

- NHTSA 원본 신고 1,301,663행에서 필터·중복 제거 후 **932,821건** 적재
- 데모 범위 **7,502건**을 LLM으로 증상·상황 분류하고 출력·출처 검사 완료
- 직전 12개월 평균 대비 **Poisson 상측 확률 p<0.001** 규칙으로 차종-월 경보
- 경보 선택 → 원문 인용·제외 → 조사 요청서 저장을 한 흐름으로 연결, 판단은 사람이 내림
- 조사 사례 백테스트와 미래 데이터 차단 검증, 한계와 미검증 항목을 README에 그대로 공개
</details>

<details>
<summary><b>와인 프로젝트 더 보기</b></summary>

- 가격만으로는 평점의 R² 0.38 (가격 2배 ≈ +2점), 산지·품종·빈티지 추가 시 Ridge 0.45 → XGBoost 0.50, 평균 오차 1.71점
- 나라별 "가성비" 차이의 상당 부분이 **나라마다 다른 평론가** 때문임을 확인 (오스트리아 +1.8점 → 같은 평론가끼리 비교 시 +0.2점)
- OLS·로지스틱 검정, GVIF, SHAP, 과적합 점검까지 포함하고 시드 고정으로 모든 숫자를 재현 가능하게 구성
</details>

<details>
<summary><b>Markov-Trade 더 보기</b></summary>

- 기대값, 손익비, R-Multiple 기반 판단 구조와 Win Rate·Profit Factor·Max Drawdown·Equity Curve 분석
- Z-score, RSI, Bollinger Band 기반 다중 타임프레임 차트 분석
- Claude Tool Use 에이전트가 가격 조회·리스크 계산·매매 기록 도구를 호출해 진입·손절·목표가를 계획
- 매매 일지를 전략·종목·패턴별로 정량화하는 복기 시스템
</details>

<details>
<summary><b>TRUVE 더 보기</b></summary>

- 재단·캠페인 탐색 → Xaman 결제 → Evidence Package 생성 → Donation Credential 발급·승인 → 기부현황 확인
- 거래 해시, 기부 시점, 원화 환산 참고값, 캠페인 정보를 하나의 증빙 묶음으로 정리
- 재단 운영 흐름을 반영한 관리자 페이지와 외부 검증 페이지
</details>


---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black) ![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB) ![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white) ![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white) ![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white)
![Cloudflare](https://img.shields.io/badge/Cloudflare-F38020?style=flat-square&logo=cloudflare&logoColor=white) ![Railway](https://img.shields.io/badge/Railway-0B0D0E?style=flat-square&logo=railway&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white) ![XRPL](https://img.shields.io/badge/XRPL-23292F?style=flat-square&logo=xrp&logoColor=white) ![Claude API](https://img.shields.io/badge/Claude_API-D97757?style=flat-square&logo=anthropic&logoColor=white)

---

## Contribution Arcade

<img src="arcade/arcade.svg" width="100%" alt="Pac-Man eating my contribution graph" />

<sub>잉어 연못과 아케이드는 이 레포의 <a href="scripts">파이썬 스크립트</a>가 GitHub Actions로 매일 새로 그립니다.</sub>
