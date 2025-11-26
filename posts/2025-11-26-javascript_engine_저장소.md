---
title: "javascript_engine_저장소"
date: "2025-11-26"
category: "Computer Science"
tags: [CS, JavaScript, V8, Memory]
description: "Deep dive into CS fundamentals of JS Memory Model."
---

# 🏛️ `javascript_engine_저장소` (Call Stack & Memory Heap)

## 📌 Abstract (핵심 요약)

> 자바스크립트 엔진(V8 등)은 프로그램 실행을 위해 **RAM(메모리)**을 할당받아 사용하며, 이를 효율적으로 관리하기 위해 **Call Stack(작업 공간)**과 **Memory Heap(저장 공간)**으로 영역을 나누어 관리한다.
>
> 핵심은 **"함수의 코드(Definition)"는 Heap에 단 한 번 저장되어 참조(Reference)될 뿐 복사되지 않지만, 함수 실행 시 내부에서 생성되는 "객체/변수(Data)"는 렌더링마다 Heap에 새로 할당(Allocation)된다**는 점이다.

## 🔍 Deep Dive (상세 분석)

### 1. Mechanism (동작 원리: 냉동과 해동)

1.  **Definition (정의/냉동):**
    - JS 파일을 다운로드하고 파싱하면, 엔진은 함수와 컴포넌트의 **코드 본문(Function Body)**을 **Memory Heap**에 저장한다.
    - 이 시점에서 코드는 실행되지 않으며, 단순한 텍스트 데이터(객체)로 존재한다.
2.  **Call (호출/해동):**
    - 함수가 호출되면 **Call Stack**에 **실행 컨텍스트(Execution Context)**가 생성된다.
    - 이 컨텍스트는 Heap에 있는 함수 코드를 **복사해오는 것이 아니라, 주소값을 참조(Reference)**하여 CPU가 로직을 읽고 수행한다.
3.  **Allocation (할당/실행 중):**
    - 함수가 실행되면서 내부에 선언된 `Object`, `Array`, `Function` 등은 **Memory Heap**의 새로운 공간에 매번 **새로 생성(Allocation)**된다.
    - React의 Re-rendering이 발생할 때 메모리가 증가하는 원인은 바로 이 내부 데이터들의 반복적인 생성 때문이다.

### 2. Key Concepts

- **Concept A: Call Stack (호출 스택 - 작업대)**
  - **역할:** 코드가 실행되는 순서를 기록하고, 원시 타입(Primitive: Number, String 등) 변수와 **Heap 영역을 가리키는 참조 주소(Pointer)**를 저장한다.
  - **특징:** LIFO(Last In First Out) 구조이며, 데이터 접근 속도가 매우 빠르지만 공간이 제한적이다.
- **Concept B: Memory Heap (메모리 힙 - 대형 창고)**
  - **역할:** 크기가 동적으로 변하는 참조 타입(Reference: Object, Array, Function Definition) 데이터를 저장한다.
  - **특징:** 공간이 크고 구조화되어 있지 않아 데이터 할당/해제가 자유롭지만, 스택보다 데이터 조회 비용이 높고 관리가 필요하다(Garbage Collection).

## ⚖️ Comparison (Stack vs Heap)

| Feature         | Call Stack (스택)                        | Memory Heap (힙)                                        |
| :-------------- | :--------------------------------------- | :------------------------------------------------------ |
| **저장 데이터** | 원시 타입, 실행 컨텍스트, **참조 주소**  | 객체, 배열, **함수 코드 본문**                          |
| **속도**        | 매우 빠름 (CPU 친화적)                   | 상대적으로 느림 (주소 찾아가야 함)                      |
| **관리 주체**   | OS가 자동 관리 (함수 종료 시 즉시 삭제)  | JS 엔진의 **Garbage Collector**가 관리                  |
| **React 관점**  | 렌더링 시 가벼운 변수들이 잠깐 머무는 곳 | `useState` 객체, 컴포넌트 코드, 핸들러 함수들이 사는 곳 |

## 📚 Reference (Optimization Insight)

- **메모리 누수 방지:** `Heap`은 자동으로 비워지지 않으므로, 더 이상 쓰지 않는 객체(Unreachable Object)를 GC가 수거해가도록 참조를 끊어주는 것이 중요하다.
- **React 최적화 (`useMemo`, `useCallback`):**
  - 렌더링(Call) 때마다 함수 내부에서 객체나 함수가 `Heap`에 무한히 새로 생성되는 것을 막기 위함이다.
  - "코드가 복사되어서"가 아니라, "내부 데이터가 새로 할당되어서" 메모리가 낭비되는 것을 방지하는 기술이다.
