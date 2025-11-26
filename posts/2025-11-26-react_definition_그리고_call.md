---
title: "React의 생명주기: Definition부터 Mount까지"
date: "2025-11-26"
category: "Language & Framework"
tags: [React, JavaScript, Rendering, Lifecycle]
description: "React 컴포넌트가 메모리에 등록되고(Definition), 호출되어(Call), 화면에 그려지는(Mount) 기술적 과정을 정리함."
---

# 🛠️ `react_definition_vs_call_lifecycle`

## 🎯 Goal (목표)

React가 번들 파일을 받아 메모리에 적재하는 시점과, 실제 함수를 호출하여 화면을 그리는 시점을 구분하여 렌더링 성능 최적화의 기본 원리를 이해한다.

## 💻 동작 원리

### Step 1. Definition (냉동 상태)

- **다운로드 & 파싱:** 브라우저(JS 엔진)는 번들 파일(`bundle.js`)을 다운로드하고 코드를 읽어(Parsing) 문법 오류를 체크한다.
- **메모리 등록 (Heap):** 파싱된 컴포넌트 함수들은 **Memory Heap**에 "함수 객체" 형태로 저장된다.
- **실행 여부:** 이때 함수 내부의 로직(`useState`, `return`, 연산 등)은 **절대 실행(Execute)되지 않는다.** 단순히 "이런 함수가 있다"는 레시피만 책장에 꽂힌 상태다.

### Step 2. Call & Rendering (해동 및 설계)

- **Trigger:** 라우터 이동이나 컴포넌트 호출이 발생하면 JS 엔진은 Heap에 저장된 함수를 찾아 **Call Stack**으로 가져와 **실행(Call)**한다.
- **Rendering (설계도 작성):** 함수가 실행되면서 `useState`로 상태를 메모리에 잡고, `return`문의 JSX를 해석해 **Virtual DOM(가상 돔)**이라는 설계도를 그린다.
- **Re-rendering:** 상태(`state`)나 속성(`props`)이 바뀌면 함수를 다시 **Call**하여 새로운 설계도를 그리고, 이전 설계도와 비교(Diffing)한다.

### Step 3. Mount (실제 건축)

- **Commit:** Rendering 단계에서 계산된 Virtual DOM을 실제 브라우저의 **Real DOM**에 강제로 주입한다.
- **Mount:** 컴포넌트가 **생애 최초로** Real DOM에 부착되는 그 순간을 의미한다.
- **Effect:** 화면이 다 그려진 직후(Paint 이후)에 `useEffect`가 실행된다.

## 📊 비교 분석 (Comparison)

| 구분         | Definition (정의)     | Call (호출/렌더링)           | Mount (마운트)            |
| :----------- | :-------------------- | :--------------------------- | :------------------------ |
| **시점**     | JS 파일 다운로드 직후 | 페이지 이동 / 데이터 변경 시 | 페이지 최초 진입 시 (1회) |
| **위치**     | Memory Heap (창고)    | Call Stack (작업대)          | Browser DOM (화면)        |
| **CPU 비용** | 낮음 (파싱만 함)      | **높음** (로직 연산)         | 중간 (DOM 조작)           |
| **상태**     | 냉동 (코드 텍스트)    | 해동 (실행 중)               | 입주 (화면 표시)          |

## 💡 회고

### 현업 활용 가이드

- **Code Splitting (Lazy):** Definition 단계의 파일 크기(Heap 메모리) 자체를 줄이기 위해, 당장 필요 없는 페이지는 `React.lazy`로 분리하여 다운로드 시점을 늦춘다.
- **Memoization:** `useMemo`나 `useCallback`은 Call 단계에서 매번 새로운 객체/함수를 생성하는 CPU 비용을 줄이기 위해, Heap에 저장된 이전 결과물을 재사용하는 기술이다.

### 주의할 점 (Gotchas)

- **무한 렌더링 (Infinite Loop):** 컴포넌트 내부에서 `setState`를 조건 없이 호출하면 `Call -> State 변경 -> Call`의 무한 루프에 빠져 **Call Stack Overflow**가 발생한다.
- **메모리 누수:** 컴포넌트가 Unmount(화면에서 사라짐)되어도, `setInterval`이나 `window`에 등록된 이벤트 리스너를 지우지 않으면 Heap 메모리에 데이터가 계속 남아있는다. (`useEffect`의 cleanup 함수로 반드시 지워야 함)
