---
id: GBT47655-ADAPTABILITY
title: 계통접속 적응성과 관통운전
type: requirements
status: active
evidence_level: Confirmed
source_ids: [SRC-CN-GBT47655-PDF]
last_verified: 2026-10-24
aliases: [Grid Adaptability]
tags: [grid-adaptability, lvrt, hvrt]
related: [GBT47655-PERFORMANCE, GBT47655-RIDETHROUGH, GBT47655-TEST]
---

# 계통접속 적응성과 관통운전

## 계통강도와 운전환경

- OSCR가 1보다 큰 교류계통과 도서계통에서 안정운전해야 한다.
- 계통연계↔도서운전 전환 시 탈락 없이 연속 운전하고, 전압변동은 10% 이내, 주파수변동은 ±1 Hz 이내, 접속점 전압이 정상값 ±5% 범위로 들어오는 시간은 200 ms 이내여야 한다.
- 45~55 Hz에서 연속운전하고 ±2 Hz/s 이내 주파수 변화율을 견뎌야 한다.
- 내부 기전력과 접속점 전압의 위상차가 0°~±90° 범위일 때 자율적으로 동기를 유지해야 한다.
- 위상점프는 5 ms 이내 자연응답하고 ±60°까지 탈락 없이 연속운전해야 한다.

## 관통운전

저전압 관통은 연속 두 번의 사고를 고려하고, 고전압 관통은 전압수준별 지속시간 요구를 둔다. 대표적인 고전압 구간은 1.10~1.15 p.u. 60 s, 1.15~1.20 p.u. 10 s, 1.20~1.25 p.u. 1 s, 1.25~1.30 p.u. 0.5 s이다. 1.30~1.50 p.u. 0.2 s 요구는 STATCOM에만 적용된다. 저전압 이후 즉시 고전압이 이어지는 조합 시험도 요구한다.

## 근거

- `SRC-CN-GBT47655-PDF`: §4.1.1~§4.1.8, 그림 1~2, 표 1

