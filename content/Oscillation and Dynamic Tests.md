---
id: GBT47655-OSCILLATION
title: 진동감쇠와 동특성 시험
type: test-method
status: active
evidence_level: Confirmed
source_ids: [SRC-CN-GBT47655-PDF]
last_verified: 2026-10-24
aliases: [Oscillation and Dynamic Tests]
tags: [oscillation, impedance-scan, dynamic-test]
related: [GBT47655-INERTIA, GBT47655-TEST]
---

# 진동감쇠와 동특성 시험

## 저주파 진동감쇠

1차 주파수조정·AGC 등 보조주파수 기능을 해제하고, 0.01~0.05 Hz 진폭과 0.2~2.5 Hz 주파수의 정현파 주파수 교란을 30 s 적용한다. 계산된 출력에너지 `Ed<0`이고 진동발산이 없어야 하며 §4.5 요구를 만족해야 한다.

## 광대역 진동감쇠

접속점에 1~200 Hz는 1 Hz 간격, 200~2500 Hz는 10 Hz 간격의 전압교란을 주입해 임피던스 크기·위상 곡선을 산출한다. 계통과 장비의 임피던스 크기 곡선 교점에서 위상차가 170°~180°이면 해당 주파수의 진동위험으로 판단하고 시험을 통과하지 못한다.

## 전력 계단응답

- 1000 km 미만 직류송전과 ESS 유효전력 상승시간: 90 ms 이내
- 1000 km 이상 직류송전 유효전력 상승시간: 150 ms 이내
- 유효전력 정정시간: 500 ms 이내
- 무효전력 상승시간: 90 ms 이내, 정정시간 500 ms 이내
- 접속점 유·무효전력 제어오차: 정격전력의 ±2% 이내

고장 제거 후 유·무효전력은 3.0 p.u./s 이상의 속도로 고장 전 수준까지 회복해야 하며 실제 복구율은 계통분석으로 정한다.

## 근거

- `SRC-CN-GBT47655-PDF`: §4.4~§4.6, §5.9~§5.10, §5.13

