---
id: GBT47655-INERTIA
title: 관성응답과 동적 전압응답
type: requirements
status: active
evidence_level: Confirmed
source_ids: [SRC-CN-GBT47655-PDF]
last_verified: 2026-10-24
aliases: [Inertia and Voltage Response]
tags: [inertia, voltage-response]
related: [GBT47655-DEFINITIONS, GBT47655-PERFORMANCE, GBT47655-OSCILLATION]
---

# 관성응답과 동적 전압응답

## 관성응답

- 주파수 변화율에 **5 ms 이내** 자연응답하여 관성응답 전력을 방출하거나 흡수한다.
- 가상동기제어 또는 고속전력제어 등을 사용할 수 있다.
- 관성시간상수 `Tj`는 **0.1~16 s** 범위에서 발주자 요구로 정한다.
- 공급자는 관성응답 에너지 구성과 등가 동기조상기 기준을 제시한다.

시험 §5.3은 50 Hz에서 55 Hz 또는 45 Hz로 1 Hz/s와 2 Hz/s의 램프를 각각 적용한다. 계산식은 `ΔPj = Tj × (df/dt) × Pn / fn`이며 해당 구간을 적분해 관성응답 에너지를 구한다.

## 동적 전압응답

- 접속점 전압크기 변화에 **5 ms 이내** 자연응답하여 전류를 방출하거나 흡수한다.
- 내부 기전력의 크기는 전압제어 루프로 조절한다.
- 공급자는 전압변화 응답전류 특성을 제시해야 한다.

시험 §5.11은 접속점 전압을 0.9, 0.6, 0.3, 0 p.u.로 각각 낮추고 1 s 유지한 뒤 복구하여 응답을 확인한다.

## 근거

- `SRC-CN-GBT47655-PDF`: §4.2~§4.3, §5.3, §5.11, 부속서 A~B

